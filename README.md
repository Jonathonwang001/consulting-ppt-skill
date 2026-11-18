# Consulting PPT Skill · v2.1.1

**阅读者视角、扎实内容与严谨版式 / Reader-aware, evidence-rich business presentations**

[中文](#中文说明) · [English](#english-guide) · [About / 关于](ABOUT.md) · [版本历史](CHANGELOG.md) · [v2.1.1升级说明](releases/v2.1.1.md)

## 中文说明

### 用途与本版升级

供AI Agent复用的咨询Proposal、内部领导/投资部汇报、战略讨论及专题研究设计Skill。基础来自用户提供的经典咨询模板、真实项目、图标素材和Proposal教学材料；v2.1根据用户实际使用反馈补齐场景和排版规范，未声称重新逐页审查所有原始材料。

v2.0已提到高管报告和渲染溢出检查，但主流程仍偏重对外Proposal。本版将阅读者任务、有效内容深度、组合证据与工程硬门槛分别落实，保留三层编码及原有框架/页面模块。

v2.1.1进一步统筹受众、用途、证据成熟度、媒介与交付约束。对外成果/研究/交流采用`external_report`，不是Proposal；对内也可能需要正式审议/说服。整稿故事线、章节信息预算、术语/单位/期间和色义先统一，再设计页面，不把逐页合格当作整稿合格。

报告优先Markdown，演示优先可编辑PPTX，文字/节点/图表数据可改；地图按需配Mermaid，实际计算图表按需配CSV及所用Python源文件。直观成品为主入口，源码为支撑；PDF/PNG预览不替代编辑源。报告/打印版单独验收A4表格/分页，投屏不强改A4。合理重排标题/摘要、表格和栏宽消除无效留白，保留必要分组/呼吸，不堆满每页。

| 维度 | v2.1执行规则 |
|---|---|
| 场景 | 按五维实际需求判断，再路由Proposal、对外非Proposal、内部领导/工作及混合稿 |
| 阅读任务 | 理解、比較、追踪、讨论或决定；内部信息汇报不编造票决 |
| 内容 | 保留事实、机制、同业、反证、风险与口径，删无支撑重复 |
| 可视化 | 一个主要阅读任务可用多个协调结构/数据/表格模块 |
| 格式 | 字体/字号/网格/内边距有项目契约；零溢出/裁切/遮挡是硬门槛 |
| 复用 | 领导/客户认可框架、图表、模板和可用案例图片优先 |
| 完整交付 | 一个完整主稿中包含执行摘要、章级小结、论证和详细支撑 |

取消15字、60%面积、强制衬线等普遍配额，不取消文字完整、字体正确和图表可读。无论内部还是外部，字形溢框、漏尾行、标签被裁、字体替代和关键证据被挡都须修复后再交付。内容草稿和规划脚本通过不能冒充真实PPT已验收。

### 内外场景分别组织

对外Proposal保留“处境/需求→验证与解决路径→相关胜任”，覆盖背景目标、问题树、初步思考、计划/交付物、经验团队和商务条款，并建立问题到工作流的闭环。

内部领导汇报先匹配读者知识、职责、时间和阅读方式，以观点、证据/反证、影响、风险、取舍与关注事项组织；不强制客户投入、报价或服务方资历。内部进度/下一步页有事项/状态/Owner/节点，纯诊断页不硬加行动。现场讲述、会前阅读与专业核对是模式维度，不默认生成三份重复稿。

组合表达可用机制+趋势/同业、矩阵+评价明细、价值链+环节指标、甘特+验收/风险。每模块声明支持哪条观点，口径和连接解释清楚。协调叠加不意味着图压图、双轴制造因果或堆无关框架。图标仅帮助对象识别，精确图表/表格可完全无图标。

### 风格与加载

| 启发风格 | 主调 | 点缀 |
|---|---|---|
| McKinsey | 深海军蓝`#002F6C`/`#1A3A5C` | 冷灰 |
| Roland Berger | 酒红`#8B0000`/`#A31621` | 深灰 |
| Deloitte | 黑/炭灰`#1A1A1A`/`#231F20`或深蓝/蓝灰 | `#86BC25`仅小面积点缀，禁满版绿 |
| BCG | 深绿`#006B3F` | 灰/白 |

以上为非官方启发式项目预设，获批参考/品牌优先，不代表机构背书。将`SKILL.md`及同级`references/`、`scripts/`、`templates/`放在`consulting-ppt`目录，依宿主加载。实际制作依宿主Slides工具，支持时优先可编辑PPTX；本仓库没有在线产品或一键生成承诺。

示例请求：

> 用consulting-ppt准备给内部投资部的会前阅读汇报，沿用领导批准框架。内容保留同业对比、反证、口径和风险；主观点可配协调图表与结构。一个完整主稿含执行摘要、章级小结和详细支撑。字号按模板，全部页面检查文字完整、四边溢出、图表标签、字体替代和遮挡。

### 两类检查与边界

```bash
python3 scripts/lint_slide_brief.py templates/slide-brief.example.json
python3 scripts/lint_slide_brief.py templates/internal-report.example.json
python3 scripts/test_lint_slide_brief.py
python3 scripts/check_layout_metrics.py templates/layout-metrics.example.json --allow-synthetic
python3 scripts/test_check_layout_metrics.py
```

仅Python标准库。规划JSON2.1新增场景、阅读模式、证据模块与布局政策；2.0仍兼容。规划脚本不解析PPT、不核实来源或真正MECE。布局脚本只检查提交的bbox与人工审阅声明，不测字形、不证明来源真实。默认拒绝合成输入用于真实验收；示例是合成算法测试，不含真实稿测量。没有可信实测时用真实全页/对象人工审阅，不能编bbox过检。

### 来源与许可

v2学习三套商务图标/人物/场景材料（8/8/86页）与17页Proposal教学材料，详见[溯源](references/source-learning-map.md)。历史模板/案例学习保留，v2.1属于反馈驱动规范升级。

原创规则、示例和脚本采用[MIT](LICENSE)。用户源PPT、教材截图、图标全集、商标、实际客户图片和私人资料不在公开包中，也不受该许可重新授权。本仓库仅维护Skill，不依赖额外字典工程。

## English guide

### Scope

A reusable AI-agent skill for consulting proposals, internal executive/investment reports, working reviews and strategy discussions. Version 2.1 adds explicit audience-scenario routing, effective information depth, composite visual evidence and strict layout gates, while preserving v2.0's proposal logic, icon semantics and original consulting modules.

The prior version mentioned executive reporting and overflow review, but its core workflow over-generalized proposal planning. Internal reports now start with reader responsibilities, knowledge, time and tasks: understanding, comparing, monitoring, discussing or deciding. A purely informational update need not invent an approval request, client inputs or sales credentials.

Version 2.1.1 separates audience, purpose, evidence maturity, medium and delivery constraints. The `external_report` route covers non-proposal results, research and exchanges without sales closure. Whole-document narrative, chapter information budgets and consistent terms, units, periods and visual semantics precede page styling. Prefer editable Markdown/PPTX, optional Mermaid/CSV/actually used Python sources, and a clear human-facing main artifact. Validate A4 print/report layouts separately from projection; remove purposeless whitespace without overpacking.

### Practical standards

Preserve decision-relevant facts, mechanisms, peer comparisons, counterevidence, risks and assumptions. Remove unsupported repetition rather than stripping useful depth. Reuse leadership-approved structures, charts, templates and available case imagery. Default to one complete main artifact with an executive summary, chapter summaries and traceable detailed support.

A page may use coordinated mechanism/trend, matrix/evaluation-table, value-chain/segment-metric or Gantt/acceptance modules. Each serves the main reader task and explains its evidence contribution, units and relationship. Composition is not physical obstruction or unrelated framework stacking. Business icons are optional entity labels; visual units encode relationships; metric units describe real quantities.

Zero unintended text overflow, missing/clipped content, obscured chart labels, and unresolved font substitution are release-blocking issues. Font roles, spacing, margins and safe regions form a project-specific contract. Removing universal word-count, 60% area and mandatory-serif quotas does not relax engineering quality. Render and inspect every final-format page, and recheck after edits.

### Tools and limitations

Load the core with its sibling directories. Actual deck creation follows the host's Slides tools, using editable authoring where supported. Run the commands above for proposal/internal planning examples and regression tests. Planning schema 2.0 remains compatible; 2.1 adds scene, reader and evidence declarations.

The layout checker consumes declared pixel bounds; it does not render PPTX, measure glyphs, authenticate provenance or establish text completeness. Synthetic fixtures are rejected by default for real acceptance and remain explicitly marked as tests even when allowed. Actual file acceptance requires credible rendering evidence plus content, font and layout review. No real deck was created or certified by this skill-update task.

Deep navy, wine red, charcoal/blue-grey with small Deloitte green accents, and deep green are non-official presets; approved reference assets override them. Original rules/examples/scripts are MIT-licensed, not source decks, proprietary icons, trademarks or confidential client content. This project maintains the skill itself, not a separate dictionary project.

## Repository map / 仓库结构

Core: `SKILL.md`; user documentation: `README.md`, `ABOUT.md`, `CHANGELOG.md`, `releases/v2.1.1.md`; historical notes: `releases/v2.1.0.md`, `releases/v2.0.0.md`.

References include the original proposal, visual grammar, icons, slide types, modules, frameworks, briefs, examples, sources and QA, plus:

| New resource | Purpose |
|---|---|
| `references/audience-scenario-routing.md` | Reader task / scenario routing |
| `references/internal-executive-reporting.md` | Effective internal report depth and structure |
| `references/composite-visual-evidence.md` | Coordinated multi-module evidence |
| `references/typography-layout-contract.md` | Font/layout contract, zero-overflow and repair |
| `references/layout-metrics-contract.md` | Measured bbox input and checker limitations |
| `templates/internal-report.example.json` | Internal planning example |
| `templates/layout-metrics.example.json` | Synthetic geometry fixture, not a real deck |
| `scripts/check_layout_metrics.py` / `test_check_layout_metrics.py` | Declared layout checks / regression |

Maintained by / 维护者：[@Jonathonwang001](https://github.com/Jonathonwang001)
