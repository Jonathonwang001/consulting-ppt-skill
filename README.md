# consulting-ppt-skill

> **A professional framework for producing top-tier consulting firm–style PPT/Proposal materials.**
> **顶级商业咨询公司风格 PPT/Proposal 制作专业框架**

---

## Overview / 概述

**English**

`consulting-ppt-skill` is a Manus Agent Skill that encodes the design language, narrative logic, visual vocabulary, and content standards of the world's leading consulting firms — McKinsey, Roland Berger, Deloitte, and BCG. Once loaded, it enables any AI agent to produce presentation materials that match the quality and aesthetic of actual consulting deliverables.

**中文**

`consulting-ppt-skill` 是一个 Manus Agent Skill，系统性地编码了全球顶级咨询公司（麦肯锡、罗兰贝格、德勤、BCG）的设计语言、叙事逻辑、视觉词汇与内容规范。加载后，AI Agent 可直接产出与真实咨询交付物质量和美学标准相符的演示材料。

---

## When to Use / 使用场景

**English**

Invoke this skill when:
- User requests a consulting-style PPT, Proposal, strategy report, or project recommendation
- User asks for "McKinsey style", "consulting firm style", or "business cold minimalist" presentation
- Task requires Issue Tree, Gantt chart, MECE framework, 3C/4P/BCG matrix or other consulting tool visualizations
- Analysis conclusions need to be structured into presentable slide format

**中文**

以下场景请调用此 Skill：
- 用户要求制作咨询级 PPT、Proposal、战略报告、项目建议书、行业分析报告、中期/最终汇报材料
- 用户要求"麦肯锡风格"、"咨询公司风格"、"商业性冷淡风"的演示文稿
- 需要构建问题树（Issue Tree）、甘特图、MECE 框架、3C/4P/BCG 矩阵等咨询工具可视化
- 需要将分析结论结构化为可汇报的幻灯片形式

---

## Brand Color System / 品牌配色体系

| Firm / 公司 | Primary / 主色 | Accent / 点缀色 | Background / 背景 |
|-------------|---------------|-----------------|-------------------|
| **McKinsey / 麦肯锡** | Deep Navy `#002F6C` | Gold `#C9A84C` | White `#FFFFFF` |
| **Roland Berger / 罗兰贝格** | Wine Red `#8B0000` | Dark Red `#A50021` | White `#FFFFFF` |
| **Deloitte / 德勤** | Charcoal Black `#1A1A1A` | Brand Green `#86BC25` | White / Dark `#FFFFFF` / `#1A1A1A` |
| **BCG** | Deep Green `#006B3F` | Light Green `#00A651` | White `#FFFFFF` |

---

## File Structure / 文件结构

```
consulting-ppt-skill/
├── README.md                              ← This file / 本文件（中英双语）
├── SKILL.md                               ← Core skill trigger document / 核心触发文档
└── references/
    ├── slide-types.md                     ← 11 slide type specifications / 11种幻灯片类型规范
    ├── visual-modules.md                  ← 11 visual module specs / 11种可视化模块规范
    ├── consulting-frameworks.md           ← 15+ framework quick reference / 15+框架速查手册
    ├── proposal-writing-standards.md      ← Proposal writing standards / Proposal撰写规范
    └── slide-content-template.md          ← Content outline templates / 内容大纲模板
```

---

## Slide Types Covered / 覆盖的幻灯片类型

| # | Type / 类型 | Description / 说明 |
|---|-------------|-------------------|
| 1 | Cover Page / 封面页 | Project title, client, date, confidentiality |
| 2 | Agenda / 议程页 | Numbered section overview with highlights |
| 3 | Section Divider / 章节过渡页 | Visual rhythm reset between chapters |
| 4 | Issue Tree / 问题树 | MECE hierarchical problem decomposition |
| 5 | Work Plan / Gantt / 工作计划甘特图 | Phase-based timeline with milestones |
| 6 | As-Is vs To-Be / 现状对比 | Before/after comparison with transition arrow |
| 7 | Data Chart / 数据图表 | Chart + Key Message Box annotation |
| 8 | 2×2 Matrix / 矩阵分析 | Quadrant analysis with bubble sizing |
| 9 | Funnel / 漏斗分析 | Conversion funnel with loss annotation |
| 10 | Arrow Logic / 逻辑箭头 | 3–5 step process or causal flow |
| 11 | Conclusion / 结论页 | 3-point conclusion + Next Steps |

---

## Visual Modules / 可视化模块

| Module / 模块 | Use Case / 使用场景 |
|---------------|-------------------|
| Numbered Badge / 编号徽章 | Step sequences, priority ranking |
| Arrow Logic Diagram / 箭头逻辑图 | Process flow, causal chain |
| 2×2 Matrix / 矩阵象限图 | Prioritization, portfolio analysis |
| Funnel Chart / 漏斗图 | Conversion analysis, pipeline |
| Waterfall Chart / 瀑布图 | Financial bridge, variance decomposition |
| Issue Tree / 问题树可视化 | Root cause analysis, MECE decomposition |
| Gantt Chart / 甘特图 | Project planning, milestone tracking |
| Comparison Box / 对比框 | Before/after, problem/solution |
| Key Message Box / 关键洞察标注框 | Chart annotation, insight callout |
| Executive Summary Box / 执行摘要框 | Report opening, key findings |
| Value Proposition Card / 价值主张卡片 | Solution benefits, capability showcase |

---

## Consulting Frameworks / 咨询框架

**Strategy / 战略**: 3C Analysis, Porter's Five Forces, BCG Matrix, Ansoff Matrix, McKinsey 7S

**Operations / 运营**: Value Chain Analysis, SWOT/TOWS Matrix, Process Flow

**Finance / 财务**: DuPont Analysis, Waterfall/Bridge Analysis

**Project Management / 项目管理**: RACI Matrix, Change Management Curve

**Market / 市场**: TAM/SAM/SOM, Customer Journey Map, Competitive Matrix

---

## Narrative Logic / 叙事逻辑规范

This skill enforces the **Pyramid Principle** (Barbara Minto) throughout:

1. **Conclusion First** — Every slide title is an Action Title (complete conclusion sentence, not a topic label)
2. **3-Point Structure** — Core arguments supported by exactly 3 sub-points
3. **MECE** — All issue trees and framework decompositions are Mutually Exclusive, Collectively Exhaustive
4. **Data-Backed** — Every claim requires a source citation and year

本 Skill 全程遵循**金字塔原理**（Barbara Minto）：

1. **结论先行** — 每页标题均为 Action Title（完整结论句，而非话题标签）
2. **3点论结构** — 核心论点由恰好3个子论点支撑
3. **MECE原则** — 所有问题树和框架分解满足相互独立、完全穷尽
4. **数据支撑** — 每个论断需标注来源和年份

---

## Proposal Structure Templates / Proposal结构模板

| Version / 版本 | Pages / 页数 | Best For / 适用场景 |
|----------------|-------------|-------------------|
| Short Proposal / 精简版 | 8–12 pages | Initial pitch, RFP response |
| Full Proposal / 完整版 | 12–20 pages | Competitive pitch, detailed scope |
| Interim Report / 中期报告 | 15–20 pages | Mid-project status update |
| Final Report / 最终报告 | 20–30 pages | Full findings and recommendations |

---

## Source Materials / 参考素材来源

This skill was developed by deep analysis of the following reference materials:

- McKinsey & Company classic PPT template collection (436 slides)
- Roland Berger classic PPT template collection (436 slides)
- Deloitte Digital Insights report for Unilever Haircare
- 绿地农垦广西大健康产业规划项目中期报告
- 久谦咨询芭睿品牌战略研究项目建议书
- 天天果园项目建议书 v3.0
- High-Profile Proposal Writing Standards (Cherry Chen, 2014)
- 1000+ flat business icon library

---

## License / 许可证

MIT License — Free to use, modify, and distribute.

---

## Author / 作者

Created by **Manus AI Agent** based on deep analysis of top consulting firm deliverables.

Maintained by: [@Jonathonwang001](https://github.com/Jonathonwang001)
