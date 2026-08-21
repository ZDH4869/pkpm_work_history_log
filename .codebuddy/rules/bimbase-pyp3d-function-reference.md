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
