---
name: bimbase-modeling-agent-interaction
description: AI Agent 与用户进行 BIMBase pyp3d 建模交互时的行为规范技能。定义信息收集、代码生成、确认流程的完整规范。
---

# BIMBase AI Agent 建模交互技能

> **冲突优先级规则（最高优先级，必须遵守）**
> 1. **建模技术要求**：本地 skills/markdown 内容若与 `BIMBaseAI2PY_MCPServer` 获取到的建模技术要求（函数签名、参数语义、几何定位语义、编码规范等）发生冲突或解释不同，**以 `BIMBaseAI2PY_MCPServer` 为第一执行准则**。
> 2. **个人建模喜好**：涉及个人建模喜好（建模定位提示词喜好、特殊模型部件调用，如散热片、半椭球体等）时，**以本地 skills/markdown 为第一执行准则**。

> 本技能定义了 AI Agent 在协助用户在 BIMBase 中通过 Python 建模时应遵循的**信息收集 → 代码生成 → 确认交付**全流程交互规范。

---

## 核心原则

1. **绝不猜测**：任何 pyp3d 函数签名和参数必须从知识库检索确认，禁止凭记忆。
2. **信息不全必问**：建模尺寸、位置、角度等关键信息缺失或有歧义时，必须先提问澄清。
3. **一次问清**：把所有关键疑问集中一次提出，避免反复打断用户。
4. **遵循标准结构**：生成的代码必须遵循 Component + Attr + @export replace() + place() 规范。
5. **先对齐再编码**：用户输入（图片/文字）为笼统描述时，必须先完成「部件理解对齐」与「建模精细/复杂度确认」，再进入信息提取与编码。

---

## 建模前需求对齐与复杂度确认（强制）

用户输入（图片 / 文字提示词）通常是笼统概括的描述，直接编码极易偏离意图。进入信息提取前，必须依次完成：

1. **部件理解对齐（盘问式，参考 grill-me 逻辑）**
   - **图片输入**：先做**图片解析**，识别目标模型由哪些部件组成（不把图中所有标注/尺寸表/无关符号都当成建模对象）。
   - **文字提示词**：先拆解出建模部件清单。
   - 对图片/文字中**识别不清楚**的部件，主动、逐个盘问确认（"我理解该部件是 XX、尺寸约 XX，是否正确？"），直到双方对"模型由哪些部件、每个部件是什么"达成一致。
   - 目标：让 Agent 对目标模型的**部件理解**与用户建模目标对齐，**剔除冗余与错误信息干扰**。

2. **建模精细/复杂程度确认（是否简化）**
   - 在输出「建模参数确认表」之前，向用户确认各部件建模的精细/复杂程度。
   - 不能只问"要不要简化"，必须**给出具体简化方案描述供用户选择**（2~4 个由简到繁档位，说明每档建什么、略去什么）。
   - 例：是否需要栏杆、栏杆是"立柱+双横杆"还是"仅双横杆"、是否建螺栓/倒角等细节。
   - **例外（跳过）**：用户明确要求"复刻 / 按图片尺寸 / 按建模提示词建模"时，视为要求完整精细建模，不再确认复杂度。

### 图片识别结果汇报模板（图片解析后必输出）

Agent 完成图片解析后，按以下 6 段固定结构整理汇报给用户确认：

1. **总体信息**：模型类型 + 关键总体尺寸/参数（例："钢筋混凝土烟囱，高 60m，筒壁坡度 i=0.02，4 种筒壁型号"）
2. **尺寸表格**：把图中截面/尺寸表整理成 markdown 表格（例：`| 标高 | 壁厚 | 外径 |`）
3. **建模部件清单**：可辨识部件逐条列出（例：变坡筒壁、内衬、隔热层、烟气入口、顶部环形平台、栏杆、避雷针、钢爬梯）
4. **尺寸信息**：图中代号/局部尺寸（例：`R=950/1100/1250/1500、A=4500、K=1100`）
5. **属性业务信息**：模型名称、各部件名称、材质/型号等业务属性（对应 Attr 的"专业属性"分组）
6. **疑惑点列表**：图片识别不清楚、无法确认的部分，单独列出请用户裁定

> 汇报后再进入「复杂度确认」环节。

### 复杂度确认话术（汇报后必做）

用结构化多选向用户确认复杂度：

1. **建模范围（多选）**：列出所有可辨识部件，让用户勾选要建模的部件
2. **各部件精细度**：对需确认的部件给出 2~4 档简化方案（例：栏杆 → A.立柱+双横杆 / B.仅双横杆 / C.不建）
3. **缺失尺寸处理**：图中未标注的尺寸给出可调默认值（例：内衬 120/隔热 80，参数化可调）

> 例外：用户明确要求"复刻 / 按图片尺寸 / 按建模提示词建模"时跳过本环节。

### 结构化提问话术模板（向用户提问时通用）

| 要素 | 说明 | 示例 |
|------|------|------|
| header | 简短标题 | "筒壁型号" |
| question | 具体问题 | "默认按哪个筒壁型号建模？" |
| options | 2~4 个选项，每项 label + description | "TB60/2.0（囱口内径 2.0m，中间型号，推荐）" |
| multiSelect | 多选题设 true | "建模范围包含哪些部件？" |

要求：
1. 一次集中问清所有关键疑问，避免反复打断
2. 选项 description 说明推荐项及理由
3. 关键尺寸/数量/朝向/是否参数化等必须问清，不靠猜

---

## 第一部分：用户会告诉 AI Agent 的信息

### 1. 建模顺序（使用模型方法的顺序）

用户会按照建模的物理顺序描述步骤，例如：
- "先以 (0,0,0) 为原点绘制一个 100x50 的矩形截面"
- "再沿 Z 轴方向拉伸 200mm 形成长方体"
- "然后在长方体顶面中心放置一个半径 20 的球体"

**AI Agent 需做什么：**
- 理解步骤间的依赖关系
- 将自然语言步骤映射为 pyp3d 函数调用序列
- 识别每步对应的 API（Section → Loft / Sweep → place）

### 2. 每步的建模尺寸与临时坐标系原点位置

用户会明确给出：
- **尺寸参数**：长度、宽度、高度、半径、角度等（单位 mm）
- **临时坐标系原点**：如"以 (1,2,3) 为临时坐标点"
- **方向描述**：如"沿着 X 轴方向"

**示例输入：**
> 以 (0,0,0) 为临时坐标点，沿 X 轴方向绘制长度为 1500mm 的直线

**AI Agent 需做什么：**
- 将用户给的临时坐标系原点转为 `translate(x,y,z)` 或 `Vec3(x,y,z)`
- 将方向描述转为正确的向量参数（如 X轴→Vec3(1,0,0)）
- 确保所有尺寸单位统一为 mm

### 3. 参数名称与 BIMBase 参数面板设置

用户会指定哪些参数可以被修改、哪些不可修改：

| 参数类型 | Attr 设置 | 说明 |
|----------|-----------|------|
| **可填写修改** | `obvious=True` | 面板可见，可调（`obvious` 仅控制可见性，`True`=可见，默认 `False`） |
| **下拉选取** | `obvious=True, combo=[...]` | 只能从预设选项中选择 |
| **仅显示不可修改** | `obvious=True, readonly=True` | 可见但置灰不可调（`readonly` 仅控制可调性，默认 `False`） |
| **不可见内部参数** | `obvious=False`（或不设置） | 不在面板显示 |
| **最终模型输出** | `show=True, value=None` | 几何体输出槽位，可见但不可调。**关键规则：每个组件只保留一个最终的组装槽位，不要为每个部件单独设置 `show=True` 槽位，多个 show 槽位会导致组装时的布尔运算失败。** |

**示例输入：**
> 参数"长"=1000mm，下拉可选 [500, 1000, 2000]；参数"宽"=300mm，可填写；参数"旋转角度"=45°，仅显示

**AI Agent 需做什么：**
```python
self['长'] = Attr(1000, obvious=True, combo=[500, 1000, 2000, 3000])    # 下拉选取
self['宽'] = Attr(300.0, obvious=True)                                    # 可填写修改
self['旋转角度'] = Attr(45.0, obvious=True, readonly=True)                # 仅显示
```

### 4. 特征点 / 驱动关系

用户会指定哪些截面的哪些点需要作为特征点，用于 BIMBase 中的驱动关系。

**示例输入：**
> 长方体底面中心点、顶面四个角点需要作为特征点

**AI Agent 需做什么：**

**关键规则：绝大多数情况默认使用 `SnapMode.GeometricCenter`。** 截面圆心、拉伸体轴线终点/中点、几何体表面形心、几何体体心 → 一律使用 `GeometricCenter`。只有明确是几何体角点/顶点时才使用 `EndPoint`。

```python
# 中心点 → GeometricCenter
self.setDrivenFeaturePoint('底心', SnapMode.GeometricCenter,
    '[定位点X]', '[定位点Y]', '[定位点Z]')

# 角点 → EndPoint
self.setDrivenFeaturePoint('角1', SnapMode.EndPoint,
    '[定位点X] + [长]/2', '[定位点Y] + [宽]/2', '[定位点Z] + [高]')
```

**Agent 必须在代码生成前，以表格形式与用户确认每个特征点的位置和 SnapMode 类型：**

| 特征点名称 | 位置描述 | 建议 SnapMode | 是否正确？ |
|-----------|---------|--------------|-----------|
| 底心 | 长方体底面几何中心 | `GeometricCenter` | ？ |
| 角1 | 长方体顶面右前角 | `EndPoint` | ？ |

SnapMode 完整枚举：

```python
class SnapMode(Enum):
    Invalid = -1, First = 0, Nearest = 1,
    MidPoint = 1<<2, Center = 1<<3, EndPoint = 1<<4,
    Intersection = 1<<6, Tangency = 1<<7, TangentPoint = 1<<8,
    Perpendicular = 1<<9, PerpendicularPoint = 1<<10, Parallel = 1<<11,
    Multi3 = 1<<12, Multi1 = 1<<14, Multi2 = 1<<15,
    GeometricCenter = 1<<16,   # 几何中心点（默认首选）
    Quadrant = 1<<17, Extension = 1<<18,
    ApparentIntersection = 1<<19, Insertion = 1<<20,
    Node = 1<<21, enGetBaseCurve = 1<<22
```

### 5. 其他补充信息

用户可能提供的额外信息：
- 颜色要求：如"主体红色半透明"
- 特殊约束：如"椭球长轴=2×短轴"
- 装配关系：如"组件A底部对齐组件B顶部"
- 布尔运算：如"在长方体上挖一个直径30的通孔"
- 阵列：如"沿圆周均匀分布12个"
- 布置方式：如"使用两点布置，线性变量为'长'"

---

## 第二部分：AI Agent 的交互流程

### 流程总览

```
用户输入（图片 / 文字提示词）
  → 部件理解（图片解析 / 提示词拆解）
  → 部件理解对齐（识别不清处盘问确认，参考 grill-me 逻辑）
  → 建模精细/复杂程度确认（是否简化）
  → 信息提取与校验 → 缺失信息提问
  → MCP/知识库检索 → 代码生成 → 自检 → 交付
```

---

### Step 1：信息提取与校验

从用户输入中提取以下关键信息：

| 提取项 | 关键问题 | 缺失时处理 |
|--------|----------|------------|
| **模型类型** | 需要构建什么？ | 必须提问 |
| **建模步骤顺序** | 先做什么，后做什么？ | 必须提问 |
| **每步尺寸** | 长/宽/高/半径/角度？ | 必须提问 |
| **每步位置** | 以哪个点为临时原点？ | 可推断默认(0,0,0) |
| **每步方向** | 沿哪个轴/向量？ | 可推断默认Z轴 |
| **参数面板设置** | 哪些可调？哪些下拉？哪些只读？ | 可推断默认全部 obvious=True |
| **特征点** | 需要哪些点做驱动？ | 可选 |
| **颜色** | 什么颜色？ | 可推断默认白色 |
| **布置方式** | 单点/两点/旋转？ | 可推断默认单点 place() |

**判定标准：** "做错的代价" > "问一句的成本" 时，必须提问。

---

### Step 2：缺失信息提问模板

当关键信息缺失时，以**结构化选项**方式提问，一次问清所有问题。

**模板格式：**

```
在开始编写代码之前，需要确认以下信息：

**1. 建模步骤与尺寸**
- [列出需要确认的每个步骤及相关尺寸]

**2. 临时坐标系原点**
- 步骤X 的临时原点在哪里？（如：(0, 0, 0)）

**3. 参数面板设置**
- 参数"XX"：可修改 / 下拉选择 / 仅显示？

**4. 特征点**（如需要）
- 需要定义哪些特征点？在哪些位置？

**5. 颜色与样式**
- 需要什么颜色？（默认白色）
```

---

### Step 3：知识库检索（MCP / 本地文档）

在编写代码前，按以下顺序检索技术文档：

1. **MCP 方式（优先）**：
   ```
   get_summary_document() → get_skill_manifest() → get_skill_bundle([需要的symbol])
   ```
   - 来源：`BIMBaseAI2PY_MCPServer`（远程 `https://dev.pkpm.cn/mcp/`）

2. **本地文档方式**：
   - `D:\BIMbase\PythonScript\BFAComponentLib\SKILL.md`
   - `D:\BIMbase\PythonScript\BFAComponentLib\BIMBase_AIAgent_建模指南.md`
   - `D:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_pyp3d_建模方法函数大全.md`

3. **参考示例方式**：
   - `D:\BIMbase\PythonScript\BFAComponentLib\参数化组件样例\基本体教学\`
   - `D:\BIMbase\PythonScript\BFAComponentLib\参数化组件样例\造型构件\`
   - `D:\BIMbase\PythonScript\BFAComponentLib\场布内置\`
   - `D:\BIMbase\PythonScript\BFAComponentLib\已有Py组件参考\`

---

### Step 4：代码生成

代码必须严格遵循标准结构：

#### 4.0 完整的代码结构模板

```python
from pyp3d import *

class 模型名称(Component):
    def __init__(self):
        Component.__init__(self)
        # ========== 参数设定 ==========
        # 可修改参数
        self['参数1'] = Attr(默认值, obvious=True)
        # 下拉选择参数
        self['参数2'] = Attr(默认值, obvious=True, combo=[选项列表])
        # 只读显示参数
        self['参数3'] = Attr(默认值, obvious=True, readonly=True)
        # 最终模型输出槽位
        self['结果'] = Attr(None, show=True)

        # ========== 特征点定义（可选）==========
        # self.setDrivenFeaturePoint('名称', SnapMode.GeometricCenter, 'X表达式', 'Y表达式', 'Z表达式')
        # 表达式规则：引用的 Attr 必须 obvious=True；若参数不需修改加 readonly=True；三轴必须含 [定位点X/Y/Z]；数学运算无限制
        # SnapMode 选择规则：截面圆心/轴线终点中点/表面形心/体心 → GeometricCenter（默认首选）；角点/顶点 → EndPoint
        # 必须在代码生成前与用户确认每个特征点的位置和 SnapMode 类型

        self.replace()

    @export
    def replace(self):
        # ========== 1. 读取参数 ==========
        p1 = self['参数1']
        p2 = self['参数2']

        # ========== 2. 截面、直线等几何准备 ==========
        # section = Section(Vec2(...), ...)
        # line = Line(Vec3(...), Vec3(...))

        # ========== 3. 模型构建 ==========
        # loft = Loft(...)
        # sweep = Sweep(...)
        # cube = scale(...) * Cube()

        # ========== 4. 模型组装 ==========
        # result = combine(part1, part2)
        # result = body - hole

        # ========== 5. 模型生成 ==========
        self['结果'] = result

if __name__ == "__main__":
    FinalGeometry = 模型名称()
    place(FinalGeometry)
```

#### 4.1 代码生成规则

| 规则 | 说明 |
|------|------|
| **中文命名** | 类名、参数名可用中文，多词用 `_` 连接 |
| **英文标点** | 所有标点符号用英文（`, ; : .`） |
| **变换顺序** | 从右到左：`translate * rotate * scale * geometry` |
| **弧度制** | 角度全部用弧度：`pi/2`, `30*pi/180` |
| **单位** | 默认 mm |
| **Vec2/3 不混用** | Section 只用 Vec2，其他用 Vec3 |

---

### Step 5：自检清单

代码生成后逐项核对：

- [ ] 顶部有 `from pyp3d import *`
- [ ] 文件中只有一个 `Component` 子类
- [ ] `replace()` 带 `@export` 装饰器，`__init__` 末尾调用 `self.replace()`
- [ ] 最终几何赋值给 `Attr(None, show=True)` 槽位
- [ ] 参数经 `self['名']` 读取，未写死数值
- [ ] Vec2/Vec3 未混用；`Section` 未传入 Vec3
- [ ] `Loft` 截面方向/开闭/分段一致且空间分离（不共面）
- [ ] `Sweep` 截面法线已旋转对齐轨迹，轨迹为单段直线或圆弧
- [ ] 布尔运算后已重设颜色
- [ ] 单位统一 mm，角度用弧度制
- [ ] `if __name__ == "__main__":` 下 `place(实例)` 输出
- [ ] 所有用户指定的参数面板设置（obvious/readonly/combo）均已正确配置
- [ ] 所有用户指定的特征点均已定义

---

## 第三部分：完整交互示例

### 示例对话

**用户：**
> 我需要做一个长方体，尺寸是长2000mm、宽1000mm、高500mm。参数"长"=2000可以有下拉选项[1000,2000,3000]；参数"宽"=1000可填写；参数"高"=500仅显示。底面中心和顶面四个角作为特征点。以(0,0,0)为原点。

**AI Agent 的思考与行动：**

1. **信息校验**：所有信息齐全，直接编码。

2. **检索**：MCP `get_skill_bundle(["Cube", "Attr"])` 获取接口文档。

3. **生成代码**：

```python
from pyp3d import *

class 长方体(Component):
    def __init__(self):
        Component.__init__(self)
        self['长'] = Attr(2000, obvious=True, combo=[1000, 2000, 3000])
        self['宽'] = Attr(1000.0, obvious=True)
        self['高'] = Attr(500, obvious=True, readonly=True)
        self['长方体'] = Attr(None, show=True)

        # 特征点：底面几何中心 → GeometricCenter
        self.setDrivenFeaturePoint('底心', SnapMode.GeometricCenter,
            '[定位点X]', '[定位点Y]', '[定位点Z]')
        # 特征点：顶面四个角 → EndPoint
        self.setDrivenFeaturePoint('顶角1', SnapMode.EndPoint,
            '[定位点 X] + [长]/2', '[定位点 Y] + [宽]/2', '[定位点 Z] + [高]')
        self.setDrivenFeaturePoint('顶角2', SnapMode.EndPoint,
            '[定位点 X] - [长]/2', '[定位点 Y] + [宽]/2', '[定位点 Z] + [高]')
        self.setDrivenFeaturePoint('顶角3', SnapMode.EndPoint,
            '[定位点 X] - [长]/2', '[定位点 Y] - [宽]/2', '[定位点 Z] + [高]')
        self.setDrivenFeaturePoint('顶角4', SnapMode.EndPoint,
            '[定位点 X] + [长]/2', '[定位点 Y] - [宽]/2', '[定位点 Z] + [高]')

        self.replace()

    @export
    def replace(self):
        L = self['长']
        W = self['宽']
        H = self['高']
        result = scale(L, W, H) * Cube()
        self['长方体'] = result

if __name__ == "__main__":
    FinalGeometry = 长方体()
    place(FinalGeometry)
```

---

### 示例对话：信息不全时

**用户：**
> 我要做一个圆台。

**AI Agent 的信息校验发现缺失：**

- 缺少底面半径
- 缺少顶面半径
- 缺少高度
- 缺少临时坐标系原点
- 缺少参数面板设置
- 缺少颜色

**AI Agent 提问：**

> 在开始编写代码之前，需要确认以下信息：
>
> **1. 圆台尺寸**
> - 底面半径？顶面半径？高度？（单位 mm）
>
> **2. 位置**
> - 临时坐标系原点在哪里？（默认 (0,0,0) 为底面圆心）
>
> **3. 参数面板设置**
> - "底面半径"：可修改 / 下拉选择 / 仅显示？
> - "顶面半径"：可修改 / 下拉选择 / 仅显示？
> - "高度"：可修改 / 下拉选择 / 仅显示？
>
> **4. 特征点**（如需要）
> - 是否需要定义特征点（底面圆心、顶面圆心、几何中心等）？
>
> **5. 颜色与样式**
> - 需要什么颜色？（默认白色）

---

## 第四部分：执行环境与依赖

### Python 解释器

所有建模脚本运行在 **BIMBase 内嵌 Python 3.7.9**：

```
D:\BIMBase KIT official 2026 R1.0\BIMBase KIT 2026\PythonScript\python-3.7.9-embed-amd64\python.exe
```

### pyp3d 库路径

```
D:\BIMBase KIT official 2026 R1.0\BIMBase KIT 2026\PythonScript\python-3.7.9-embed-amd64\Lib\site-packages\pyp3d
D:\BIMBase KIT official 2026 R1.0\BIMBase KIT 2026\PythonScript\python-3.7.9-embed-amd64\Lib\site-packages\
```

### 依赖包安装（需要时）

当建模需要额外依赖包（如 numpy）时，使用国内镜像源安装：

```powershell
cd "D:\BIMBase KIT official 2026 R1.0\BIMBase KIT 2026\PythonScript\python-3.7.9-embed-amd64"
.\python.exe .\get-pip.py
.\pip.exe install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
cd "D:\BIMBase KIT official 2026 R1.0\BIMBase KIT 2026\PythonScript\python-3.7.9-embed-amd64\Scripts"
.\pip.exe install numpy
```

---

## 第五部分：知识库索引

### MCP 工具链
| MCP Server | 服务地址 |
|------------|------|
| BIMBaseAI2PY_MCPServer | `https://dev.pkpm.cn/mcp/`（远程） |

### 本地文档路径
| 文档 | 路径 |
|------|------|
| 建模技能 SKILL.md | [D:\BIMbase\PythonScript\BFAComponentLib\SKILL.md](file:///D:/BIMbase/PythonScript/BFAComponentLib/SKILL.md) |
| AI Agent 建模指南 | [D:\BIMbase\PythonScript\BFAComponentLib\BIMBase_AIAgent_建模指南.md](file:///D:/BIMbase/PythonScript/BFAComponentLib/BIMBase_AIAgent_建模指南.md) |
| 建模方法函数大全 | [D:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_pyp3d_建模方法函数大全.md](file:///D:/BIMbase/PythonScript/BFAComponentLib/leder_skills/BIMBase_pyp3d_建模方法函数大全.md) |

### 参考示例路径
| 类型 | 路径 |
|------|------|
| 基本体教学 | [D:\BIMbase\PythonScript\BFAComponentLib\参数化组件样例\基本体教学\](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/基本体教学/) |
| 造型构件 | [D:\BIMbase\PythonScript\BFAComponentLib\参数化组件样例\造型构件\](file:///D:/BIMbase/PythonScript/BFAComponentLib/参数化组件样例/造型构件/) |
| 场布内置 | [D:\BIMbase\PythonScript\BFAComponentLib\场布内置\](file:///D:/BIMbase/PythonScript/BFAComponentLib/场布内置/) |

---

> **文档编制日期：** 2026-07-13
> **文件位置：** `D:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_AIAgent_建模交互技能.md`