# 绘图学习来源与实现范围

本包绘图设计参考 `Yuan1z0825/nature-skills` 的 `nature-figure`，参考快照为提交 `287ee37542620711a56c7c58a73f44ef5c2bede0`（2026-09-07）。只借鉴设计和验收思路，本项目的绘图与三线表工具独立实现，未复制其脚本、模板、预览图或第三方图件。

| 来源 | 借鉴内容 |
|---|---|
| [README](https://github.com/Yuan1z0825/nature-skills/blob/287ee37542620711a56c7c58a73f44ef5c2bede0/skills/nature-figure/README.md) | 先明确图意、面板作用、真实数据及导出要求 |
| [SKILL.md](https://github.com/Yuan1z0825/nature-skills/blob/287ee37542620711a56c7c58a73f44ef5c2bede0/skills/nature-figure/SKILL.md) | 按需加载规则，布局修改后重新渲染，自动检查不能代替视觉验收 |
| [API](https://github.com/Yuan1z0825/nature-skills/blob/287ee37542620711a56c7c58a73f44ef5c2bede0/skills/nature-figure/references/api.md) | 克制且一致的配色、按最终物理尺寸排版、对插值及标注范围进行检查 |
| [QA](https://github.com/Yuan1z0825/nature-skills/blob/287ee37542620711a56c7c58a73f44ef5c2bede0/skills/nature-figure/references/qa-contract.md) | 来源可追溯、误差定义一致、逐面板检查，区分机器通过与人工验收 |
| [图型参考](https://github.com/Yuan1z0825/nature-skills/blob/287ee37542620711a56c7c58a73f44ef5c2bede0/skills/nature-figure/references/chart-types.md) | 按数据和问题选择图型，颜色结合线型，不把概念示意图误写为定量结果 |

宋体/Times New Roman 混排、中文下置图题、600 dpi PNG和三线表是本包提供的推荐默认，现行覆盖规则见绘图说明。没有继承上游的 Arial 字体、SVG 主导、Nature 栏宽字号、英文图注字数、主图数量或期刊 AI 制图规则。当前本项目只实现 [绘图说明](figures.md) 列出的自动检查，未集成上游完整 PDF 碰撞和面板对齐审计器。

## 字体与实现依据

- [Matplotlib 字体回退](https://matplotlib.org/stable/users/explain/text/fonts.html#font-fallback)：3.6 起支持同一文本内按字体列表逐字形回退；本项目优先 Times New Roman，再用宋体覆盖汉字。
- [Matplotlib Mathtext](https://matplotlib.org/stable/users/explain/text/mathtext.html#custom-fonts)：自定义正体/斜体数学字体及缺字回退；STIX 用于补足复杂符号，实际保存图仍须检查。
- [SciencePlots FAQ](https://github.com/garrettj403/SciencePlots/wiki/FAQ)：保留 `science` 样式并关闭外部 TeX 路径，支持调整字体。配置与运行环境见 [依赖说明](../DEPENDENCIES.md)。

## 许可边界

参考提交的根目录 [LICENSE](https://github.com/Yuan1z0825/nature-skills/blob/287ee37542620711a56c7c58a73f44ef5c2bede0/LICENSE) 为 Apache-2.0；部分说明仍写 MIT，不能据旧文字判断现行许可。上游 `figures4papers` 另有 [第三方声明](https://github.com/Yuan1z0825/nature-skills/blob/287ee37542620711a56c7c58a73f44ef5c2bede0/skills/nature-figure/assets/figures4papers/THIRD_PARTY_NOTICES.md)，其文件和图片未随本项目分发。今后若直接引入外部文件，需另行核对对应文件及版本的许可，并保留必要声明；本页不额外授予第三方材料使用权。

本包也不分发系统商业字体文件。参考仓库提供学习方法，不能作为本项目已符合当届数学建模比赛规则的依据；年度提交要求仍须查正式文件。
