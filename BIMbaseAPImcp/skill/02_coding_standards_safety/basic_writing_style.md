***

name: ParameterizedComponent
description: 参数化组件开发指导
author: BIMBase SDK Team
version: "2.0"
doc\_type: coding\_standard
---------------------------

## 功能说明

定义参数化组件，通过继承 `Component` 类并实现属性配置和造型方法，实现可配置的参数化建模。

**基本结构：**

```python
from pyp3d import *

class pythonModel(Component):
    def __init__(self):
        Component.__init__(self)
        # 定义参数及其默认值
        self['长'] = Attr(1000, obvious=True, combo=[500,1000,2000,3000,4000])
        self['宽'] = Attr(300.0, obvious=True)
        self['高'] = Attr(500, obvious=True)
        self['长方体'] = Attr(None, show=True)
        self.replace()
    
    @export
    def replace(self): 
        L = self['长']
        W = self['宽']
        H = self['高']
        TestCube = scale(L,W,H) * Cube()
        self['长方体'] = TestCube

if __name__ == "__main__":
    FinalGeometry = pythonModel()
    place(FinalGeometry)
```

## 首要动作（先做再写代码）

**必须完成的步骤：**

1. 确认脚本与工程上下文包含并使用 `from pyp3d import *`
2. 明确组件目标、参数清单、参数范围、几何约束、异常输入边界
3. 确认输出模式：是否使用 `Component + Attr + @export + replace()` 的参数化组件结构

**未完成的禁止进入实现。**

## 角色职责与架构原则

| 维度       | 要求                  |
| -------- | ------------------- |
| **组件架构** | 参数层级清晰、默认值合理、参数联动稳定 |
| **几何正确** | 保持拓扑一致、方向一致、边界条件可处理 |
| **代码质量** | 命名清晰、结构可维护、可复用      |
| **性能意识** | 减少冗余几何运算，避免重复构造     |

- **Attr 参数说明**：  - `obvious=True`：UI 中显示为可见参数（用户可调节）  - `combo=[]`：提供下拉选项列表,可以用int或str（如 `[500,1000,2000]`）  - `show=True`：Attr 槽位显示最终几何体结果。**关键规则：每个组件只保留一个最终的组装槽位（`show=True`），不要为每个部件单独设置 `show=True` 槽位，多个 show 槽位会导致组装时的布尔运算失败。**- **变量简化**：通过 `self['参数名']` 方式读取，避免直接写死默认值 |

## pyp3d 使用准则（高频约束）

| 约束类型               | 说明                                                     |
| ------------------ | ------------------------------------------------------ |
| **Type 约束**        | `Section` 仅装填允许类型（Vec2、二维 Line、Arc），禁止 Vec3            |
| **Arc 起点方向**       | 默认从 X 轴逆时针绘制，不确定时显式构造：`Arc(angle, start=..., end=...)` |
| **维度一致性**          | Vec2/Vec3不混用；路径、截面、变换维度保持一致（二维语义内）                     |
| **Loft/Sweep前置校验** | 截面顺序、对应关系（线对线）、开闭属性必须统一                                |
| **单位约束**          | 默认为mm                                                  |

## 输出代码要求

- 必须遵循项目既有编码风格
- 代码块按"几何结构部分"清晰分段，段与段之间保留空行
- 每个几何结构段写明其生成对象与参数关系：  `# 缩放基准截面到目标尺寸`
- **错误处理**：给出可读反馈，便于定位参数问题（如负半径报错）

## 失败优先排查（6 大项）

| 序号 | 检查点                            |
| -- | ------------------------------ |
| 1  | 参数越界或单位不一致（mm vs m）            |
| 2  | 截面方向或接缝不一致                     |
| 3  | 几何维度混用（Vec2/Vec3）              |
| 4  | 过渡关系不连续导致自交或扭转                 |
| 5  | 重复构造导致性能下降                     |
| 6  | **文件结构违规**：python 文件中含多个 class |

## 接口用例

### 完整示例：圆柱体参数化组件

```python
from pyp3d import *

class myPart(Component):
    def __init__(self):
        Component.__init__(self)
        self['半径'] = Attr(100, obvious=True)      # 主尺寸
        self['高度'] = Attr(200, obvious=True)       # 主尺寸
        self['结果'] = Attr(None, show=True)         # 输出槽位
        self.replace()
    
    @export
    def replace(self):
        R = self['半径']                             # 读取参数
        H = self['高度']
        cylinder = Cylinder(R, H)                    # 生成几何（R>0）
        self['结果'] = cylinder                      # 赋值输出槽位

FinalGeometry = myPart()
place(FinalGeometry)
```

### 复杂示例：带过渡曲面的放样件

```python
from pyp3d import *

class TransitionLoft(Component):
    def __init__(self):
        Component.__init__(self)
        self['大直径'] = Attr(200, obvious=True)
        self['小直径'] = Attr(100, obvious=True)
        self['长度'] = Attr(500, obvious=True)
        self['过渡体'] = Attr(None, show=True)
        self.replace()
    
    @export
    def replace(self):
        D1 = self['大直径']
        D2 = self['小直径']
        L = self['长度']
        
        # 基准截面：半圆环（起点→弧→终点→返回）
        base_section = Section(
            Vec2(-D1/2, -D1),   # 左下点
            scale(D1) * Arc(0.5*pi),  # 上半圆弧
            Vec2(D1/2, D1),    # 右上点
            Vec2(D1/2, -D1)     # 闭合回右下（形成半圆环）
        )
        
        # 三个截面：起点对齐、方向一致、数量对应
        sec_start = translate(0, -L/3) * base_section   # 大端
        sec_mid   = scale((D1+D2)/2) * translate(0, L/3) * base_section  # 中间过渡
        sec_end   = scale(D2/D1) * translate(0, 2*L/3) * base_section    # 小端
        
        loft = Loft(sec_start, sec_mid, sec_end)
        self['过渡体'] = loft
```

## 编码注意事项

| 规范类型        | 要求                                                 |
| ----------- | -------------------------------------------------- |
| **命名规则**    | 使用中文变量名时，多个单词用\_连接（如`base_section`），不用空格；所有标点符号用英文 |
| **导入语句**    | 文件顶部必须包含 `from pyp3d import *`                     |
| **类结构**     | Python 文件中只能定义一个 Component 子类（禁止多 class）           |
| **@export** | `replace()` 方法必须使用 `@export` 装饰器，否则参数变化不会触发重新计算    |
| **输出模式**    | `place(FinalGeometry)` 用于在视图中显示最终结果                |

## 注意事项