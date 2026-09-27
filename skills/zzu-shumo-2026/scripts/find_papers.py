import argparse  # 解析用户明确给出的检索条件。
import hashlib  # 以完整 SHA256 校验原文身份，避免误认同名论文。
import json  # 读取并输出可追溯的论文元数据。
import os  # 读取可选语料环境变量并遍历本地目录。
import re  # 检查索引中的 SHA256 格式。
import sys  # 确保 Windows 终端和重定向输出使用 UTF-8。
from pathlib import Path, PurePosixPath, PureWindowsPath  # 处理跨平台相对路径及本地真实路径。

for stream in (sys.stdout, sys.stderr):  # 分别配置正常输出和错误输出。
    if hasattr(stream, 'reconfigure'):  # 兼容没有编码重配置接口的嵌入式环境。
        stream.reconfigure(encoding='utf-8', errors='backslashreplace')  # 避免中文在 Windows 编码下报错。

SKILL_ROOT = Path(__file__).resolve().parents[1]  # 从脚本位置确定安装目录，不依赖当前工作目录。

def safe_relative_path(value):  # 将索引中的路径转换为不越出语料根目录的相对路径。
    normalized = str(value or '').replace('\\', '/')  # 同时支持 Windows 和 POSIX 分隔符。
    relative = PurePosixPath(normalized)  # 以统一语法检查可移植路径。
    if not normalized or relative.is_absolute() or PureWindowsPath(normalized).drive or '..' in relative.parts:  # 拒绝绝对路径、盘符及父目录跳转。
        return None  # 无效路径不会被用于读取文件。
    return Path(*relative.parts)  # 根据当前系统重建可访问的相对路径。

def inside_root(candidate, root):  # 确认解析符号链接后的真实文件仍在用户指定语料目录内。
    try:  # 处理无法解析或越界的路径。
        resolved = candidate.resolve()  # 解析符号链接及规范化文件路径。
        resolved.relative_to(root)  # 越出语料目录时抛出异常。
        return resolved if resolved.is_file() else None  # 只接受目录内的普通文件。
    except (OSError, ValueError, RuntimeError):  # 路径不可访问或符号链接循环均视为不可用。
        return None  # 不读取未经边界确认的候选文件。

def file_sha256(path):  # 对论文文件计算完整 SHA256，不用文件名或大小代替校验。
    digest = hashlib.sha256()  # 初始化标准库哈希对象。
    with path.open('rb') as handle:  # 以只读二进制方式打开原文。
        for block in iter(lambda: handle.read(1024 * 1024), b''):  # 分块读取以控制大文件内存占用。
            digest.update(block)  # 累积当前文件块的哈希。
    return digest.hexdigest()  # 返回可与索引比较的完整十六进制哈希。

def build_filename_index(root, wanted_names, scan_errors):  # 仅为本次返回的论文建立同名候选目录。
    candidates = {name: [] for name in wanted_names}  # 按大小写折叠后的文件名保存候选。
    for directory, subdirectories, filenames in os.walk(root, followlinks=False, onerror=lambda error: scan_errors.append(str(error))):  # 递归扫描并记录无法访问的子目录。
        subdirectories.sort(key=str.casefold)  # 保持不同运行之间的候选顺序稳定。
        for filename in sorted(filenames, key=str.casefold):  # 按稳定顺序处理当前目录中的文件。
            if filename.casefold() in candidates:  # 不收集本次查询无关的文件。
                candidate = inside_root(Path(directory) / filename, root)  # 验证候选不通过符号链接越界。
                if candidate is not None:  # 仅收集确实存在且可定位的文件。
                    candidates[filename.casefold()].append(candidate)  # 同名文件全部保留以逐个进行哈希比对。
    return candidates  # 返回候选映射，不据文件名认定论文身份。

def attach_pdf_status(records, corpus_value):  # 为元数据附加明确的本地原文状态。
    diagnostics = {'configured': bool(corpus_value), 'root': None, 'scan_errors': []}  # 即使没有原文也提供清楚的诊断。
    if not corpus_value:  # 默认检索不需要任何第三方论文原文。
        for item in records:  # 为每条返回记录附加一致字段。
            item.update(local_pdf=None, pdf_status='not_provided')  # 明确没有配置语料，不暗示原文已核验。
        return diagnostics  # 正常结束元数据检索。
    try:  # 检查用户给出的实际语料目录。
        root = Path(corpus_value).expanduser().resolve()  # 支持用户目录写法并转为绝对路径。
        available = root.is_dir()  # 只把存在的目录视为可扫描语料。
    except (OSError, RuntimeError):  # 捕获无法解析路径的异常。
        root, available = Path(corpus_value), False  # 保留输入用于提示，但不访问错误路径。
    diagnostics['root'] = str(root)  # 在结果中说明本次实际使用的语料根目录。
    if not available:  # 缺失语料不影响元数据功能。
        for item in records:  # 逐条标明语料不可用。
            item.update(local_pdf=None, pdf_status='corpus_root_unavailable')  # 避免把错误目录与论文不存在混淆。
        return diagnostics  # 保留成功的元数据查询结果。
    pending = []  # 收集需要按文件名寻找的论文。
    hash_cache = {}  # 避免同一候选文件被重复读取。
    for item in records:  # 先尝试索引中记录的相对路径。
        item.update(local_pdf=None, pdf_status='not_found')  # 校验成功前绝不填入可用原文路径。
        expected = item.get('sha256', '').lower()  # 取得索引中的完整文件身份。
        if re.fullmatch(r'[0-9a-f]{64}', expected) is None:  # 不能在缺少有效哈希时安全认定同名文件。
            item['pdf_status'] = 'invalid_index_sha256'  # 明确索引异常，保留其余元数据。
            continue  # 不访问无法校验身份的论文候选。
        relative = safe_relative_path(item.get('corpus_relative_path'))  # 验证可移植路径是否合法。
        direct = inside_root(root / relative, root) if relative is not None else None  # 只访问用户语料根目录内的文件。
        failures = []  # 保存候选校验失败原因，供未匹配时解释。
        if direct is not None:  # 优先校验原目录结构下的论文。
            try:  # 文件读取失败不应打断其他论文的检索。
                actual = file_sha256(direct)  # 计算直接路径文件的真实哈希。
                hash_cache[direct] = actual  # 缓存已读取候选的哈希。
                if actual == expected:  # 只有完整哈希一致才能确认是索引原文。
                    item.update(local_pdf=str(direct), pdf_status='verified_relative_path')  # 返回已核验的本地原文位置。
                    continue  # 无需为本条记录继续递归寻找同名文件。
                failures.append('hash_mismatch')  # 同路径内容不同也不能当作原文。
            except OSError:  # 记录被占用、权限不足等读取问题。
                failures.append('read_error')  # 将错误限制在当前候选。
        pending.append((item, expected, direct, failures))  # 保存需要进一步搜索的记录及校验上下文。
    if not pending:  # 所有记录已通过直接路径验证时不扫描整套语料。
        return diagnostics  # 返回已完成的原文状态。
    names = {str(item.get('filename', '')).casefold() for item, _, _, _ in pending}  # 只搜索返回结果涉及的确切文件名。
    candidates = build_filename_index(root, names, diagnostics['scan_errors'])  # 扫描一次即可服务全部待定记录。
    for item, expected, direct, failures in pending:  # 逐篇验证同名候选的真实身份。
        for candidate in candidates.get(str(item.get('filename', '')).casefold(), []):  # 遍历全部同名候选，不选择第一个就认定匹配。
            if candidate == direct:  # 直接路径已经完成校验，无需重复读文件。
                continue  # 继续检查其他目录中的同名论文。
            try:  # 单个文件不可读不阻断其余候选。
                actual = hash_cache[candidate] if candidate in hash_cache else file_sha256(candidate)  # 优先复用已计算的文件哈希。
                hash_cache[candidate] = actual  # 保存本次读取结果供后续记录复用。
                if actual == expected:  # 只有 SHA256 完全一致才可返回该候选。
                    item.update(local_pdf=str(candidate), pdf_status='verified_filename_sha256')  # 标明通过同名搜索和哈希完成定位。
                    break  # 当前论文已经找到可靠原文，停止搜索本条记录。
                failures.append('hash_mismatch')  # 保留同名但内容不同的事实。
            except OSError:  # 容忍单个原文文件的权限或读取异常。
                failures.append('read_error')  # 为最终状态提供读取失败原因。
        if item['local_pdf'] is None:  # 所有候选均未能通过校验时明确解释结果。
            item['pdf_status'] = 'hash_mismatch' if 'hash_mismatch' in failures else ('read_error' if failures else 'not_found')  # 不把错误同名文件暴露为可用原文。
    return diagnostics  # 返回整体语料诊断及逐条已更新状态。

def main():  # 命令行入口也便于在 Notebook 中通过子进程调用。
    parser = argparse.ArgumentParser(description='按年份、题号、任务或方法检索论文元数据；原文可选且必须通过 SHA256 校验。')  # 说明工具能力及证据边界。
    parser.add_argument('--year', type=int, help='按比赛年份筛选。')  # 保留原工具的年份筛选。
    parser.add_argument('--question', choices=list('ABCDEF'), help='按当年的 A—F 题号筛选。')  # 保留按当年题号定位的方式。
    parser.add_argument('--task', help='按任务标签关键词筛选。')  # 保留人工任务类别检索。
    parser.add_argument('--method', help='按方法规范名或原名关键词筛选，不区分英文大小写。')  # 保留方法名称检索。
    parser.add_argument('--file', help='按文件名关键词或 SHA256 前缀筛选。')  # 保留文件名及哈希查询。
    parser.add_argument('--limit', type=int, default=5, help='返回 1—100 条记录，默认 5 条。')  # 控制单次结果规模。
    parser.add_argument('--corpus-root', help='可选原文根目录；未指定时读取 ZZU_SHUMO_CORPUS 环境变量。')  # 允许使用者接入自行提供的论文集合。
    args = parser.parse_args()  # 读取用户实际查询条件。
    if not 1 <= args.limit <= 100:  # 保持原工具的合理输出限制。
        parser.error('--limit 须在 1 到 100 之间。')  # 以标准参数错误退出。
    try:  # 将索引缺失或损坏转换为明确命令行错误。
        data = json.loads((SKILL_ROOT / 'references' / 'paper-index.json').read_text(encoding='utf-8-sig'))  # 从安装包读取 UTF-8 索引。
        if not isinstance(data.get('records'), list):  # 检查检索依赖的基础索引结构。
            raise ValueError('索引的 records 必须是列表。')  # 给出可理解的结构错误原因。
    except (OSError, ValueError, AttributeError) as error:  # 捕获文件及 JSON 格式异常。
        parser.error(f'无法读取论文索引：{error}')  # 缺失包内索引属于核心错误。
    matches = []  # 按索引原始稳定顺序保存全部匹配论文。
    for item in data['records']:  # 对论文逐条应用用户指定条件。
        if args.year is not None and item.get('year') != args.year:  # 过滤不匹配年份。
            continue  # 继续检查下一篇论文。
        if args.question and item.get('question') != args.question:  # 过滤不匹配题号。
            continue  # 不把跨年同题号视为同一种任务。
        if args.task and not any(args.task in tag for tag in item.get('task_tags', [])):  # 查询人工整理的任务标签。
            continue  # 无对应标签时跳过本篇论文。
        if args.method and not any(args.method.casefold() in (method.get('name', '') + ' ' + method.get('original_name', '')).casefold() for method in item.get('methods', [])):  # 在规范名及原名中进行大小写无关检索。
            continue  # 不用未公开全文关键词猜测采用方法。
        if args.file and args.file.casefold() not in (item.get('filename', '') + ' ' + item.get('sha256', '')).casefold():  # 支持文件名片段和哈希前缀。
            continue  # 跳过身份不符合查询条件的论文。
        matches.append(dict(item))  # 复制顶层字段以安全附加本次查询状态。
    returned = matches[:args.limit]  # 仅对实际返回记录定位原文，避免无关扫描和哈希计算。
    corpus = attach_pdf_status(returned, args.corpus_root if args.corpus_root is not None else os.environ.get('ZZU_SHUMO_CORPUS'))  # 命令行显式目录优先于环境变量。
    result = {'matched_papers': len(matches), 'returned_papers': len(returned), 'scope': data.get('scope'), 'corpus': corpus, 'records': returned}  # 保留原结果结构并补充原文诊断。
    print(json.dumps(result, ensure_ascii=False, indent=2))  # 使用 UTF-8 输出，无匹配或缺原文也是成功查询。
    return 0  # 核心元数据查询成功时返回零退出码。

if __name__ == '__main__':  # 仅在命令行执行时运行入口，导入不会自行查询。
    raise SystemExit(main())  # 将查询结果状态传递给终端或 Notebook 调用者。
