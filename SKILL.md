---
name: bimbase-pyp3d-modeling
description: 使用 BIMBase 的 pyp3d 库进行参数化三维几何建模并生成可运行 Python 脚本时使用。当用户要求创建、编辑、组装 BIMBase 模型/构件（立方体、圆柱、球、圆锥、圆环、椭球、放样、扫掠、布尔运算、参数化组件等），或需要编写继承 Component 的 pyp3d 脚本时，务必加载本技能。核心目标：准确无误地理解用户建模目标与要求，高效准确地产出符合规范的 pyp3d 代码。
---

# BIMBase pyp3d 建模技能

> **冲突优先级规则（最高优先级，必须遵守）**
> 1. **建模技术要求**：本地 skills/markdown 内容若与 `BIMBaseAI2PY_MCPServer` 获取到的建模技术要求（函数签名、参数语义、几何定位语义、编码规范等）发生冲突或解释不同，**以 `BIMBaseAI2PY_MCPServer` 为第一执行准则**。
> 2. **个人建模喜好**：涉及个人建模喜好（建模定位提示词喜好、特殊模型部件调用，如散热片、半椭球体等）时，**以本地 skills/markdown 为第一执行准则**。

本技能指导你使用 BIMBase 建模软件的 `pyp3d` 库，把用户的自然语言需求转化为**符合规范、可直接在 BIMBase 内嵌 Python 中运行**的参数化建模脚本。

## 最高准则：先准确理解，再动手编码

**核心目标是准确无误地理解用户的建模目标与要求。** 在写任何代码前，必须先在脑中形成清晰、无歧义的建模意图。遇到任何不清楚的点，严格按下面的「三级解惑协议」处理，绝不带着不确定直接猜着写代码。

### 三级解惑协议（遇到不清楚时按序执行，不可跳级）

1. **第一级 · 检索本项目技能与 MCP**
   - 先在本技能库 / BIMBase 知识库中检索：`get_summary_document()` → `get_skill_manifest()` → 用别名/关键词定位相关 symbol → `get_skill_doc()` / `get_skill_bundle()` 读取正文。
   - 未接 MCP 时，查阅本技能的「API 速查」「标准结构」「自定义组件模板」章节。
   - 涉及 API 签名、参数含义、几何约束、退化风险等**技术性问题**，必须在此级解决，禁止凭记忆猜测。

2. **第二级 · 自主合理推断（仅限非关键项）**
   - 对**不影响建模正确性**的次要参数（如未指定的颜色、微小位置偏移、截面数等），可补合理默认值并在代码注释中标明假设。
   - 对**影响几何形状/尺寸/拓扑/装配关系**的关键信息，不得擅自假设，转第三级。

3. **第三级 · 向用户提问澄清**
   - 当检索无法解决、且信息缺失会导致建模目标有歧义或可能做错时，**必须停下来向用户提问**。
   - 提问要具体、可选项化、聚焦关键项，例如：尺寸/单位、数量、相对定位、朝向、是否参数化、输出形式（单体/组合/装配）。
   - 一次把关键疑问集中问清，避免反复打断；用户答复后再继续。

> 判定标准：**"做错的代价" > "问一句的成本"** 时，就去问。宁可多确认一次，也不要交付偏离用户意图的模型。

## 核心原则（不可违反）

1. **绝对不要凭记忆猜测函数名或参数**。`pyp3d` 与任何常规 Python 库都不同。使用任一 API 前，必须先通过检索工具/知识库确认其签名与用法。
2. **单位默认 mm，角度默认弧度制，坐标系为右手系**。
3. **一个脚本文件只能定义一个继承 `Component` 的类**。
4. **Vec2 与 Vec3 不能混用**；截面 `Section` 只接受 Vec2/二维 Line/Arc，禁止 Vec3。

## 工作流（按序执行）

### Step 0 — 理解与确认需求（最先做）
- 从用户需求中提取：物体类型、尺寸、位置、朝向、颜色、参数清单、参数范围、几何约束、装配关系、异常边界、输出形式。
- 复述/在心中固化建模目标；识别缺失或歧义项。
- 对缺失/歧义项启动「三级解惑协议」：先检索 → 次要项合理推断 → 关键项向用户提问。
- **只有当建模目标清晰无歧义后，才进入 Step 1。**

**临时坐标系规则（Step 0 中必须理解并遵守）：**

> 1. 当用户说"**以某点为临时坐标系原点**"后，该段落中后续所有坐标参数和数值描述均以该临时坐标系原点为基准（即相对坐标），除非用户明确说明是原始坐标系参数。
> 2. 临时坐标系**仅做原点平移**，X/Y/Z 轴方向及各平面（xoy、zoy、zox 等）均与原始坐标系保持平行，不涉及任何旋转。
> 3. 若用户在新的段落中**重新声明**"以某点为临时坐标系原点"，则后续坐标切换为新的临时坐标系。
> 4. 若用户**未提及任何临时坐标系**，默认所有坐标均为原始坐标系（全局坐标系）下的绝对坐标。
> 5. 代码实现时，先计算临时坐标系原点在全局坐标中的位置，再将段落内所有相对坐标叠加该原点偏移得到全局坐标。

### Step 1 — 检索与规划
- 若接入了 BIMBase MCP Server，优先调用：
  1. `get_summary_document()` — 首次建模必调，了解全部可用 SDK 与文档路径。
  2. `get_skill_manifest()` — 获取结构化 symbol 索引（名称、路径、别名、关键词、依赖）。
- 规划需要组合哪些 API（如 `Cube` + `Bool`，`Section` + `Loft`）。

### Step 2 — 批量获取文档
- 调用 `get_skill_bundle(symbols=["Cube","Sweep","Bool"])` 一次性取回所需文档正文（会自动附带编码规范 `basic_writing_style`）。
- 需要配套函数时调用 `get_related_skills(symbol)`。
- 单个查询用 `get_skill_doc(symbol)`。
- 若检索后仍存在技术性疑问，回到「三级解惑协议」相应层级处理。

> 未接 MCP 时：从本技能第「API 速查」与「代码模板」章节取用，仍须遵守全部规范。

### Step 3 — 生成代码
- 严格套用「标准结构」，用 `@export` 的 `replace()` 承载造型逻辑。
- **生成代码前，必须先输出「建模参数确认表」**（见下方模板），列出每个部件的 API、临时坐标系原点、截面定义、拉伸方向、全局坐标范围，供用户确认。
- 参数用 `self['名']` 读取，不写死数值；对已确认的次要缺省项补合理默认值并注释假设。
- 复杂几何（椭球、圆环）优先复用「自定义组件模板」。

**建模参数确认表模板（代码生成前必须输出）：**

| 步骤 | 部件 | API | 临时坐标系原点 | 截面/轴线定义 | 拉伸方向/距离 | 全局坐标范围 |
|------|------|-----|-------------|-------------|-------------|------------|
| 1 | 部件名 | 函数名 | 坐标 | 形心/起点/终点 | 方向±距离 | min→max |

用户确认后再生成代码。

### Step 4 — 自检
逐项核对「输出前检查清单」，尤其是文件结构、维度一致性、单位与弧度；确认成品与 Step 0 固化的建模目标一致。

**主动复盘规则（触发条件：用户对同一问题进行 ≥2 次修改时）：**
1. 暂停修改，不继续尝试
2. 复盘列出所有不确定的坐标起点/终点/截面原点/拉伸方向
3. 以表格形式向用户提问确认（"我当前理解" vs "请确认是否正确"）
4. 用户确认后再修改代码

## 标准结构（必须遵循）

```python
from pyp3d import *

class pythonModel(Component):
    def __init__(self):
        Component.__init__(self)
        # 参数定义：obvious True=可见（默认False），readonly True=置灰不可调（默认False），combo 下拉，show 输出槽位
        self['长'] = Attr(1000, obvious=True, combo=[500,1000,2000,3000,4000])
        self['宽'] = Attr(300.0, obvious=True)
        self['高'] = Attr(500, obvious=True)
        self['长方体'] = Attr(None, show=True)   # 最终组装输出槽位（只保留一个）
        self.replace()

    @export
    def replace(self):
        L = self['长']
        W = self['宽']
        H = self['高']
        result = scale(L, W, H) * Cube()
        self['长方体'] = result

if __name__ == "__main__":
    FinalGeometry = pythonModel()
    place(FinalGeometry)
```

**结构要点**
- 顶部必须 `from pyp3d import *`。
- `Attr(value, obvious=False, readonly=False, combo=None, show=False)`
  - `obvious` 属性的可见性：`True` 时可见，`False` 时不可见。默认为 `False`。
  - `readonly` 属性的只读性：`True` 时不可调，为置灰状态，`False` 时可调。默认为 `False`。
  - `combo` 下拉选项列表，元素类型须与 value 一致且含默认值；控制标签全小写。
  - `show=True` 最终几何体输出槽位，默认值填 `None`。**关键规则：每个组件只保留一个最终的组装槽位（`show=True`），不要为每个部件单独设置 `show=True` 槽位，多个 show 槽位会导致组装时的布尔运算失败。**
- `__init__` 末尾调用 `self.replace()`；造型逻辑写在 `@export` 的 `replace(self)` 中（否则参数变化不重算）。
- 入口 `place(实例)` 才能在视图中显示结果。

## API 速查

### 基础几何体
- `Cube()` / `scale(L,W,H)*Cube()` — 单位立方体（中心在原点）/长方体。
- `Sphere()` / `scale(r)*Sphere()` — 球体，仅等比缩放（不支持椭球）。
- `Cone(centerA, centerB, radiusA, radiusB)` — 圆锥/圆台；`radiusA==radiusB` 时为圆柱。
- `Box(...)` — 四棱台/长方体（**无本地 .py，须以 MCP `get_skill_doc("Box")` 为准**）。
- `Arc(angle)`（单位圆弧，半径1，X轴起点逆时针）/ `Arc(startP, midP, endP)`（三点）。
- `Line(p1, p2, ...)` — 二维/三维线段（Vec2/Vec3 不混用）。
- `Text(content, width, height)` — 二维文字；三维文字用 `Sweep(text, Line(Vec3(0,0,0),Vec3(0,0,h)))`。

### 复杂造型
- `Section(p1, geom1, p2, ...)` — 放样/扫掠截面，默认位于 XOY 平面，仅二维元素。
- `Loft(sec1, sec2, ..., secN)` — 多截面放样（≥2）；各截面须空间分离、方向一致、开闭一致、分段一一对应（线对线/弧对弧/点对点）。
- `Sweep(section, path)` — 截面沿轨迹扫掠；**必须旋转截面使其法线对齐轨迹方向**，否则退化为平面；轨迹只能是一段直线或一段圆弧。
- `combine(a, b, ...)` — 成组，不做布尔融合，保留各自属性/颜色。
- 布尔：`a - b`（减）、`Intersect(a, b)`（交）；**布尔后颜色被抹除，需重设**。
- `linspace(a, b, n)` — 等分点序列（n 个点，n-1 份），支持矢量/数值。

### 变换与布置
- 变换用 `*` 作用于几何体，**从右到左**执行：`translate(x,y,z)` / `trans(...)` / `rotate(axis, rad)` / `rotx|roty|rotz(rad)` / `scale(...)`。
- `geom.color(R, G, B, Alpha)` — RGBA 均 0~1，链式调用。
- 布置：`RotationPlace.RotationFunction(g)`（旋转布置）、`TwoPointPlace.linearize(g, '长')`（两点线性布置，线性变量名须与 Attr 名完全一致）。
- 驱动点：`self.setDrivenFeaturePoint(name, SnapMode.GeometricCenter|EndPoint, 'X表达式','Y表达式','Z表达式')`，在 `replace()` 之前定义。
- **驱动点表达式规则**（经实验验证）：引用的 Attr **必须** `obvious=True`（隐藏参数导致解析失败，是驱动点失效的根因）；若该参数用户不应修改，加 `readonly=True` 置灰；三轴都必须含 `[定位点X/Y/Z]`；数学运算（`*` `/` `()` `**`）无限制。
- **SnapMode 吸附模式**：驱动点常用 `GeometricCenter`（几何中心）和 `EndPoint`（端点）。完整枚举见下方：

```python
class SnapMode(Enum):
    Invalid=-1, First=0, Nearest=1,
    MidPoint=1<<2, Center=1<<3, EndPoint=1<<4,
    Intersection=1<<6, Tangency=1<<7, TangentPoint=1<<8,
    Perpendicular=1<<9, PerpendicularPoint=1<<10, Parallel=1<<11,
    Multi3=1<<12, Multi1=1<<14, Multi2=1<<15,
    GeometricCenter=1<<16,   # 几何中心点
    Quadrant=1<<17, Extension=1<<18,
    ApparentIntersection=1<<19, Insertion=1<<20,
    Node=1<<21, enGetBaseCurve=1<<22
```

### 变换示例
```python
testcube  = translate(100,100,100) * scale(500,200,400) * Cube()   # 先缩放后平移
rotatecube = rotate(Vec3(0,0,1), pi/2) * scale(500,200,400) * Cube()
```

## 矩形截面形心理解与 Loft 拉伸规范（必读）

### 矩形截面形心理解

矩形截面的**形心是矩形的几何中心**，四个顶点相对于形心均匀分布。

**XOY 面矩形截面（形心在原点）：**

若截面长（X方向）为 L，宽（Y方向）为 W，则四个顶点为：
- (L/2, W/2, 0)、(-L/2, W/2, 0)、(-L/2, -W/2, 0)、(L/2, -W/2, 0)

**XOZ 面矩形截面（形心在原点）：**

若截面长（X方向）为 L，高（Z方向）为 H，则四个顶点为：
- (L/2, 0, H/2)、(-L/2, 0, H/2)、(-L/2, 0, -H/2)、(L/2, 0, -H/2)

**YOZ 面矩形截面（形心在原点）：**

若截面宽（Y方向）为 W，高（Z方向）为 H，则四个顶点为：
- (0, W/2, H/2)、(0, -W/2, H/2)、(0, -W/2, -H/2)、(0, W/2, -H/2)

### 矩形截面拉伸标准做法：Section + Loft（推荐）

**禁止使用 `Box` 或 `Cube` 进行矩形截面拉伸**，因为 `Box` 的底面/顶面原点在矩形角点而非形心，容易导致定位错误。应使用 `Section + Loft` 模式：

```python
# 步骤1：在XOY面创建矩形截面，形心在原点
rect_section = translate(-L/2, -W/2, 0) * Section(
    Vec2(0, 0), Vec2(L, 0), Vec2(L, W), Vec2(0, W)
)

# 步骤2：用 Loft 沿指定方向拉伸（两个截面空间分离）
# XOY面沿Z+拉伸距离H：
solid = Loft(
    translate(0, 0, z_centroid) * rect_section,
    translate(0, 0, z_centroid + H) * rect_section
)

# XOZ面沿X+拉伸：需先旋转截面到XOZ面
section_xoz = rotx(-pi/2) * rect_section
solid = Loft(
    translate(x_start, 0, z_centroid) * section_xoz,
    translate(x_start + H, 0, z_centroid) * section_xoz
)

# YOZ面沿X-拉伸：需先旋转截面到YOZ面
section_yoz = roty(-pi/2) * rect_section
solid = Loft(
    translate(0, 0, z_centroid) * section_yoz,
    translate(-H, 0, z_centroid) * section_yoz
)
```

> **核心原则**：`translate(-L/2, -W/2, 0)` 将矩形左下角对齐的截面平移至形心在原点，然后通过 `translate(x, y, z)` 将截面平移到目标位置，再用 `Loft` 完成拉伸。

### 截面旋转到不同坐标面

| 目标面 | 旋转操作 | 坐标映射 |
|--------|----------|----------|
| XOY（默认） | 无需旋转 | X→X, Y→Y |
| XOZ | `rotx(-pi/2)` | X→X, Y→Z |
| YOZ | `roty(-pi/2)` | X→Z, Y→Y |

## 自定义组件模板（原生 API 不支持，直接复用）

### 椭球体（Loft 逐层截面放样）
```python
from pyp3d import *
import math

class 椭球体(Component):
    def __init__(self):
        Component.__init__(self)
        self["X半轴"] = Attr(1000.0, obvious=True)
        self["Y半轴"] = Attr(700.0, obvious=True)
        self["Z半轴"] = Attr(500.0, obvious=True)
        self["截面数"] = Attr(25, obvious=True)
        self["旋转角度"] = Attr(0.0, obvious=True)
        self["X"] = Attr(0.0, obvious=True)
        self["Y"] = Attr(0.0, obvious=True)
        self["Z"] = Attr(0.0, obvious=True)
        self["椭球"] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        ax = max(float(self["X半轴"]), 1e-3)
        by = max(float(self["Y半轴"]), 1e-3)
        cz = max(float(self["Z半轴"]), 1e-3)
        n = max(int(self["截面数"]), 5)
        if n % 2 == 0:
            n += 1
        sections = []
        eps = 1e-3
        for i in range(n):
            t = -1.0 + 2.0 * i / (n - 1)
            z = cz * t
            scale_xy = math.sqrt(max(0.0, 1.0 - t * t))
            rx = max(ax * scale_xy, eps)
            ry = max(by * scale_xy, eps)
            sections.append(translate(0, 0, z) * scale(rx, ry) * Section(Arc(2 * math.pi)))
        solid = Loft(*sections)
        solid.smooth = True
        ang = float(self["旋转角度"]) * math.pi / 180.0
        self["椭球"] = translate(float(self["X"]), float(self["Y"]), float(self["Z"])) * rotation(ang) * solid

if __name__ == "__main__":
    place(椭球体())
```

### 半椭球体（底面椭圆/圆截面，高度拉伸）

通过 Loft 逐层截面放样实现。t ∈ [0, 1] 仅覆盖上半部分，底面（t=0）为完整椭圆截面，顶点（t=1）缩为一点。

```python
from pyp3d import *
import math

class 半椭球体(Component):
    def __init__(self):
        Component.__init__(self)
        self["半长轴"] = Attr(1000.0, obvious=True)
        self["半短轴"] = Attr(700.0, obvious=True)
        self["椭球高度"] = Attr(500.0, obvious=True)
        self["半椭球体"] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        ax = max(float(self["半长轴"]), 1e-3)
        by = max(float(self["半短轴"]), 1e-3)
        cz = max(float(self["椭球高度"]), 1e-3)
        n = 25
        if n % 2 == 0:
            n += 1
        sections = []
        eps = 1e-3
        for i in range(n):
            t = 1.0 * i / (n - 1)                # t ∈ [0, 1]，底面→顶点
            z_local = cz * t
            scale_xy = math.sqrt(max(0.0, 1.0 - t * t))
            rx = max(ax * scale_xy, eps)
            ry = max(by * scale_xy, eps)
            sections.append(
                translate(0, 0, z_local) * scale(rx, ry) * Section(Arc(2 * math.pi))
            )
        half_ellipsoid = Loft(*sections)
        half_ellipsoid.smooth = True
        self["半椭球体"] = half_ellipsoid

if __name__ == "__main__":
    place(半椭球体())
```

> **关键差异**：半椭球体 t ∈ [0,1]（完整椭球体 t ∈ [-1,1]），底面在 XOY 面为完整椭圆截面。当 `半长轴 = 半短轴` 时退化为圆截面半椭球。
> 参考：[椭底面高度拉伸.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/task/830建模/椭底面高度拉伸.py)

### 圆形截面圆环（Sweep 沿圆形路径扫掠圆形截面）
```python
from pyp3d import *
import math

class 圆形截面圆环(Component):
    def __init__(self):
        Component.__init__(self)
        self["环半径"] = Attr(1000.0, obvious=True)
        self["截面半径"] = Attr(120.0, obvious=True)
        self["旋转角度"] = Attr(0.0, obvious=True)
        self["X"] = Attr(0.0, obvious=True)
        self["Y"] = Attr(0.0, obvious=True)
        self["Z"] = Attr(0.0, obvious=True)
        self["圆形截面圆环"] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        ring_r = max(float(self["环半径"]), 1.0)
        tube_r = max(float(self["截面半径"]), 0.1)
        if ring_r <= tube_r:                      # 避免截面跨过旋转轴退化
            ring_r = tube_r + 0.1
        section_2d = translate(ring_r, 0) * scale(tube_r, tube_r) * Section(Arc(2.0 * math.pi))
        section_3d = rotate(Vec3(1, 0, 0), -0.5 * math.pi) * section_2d
        path = Line(Arc(2.0 * math.pi))
        torus = Sweep(section_3d, path)
        ang = float(self["旋转角度"]) * math.pi / 180.0
        self["圆形截面圆环"] = translate(float(self["X"]), float(self["Y"]), float(self["Z"])) * rotation(ang) * torus

if __name__ == "__main__":
    place(圆形截面圆环())
```

### 方形截面圆环（Sweep 沿圆形路径扫掠方形截面）
```python
from pyp3d import *
import math

class 方形截面圆环(Component):
    def __init__(self):
        Component.__init__(self)
        self["环半径"] = Attr(1000.0, obvious=True)
        self["截面边长"] = Attr(200.0, obvious=True)
        self["旋转角度"] = Attr(0.0, obvious=True)
        self["X"] = Attr(0.0, obvious=True)
        self["Y"] = Attr(0.0, obvious=True)
        self["Z"] = Attr(0.0, obvious=True)
        self["方形截面圆环"] = Attr(None, show=True)
        self.replace()

    @export
    def replace(self):
        ring_r = max(float(self["环半径"]), 1.0)
        side = max(float(self["截面边长"]), 0.1)
        half = 0.5 * side
        if ring_r <= half:
            ring_r = half + 0.1
        section_2d = Section(
            Vec2(ring_r - half, -half),
            Vec2(ring_r + half, -half),
            Vec2(ring_r + half, half),
            Vec2(ring_r - half, half),
            Vec2(ring_r - half, -half),
        )
        section_3d = rotate(Vec3(1, 0, 0), -0.5 * math.pi) * section_2d
        torus = Sweep(section_3d, Line(Arc(2.0 * math.pi)))
        ang = float(self["旋转角度"]) * math.pi / 180.0
        self["方形截面圆环"] = translate(float(self["X"]), float(self["Y"]), float(self["Z"])) * rotation(ang) * torus

if __name__ == "__main__":
    place(方形截面圆环())
```

## 多组件内联装配

当用户要求把多个 `.py` 组件合并为一个总装脚本时：
- **禁止**跨文件类导入（`from a import A`）与动态加载（`importlib`/`exec`/`eval`）。
- 两组件建模逻辑内联到同一文件；命名冲突用前缀消歧（`comp_a_*`、`comp_b_*`）。
- 文件结构顺序：公共 import/常量 → 组件A内联区 → 组件B内联区 → 总装定位/组合区 → 统一入口。
- 交付一个可独立运行的总装 `.py`，在总装层做相对定位（平移/旋转/镜像）并合并输出。

## 输出前检查清单

- [ ] 顶部有 `from pyp3d import *`
- [ ] 文件中只有一个 `Component` 子类
- [ ] `replace()` 带 `@export` 装饰器，`__init__` 末尾调用 `self.replace()`
- [ ] 最终几何赋值给唯一的 `Attr(None, show=True)` 槽位（每个组件只保留一个最终组装槽位，多个 show 槽位会导致布尔运算失败）
- [ ] 参数经 `self['名']` 读取，未写死数值
- [ ] Vec2/Vec3 未混用；`Section` 未传入 Vec3
- [ ] `Loft` 截面方向/开闭/分段一致且空间分离
- [ ] `Sweep` 截面法线已旋转对齐轨迹，轨迹为单段直线或圆弧
- [ ] 布尔运算后已重设颜色
- [ ] 单位统一 mm，角度用弧度制
- [ ] 中文变量名多词用 `_` 连接，标点全用英文，参数名无特殊符号/角标
- [ ] `if __name__ == "__main__":` 下 `place(实例)` 输出

## 执行环境提示

- 生成脚本由 BIMBase **内嵌 Python 3.7.9**（`<BIMBase>\PythonScript\python-3.7.9-embed-amd64\python.exe`）运行，请确保语法兼容。
- 脚本须含 `if __name__ == "__main__":` 与 `place(...)` 才能布置到视图。
- 输出完整可独立运行的代码。
- **缺参数处理遵循「三级解惑协议」**：技术性疑问先检索本项目技能/MCP；不影响正确性的次要项补合理默认值并注释假设；影响几何形状/尺寸/拓扑/装配的关键信息缺失或有歧义时，必须先向用户提问澄清，不得猜着交付。

---

## 给部件表面添加散热片（线性阵列）

给长方体部件的外表面添加线性阵列的散热片，散热片为矩形截面长方体，沿表面方向线性排列。

### 核心思路

1. 使用 `rect_section_xoy()` 创建散热片截面（形心在原点）
2. 使用 `Loft` 沿 Z 方向拉伸得到单个散热片
3. 通过循环计算阵列位置，将散热片平移到各个位置
4. 使用 `combine()` 合并所有散热片

### 关键参数

| 参数 | 说明 |
|------|------|
| 散热片厚度 | 沿阵列方向的尺寸（mm） |
| 散热片深度 | 沿外伸方向的尺寸（mm） |
| 散热片高度 | 散热片高度（mm），通常与主体高度相关 |
| 散热片间距 | 阵列间距，中心到中心（mm） |
| 散热片数量 | `int((主体边长 - 散热片厚度) / 散热片间距) + 1` |

### 居中放置

阵列整体形心与阵列面形心重合：

```python
start_pos = -(散热片数量 - 1) * 散热片间距 / 2.0
```

### 散热片与主体表面的贴附关系

散热片贴在主体表面的**外侧**：
- 散热片靠近主体的面与主体表面**重合**
- 散热片形心在主体表面之外 `散热片深度/2` 处

### 完整示例代码

```python
# ========== 散热片阵列：散热箱体外侧三个面的线性阵列 ==========
散热片厚度 = 10.0       # 沿阵列方向的厚度
散热片深度 = 20.0       # 沿外伸方向的深度
散热片高度 = 0.85 * 散热箱拉伸距离  # 散热片高度
散热片间距 = 50.0       # 阵列间距（中心到中心）

# 散热片截面A：用于X向面，深度(X方向)=20，厚度(Y方向)=10
散热片截面_X面 = rect_section_xoy(散热片深度, 散热片厚度)

# 散热片截面B：用于Y向面，厚度(X方向)=10，深度(Y方向)=20
散热片截面_Y面 = rect_section_xoy(散热片厚度, 散热片深度)

# 计算每个面的散热片数量
散热片数量 = int((散热箱边长 - 散热片厚度) / 散热片间距) + 1

half_side = 散热箱边长 / 2.0
start_pos = -(散热片数量 - 1) * 散热片间距 / 2.0

散热片Z底 = 散热箱中点Z - 散热片高度 / 2.0
散热片Z顶 = 散热箱中点Z + 散热片高度 / 2.0

def 创建散热片(section, cx, cy):
    return Loft(
        translate(cx, cy, 散热片Z底) * section,
        translate(cx, cy, 散热片Z顶) * section
    )

散热片列表 = []

# 面A：Y负向面（沿Y负向视角查看的正面），散热片贴在外侧，阵列沿X方向
fin_cy = -half_side - 散热片深度 / 2.0
for i in range(散热片数量):
    fin_cx = start_pos + i * 散热片间距
    散热片列表.append(创建散热片(散热片截面_Y面, fin_cx, fin_cy))

# 面B：Y正向面（沿Y负向视角查看的背面），散热片贴在外侧，阵列沿X方向
fin_cy = half_side + 散热片深度 / 2.0
for i in range(散热片数量):
    fin_cx = start_pos + i * 散热片间距
    散热片列表.append(创建散热片(散热片截面_Y面, fin_cx, fin_cy))

# 面C：X正向面（沿X负向视角查看的正面 = 左视图面），散热片贴在外侧，阵列沿Y方向
fin_cx = half_side + 散热片深度 / 2.0
for i in range(散热片数量):
    fin_cy = start_pos + i * 散热片间距
    散热片列表.append(创建散热片(散热片截面_X面, fin_cx, fin_cy))

散热片阵列 = combine(*散热片列表)
```

> 参考：[水泵.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/task/830建模/水泵/水泵.py)

## 关联技能与知识库文档

建模时务必同步加载以下文档：

| 文档 | 路径 | 用途 |
|------|------|------|
| 几何建模精确交互规范 | `leder_skills/BIMBase_几何建模精确交互规范.md` | 用户提示词编写规范、三段式流程、精确描述模板 |
| Agent几何理解与验证规则 | `leder_skills/BIMBase_Agent几何理解与验证规则.md` | Agent 推理规则、建模参数确认表、主动复盘规则 |
| 建模交互技能 | `leder_skills/BIMBase_AIAgent_建模交互技能.md` | 交互流程、信息收集、参数面板设置 |
| 建模方法函数大全 | `leder_skills/BIMBase_pyp3d_建模方法函数大全.md` | 所有 pyp3d 函数详细用法 |
| 建模指南 | `BIMBase_AIAgent_建模指南.md` | 完整技术参考、SDK 接口速查 |
