---
name: bimbase-pyp3d-function-reference
description: BIMBase pyp3d 建模方法函数大全。系统整理了所有 pyp3d 函数的标准结构、Attr 参数规范、9 种基础几何体、6 种复杂造型、变换、布置、驱动点、颜色、3 种自定义组件、建模决策树与完整示例。当 Agent 需要查阅具体 pyp3d 函数用法时加载。
---

# BIMBase pyp3d 建模方法函数大全

> 本文档系统整理了 BIMBase 建模中所有 `pyp3d` 建模方法函数的使用要求、参数设定方法和代码示例。
> 所有函数接口均以 mm 为单位，角度使用弧度制，采用右手坐标系。

---

## 目录

1. [Python 建模文件标准结构](#一python-建模文件标准结构)
2. [参数定义：Attr](#二参数定义attr)
3. [基础几何体](#三基础几何体)
   - [Cube 立方体](#31-cube--立方体)
   - [Sphere 球体](#32-sphere--球体)
   - [Cone 圆锥/圆台/圆柱](#33-cone--圆锥圆台圆柱)
   - [Box 四棱台/长方体](#34-box--四棱台长方体)
   - [Arc 圆弧](#35-arc--圆弧)
   - [Line 线段](#36-line--线段)
   - [Text 文字](#37-text--文字)
4. [复杂造型](#四复杂造型)
   - [Section 截面](#41-section--截面)
   - [Loft 放样](#42-loft--放样)
   - [Sweep 扫掠](#43-sweep--扫掠)
   - [Combine 组合](#44-combine--组合)
   - [Bool 布尔运算](#45-bool--布尔运算)
   - [Linspace 等分点序列](#46-linspace--等分点序列)
5. [变换操作](#五变换操作)
6. [布置接口](#六布置接口)
7. [驱动点/特征点](#七驱动点特征点)
8. [颜色设置](#八颜色设置)
9. [自定义组件模板](#九自定义组件模板)
10. [Python 建模文件五大组成部分](#十python-建模文件五大组成部分)
11. [建模决策树](#十一建模决策树)

---

## 一、Python 建模文件标准结构

每个建模 Python 文件遵循以下固定结构：

```python
from pyp3d import *                         # 1. 必须导入

class pythonModel(Component):               # 2. 单一 Component 子类
    def __init__(self):
        Component.__init__(self)
        # 3. 参数定义区
        self['长'] = Attr(1000, obvious=True, combo=[500,1000,2000])
        self['宽'] = Attr(300.0, obvious=True)
        self['高'] = Attr(500, obvious=True)
        self['长方体'] = Attr(None, show=True)   # 最终几何输出槽位
        self.replace()                           # 4. 必须调用

    @export                                      # 5. 必须 @export
    def replace(self):                           # 6. 造型逻辑
        L = self['长']
        W = self['宽']
        H = self['高']
        result = scale(L, W, H) * Cube()
        self['长方体'] = result

if __name__ == "__main__":                       # 7. 入口
    FinalGeometry = pythonModel()
    place(FinalGeometry)
```

**核心规则：**
- 文件顶部必须 `from pyp3d import *`
- 一个文件只能定义一个 `Component` 子类
- `__init__` 末尾必须调用 `self.replace()`
- 造型逻辑写在 `@export` 装饰的 `replace(self)` 方法中
- 入口必须 `place(实例)` 才能在视图中显示

> 来源：[SKILL.md](file:///D:/BIMbase/PythonScript/BFAComponentLib/SKILL.md)、[basic_writing_style.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/02_coding_standards_safety/basic_writing_style.md)

---

## 二、参数定义：Attr

```python
Attr(value, obvious=False, readonly=False, combo=None, show=False)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `value` | Any | 默认值（数值、字符串或 None） |
| `obvious` | bool | 属性的可见性：`True` 时可见，`False` 时不可见。默认为 `False`。 |
| `readonly` | bool | 属性的只读性：`True` 时不可调，为置灰状态，`False` 时可调。默认为 `False`。 |
| `combo` | list | 下拉选项列表，元素类型须与 value 一致，必须包含默认值 |
| `show` | bool | `True`=最终几何输出槽位，value 填 `None` |

```python
# 常规可调参数
self['宽'] = Attr(300.0, obvious=True)

# 带下拉选项
self['长'] = Attr(1000, obvious=True, combo=[500, 1000, 2000, 3000, 4000])

# 只读参数（仅显示，不可修改）
self['旋转角度'] = Attr(0, obvious=True, readonly=True)

# 最终几何输出槽位（不可修改，仅显示模型）
self['长方体'] = Attr(None, show=True)
```

> 来源：[property_Attr.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/property_Attr.md)

---

## 三、基础几何体

### 3.1 Cube — 立方体

**功能：** 创建棱长为 1 的单位立方体（中心在原点），通过 `scale` 缩放得任意长方体。

**接口：**
```python
Cube()                              # 单位立方体 (1x1x1)
scale(L, W, H) * Cube()             # 自定义长宽高
```

**示例：**
```python
cube = scale(100, 200, 50) * Cube()       # 100x200x50 长方体
cube = translate(500, 0, 0) * scale(100, 200, 50) * Cube()  # 平移+缩放
```

> 来源：[geometry_Cube.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Cube.md)
> 参考：[Cube参数化.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/Cube参数化.py)

---

### 3.2 Sphere — 球体

**功能：** 创建单位球体，仅支持等比缩放（不支持椭球，椭球需用 Loft 自定义）。

**接口：**
```python
Sphere()                        # 单位球体（半径1）
scale(r) * Sphere()             # 单参数缩放
scale(r, r, r) * Sphere()       # 三轴等比例缩放
```

**示例：**
```python
sphere = scale(200) * Sphere()                    # 半径200的球
sphere = translate(100, 100, 100) * scale(200) * Sphere()  # 平移+缩放
```

> 来源：[geometry_Sphere.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Sphere.md)

---

### 3.3 Cone — 圆锥 / 圆台 / 圆柱

**功能：** 创建由两个圆心和两个半径定义的锥体。`radiusA == radiusB` 时为圆柱。

**接口：**
```python
Cone(centerA, centerB, radiusA, radiusB)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `centerA` | Vec3 | 底面 A 圆心坐标 |
| `centerB` | Vec3 | 底面 B 圆心坐标 |
| `radiusA` | float | 底面 A 半径 |
| `radiusB` | float | 底面 B 半径 |

**示例：**
```python
# 圆柱：两端半径相等
cyl = Cone(Vec3(10000, 0, 0), Vec3(10000, 0, 2000), 1000, 1000).color(1, 0, 0, 0.3)

# 圆台：两端半径不等
frustum = Cone(Vec3(0, 0, 0), Vec3(0, 0, 500), 200, 100)
```

> 来源：[geometry_Cone.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Cone.md)

---

### 3.4 Box — 四棱台 / 长方体

**功能：** 创建任意朝向的四棱台，顶底尺寸相同即为棱柱/长方体。

**接口：**
```python
Box(baseOrigin, topOrigin, vectorX, vectorY, baseX, baseY, topX, topY)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `baseOrigin` | Vec3 | 底部原点 |
| `topOrigin` | Vec3 | 顶部原点 |
| `vectorX` | Vec3 | 局部 X 方向基矢 |
| `vectorY` | Vec3 | 局部 Y 方向基矢 |
| `baseX` | float | 底部 X 方向长度 |
| `baseY` | float | 底部 Y 方向长度 |
| `topX` | float | 顶部 X 方向长度 |
| `topY` | float | 顶部 Y 方向长度 |

**示例：**
```python
box = Box(
    Vec3(0, 0, 0),        # 底面原点
    Vec3(0, 0, 3000),     # 顶面原点（决定高度=3000）
    Vec3(1, 0, 0),        # X 方向
    Vec3(0, 1, 0),        # Y 方向
    3000, 5000,           # 底面 3000x5000
    3000, 5000            # 顶面 3000x5000
).color(1, 1, 0, 0.5)
```

> **重要提醒**：`Box` 的底面/顶面原点在矩形角点（非形心），定位时需额外计算平移偏移。**对于等截面矩形拉伸体，推荐使用 `Section + Loft` 模式**（见 4.2 节），形心在原点，定位更直观准确。

> 来源：[geometry_Box.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Box.md)

---

### 3.5 Arc — 圆弧

**功能：** 创建单位圆弧（半径1，X轴起点逆时针）或三点圆弧。

**接口（两种重载形式）：**
```python
Arc(angle)                                # 按弧度创建，默认圆心(0,0,0)，起点(1,0,0)
Arc(startPoint, midPoint, endPoint)       # 按三点创建，三点为 Vec3
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `angle` | float | 弧度值（`pi*2`=整圆，`pi`=半圆） |
| `startPoint` | Vec3 | 起点 |
| `midPoint` | Vec3 | 中间点 |
| `endPoint` | Vec3 | 终点 |

**示例：**
```python
arc = Arc(pi * 2)                                  # 完整圆（半径1）
arc = Arc(pi * 1.5)                                # 3/4 圆弧
arc = Arc(Vec3(0,0,0), Vec3(100,100,0), Vec3(0,200,0))  # 三点圆弧
arc_scaled = scale(100) * Arc(pi * 2)              # 半径100的圆
```

> 来源：[geometry_Arc.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Arc.md)

---

### 3.6 Line — 线段

**功能：** 创建二维或三维线段，Vec2/Vec3 不能混用。

**接口：**
```python
# 三维线（Vec3）
Line(Vec3(x1,y1,z1), Vec3(x2,y2,z2), Vec3(x3,y3,z3), ...)

# 二维线（Vec2）
Line(Vec2(x1,y1), Vec2(x2,y2), Vec2(x3,y3), ...)
```

**示例：**
```python
line3d = Line(Vec3(0,0,0), Vec3(100,0,25), Vec3(0,100,50))
line2d = Line(Vec2(0,0), Vec2(100,0), Vec2(0,100))
```

> 来源：[geometry_Line.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Line.md)

---

### 3.7 Text — 文字

**功能：** 创建二维文字或三维文字（通过 Sweep 扫掠）。

**接口：**
```python
# 二维文字
Text(content, width, height).color(r, g, b, a)

# 三维文字
text = Text(content, width, height)
line = Line(Vec3(0,0,0), Vec3(0,0,thickness))
ThreeDText = Sweep(text, line).color(r, g, b, a)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `content` | str | 文字内容 |
| `width` | float | 文字宽度 |
| `height` | float | 文字高度 |

**示例：**
```python
text2d = Text('参数化组件', 10, 10).color(1, 1, 1, 1)

text = Text('BIMBase', 100, 100)
line = Line(Vec3(0,0,0), Vec3(0,0,20))
text3d = Sweep(text, line).color(0, 0, 1, 1)
```

> 来源：[geometry_Text.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Text.md)

---

## 四、复杂造型

### 4.1 Section — 截面

**功能：** 装填二维几何体（Vec2、Line、Arc）作为放样截面，供 Loft / Sweep 使用。截面默认位于 XOY 平面。

**接口：**
```python
Section(point1, geom1, point2, geom2, ...)
```

**关键约束：**
- 仅接受 **Vec2** 和二维 Line/Arc，**禁止 Vec3**
- 相邻元素首尾相接（前一终点 = 后一起点）
- 支持截面间布尔操作：`Section(...) - Section(...)`

**矩形截面形心规范（必读）：**

矩形截面的形心是几何中心，四个顶点关于形心对称分布。创建矩形截面时，**必须使用 `translate(-L/2, -W/2, 0)` 将截面平移至形心在原点**：

```python
# 正确：形心在原点（推荐）
rect_section = translate(-L/2, -W/2, 0) * Section(
    Vec2(0, 0), Vec2(L, 0), Vec2(L, W), Vec2(0, W)
)

# 错误：形心不在原点，定位困难
rect_section = Section(Vec2(0,0), Vec2(L,0), Vec2(L,W), Vec2(0,W))
```

**示例：**
```python
# 矩形截面（4个Vec2角点自动闭合）
section = Section(Vec2(0,0), Vec2(100,0), Vec2(100,50), Vec2(0,50))

# 半圆弧截面
section = Section(
    Vec2(100, -100),              # 起点
    scale(100) * Arc(0.5 * pi),   # 上半圆弧
    Vec2(-100, 100),              # 终点
    Vec2(-100, -100)              # 闭合回起点
)

# 圆形截面
section = Section(scale(100, 100) * Arc(2 * pi))

# 截面布尔（外矩形挖孔）
sectionOut = Section(Vec2(0,0), Vec2(100,0), Vec2(100,100), Vec2(0,100))
sectionHole = Section(Vec2(80,80), Vec2(60,80), Vec2(60,60), Vec2(80,60))
combined = sectionOut - sectionHole   # 带矩形孔的截面
```

> 来源：[geometry_Section.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Section.md)
> 参考：[Section参数化.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/Section参数化.py)

---

### 4.2 Loft — 放样

**功能：** 通过多个截面（至少 2 个）按顺序连接扫掠形成复杂曲面或实体。适用于变截面建模。

**接口：**
```python
Loft(section1, section2, ..., sectionN)          # 至少2个截面
Loft(*section_list)                              # 列表解包
```

**关键约束：**
| 约束 | 说明 |
|------|------|
| **数量** | 至少 2 个截面 |
| **空间分离** | 截面必须通过 `translate` 在空间上分离，否则退化为平面 |
| **结构对应** | 线对线、弧对弧、点对点，分段数一致 |
| **方向一致** | 所有截面同为顺时针或同为逆时针 |
| **开闭一致** | 所有截面同开或同闭 |
| **Type约束** | Section 内仅用 Vec2，禁止 Vec3 |
| **截面数建议** | 简单形状 2~5，复杂形状 7~15，>20 有波动风险 |

**示例：**
```python
# 示例1：矩形截面等截面拉伸（推荐：Section+Loft 替代 Box/Cube）
# 形心在原点，沿Z+拉伸 H
rect_section = translate(-L/2, -W/2, 0) * Section(
    Vec2(0, 0), Vec2(L, 0), Vec2(L, W), Vec2(0, W)
)
loft = Loft(
    translate(0, 0, z_centroid) * rect_section,
    translate(0, 0, z_centroid + H) * rect_section
)

# 示例2：圆形渐变截面（三截面：大→中→小）
base = Section(scale(D1) * Arc(2 * pi))              # 基准圆截面
sec1 = translate(0, 0, 0) * base                     # 起始
sec2 = scale(0.75) * translate(0, 0, H/2) * base     # 中间缩小
sec3 = scale(0.5) * translate(0, 0, H) * base        # 终点缩小
loft = Loft(sec1, sec2, sec3)

# 示例3：弹簧螺旋（密集截面采样）
sections = []
for angle in linspace(0, total_angle, n):
    z = z_per_rad * angle
    positioned = translate(0, 0, z) * (rotz(angle) * section)
    sections.append(positioned)
spring = Loft(*sections)
spring.smooth = True                                 # 启用平滑
```

> 来源：[geometry_Loft.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Loft.md)
> 参考：[Loft参数化.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/Loft参数化.py)、[弹簧.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/造型构件/弹簧.py)

---

### 4.3 Sweep — 扫掠

**功能：** 将一个截面沿轨迹路径扫掠形成实体。适用于等截面沿路径建模。

**接口：**
```python
Sweep(section, path)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `section` | Section | 扫掠截面（需预先旋转使法线对齐轨迹） |
| `path` | Line | 扫掠轨迹，只能为 **一段直线** 或 **一段圆弧** |

**关键约束：**
- **必须旋转截面使法线对齐轨迹方向**，否则退化为平面
- 轨迹只能为单段直线或单段圆弧，禁止多段线
- 截面旋转：`rotate(Vec3(1,0,0), 0.5*pi) * Section(...)` 将 XOY 截面翻转到 XOZ 平面

**示例：**
```python
# 基本扫掠：矩形截面沿直线
section = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), Vec2(100,0), Vec2(100,100), Vec2(0,100))
path = Line(Vec3(0,0,0), Vec3(500, 0, 0))
sweep = Sweep(section, path)

# 圆形扫掠：截面沿弧线（形成弯管）
section = translate(R, 0, 0) * rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(r) * Arc(2*pi))
path = Line(Arc(pi/2))                                  # 90度圆弧轨迹
sweep = Sweep(section, path)                            # 90度弯管

# 带孔洞截面的扫掠
sectionOut = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(0,0), Vec2(100,0), Vec2(100,100), Vec2(0,100))
sectionHole = rotate(Vec3(1,0,0), 0.5*pi) * Section(Vec2(80,80), Vec2(60,80), Vec2(60,60), Vec2(80,60))
line = Line(Arc(pi/2))
sweep = Sweep(sectionOut - sectionHole, line)             # 带矩形孔的管
```

> 来源：[geometry_Sweep.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Sweep.md)
> 参考：[Sweep参数化.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/Sweep参数化.py)

---

### 4.4 Combine — 组合

**功能：** 将多个几何体组合成一个逻辑组，不做布尔融合，保留各自颜色和属性。

**接口：**
```python
combine(geom1, geom2, ..., geomN)
```

**示例：**
```python
group = combine(part1, part2, part3)
# 可对整个 group 进行统一变换
transformed_group = translate(100, 0, 0) * group
```

> 来源：[geometry_Combine.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Combine.md)
> 参考：[Combine参数化.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/Combine参数化.py)

---

### 4.5 Bool — 布尔运算

**功能：** 执行几何体的布尔减和布尔交运算。

**接口：**
```python
result = a - b                   # 布尔减：从 a 中减去 b
result = Intersect(a, b)         # 布尔交：取 a 和 b 的交集
```

**注意：** 布尔运算后会**抹除颜色**，需重新 `.color(r,g,b,a)` 设置。

**示例：**
```python
# 布尔减：挖洞
result = (box_a - box_b).color(0, 0.7, 0, 1)

# 布尔交：取交集
result = Intersect(box_a, box_b).color(0, 0, 1, 1)
```

> 来源：[geometry_Bool.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Bool.md)
> 参考：[Fusion参数化.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/Fusion参数化.py)、[Intersect参数化.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/Intersect参数化.py)

---

### 4.6 Linspace — 等分点序列

**功能：** 生成从起点到终点的等分点序列，支持矢量和数值形式。

**接口：**
```python
linspace(a, b, n)              # 生成 n 个等分点（n-1 份）
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `a`, `b` | Vec3 / float | 起点和终点 |
| `n` | int | 生成 n 个点（等分 n-1 份） |

**示例：**
```python
# 空间矢量：沿 X 轴 10 个等分点
for i in linspace(Vec3(0,0,0), Vec3(1000,0,0), 10):
    points.append(translate(i))

# 数值：圆周等分
for i in linspace(0, pi*2*11/12, 12):
    points.append(translate(Vec3(R*cos(i), R*sin(i), 0)))
```

> 来源：[geometry_Linspace.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Linspace.md)

---

## 五、变换操作

变换通过 `*` 作用于几何体，**从右到左**执行。角度使用**弧度制**。

### 平移 translate

```python
translate(x, y, z) * geom              # 三维数值
translate(Vec3(x,y,z)) * geom          # Vec3 矢量
translate(x, y) * geom                 # 二维（仅 XY 平面）
trans(x, y, z) * geom                  # 简写
```

### 旋转 rotate

```python
rotate(Vec3(0,0,1), pi/2) * geom       # 绕 Z 轴正方向 90°
rotate(pi/2) * geom                    # 默认绕 Z 轴
rotx(pi/2) * geom                      # 绕 X 轴
roty(pi/2) * geom                      # 绕 Y 轴
rotz(pi/2) * geom                      # 绕 Z 轴
```

### 缩放 scale

```python
scale(r) * geom                        # 单参数等比缩放
scale(rx, ry) * geom                   # 两参数平面缩放
scale(rx, ry, rz) * geom               # 三参数三轴缩放
```

### 组合变换

```python
# 从右到左：先缩放(scale)，再平移(translate)
result = translate(100, 0, 0) * scale(500, 200, 400) * Cube()

# 先缩放，再绕 Z 轴旋转90°，再平移
result = translate(1000, 0, 0) * rotate(Vec3(0,0,1), pi/2) * scale(500,200,400) * Cube()
```

> 来源：[matrix_interface.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/matrix_interface.md)
> 参考：[旋转平移.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/旋转平移.py)

---

## 六、布置接口

### 旋转布置

```python
FinalGeometry = 我的组件()
RotationPlace.RotationFunction(FinalGeometry)
place(FinalGeometry)
```

### 两点线性布置

沿线性变量（如"长"）均匀排布，变量名须与 Attr 名完全一致。

```python
FinalGeometry = 我的组件()
TwoPointPlace.linearize(FinalGeometry, '长')
place(FinalGeometry)
```

> 来源：[place_interface.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/place_interface.md)
> 参考：[两点布置.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/两点布置.py)

---

## 七、驱动点/特征点

在组件上定义几何特征点，支持吸附对齐和参数化联动。在 `replace()` **之前**调用。

**接口：**
```python
self.setDrivenFeaturePoint(
    '特征点名称',                    # 必须唯一
    SnapMode.GeometricCenter,       # 吸附模式
    'X坐标表达式',                   # 支持数学运算和 Attr 引用
    'Y坐标表达式',
    'Z坐标表达式'
)
```

**SnapMode 枚举：**

```python
class SnapMode(Enum):
    Invalid              = -1          # 非法值
    First                = 0           # 初始化
    Nearest              = 1           # 最近点
    MidPoint             = 1 << 2      # 中点
    Center               = 1 << 3      # 中心点
    EndPoint             = 1 << 4      # 端点
    Intersection         = 1 << 6      # 交点
    Tangency             = 1 << 7      # 相切
    TangentPoint         = 1 << 8      # 相切点
    Perpendicular        = 1 << 9      # 垂直
    PerpendicularPoint   = 1 << 10     # 垂直点
    Parallel             = 1 << 11     # 平行
    Multi3               = 1 << 12     # （内部使用）
    Multi1               = 1 << 14     # （内部使用）
    Multi2               = 1 << 15     # （内部使用）
    GeometricCenter      = 1 << 16     # 几何中心点，闭合截面/对称体
    Quadrant             = 1 << 17     # 象限点
    Extension            = 1 << 18     # 延伸线
    ApparentIntersection = 1 << 19     # 外观交点
    Insertion            = 1 << 20     # 插入点
    Node                 = 1 << 21     # 节点
    enGetBaseCurve       = 1 << 22     # 基准线
```

> **驱动点常用**：`SnapMode.GeometricCenter`（几何中心）、`SnapMode.EndPoint`（端点）。其余枚举值用于 BIMBase 内部捕捉系统。

**示例：**
```python
class myPart(Component):
    def __init__(self):
        Component.__init__(self)
        self['长'] = Attr(1000, obvious=True)
        self['宽'] = Attr(300, obvious=True)
        self['高'] = Attr(500, obvious=True)
        self['结果'] = Attr(None, show=True)

        # 中心点：几何中心
        self.setDrivenFeaturePoint('point_center', SnapMode.GeometricCenter,
            '[定位点 X]', '[定位点 Y]', '[定位点 Z]')

        # 前端右上角：端点
        self.setDrivenFeaturePoint('point_front_top_right', SnapMode.EndPoint,
            '[定位点 X] + [长]', '[定位点 Y] + [宽]', '[定位点 Z] + [高]')

        self.replace()
```

> 来源：[drive_point_interface.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/drive_point_interface.md)

### 表达式编写规则（经实验验证）

> 对照实验（椭圆球.py vs 椭圆球 copy.py）确认：`*` `/` `()` `**` 均正常支持。驱动点失效的唯一根因是**表达式引用了 `obvious=False` 的隐藏 Attr 参数**。

| 规则 | 严重性 | 说明 |
|------|--------|------|
| **引用的 Attr 必须 obvious=True** | **硬性要求** | 隐藏参数导致表达式解析失败，驱动点不显示 |
| **不需修改时加 readonly=True** | 最佳实践 | `obvious=True, readonly=True` 置灰，保证驱动点正常同时满足不可改性 |
| **三轴必须含定位点** | 硬性要求 | 不含 `[定位点X/Y/Z]` 则无法跟随插入点偏移 |
| `*0.5` 等乘法 | 无限制 | 已证实可用 |
| 括号 `()` 分组 | 无限制 | 已证实可用 |

---

## 八、颜色设置

**接口：**
```python
geom.color(R, G, B, Alpha)
```

| 参数 | 范围 | 说明 |
|------|------|------|
| R, G, B | 0.0 ~ 1.0 | 红、绿、蓝分量 |
| Alpha | 0.0 ~ 1.0 | 不透明度（1=完全不透明，0=完全透明） |

**常用颜色速查：**

| 颜色 | 代码 |
|------|------|
| 白色 | `.color(1, 1, 1, 1)` |
| 黑色 | `.color(0, 0, 0, 1)` |
| 红色 | `.color(1, 0, 0, 1)` |
| 绿色 | `.color(0, 1, 0, 1)` |
| 蓝色 | `.color(0, 0, 1, 1)` |
| 黄色 | `.color(1, 1, 0, 1)` |
| 半透明 | `.color(1, 0, 0, 0.5)` |

**注意：** 布尔运算后会抹除颜色，需重新设置。

> 来源：[geometry_Color.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/01_sdk_interface_guide/geometric_interface/geometry_Color.md)

---

## 九、自定义组件模板

以下组件原生 API 不支持，需用 Loft/Sweep 组合实现，直接复用代码。

### 9.1 椭球体

通过逐层 Loft 放样椭圆截面实现。t ∈ [-1, 1] 覆盖完整椭球（两端缩为点）。

> 来源：[custom_Ellipsoid.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/04_custom_components/custom_Ellipsoid.md)
> 参考：[SKILL.md 椭球体模板](file:///D:/BIMbase/PythonScript/BFAComponentLib/SKILL.md#L136-L178)

### 9.1b 半椭球体（底面椭圆截面，高度拉伸）

通过逐层 Loft 放样椭圆截面实现。t ∈ [0, 1] 仅覆盖上半部分，底面（t=0）为完整椭圆截面，顶点（t=1）缩为一点。缩放因子 `scale_xy = sqrt(1 - t²)` 来自椭球方程 `(x/a)² + (y/b)² + (z/c)² = 1`。

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

### 9.2 圆形截面圆环

圆形截面沿圆形路径 Sweep 扫掠。

```python
# 关键步骤：
# 1. 创建圆形截面并径向偏移
section_2d = translate(ring_r, 0) * scale(tube_r, tube_r) * Section(Arc(2.0 * pi))
# 2. 旋转截面法线对齐轨迹（绕X轴旋转-90°）
section_3d = rotate(Vec3(1, 0, 0), -0.5 * pi) * section_2d
# 3. 创建圆形轨迹
path = Line(Arc(2.0 * pi))
# 4. 扫掠
torus = Sweep(section_3d, path)
```

> 来源：[custom_CircularTorus.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/04_custom_components/custom_CircularTorus.md)

### 9.3 方形截面圆环

方形截面沿圆形路径 Sweep 扫掠。

```python
section_2d = Section(
    Vec2(ring_r - half, -half),
    Vec2(ring_r + half, -half),
    Vec2(ring_r + half, half),
    Vec2(ring_r - half, half),
    Vec2(ring_r - half, -half),
)
section_3d = rotate(Vec3(1, 0, 0), -0.5 * pi) * section_2d
torus = Sweep(section_3d, Line(Arc(2.0 * pi)))
```

> 来源：[custom_SquareTorus.md](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/04_custom_components/custom_SquareTorus.md)

---

## 十、Python 建模文件五大组成部分

完成一个 BIMBase 模型建模 Python 文件，包含以下五个部分：

### 第一部分：参数设定（`__init__` + `Attr`）

定义所有用户可调参数、下拉选项、只读显示参数和最终模型输出槽位。

```python
class 长方体(Component):
    def __init__(self):
        Component.__init__(self)
        self['长'] = Attr(1000, obvious=True, combo=[500,1000,2000])
        self['宽'] = Attr(300.0, obvious=True)
        self['高'] = Attr(500, obvious=True)
        self['长方体'] = Attr(None, show=True)      # 最终输出槽位
        self.replace()
```

### 第二部分：截面、直线等几何准备

在 `replace()` 中定义截面、线段、圆弧等基础几何元素，为后续建模做准备。

```python
    @export
    def replace(self):
        L = self['长']; W = self['宽']; H = self['高']

        # 截面定义
        test_section = Section(Vec2(0,0), Vec2(L,0), Vec2(L,W), Vec2(0,W))

        # 轨迹直线
        test_line = Line(Vec3(0,0,0), Vec3(0,0,H))

        # 圆截面
        circle_section = Section(scale(50) * Arc(2*pi))
```

### 第三部分：模型构建

使用 Loft、Sweep、Cube、Cone、Sphere、Box 等方法构建三维实体。

```python
        # 放样构建
        loft = Loft(test_section, translate(0,0,H) * test_section)

        # 扫掠构建
        sweep = Sweep(rotated_section, test_line)

        # 基础几何体
        cube = scale(L, W, H) * Cube()
```

### 第四部分：模型组装

使用 `combine()` 组合多个几何体，或使用布尔运算 `-` / `Intersect()` 进行切割。

```python
        # 组合装配
        result = combine(body, cap, handle)

        # 布尔切割
        body_with_hole = body - hole_cutter
```

### 第五部分：模型生成（输出）

将最终结果赋值给 `show=True` 的 Attr 槽位，并在 `__main__` 中 `place()`。

```python
        # 赋值输出
        self['长方体'] = result

if __name__ == "__main__":
    FinalGeometry = 长方体()
    place(FinalGeometry)
```

---

## 十一、建模决策树

```
┌─────────────────────────────────────────────────────────┐
│                    选择建模方法                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 简单规则体？                                          │
│     ├─ 是 → Cube / Sphere / Cone / Box                   │
│     └─ 否 → 进入 2                                       │
│                                                         │
│  2. 截面是否沿路径渐变（变截面）？                          │
│     ├─ 否（等截面）→ 使用 Sweep                           │
│     │   - 单段直线轨迹：Line(Vec3(...), Vec3(...))       │
│     │   - 单段圆弧轨迹：Line(Arc(angle))                 │
│     │   - 必须旋转截面：rotate(Vec3(1,0,0), -pi/2)       │
│     │                                                   │
│     └─ 是（变截面）→ 使用 Loft                           │
│         - 线性渐变：2 截面即可                            │
│         - 非线性路径/螺旋：密集截面采样（linspace）        │
│         - 截面方向/开闭/分段必须一致                       │
│                                                         │
│  3. 多个独立几何体需要统一管理？                           │
│     ├─ 需融合 → combine()                                │
│     ├─ 需切割 → 布尔减 a - b                             │
│     └─ 需取交集 → Intersect(a, b)                        │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                 核心约束速查                               │
├─────────────────────────────────────────────────────────┤
│  - Vec2 ⊆ Section, Vec3 ⊆ Line/变换/几何体               │
│  - Section 禁止混入 Vec3                                 │
│  - Loft 截面 ≥ 2，结构一致（线对线、弧对弧）               │
│  - Sweep 轨迹仅单段直线或圆弧；截面法线必须对齐轨迹         │
│  - 布尔运算后颜色被抹除，需重设 .color()                   │
│  - 单位 mm，角度弧度制，右手坐标系                          │
│  - 变换从右到左执行：translate * rotate * scale * geometry │
└─────────────────────────────────────────────────────────┘
```

---

## 附录：完整示例 — 月饼建模

> 来源：[月饼.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/造型构件/月饼.py)

该示例综合运用了 Section、Loft、Sweep、Sphere、Bool、Combine、Array、Text 等方法：

```python
from pyp3d import *

class 月饼(Component):
    def __init__(self):
        Component.__init__(self)
        self['月饼直径'] = Attr(128.0, obvious=True)          # 参数设定
        self['月饼厚'] = Attr(48.0, obvious=True)
        self['月饼'] = Attr(None, show=True)                  # 输出槽位
        self.replace()

    @export
    def replace(self):
        radis = self['月饼直径']
        thickness = self['月饼厚']

        # 截面准备：圆形截面
        mainsection = Section(scale(radis/2) * Arc(2*pi))

        # 模型构建：主体放样
        mainloft = Loft(mainsection, translate(0,0,thickness) * mainsection)
        mainloft = mainloft.color(255/255, 183/255, 14/255, 0.95)

        # 内馅放样
        mainsectioninner = Section(scale(radis/2 - radis/20) * Arc(2*pi))
        mainloftinner = Loft(
            translate(0,0,radis/20) * mainsectioninner,
            translate(0,0,thickness - radis/20) * mainsectioninner
        ).color(228/255, 101/255, 29/255, 1)

        # 花边：Sweep 扫掠 + Array 阵列
        sectionOutloop = translate(-radis/3, 0, thickness) * \
            rotate(Vec3(1,0,0), 0.5*pi) * Section(scale(radis/100) * Arc(pi))
        sweeploop = Sweep(sectionOutloop, Line(Arc(2*pi)))

        # 模型组装：combine 组合
        self['月饼'] = combine(mainloft, mainloftinner, sweeploop)

if __name__ == "__main__":
    place(月饼())
```

---

> **文档编制日期：** 2026-07-13
> **知识库来源：**
> - [SKILL.md](file:///D:/BIMbase/PythonScript/BFAComponentLib/SKILL.md)
> - [BIMBase_AIAgent_建模指南.md](file:///D:/BIMbase/PythonScript/BFAComponentLib/BIMBase_AIAgent_建模指南.md)
> - [BIMBaseMCP/skill/](file:///D:/01/tyafc-master/tyafc-master/BIMBaseMCP/skill/)
> - [参数化组件样例/基本体教学](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学)
> - [参数化组件样例/造型构件](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/造型构件)
> - [参数化组件样例/自建/建模方法分析.md](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/自建/建模方法分析.md)

---

## 十二、给部件表面添加散热片（线性阵列）

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
- 例如：主体 X 正向面在 `X = half_side`，散热片形心 `X = half_side + 散热片深度/2`

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
# 居中放置：阵列整体形心与阵列面形心重合
start_pos = -(散热片数量 - 1) * 散热片间距 / 2.0

# 散热片Z方向范围（居中于主体中点）
散热片Z底 = 散热箱中点Z - 散热片高度 / 2.0
散热片Z顶 = 散热箱中点Z + 散热片高度 / 2.0

# 创建单个散热片（截面在XOY面，形心在(cx,cy)，沿Z拉伸）
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

# 合并所有散热片
散热片阵列 = combine(*散热片列表)
```

> 参考：[水泵.py](file:///D:/BIMbase/PythonScript/BFAComponentLib/task/830建模/水泵/水泵.py)
