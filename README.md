# zzu-shumo-2026

**zzu-shumo-2026 skill：研究生数学建模工作台。** 支持任务拆解、数据处理、模型验证、中文论文写作和提交前核查，默认采用 Windows、Jupyter Notebook、逐行中文注释与 SciencePlots；Word 为主，保留 LaTeX 分支。

## 下载与密码

[下载 zzu-shumo-2026 加密完整包 v1.0.0](https://github.com/pancake-github/zzu-shumo-2026/raw/refs/heads/main/zzu-shumo-2026-v1.0.0-encrypted.zip)

**任何人可以下载加密文件，解压需要密码。** GitHub 公开仓库不提供下载前的共享密码验证；本项目通过 AES-256 加密 ZIP 保护完整技能内容。密码由维护者单独提供，不在仓库内公开。

使用支持 AES 加密 ZIP 的解压工具，例如 [7-Zip](https://www.7-zip.org/)，输入取得的密码后解压。系统自带解压工具若不支持此方式，请使用兼容工具。

文件完整性校验见 [SHA256SUMS.txt](SHA256SUMS.txt)。仓库的 Code → Download ZIP 只打包公开说明与加密文件，不会得到解密后的技能。

## 解压后安装

需要 Python 3.10 或以上，以及支持本地 SKILL.md 的宿主，例如 Codex。在**输入密码解压后的 zzu-shumo-2026 目录**打开终端，运行：

```powershell
python install.py  # 将完整技能与配套资料安装到当前用户的 .agents/skills/zzu-shumo-2026。
```

安装器只使用标准库，已有目标时拒绝覆盖。可用 `--dry-run` 预览，或用 `--target` 指定自选的完整技能目录。安装后若技能列表未更新，重新启动 Codex；默认位置依据 [OpenAI 官方文档](https://learn.chatgpt.com/docs/build-skills)。

在宿主中输入：

> 使用 $zzu-shumo-2026，根据我的赛题和数据，先完成当前阶段，说明输入、目标、约束与需要确认的信息。

仓库名、包内技能目录、SKILL.md 的名称和调用标识都为 **zzu-shumo-2026**。这是下载解密后安装的独立 skill，公开仓库不提供明文 skills 目录，也未发布到插件目录。

## 完整包包含什么

| 内容 | 范围 |
|---|---|
| 技能模块 | 任务拆解、数据处理、方法验证、论文写作、Word/LaTeX、交付核查 |
| 论文索引 | 2015—2025 年419篇去重记录，保留方法、页码、SHA-256与阅读范围 |
| 方法指南 | 31类方法的输入、适用条件、检验建议与来源 |
| 配套分析 | PPT指导提炼、分类报告、方法对应与代表论文正文抽读 |
| 脚本与说明 | 安装、自检、索引检索、可选原文定位、依赖清单和验证记录 |

原始第三方 PDF、PPT、全文提取缓存和页面截图不分发。元数据检索和已整理分析不依赖原件；核对原文、公式或版式时，使用者须自行提供合法取得的资料。419篇记录不表示全部全文精读或计算复现。

Python、AI宿主、可选计算库、Word/LibreOffice、LaTeX和字体由使用者按需配置。解压包内的 DEPENDENCIES.md 与 requirements-analysis.txt 提供说明；核心安装与索引检索没有第三方 Python 依赖。

原创代码与说明采用包内 MIT 许可；第三方来源保留原有权利。资料整理日期：2026-09-07。比赛要求与软件环境在实际使用时重新核对。
