# 依赖与运行范围

适用于 zzu-shumo-2026 v2.0.0。技能由支持本地 SKILL.md 的宿主读取；仓库公开完整源码及安装器。宿主提供模型、工具和文件访问能力，本包不是独立聊天程序。

## 核心与可选环境

Python 3.10以上标准库即可运行安装、自检和索引检索，无需额外API密钥。安装器只复制文件，不执行pip、不下载原文。

优先使用当前项目已验证的环境。先检查实际解释器及所需模块；仅在任务需要且已有环境不满足时处理缺失依赖，不自动升级、替换环境或重新注册内核。

| 文件 | 用途 |
|---|---|
| requirements.txt | 核心，无第三方包 |
| requirements-figures.txt | Matplotlib、SciencePlots、Pillow、NumPy、python-docx，用于可选图表工具 |
| requirements-notebook.txt | nbformat、nbclient、ipykernel，用于Notebook创建和执行 |
| requirements-analysis.txt | 按需选择的统计、机器学习、分析及文档依赖 |

requirements中的版本范围是可安装范围，不代表所有组合都已验证。已有工具可以完成任务时，无需安装全部依赖。Word、Notebook和SciencePlots为推荐工作方式，用户选择的LaTeX、其他绘图工具或脚本流程同样适用。

## 图表与字体

新建Matplotlib科研图推荐SciencePlots；无外部TeX时可使用 `plt.style.use(['science', 'no-latex'])`，由Mathtext排版公式。`scripts/figure_style.py` 提供可覆盖的字体、版式及PNG导出设置；已有图件的轻量调整不要调用全局重设样式。

默认中文宋体、西文Times New Roman；包内不分发商业字体。字体检查应以实际可用字体和当前模板为准。默认候选还包括Songti SC、Noto Serif CJK SC、Source Han Serif SC、Liberation Serif及DejaVu Serif；发生替代时报告实际字体。`strict_fonts=True`用于确有指定字体要求的交付，不是所有任务的安装门槛。

位图推荐600 dpi，用户或模板另有要求时采用指定值；矢量PDF中的栅格内容亦需设置合适分辨率。核对实际像素、DPI与最终显示尺寸。复杂数学字符允许合适字体补字，并检查实际字形。Tavotto为可选后处理工具，不是核心依赖，已有环境可用时才接入。

## 文档与页面

python-docx可创建可编辑表格，Office Math需相应文档转换或OOXML流程。分页与最终页面检查使用现有Microsoft Word或兼容渲染器；XML检查不能替代视觉核验。选择LaTeX时使用已有工程与引擎。

Python、系统字体、文档引擎、AI宿主和第三方论文原件不随包附带。原始材料由使用者合法取得；没有原件仍可检索索引及阅读整理资料，重新核验原文则需要原件或可访问的正式来源。
