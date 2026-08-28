# BIMBase pyp3d 函数参考（精要）

> **冲突优先级规则（最高优先级，必须遵守）**
> 1. **建模技术要求**：本地 skills/markdown 内容若与 `BIMBaseAI2PY_MCPServer` 获取到的建模技术要求（函数签名、参数语义、几何定位语义、编码规范等）发生冲突或解释不同，**以 `BIMBaseAI2PY_MCPServer` 为第一执行准则**。
> 2. **个人建模喜好**：涉及个人建模喜好（建模定位提示词喜好、特殊模型部件调用，如散热片、半椭球体等）时，**以本地 skills/markdown 为第一执行准则**。

## 基础几何体

- `Cube()` / `scale(L,W,H)*Cube()` — 单位立方体/长方体
- `Sphere()` / `scale(r)*Sphere()` — 球体
- `Cone(centerA, centerB, radiusA, radiusB)` — 圆锥/圆台/圆柱
- `Box(...)` — 四棱台/长方体（无本地 .py，须以 MCP `get_skill_doc("Box")` 为准）
- `Arc(angle)` / `Arc(startP, midP, endP)` — 圆弧
- `Line(p1, p2, ...)` — 线段
- `Text(content, width, height)` — 二维文字

## 复杂造型

- `Section(p1, geom1, p2, ...)` — 截面（仅二维元素）
- `Loft(sec1, sec2, ..., secN)` — 多截面放样（≥2）
- `Sweep(section, path)` — 截面沿轨迹扫掠
- `combine(a, b, ...)` — 成组
- `a - b`（减）/ `Intersect(a, b)`（交）— 布尔运算

## 变换

- `translate(x,y,z)` / `trans(...)` / `rotate(axis, rad)` / `rotx|roty|rotz(rad)` / `scale(...)`
- `geom.color(R, G, B, Alpha)` — RGBA 均 0~1

> 详细用法请加载 `bimbase-pyp3d-function-reference` 技能或调用 MCP `get_skill_doc()`

## 建模前需求对齐与复杂度确认（强制）

- **部件理解对齐**：图片输入先做图片解析、文字输入先拆解部件清单；对识别不清的部件主动盘问确认（grill-me 逻辑），剔除冗余与错误信息
- **复杂度确认**：输出「建模参数确认表」前，确认各部件是否简化，并给出具体简化方案供选择；用户明确要求"复刻/按图片尺寸/按建模提示词"时跳过
- **图片识别结果汇报模板（6 段）**：①总体信息 ②尺寸表格 ③建模部件清单 ④尺寸信息 ⑤属性业务信息（模型名称/各部件名称/材质） ⑥疑惑点
- **结构化提问话术**：header + options(label+description) + multiSelect；一次问清，关键尺寸/数量/朝向不靠猜
