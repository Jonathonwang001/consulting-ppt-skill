# Consulting PPT Skill · v2.0.0

**内容驱动的咨询级 Proposal 与幻灯片设计方法 / Content-driven consulting proposals and slide design**

[中文](#中文说明) · [English](#english-guide) · [About / 关于](ABOUT.md) · [版本历史 / Changelog](CHANGELOG.md) · [v2.0.0升级说明 / Release notes](releases/v2.0.0.md)

## 中文说明

### 这是什么

一个供AI Agent加载的可复用Skill，沉淀用户提供的经典咨询模板、实际项目和Proposal教学材料中的结构化思考、客户定制、视觉表达与写作方法。采用顶级咨询公司启发的“商业性冷淡风”：逻辑先行、证据可核验、排版克制。它不是在线PPT产品，也不保证加载后自动达到任何机构的官方交付标准。

**v2.0.0的核心升级：客户问题 → 内容关系 → 视觉表达单元 → 商务扁平化图标 → 真实指标与证据。** 页面类型只是结构选择之一；图标适时帮助对象识别，而非每页的必备装饰。

### 适用场景

适用于咨询Proposal、战略报告、项目建议书、中期/最终汇报、高管决策材料，以及问题树、价值链、甘特图、矩阵、漏斗、箭头等可视化设计。没有要求制作演示文稿时可以只产出内容大纲；真正制作PPT时由宿主Slides工具完成，支持情况下优先可编辑结构。

### 新版怎样工作

| 层次 | 作用 | 示例 |
|---|---|---|
| 客户决策 | 说明读者需要确认什么 | 确认研究范围、选择战略方案 |
| 关系编码 | 表达对象如何关联 | 并列框、问题树、泳道、甘特、矩阵 |
| 实体编码 | 用图标帮助辨识业务对象 | 客户群、工厂、仓储、门店、访谈、交付物 |
| 度量与证据 | 说明实际数量及可信边界 | 金额、人数、周、分母、来源、初步假设 |

这里沿用用户的“Unit of Measure”指视觉表达单元；统计数据的单位另行记录。并列杠杆不能乱画成因果链；通用人物头像不能冒充真实团队；图标大小不能暗示无依据的数量。数据密集、商务条款与精确对标页可以不用图标。

Proposal从三条说服主线展开：理解客户处境与需求、知道如何解决、具有相关胜任能力。把背景与目标、问题树、初步思考、工作计划及交付物、相关案例与团队、商务条款串成闭环，**不强求每页或每个结论恰好三个子点**。

### 风格预设与客户定制

客户要求和客户品牌优先。下面是项目用的启发式预设，不是各公司官方品牌手册，也不代表机构背书。

| 启发风格 | 主调 | 点缀 |
|---|---|---|
| McKinsey | 深海军蓝 `#002F6C` / `#1A3A5C` | 冷灰，少量强调色 |
| Roland Berger | 酒红 `#8B0000` / `#A31621` | 深灰 |
| Deloitte | 黑/炭灰 `#1A1A1A` / `#231F20`，可用深蓝/蓝灰 | `#86BC25`绿色仅作小面积点缀，**不是满版绿色** |
| BCG | 深绿 `#006B3F` | 白与中性灰 |

### 加载与使用

将`SKILL.md`及`references/`、`scripts/`、`templates/`保留在同一`consulting-ppt`技能目录中，通过所用Agent的技能加载方式添加。Manus交付的技能卡可以用于添加到My Skills。其他Agent须自行适配工具能力；本仓库不提供通用一键PPT生成器。

示例请求：

> 请按consulting-ppt制作渠道策略研究Proposal。先写客户决策、问题树和工作流/交付物映射，再逐页选择视觉表达单元；商务图标仅用于识别渠道、角色和活动。数据不足标待验证；德勤启发风格以黑/蓝灰为主，绿只点缀。

### 简报校验

```bash
python3 scripts/lint_slide_brief.py templates/slide-brief.example.json
python3 scripts/test_lint_slide_brief.py
```

脚本仅用Python标准库，检查简报字段、图标意图、比例声明、来源声明和工作流闭环。示例是研究设计示意，**没有真实市场数据**。脚本不解析PPT、不判断MECE真实性、不核实来源，也不能替代页面渲染与可编辑性检查。修改项目数据时复制示例，不改示例源文件。

### 学习材料与许可边界

v2新增学习：三套商务扁平化图标/人物/场景PPTX（实际8、8、86页）及High Profile Proposal教学PPTX（17页）。正文中的日期为2013年4月27日；文件名带2014，不能仅按文件名判断创作时间。观察与页码入口见[学习溯源](references/source-learning-map.md)。原版保留麦肯锡/罗兰贝格模板、德勤及实际项目、久谦和天天果园建议书等背景资料的学习基础，不把全部历史材料宣称本次逐页重审。

**本仓库发布的是规则、示例和脚本，不发布用户上传的原PPTX、教材截屏、图标全集或私人客户数据。** 源素材的授权不因上传而变成可公开再分发。原文摘录限于必要说明；机构名称仅说明风格启发。仓库原创内容采用[MIT License](LICENSE)，第三方材料不受该许可证覆盖。

## English guide

### Purpose

A reusable skill for AI agents, distilled from user-provided consulting templates, project materials and proposal training. It promotes structured thinking, client-specific persuasion, restrained visual design and traceable evidence. It is **not** an online presentation product, an official firm template or a guarantee of consulting-quality output.

**The v2.0.0 workflow is: client decision → content relationship → visual unit → business icon → measurement and evidence.** A slide type is a structural option, not the starting point of reasoning.

### Core capabilities

The skill retains the original consulting frameworks and 11 slide types / 11 visual modules. It adds semantic icon selection, relationship-driven layout decisions, planning-to-deliverable traceability, examples, source-learning notes and an executable planning linter.

Visual units encode relationships; business icons identify entities; metric units describe real quantities. Use arrows only for defined sequence, dependency or evidenced causality. Use neutral avatars only for illustrative roles, not real staff identity. Keep icon families and optical weight consistent. Data-heavy charts, precise comparison tables and commercial terms may correctly use **no icons**.

Proposals address three persuasion goals: understand the client's situation, explain how to solve the problem, and demonstrate relevant capability. Link context, issue tree, initial hypotheses, work streams, owners, deliverables, client inputs and checkpoints. This is not a rule that every argument must contain exactly three points.

### Usage and tools

Load `SKILL.md` with its sibling `references/`, `scripts/` and `templates/` in a `consulting-ppt` skill directory. Installation depends on the host agent. For actual presentation creation, follow the host's Slides tooling; prefer native editable authoring where supported. This repository does not implement a universal one-click deck generator.

Example request:

> Apply consulting-ppt to a channel strategy proposal. Start with the client decision and question-to-workstream map. Select each visual unit from the underlying relationship. Add flat business icons only when they improve entity recognition. Mark unverified assumptions. Use charcoal/blue-grey for the Deloitte-inspired preset, with green accents only.

Run the commands in the Chinese section to validate a planning brief and run regression tests. The linter uses only Python's standard library; it does not validate actual PowerPoint layouts, factual accuracy, true MECE decomposition, licensing or editability.

### Presets, sources and limitations

Client instructions and brand assets override the illustrative firm-inspired presets. McKinsey-inspired uses deep navy; Roland Berger-inspired uses wine red; Deloitte-inspired uses black/charcoal or blue-grey with small green accents; BCG-inspired uses deep green. These are project presets, **not official brand specifications or endorsements**.

New learning sources comprise three icon collections (8, 8 and 86 slides) and a 17-slide proposal-training file. The latter's internal cover is dated 27 April 2013 although its filename contains 2014. See the [source-learning map](references/source-learning-map.md) for scope and page references. No claim is made that all historical materials were re-reviewed in this release.

Original skill documentation, examples and scripts are covered by the [MIT License](LICENSE). Uploaded source presentations, icon artwork, firm logos and confidential client materials are not included and are not relicensed. Do not publish them without explicit permission.

## Repository map / 仓库结构

```text
SKILL.md                              # Agent workflow / Agent核心流程
README.md                             # Bilingual user guide / 双语说明
CHANGELOG.md                          # Bilingual version history / 双语版本历史
LICENSE                               # Original content only / 原创内容许可证
releases/v2.0.0.md                     # Upgrade & migration notes / 升级与迁移说明
references/
  proposal-writing-standards.md        # Proposal persuasion and planning
  content-visual-grammar.md            # Relationship-driven visual selection
  business-icon-system.md              # Business icon semantics and consistency
  slide-types.md                       # 11 structural slide options
  visual-modules.md                    # 11 visual building blocks
  consulting-frameworks.md             # Consulting framework reference
  slide-content-template.md            # Storyline and slide briefs
  design-examples.md                   # Input/output examples and counterexamples
  source-learning-map.md               # Source scope and page traceability
  quality-assurance.md                 # Human and machine review boundaries
scripts/
  lint_slide_brief.py                  # Planning structure checks
  test_lint_slide_brief.py             # Regression tests
templates/
  slide-brief.example.json             # Illustrative planning example
  version.json                        # Version metadata
```

Maintained by / 维护者：[@Jonathonwang001](https://github.com/Jonathonwang001)
