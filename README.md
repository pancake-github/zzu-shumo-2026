# zzu-shumo-2026

**研究生数学建模工作台 v2.0.0**。支持赛题理解、数据处理、建模验证、论文写作与精简、图表排版和Word整合。源码公开，采用MIT许可；安装包可直接解压，无需密码。

本版将实际论文修改经验整理为按情境执行的规范：遇到熟悉的问题直接处理，必要时才集中询问。保留科学真实性和验证边界，将Word、Notebook、SciencePlots及600 dpi等设为可覆盖的推荐默认。简单改写直接给结果，完整研究按授权连续推进；用户指定的逐阶段确认仍然有效。

## 下载与安装

[下载 v2.0.0 安装包](https://github.com/pancake-github/zzu-shumo-2026/releases/download/v2.0.0/zzu-shumo-2026-v2.0.0.zip) · [发布页与SHA-256校验文件](https://github.com/pancake-github/zzu-shumo-2026/releases/tag/v2.0.0)

也可使用GitHub的 **Code → Download ZIP** 下载完整源码。解压后，在包含 `install.py` 的目录运行：

```powershell
python install.py
```

需要Python 3.10或以上；默认安装到当前用户的 `~/.agents/skills/zzu-shumo-2026`。安装器只复制技能，不安装软件、不联网下载论文、不覆盖已有目录。可使用 `--dry-run` 预览，或用 `--target` 指定宿主支持的完整目标路径。

升级时，将旧安装目录备份至宿主技能扫描目录之外，再安装新版。旧名称 `gmcm-workbench` 的用户可在迁移项目专属设置后停用旧目录，避免两个工作台同时触发。开发源码和原始参考资料无需删除。安装后刷新技能列表或开启新会话。

## 使用

> 使用 $zzu-shumo-2026，按题目要求检查已有模型并完善当前论文，普通修改直接完成。

> 使用 $zzu-shumo-2026，精简结果与小结的重复，保留指定检验和独有证据。

> 使用 $zzu-shumo-2026，只调整这幅图的字号与底部留白，保留数据、坐标和配色。

入口：[SKILL.md](skills/zzu-shumo-2026/SKILL.md)。详细模块按需读取：[研究流程](skills/zzu-shumo-2026/references/workflow.md)、[建模验证](skills/zzu-shumo-2026/references/model-validation.md)、[论文写作](skills/zzu-shumo-2026/references/paper-writing.md)、[Word整合](skills/zzu-shumo-2026/references/word-latex.md)、[科研图](skills/zzu-shumo-2026/references/figures.md)。

## 资料与环境

- 419篇2015—2025年历史论文索引，保留来源身份及实际阅读范围。
- 31类方法资料及来源链接，服务方法选择与条件核查。
- 标准库安装、自检与索引检索；可选绘图、三线表和Notebook示例。
- 核心内容与脚本跨平台；Word分页依赖当前可用的文档渲染环境。

```powershell
python skills/zzu-shumo-2026/scripts/check_install.py
python skills/zzu-shumo-2026/scripts/find_papers.py --year 2024 --question D --limit 3
```

按任务复用现有环境，依赖见[DEPENDENCIES.md](DEPENDENCIES.md)。需要新增依赖时才采用相应requirements文件。配套[绘图示例](skills/zzu-shumo-2026/examples/figure_gallery.ipynb)使用教学数据，不代表研究结果；现成图片调整请采用保留式处理，不套用新图的全局样式。

原始论文、PPT、全文缓存、原页截图和实际参赛文稿不随包分发。419条索引不表示全部论文已全文精读或计算复现。使用者自行合法取得原件；比赛格式和人工智能使用规定以当届正式文件为准。

[MIT许可](LICENSE) · [来源及权利说明](THIRD_PARTY_NOTICES.md) · [验证范围](VALIDATION.md)
