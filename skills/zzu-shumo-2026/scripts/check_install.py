import argparse  # 提供可选的环境能力诊断开关。
import importlib.util  # 只检查可选模块是否可发现，不强制加载第三方依赖。
import json  # 读取索引并输出结构化安装检查结果。
import os  # 检查可选语料环境变量和系统字体目录。
import re  # 核验技能名称、SHA256 格式及 Markdown 本地引用。
import shutil  # 定位可选的 LaTeX 和字体查询程序。
import sys  # 读取 Python 版本并确保中文输出采用 UTF-8。
from pathlib import Path, PurePosixPath, PureWindowsPath  # 处理跨平台可移植路径。
from urllib.parse import unquote  # 解码 Markdown 引用中的百分号转义。

for stream in (sys.stdout, sys.stderr):  # 对正常结果和错误信息应用相同编码设置。
    if hasattr(stream, 'reconfigure'):  # 兼容嵌入式输出流。
        stream.reconfigure(encoding='utf-8', errors='backslashreplace')  # 避免 Windows 默认编码导致中文打印异常。

SKILL_ROOT = Path(__file__).resolve().parents[1]  # 从脚本自身定位安装包，不要求固定工作目录。
EXPECTED_NAME = 'zzu-shumo-2026'  # 本公开包的稳定技能标识。
EXPECTED_COUNT = 419  # 本次发布经过整理的唯一论文记录数。
REQUIRED_FILES = ('SKILL.md', 'references/paper-index.json', 'references/workflow.md', 'references/data-preparation.md', 'references/model-validation.md', 'references/method-catalog.md', 'references/paper-writing.md', 'references/word-latex.md', 'references/review.md', 'references/evidence.md', 'scripts/find_papers.py', 'scripts/check_install.py', 'scripts/figure_style.py', 'scripts/word_tables.py', 'references/figures.md', 'references/figure-sources.md', 'references/three-line-tables.md', 'examples/figure_gallery.ipynb', 'requirements-figures.txt', 'requirements-notebook.txt')  # 元数据查询及核心工作流必须随包交付。

def relative_target(value):  # 检查包内引用或语料路径是否为安全的相对路径。
    normalized = str(value or '').replace('\\', '/')  # 统一 Windows 和 POSIX 路径分隔符。
    path = PurePosixPath(normalized)  # 独立于当前系统判断路径结构。
    if not normalized or path.is_absolute() or PureWindowsPath(normalized).drive or '..' in path.parts:  # 拒绝绝对路径、盘符及向父目录跳转。
        return None  # 非可移植引用不能算安装完整。
    return Path(*path.parts)  # 返回适合当前系统的相对文件路径。

def check_core():  # 检查独立安装后必须成立的文件、名称和索引约束。
    errors = []  # 收集所有核心错误，避免每次只显示第一个问题。
    for directory in ('references', 'scripts'):  # 检查核心资源目录。
        if not (SKILL_ROOT / directory).is_dir():  # 缺少目录会使技能无法定位配套资源。
            errors.append(f'缺少必需目录：{directory}')  # 说明需要恢复的目录。
    for filename in REQUIRED_FILES:  # 逐个检查工作流与查询脚本。
        if not (SKILL_ROOT / filename).is_file():  # 核心文件必须随公开包完整提供。
            errors.append(f'缺少必需文件：{filename}')  # 记录准确相对路径便于修复。
    skill_file = SKILL_ROOT / 'SKILL.md'  # 定位技能入口。
    if skill_file.is_file():  # 只在入口存在时进行内容检查。
        try:  # 将入口编码或读取错误归为核心安装问题。
            content = skill_file.read_text(encoding='utf-8-sig')  # 支持常见 UTF-8 带或不带 BOM 的文本。
            frontmatter = re.match(r'\A---\s*\n(.*?)\n---(?:\s*\n|$)', content, flags=re.DOTALL)  # 只读取文件开头的技能元数据块。
            name = re.search(r'^name:\s*[\"\']?([^\s\"\']+)[\"\']?\s*$', frontmatter.group(1), flags=re.MULTILINE) if frontmatter else None  # 不把正文中的同名说明误认作元数据。
            if name is None or name.group(1) != EXPECTED_NAME:  # 技能名称必须与公开安装标识一致。
                errors.append(f'SKILL.md 的 name 应为 {EXPECTED_NAME}。')  # 明确需要修正的入口属性。
        except (OSError, UnicodeError) as error:  # 保留入口读取失败的原因。
            errors.append(f'无法读取 SKILL.md：{error}')  # 让检查继续覆盖其余资源。
    if SKILL_ROOT.name != EXPECTED_NAME:  # 标准安装目录名称应与技能标识一致。
        errors.append(f'技能目录应命名为 {EXPECTED_NAME}，当前为 {SKILL_ROOT.name}。')  # 防止复制层级错误或技能安装名混淆。
    records = []  # 索引异常时仍可检查 Markdown 资源。
    index_path = SKILL_ROOT / 'references' / 'paper-index.json'  # 定位本次发布索引。
    try:  # 集中处理索引读取和基础结构错误。
        data = json.loads(index_path.read_text(encoding='utf-8-sig'))  # 只使用标准库读取可移植元数据。
        records = data['records']  # 获取待检查论文记录。
        if not isinstance(records, list):  # 记录集合必须是 JSON 数组。
            raise ValueError('records 不是列表。')  # 明确索引结构错误。
        if len(records) != EXPECTED_COUNT or data.get('unique_papers') != EXPECTED_COUNT:  # 核验记录数和声明的唯一论文数。
            errors.append(f'索引应含 {EXPECTED_COUNT} 条论文记录且 unique_papers 为 {EXPECTED_COUNT}；实际记录数为 {len(records)}。')  # 不以错误清单蒙混完整安装。
        hashes = []  # 收集合法哈希以检查重复论文。
        for number, item in enumerate(records, start=1):  # 为每条异常提供清楚的位置。
            if not isinstance(item, dict):  # 跳过损坏的记录对象并记录错误。
                errors.append(f'第 {number} 条记录不是对象。')  # 描述无法执行字段检查的原因。
                continue  # 保持其他记录仍可检查。
            sha256 = item.get('sha256', '')  # 读取索引中的原文身份字段。
            if not isinstance(sha256, str) or re.fullmatch(r'[0-9a-fA-F]{64}', sha256) is None:  # 完整 SHA256 是可选原文匹配的基础。
                errors.append(f'第 {number} 条记录的 SHA256 无效。')  # 不允许不完整身份索引通过检查。
            else:  # 对合法哈希执行统一大小写后去重。
                hashes.append(sha256.lower())  # 保存可比较的文件身份。
            for field in ('filename', 'year', 'question', 'task_tags', 'methods', 'read_scope', 'corpus_relative_path', 'body_review_refs'):  # 保持查询条件和证据范围字段完整。
                if field not in item:  # 核验核心元数据字段存在。
                    errors.append(f'第 {number} 条记录缺少 {field}。')  # 指向需要恢复的字段。
            if relative_target(item.get('corpus_relative_path')) is None:  # 原文定位只能使用使用者语料目录下的相对路径。
                errors.append(f'第 {number} 条记录的 corpus_relative_path 不是安全相对路径。')  # 防止携带原作者机器绝对路径。
            for reference in item.get('body_review_refs', []):  # 检查额外正文抽读报告的包内指针。
                value = reference.get('report_path', '') if isinstance(reference, dict) else reference  # 兼容对象和纯路径形式引用。
                target = relative_target(value)  # 引用统一相对技能安装根目录。
                if target is None or not (SKILL_ROOT / target).is_file():  # 报告必须包含在可移植发布包内。
                    errors.append(f'第 {number} 条记录的正文报告引用不可用：{value}')  # 明确哪条证据链发生断裂。
            for feature in item.get('writing_features', []):  # 检查写作特征中附加的包内报告来源。
                value = feature.get('source', '') if isinstance(feature, dict) else ''  # 普通描述文字不当作文件路径。
                if isinstance(value, str) and value.lower().endswith('.json'):  # 只检查明确指向 JSON 报告的来源字段。
                    target = relative_target(value)  # 来源应相对技能根目录定位。
                    if target is None or not (SKILL_ROOT / target).is_file():  # 不允许保留作者机器上的失效报告路径。
                        errors.append(f'第 {number} 条记录的写作证据引用不可用：{value}')  # 给出可定位的证据链问题。
        if len(hashes) != EXPECTED_COUNT or len(set(hashes)) != EXPECTED_COUNT:  # 必须具备 419 个互不重复的有效哈希。
            errors.append(f'索引应含 {EXPECTED_COUNT} 个唯一有效 SHA256；实际为 {len(set(hashes))}。')  # 区分重复论文与声明的总记录数。
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:  # 捕获索引文件和结构异常而不显示长堆栈。
        errors.append(f'无法检查论文索引：{error}')  # 保留实际错误原因用于排查。
    for document in sorted(SKILL_ROOT.rglob('*.md')):  # 检查所有已分发 Markdown 中的相对链接。
        try:  # 某个说明文件不可读时记录问题并继续其余文件。
            content = document.read_text(encoding='utf-8-sig')  # 以统一编码读取公开文本资源。
            for match in re.finditer(r'\]\(([^\n]+?)\)', content):  # 提取 Markdown 普通链接的目标。
                value = match.group(1).strip().strip('<>')  # 支持用尖括号包围含空格路径。
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', value) and not re.match(r'^[a-zA-Z]:[\\/]', value):  # 网络链接不属于本地安装完整性检查。
                    continue  # 不因离线或第三方网络状态影响核心结果。
                value = unquote(value.split('#', 1)[0])  # 页内锚点无需文件检查，同时恢复编码后的文件名。
                if not value:  # 当前页锚点没有外部文件依赖。
                    continue  # 保持正常 Markdown 目录链接可用。
                target = (document.parent / value).resolve()  # 按所在 Markdown 文件解析真实相对目标。
                try:  # 禁止链接依赖技能安装包以外的作者本地文件。
                    target.relative_to(SKILL_ROOT)  # 越界时抛出异常。
                    portable = not PureWindowsPath(value).drive and not PurePosixPath(value.replace('\\', '/')).is_absolute()  # 同时识别两种平台的绝对路径。
                except ValueError:  # 相对路径越出安装包时视为非可移植。
                    portable = False  # 标记无法独立安装的外部路径。
                if not portable or not target.exists():  # 所有本地引用应能在安装目录中解析。
                    errors.append(f'{document.relative_to(SKILL_ROOT).as_posix()} 的本地引用不可用：{value}')  # 给出来源文件和断裂目标。
        except (OSError, UnicodeError, RuntimeError) as error:  # 捕获文本或路径读取异常。
            errors.append(f'无法检查 {document.name}：{error}')  # 继续完成其他安装诊断。
    return {'status': 'PASS' if not errors else 'FAIL', 'skill_name': EXPECTED_NAME, 'skill_root': str(SKILL_ROOT), 'paper_records': len(records), 'errors': errors}  # 核心结论仅由必需资源决定。

def optional_environment():  # 可选计算和排版能力仅用于信息提示，绝不使核心检查失败。
    modules = {}  # 保存各项扩展能力的可发现状态。
    for module in ('numpy', 'pandas', 'scipy', 'matplotlib', 'scienceplots', 'sklearn', 'statsmodels', 'sympy', 'networkx', 'openpyxl', 'docx', 'pypdf', 'nbformat', 'nbclient', 'ipykernel'):  # 覆盖数模、图表、文档及 Notebook 常用扩展。
        try:  # 环境异常同样只能形成提示。
            modules[module] = importlib.util.find_spec(module) is not None  # 不下载、不安装也不执行第三方模块。
        except (ImportError, ValueError, AttributeError):  # 损坏的环境元数据不影响索引功能。
            modules[module] = False  # 仅标记该可选模块尚不可发现。
    font_directories = [Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts', Path.home() / '.fonts', Path.home() / '.local/share/fonts', Path('/usr/share/fonts'), Path('/Library/Fonts')]  # 信息性定位常见系统字体目录。
    tools = {name: shutil.which(name) for name in ('latex', 'xelatex', 'pdflatex', 'dvipng', 'fc-list')}  # 标明 LaTeX 渲染及字体枚举程序是否可用。
    return {'informational_only': True, 'python': sys.version.split()[0], 'modules_discoverable': modules, 'executables': tools, 'existing_font_directories': [str(path) for path in font_directories if path.is_dir()], 'font_note': '仅枚举字体目录；实际中文字体、science 样式及 LaTeX 联合渲染应在绘图时验证。', 'corpus_configured': bool(os.environ.get('ZZU_SHUMO_CORPUS')), 'note': '缺少可选模块、字体或 LaTeX 不影响技能文本和元数据检索；按实际任务安装依赖。'}  # 避免把模块存在误述为完整绘图功能通过。

def main():  # 提供清楚的命令行检查入口。
    parser = argparse.ArgumentParser(description='检查 zzu-shumo-2026 核心安装；可选环境能力仅作提示。')  # 解释必需资源和可选环境的区别。
    parser.add_argument('--environment', action='store_true', help='附加可选模块、LaTeX 和字体目录诊断；不改变核心通过条件。')  # 由使用者决定是否读取扩展能力状态。
    args = parser.parse_args()  # 读取实际检查选项。
    result = {'core': check_core()}  # 默认只检查技能本身能否独立工作。
    if args.environment:  # 仅在明确要求时附加环境信息。
        result['optional_environment'] = optional_environment()  # 环境状态不会进入核心错误列表。
    print(json.dumps(result, ensure_ascii=False, indent=2))  # 输出便于终端阅读或 Notebook 解析的 UTF-8 JSON。
    return 0 if result['core']['status'] == 'PASS' else 1  # 仅必需安装资源失败才返回非零退出码。

if __name__ == '__main__':  # 防止导入此模块时自动执行诊断。
    raise SystemExit(main())  # 将核心检查结论传递给终端或自动化流程。
