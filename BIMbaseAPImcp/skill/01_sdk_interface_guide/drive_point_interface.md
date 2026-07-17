---
name: DrivePointInterface
description: 驱动点（特征点）设置与联动特性指南
author: BIMBase SDK Team
version: "1.0"
doc_type: sdk_interface
---

## 功能说明

`setDrivenFeaturePoint()` 方法用于在组件上定义几何特征点，支持与其他组件通过吸附模式（SnapMode）实现位置联动和对齐。

**核心能力：**<br>
- 定义组件的关键几何位置（中心、端点、角点等）
- 通过 SnapMode 指定吸附模式：`GeometricCenter`（几何中心）、`EndPoint`（端点）
- 坐标表达式支持数学运算，实现参数化联动

## 接口形式

```python
self.setDrivenFeaturePoint(
    'point1',              # 特征点名称
    SnapMode.GeometricCenter,  # 吸附模式
    '[定位点 X]',          # X 坐标表达式
    '[定位点 Y]',          # Y 坐标表达式  
    '[定位点 Z]'           # Z 坐标表达式
)
```

## SnapMode（吸附模式）枚举

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
    GeometricCenter      = 1 << 16     # 几何中心点，适用于闭合截面/对称体
    Quadrant             = 1 << 17     # 象限点
    Extension            = 1 << 18     # 延伸线
    ApparentIntersection = 1 << 19     # 外观交点
    Insertion            = 1 << 20     # 插入点
    Node                 = 1 << 21     # 节点
    enGetBaseCurve       = 1 << 22     # 基准线
```

> **驱动点常用**：`SnapMode.GeometricCenter`（几何中心）、`SnapMode.EndPoint`（端点）。其余枚举值用于 BIMBase 内部捕捉系统，驱动点定义中通常不使用。

## 标准流程

### Step 1：在 `__init__` 中定义驱动点
```python
class Cylinder(Component):
    def __init__(self, r=1.0, h=10.0):
        Component.__init__(self)
        self['圆柱'] = Attr(None, show=True)      # 几何输出槽位
        
        # ========== 定义驱动点 ==========
        # 中心点：用于对齐其他组件的基准位置
        self.setDrivenFeaturePoint('point_center', SnapMode.GeometricCenter, '[定位点 X]', '[定位点 Y]', '[定位点 Z]')
        
        # 上端面中心：顶部对齐位
        self.setDrivenFeaturePoint('point_top', SnapMode.EndPoint, 
            '[定位点 X]', '[定位点 Y] + self.h/2', '[定位点 Z]')
        
        # 下端面中心：底部对接位
        self.setDrivenFeaturePoint('point_bottom', SnapMode.EndPoint,
            '[定位点 X]', '[定位点 Y] - self.h/2', '[定位点 Z]')
```

### Step 2：在 `replace()` 中生成几何
```python
    @export
    def replace(self):
        r, h = self.r, self.h
        # 生成圆柱体（具体实现略）
        solid = Cylinder(r, h)
        self['圆柱'] = solid
```

## 核心特性总结

| 特性 | 说明 |
|------|------|
| **位置绑定** | 特征点坐标表达式随组件尺寸变化自动更新，实现参数化联动 |
| **吸附对齐** | SnapMode 决定与其他组件的吸附行为：中心对中心、端点对端点 |
| **数学运算** | 支持 `+`、`-`、`*`、`/`、`**` 及属性引用（如 `[长]`）。**注意**：引用的 Attr 参数必须 `obvious=True`，否则表达式解析失败 |
| **批量定义** | 可在一个组件中定义多个特征点，分别用于不同对接需求 |

## 表达式编写规则（经实验验证）

> 通过对照实验（椭圆球.py 对比椭圆球 copy.py）证实：**BIMBase 表达式解析器支持 `*`、`/`、`()`、`**` 等全部数学运算符**，驱动点失效的唯一原因是**引用了 `obvious=False` 的隐藏 Attr 参数**。

| 规则 | 严重性 | 说明 |
|------|--------|------|
| **引用的 Attr 必须 obvious=True** | **硬性要求** | 引用 `obvious=False` 的隐藏参数会导致表达式整体解析失败，驱动点不显示或回退到原点 |
| **不想让用户修改加 readonly=True** | 最佳实践 | 参数仅为驱动点服务、用户不应修改时，设 `obvious=True, readonly=True` 置灰，既保证驱动点正常又满足不可改性 |
| **三轴必须含定位点** | 硬性要求 | 表达式必须包含 `[定位点X]`/`[定位点Y]`/`[定位点Z]`，否则特征点无法跟随插入点 |
| `*0.5` 和 `*` 乘法 | 无限制 | 椭圆球.py 已验证 `*`、`**` 均可正常使用 |
| 括号 `()` 分组 | 无限制 | 椭圆球.py 已验证嵌套括号 `((...)/(...))` 正常工作 |

## 注意事项

```markdown
- **特征点名称唯一性**：每个组件内的驱动点名称必须唯一<br>- **SnapMode 匹配**：对接时两个组件的 SnapMode 需语义一致（中心对中心、端点对端点）<br>- **表达式维度**：X/Y/Z 三个表达式缺一不可，用于三维空间定位<br>- **表达式语法**：必须包含 `[定位点X/Y/Z]`；引用的 Attr 参数必须 `obvious=True`；若参数不需用户修改则加 `readonly=True`；数学运算（`+` `-` `*` `/` `**` `()`）无限制<br>- **几何顺序**：先调用 `setDrivenFeaturePoint`，最后再调用 `self.replace()` |
```

## 接口用例

### 示例 1：实心圆柱驱动点定义（中心 + 上下端面）
```python
from pyp3d import *

class SolidCylinder(Component):
    def __init__(self, r=1.0, h=10.0):
        Component.__init__(self)
        self['圆柱'] = Attr(None, show=True)
        
        # 中心：对齐基准<br>self.setDrivenFeaturePoint('point1', SnapMode.GeometricCenter,
            '[定位点 X]', '[定位点 Y]', '[定位点 Z]')
        
        # 上端中心（Y+ 偏移）<br>self.setDrivenFeaturePoint('point2', SnapMode.EndPoint,
            '[定位点 X]', '[定位点 Y] + self.h/2', '[定位点 Z]')
        
        # 下端中心（Y- 偏移）<br>self.setDrivenFeaturePoint('point3', SnapMode.EndPoint,
            '[定位点 X]', '[定位点 Y] - self.h/2', '[定位点 Z]')
    
    @export
    def replace(self):
        r, h = self.r, self.h
        # Sweep 实现省略...
        pass
```

### 示例 2：长方体主体对接位（核心中心 + 角点对齐）
```python
from pyp3d import *

class BoxBody(Component):
    def __init__(self, section_h=120):
        Component.__init__(self)
        self['长'] = Attr(section_h - 16)      # 长度联动变量<br>self['宽'] = Attr(5.0)<br>self['高'] = Attr(100.0)<br>self['扫掠体'] = Attr(None, show=True)
        
        # point1: 前端左上角<br>self.setDrivenFeaturePoint('point1', SnapMode.EndPoint,
            '[定位点 X]', '[定位点 Y]', '[定位点 Z]')
        
        # point2: 前端右上角（X+长）<br>self.setDrivenFeaturePoint('point2', SnapMode.EndPoint,
            '[定位点 X] + [长]', '[定位点 Y]', '[定位点 Z]')
        
        # point3: 几何中心（核心对接位，用于整体对齐）<br>self.setDrivenFeaturePoint('point3', SnapMode.GeometricCenter,
            '[定位点 X] + [长]/2', '[定位点 Y] + [宽]/2', '[定位点 Z] + [高]/2')
    
    @export
    def replace(self):
        L, W, H = self['长'], self['宽'], self['高']<br>pass  # Sweep/Loft 实现省略
```

## 质量检查 Checklist

```markdown
- [ ] 驱动点名称在组件内唯一<br>- SnapMode.GeometricCenter 用于中心对齐<br>- SnapMode.EndPoint 用于端点对齐<br>- X/Y/Z 表达式包含三个维度，缺一不可<br>- 数学运算使用英文符号（`+` `-` `*` `/` `**` `()`），无特殊限制<br>- 三轴必须包含 `[定位点X]`/`[定位点Y]`/`[定位点Z]`<br>- 表达式引用的所有 Attr 必须 `obvious=True`（隐藏参数导致解析失败）
```

## 性能提示

- 驱动点不产生额外几何计算开销，仅存储位置约束信息<br>- 复杂组件建议集中定义 3–5 个关键点：中心 + 两端/四角 + 特征面