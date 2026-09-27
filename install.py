# 使用 Python 3.10 或更新版本运行本安装器。
import argparse  # 使用标准库解析安装目标与预览参数。
import shutil  # 使用标准库完整复制技能目录。
import sys  # 检查 Python 版本并设置终端输出编码。
from pathlib import Path  # 使用跨平台路径对象处理 Windows 与其他系统路径。

def main() -> int:  # 定义安装入口并以整数状态码报告执行结果。
    if hasattr(sys.stdout, "reconfigure"):  # 仅在输出流支持重配置时设置编码。
        sys.stdout.reconfigure(encoding="utf-8")  # 确保中文标准输出使用 UTF-8 编码。
    if hasattr(sys.stderr, "reconfigure"):  # 仅在错误输出流支持重配置时设置编码。
        sys.stderr.reconfigure(encoding="utf-8")  # 确保中文错误信息使用 UTF-8 编码。
    if sys.version_info < (3, 10):  # 在复制任何文件前检查最低 Python 版本。
        print("安装失败：需要 Python 3.10 或更新版本。", file=sys.stderr)  # 输出明确的版本要求。
        return 1  # 返回失败状态且不修改文件系统。
    parser = argparse.ArgumentParser(description="安装 zzu-shumo-2026 技能；安装器仅使用 Python 标准库。")  # 创建中文命令行帮助。
    parser.add_argument("--target", type=Path, default=Path.home() / ".agents" / "skills" / "zzu-shumo-2026", help="技能目标完整目录；默认 ~/.agents/skills/zzu-shumo-2026。")  # 接收包含技能名称的完整安装路径。
    parser.add_argument("--dry-run", action="store_true", help="仅检查并显示复制计划，不创建或修改文件。")  # 支持完全只读的安装预览。
    args = parser.parse_args()  # 解析用户提供的命令行参数。
    try:  # 将文件系统错误统一转为可理解的中文提示。
        source = (Path(__file__).resolve().parent / "skills" / "zzu-shumo-2026").resolve()  # 从安装器所在仓库定位完整技能源目录。
        requested_target = args.target.expanduser().absolute()  # 展开用户目录并保留目标路径本身以检查符号链接。
        target = requested_target.resolve()  # 规范化目标路径以判断是否会复制进入源目录。
        if not source.is_dir() or not (source / "SKILL.md").is_file():  # 确保下载的仓库包含有效的技能入口。
            raise ValueError("找不到完整技能源目录或 SKILL.md；请下载并解压整个仓库后重试。")  # 阻止只下载安装器时产生不完整安装。
        if target == source or target.is_relative_to(source):  # 检查目标是否等于源目录或位于其内部。
            raise ValueError("目标不能等于技能源目录，也不能位于技能源目录内部。")  # 避免自我复制和改写源码。
        if requested_target.exists() or requested_target.is_symlink() or target.exists():  # 同时拒绝已有文件、目录和失效符号链接。
            raise ValueError("目标路径已存在，安装器不会覆盖；请指定一个尚不存在的完整目标目录。")  # 保留用户现有技能与其他数据。
        file_count = sum(1 for item in source.rglob("*") if item.is_file())  # 统计技能包中的文件数量以便用户核对。
        print(f"技能名称：zzu-shumo-2026\n源目录：{source}\n目标目录：{target}\n待复制文件：{file_count}")  # 显示具体且可审查的安装计划。
        if args.dry_run:  # 在预览模式下停止于只读检查。
            print("预览完成：未创建或修改任何文件。")  # 明确报告此次操作没有写入内容。
            return 0  # 返回预览成功状态。
        shutil.copytree(source, target, dirs_exist_ok=False)  # 复制整个技能目录并在目标已被创建时拒绝覆盖。
        print("安装完成；请在技能宿主中刷新技能列表或开启新会话，并调用 $zzu-shumo-2026。")  # 提供安装后的技能调用方式。
        return 0  # 返回安装成功状态。
    except (OSError, ValueError, shutil.Error) as exc:  # 捕获路径、权限及目录复制错误并保留详细原因。
        print(f"安装失败：{exc}", file=sys.stderr)  # 输出实际错误供用户排查。
        print("若复制中断后产生了不完整目标目录，请核对其内容后手动清理，再重新安装。", file=sys.stderr)  # 说明中断后的恢复方式且不自动删除用户目录。
        return 1  # 返回失败状态供命令行或自动检查识别。

if __name__ == "__main__":  # 只在直接运行本脚本时执行安装流程。
    raise SystemExit(main())  # 将安装结果转为进程退出状态码。
