# consulting-ppt v2.1 轻量布局指标契约

## 范围与来源
- 本工具只消费 JSON bbox 指标；不创建演示文稿、不解析 PPTX、不调用渲染器。
- 坐标统一为同一次真实渲染的实际 px，原点在 slide 左上，x 向右、y 向下。
- 禁止混用 EMU、pt、CSS 逻辑像素、截图缩放前后坐标；先按实际渲染比例统一。
- `frame` 是真实渲染坐标系中的元素外框；`canvas` 是最终渲染画布像素尺寸。
- `ink_bounds` 必须来自真实 glyph 墨迹测量或逐字形审阅，而非文本外框。
- `content_box` 是扣除内边距等后的实际可用文字区，应从渲染器/审阅提取。
- `region` 是图表标签明确获准的 chart/safe region，不能为掩盖泄漏任意放大。
- 图例可以在 plot 外；只要墨迹在明示安全 region、frame 和 slide 内即可。
- `provenance.kind=render_measured` 表示提交者声称真实测量；不是工具自行验证。
- `artifact` 填具体稿件/渲染件标识（宜含版本/哈希），`method` 填测量方式与来源。
- 合成示例和测试必须用 `synthetic`；本次没有真实稿测量或真实稿通过证据。

## 输入字段（schema_version = "1.0"）
| 位置 | 必需字段与规则 |
|---|---|
| root | object；`schema_version` 精确为字符串 `1.0`；`provenance`；`slides` |
| provenance | object；`kind` 为 `render_measured` 或 `synthetic`；`artifact`/`method` 非空字符串 |
| slides | 非空数组；每项为 slide object |
| slide | 非空字符串 `id`；`canvas`；非空 `elements`；`review` |
| canvas | `width`/`height` 有限、非 bool、正数；坐标固定为 (0,0) |
| element | 非空字符串 `id`；`kind`；`frame` |
| kind | `text` / `chart_label` / `shape` / `image` |
| text | 必需 `ink_bounds` 与 `content_box` |
| chart_label | 必需 `ink_bounds` 与明示 `region`（包含 data_label、图例等） |
| rect | object，`x`/`y`/`width`/`height` 有限数值且非 bool；宽高默认严格正 |
| review | 下述四项都必须为字面值 `true`，包括合成测试输入 |

`slide.id` 在 root 内去重，`element.id` 在各 slide 内去重；跨 slide 可重复元素 id。
不支持空白文字的零宽 ink；无墨迹内容应不作为 text 语义元素提交。
若提供可选 bbox，也必须有效且在 canvas 内。未知扩展字段不参与检查。
`intentionally_outside_canvas` 可省略或为字面值 `false`；无出画布豁免。

## 几何与误差规则
- 全部语义元素的 frame 严格在 canvas 内；shape/image 同样受检。
- text ink 严格包含于 content_box；content_box 必须在 frame 内。
- chart_label ink 严格在 region 内；全部 ink 亦必须在其 frame 与 canvas 内。
- “严格”意为没有任何正向越界量；共边可合法，全屏背景可以精确铺满 canvas。
- epsilon 默认 `0.0`，只能为有限非 bool 数值 `0 ≤ epsilon ≤ 0.5` px。
- epsilon 仅区分 ink 内部包含测量的误差类别；绝不是设计许可或留白预算。
- 即使正向泄漏 ≤ epsilon，也报 `measurement_uncertainty` 错误、禁止 pass，须复测。
- 大于 epsilon 报 `overflow`；frame/任意 box 的 canvas 越界始终零容差。
- 验收是零工程溢出，不允许“差一点也通过”。未知/缺失指标与坏结构均 fail closed。

## 人工审阅与能力边界
- `complete_text_checked`：逐段对照完整原文，确认没有截断、遗漏或错误省略。
- `glyph_clipping_checked`：确认每个 glyph 完整；已裁切的墨迹 bbox 可能仍在框内。
- `font_substitution_checked`：确认字体/字形替代及其影响已审查并处理。
- `occlusion_checked`：人工检查文字及其他语义元素的遮挡，不由矩形重叠杜撰。
- 任一项缺失、false 或非布尔 true 均报错；bbox 在框内不能证明原文完整。
- 工具不能证明提交的测量、provenance 或人工声明真实性；真实验收仍需可信证据链。
- 不用 AutoFit、字号/字数估算冒充 glyph 测量；不检测字体可读性、不做 MECE 评分。
- 不普遍自动判断文本与互遮挡，不承诺 PPT 完美、无字体问题或像素级全能检测。

## API 与 CLI
`lint(data, epsilon=0.0, allow_synthetic=False)` 返回 status、declared_metrics_pass、real_slide_acceptance、notice、errors。
`pass` 仅在声明真实 provenance、全部 review true 且所有指标合法无泄漏时返回。
`declared_metrics_pass=true` 仅代表声明契约条件满足；`real_slide_acceptance` 始终为 false，真实PPT验收必须另有可信测量及全页审阅证据。
synthetic 默认 `error`；`--allow-synthetic` 仅测试用，成功状态为 `synthetic_test_ok`。
所有 synthetic 结果醒目标注 `NOT REAL-SLIDE ACCEPTANCE` 且真实验收始终为 false。
CLI 退出码：真实条件通过/合成测试合格为 0；输入/检查失败为 1；参数语法错误为 2。
```bash
python3 check_layout_metrics.py layout-metrics.example.json
python3 check_layout_metrics.py layout-metrics.example.json --allow-synthetic
python3 -B -m unittest -v test_check_layout_metrics.py
```
仅标准库；坏 JSON、缺文件、错误 root/list/dict、NaN/Infinity 均不会因此机械通过。
