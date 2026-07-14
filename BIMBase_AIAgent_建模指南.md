# BIMBase AI Agent Python 编程建模指南

> 本文档基于对 `tyafc` 项目（BIMBase AI 智能助手）的源码解析整理而成，目标是帮助你使用 AI Agent + MCP 完成 BIMBase 的 `pyp3d` 参数化建模。

---

## 一、项目作用与功能总览

`tyafc` 是一个面向 **BIMBase 建模软件** 的 AI 智能编程助手，核心目标是：**用户用自然语言描述几何构件 → AI Agent 检索 SDK 知识库 → 生成符合规范的 `pyp3d` Python 脚本 → 在 BIMBase 内嵌 Python 中执行 → 自动布置到视图**。

### 1.1 技术栈

| 层 | 技术 | 说明 |
|----|------|------|
| 前端 | PySide6 (Qt) | 桌面聊天客户端，SSE 流式对话，代码提取与执行 |
| 后端 | Flask | REST API + LangGraph Agent 调度 |
| AI 框架 | LangChain / LangGraph | Agent、工具调用、流式输出 |
| LLM | MiniMax / DeepSeek / 本地 Qwen | 多模型可切换 |
| 数据库 | MySQL 8.0 | 用户、会话、消息持久化 |
| 知识检索 | **MCP Server (FastMCP)** | BIMBase SDK 知识库的结构化检索 |
| 知识库 | Markdown + YAML frontmatter | 按能力分级组织的 SDK 文档 |

### 1.2 数据流

```
用户自然语言输入
    → Qt 前端 (chat_app.py) 发送 HTTP/SSE
    → Flask 后端 LangGraph Agent
    → 通过 MCP / skill_doc 工具检索知识库
    → 调用 LLM 生成 pyp3d 代码
    → 前端提取 ```python 代码块，保存到 generated_scripts/
    → 调用 BIMBase 内嵌 Python (python-3.7.9-embed-amd64) 执行
    → place() 布置到 BIMBase 视图
```

### 1.3 目录关键点

- `BIMBaseMCP/mcpServer/` — **MCP 服务器**（本文档重点），提供知识库检索工具链。
- `BIMBaseMCP/skill/` — **SDK 知识库**，按 P0~P3 能力分级组织的 Markdown 文档。
- `backend/agent/` — LangGraph Agent（prompts、tools、core、config）。
- `frontend/` — PySide6 客户端，负责代码提取与 BIMBase 内嵌 Python 执行。

---

## 二、MCP 服务器：协助 AI Agent 建模的核心

MCP（Model Context Protocol）服务器是让 AI Agent **稳定、可控地检索 BIMBase SDK 文档** 的关键组件。它避免了 Agent 凭记忆瞎猜 `pyp3d` 函数名/参数的问题。

### 2.1 启动方式

MCP 服务器基于 `fastmcp`，要求 **Python >= 3.10**（BIMBase 内嵌的 3.7.9 不兼容，需用独立 Python，如 Miniconda）。

`BIMBaseMCP/mcpServer/start_mcp_server.bat`：
```bat
@echo off
REM fastmcp 要求 Python >= 3.10
"D:\Miniconda\python.exe" "...\BIMBaseMCP\mcpServer\MCPServer.py"
```

服务器以 HTTP 传输方式启动在 `0.0.0.0:8888`：
```python
mcp.run(transport="http", host="0.0.0.0", port=8888)
```

MCP 客户端配置示例（`.mcp.json` 风格；本项目内 codegraph 用的是 stdio，BIMBase 建模服务器则是 HTTP/SSE，接入时按客户端支持的方式配置到 `http://<host>:8888`）。

### 2.2 MCP 提供的工具（Tools）

| 工具 | 参数 | 作用 |
|------|------|------|
| `get_summary_document()` | 无 | **首次建模必调**。返回知识库概要（`summary_skill.md`），了解全部可用 SDK 与文档路径。 |
| `get_skill_manifest(include_reference=False, force_refresh=False, agent_input="")` | 见下 | 返回**结构化 JSON 索引**：所有 symbol、路径、分类、别名、关键词、依赖、优先级。用于稳定检索、避免猜函数名。 |
| `get_skill_doc(symbol, include_reference=False, agent_input="")` | symbol 如 `Cube`/`Sweep`/`Bool`/`matrix_interface` | 按标准 symbol 获取**单个**文档正文（返回 `{symbol, path, content}`）。 |
| `get_skill_bundle(symbols, include_reference=False, include_dependencies=True, agent_input="")` | symbols 为列表 | **批量**获取多个文档正文，减少多次调用；`include_dependencies=True` 时自动附带 `must_load_with` 依赖（如 `basic_writing_style`）。 |
| `get_related_skills(symbol, include_reference=False, agent_input="")` | symbol | 返回该 symbol 的常见配套函数（基于 `related`）与必载依赖。 |

> `agent_input` 参数用于把 Agent 的原始意图/上下文摘要传给监控层（`monitoring.py`），便于调试与评测，可选。

### 2.3 MCP 提供的 Prompt

`bimbase_modeling_guide()` — 一个可附加的 System Prompt，指导 Agent 的建模工作流（详见第三节）。客户端在处理建模需求时应把它注入到对话上下文。

### 2.4 检索机制内部原理（`MCPServer.py`）

- **扫描**：`_scan_skill_docs()` 递归扫描 `skill/**/*.md`，解析 YAML frontmatter，推断 symbol 与分类（geometry/interface/safety/pattern/custom_component）。
- **覆盖增强**：`skill_manifest_overrides.json` 为每个 symbol 补充 `aliases`（中英文别名）、`keywords`、`related`、`priority`，大幅提升模糊匹配命中率。例如 `Cube` 别名含 `立方体/长方体/方盒`。
- **归一化匹配**：`_normalize_text()` 做大小写、全半角、标点、空白归一化并保留 CJK，使中文/英文/别名都能匹配到同一文档。
- **强制依赖注入**：所有 `geometry/interface/pattern` 类文档自动附带 `basic_writing_style`（编码规范），确保生成代码始终符合规范。
- **安全沙箱**：`_safe_resolve_skill_path()` 禁止路径穿越与符号链接逃逸，只能访问 `SKILL_ROOT` 内文档。
- **缓存**：manifest 结果缓存，`force_refresh=True` 可强制刷新。

### 2.5 Agent 使用 MCP 的推荐调用序列

```
1. get_summary_document()                       # 了解全局
2. get_skill_manifest()                          # 拿到结构化 symbol 索引
3. 规划需要的 symbol（如 Cube / Sweep / Bool）
4. get_skill_bundle(["Cube","Sweep","Bool"])     # 批量取文档（自动带编码规范）
   （可选）get_related_skills("Sweep")            # 找配套函数
5. 依据文档生成 pyp3d 代码
```

---

## 三、AI Agent 建模标准工作流（Prompt 约定）

来自 `MCPServer.py::bimbase_modeling_guide()` 与 `backend/agent/prompts.py`。

### 3.1 检索与规划
- **绝对不要凭记忆猜测函数名或参数**（`pyp3d` API 与常规 Python 库完全不同）。
- 先 `get_skill_manifest()` 浏览所有几何体/操作 API，找到 `description` 符合预期的 `symbol`。

### 3.2 批量获取文档
- 规划好所有 symbol 后调用 `get_skill_bundle(...)` 一次性取回，含前置依赖规范。
- 需配套操作时用 `get_related_skills(symbol)`。

### 3.3 遵循编码规范（不可违反）
- 顶部必须 `from pyp3d import *`
- 文件中**只能有一个**继承 `Component` 的类
- 用 `self['参数名'] = Attr(...)` 定义参数，`__init__` 末尾调用 `self.replace()`
- 造型逻辑写在 `@export` 装饰的 `replace(self)` 方法中
- 在 `replace` 内通过 `L = self['长']` 提取参数，不写死数值
- `if __name__ == "__main__":` 下实例化并 `place(实例)` 显示结果

### 3.4 渐进式披露（backend Agent 的 `skill_doc` 版本）
后端另有一套基于 `skill_doc` 工具的三级检索（概览 → 列表 → 详情），与 MCP 工具功能等价，适用于未接 MCP 的场景。

---

## 四、pyp3d 建模规范（必读）

来源：`02_coding_standards_safety/basic_writing_style.md`

### 4.1 参数化组件基本结构

```python
from pyp3d import *

class pythonModel(Component):
    def __init__(self):
        Component.__init__(self)
        # 定义参数及默认值
        self['长'] = Attr(1000, obvious=True, combo=[500,1000,2000,3000,4000])
        self['宽'] = Attr(300.0, obvious=True)
        self['高'] = Attr(500, obvious=True)
        self['长方体'] = Attr(None, show=True)   # 输出槽位
        self.replace()

    @export
    def replace(self):
        L = self['长']
        W = self['宽']
        H = self['高']
        TestCube = scale(L, W, H) * Cube()
        self['长方体'] = TestCube

if __name__ == "__main__":
    FinalGeometry = pythonModel()
    place(FinalGeometry)
```

### 4.2 Attr 参数说明

`Attr(value, obvious=False, readonly=False, combo=None, show=False)`

- `obvious` 属性的可见性：`True` 时可见，`False` 时不可见。默认为 `False`。
- `readonly` 属性的只读性：`True` 时不可调，为置灰状态，`False` 时可调。默认为 `False`。
- `combo=[...]`：下拉选项（元素类型须与 value 一致，且必须包含默认值）
- `show=True`：最终几何体输出槽位（默认值填 `None`）
- 控制标签必须**全小写**

### 4.3 高频约束

| 约束 | 说明 |
|------|------|
| Type 约束 | `Section` 仅装填 Vec2、二维 Line、Arc，**禁止 Vec3** |
| Arc 起点方向 | 默认从 X 轴逆时针；不确定时显式构造 |
| 维度一致性 | Vec2/Vec3 不混用；路径/截面/变换维度一致 |
| Loft/Sweep 前置校验 | 截面顺序、线对线对应、开闭属性统一 |
| 单位 | 默认 **mm** |
| 命名 | 中文变量名多词用 `_` 连接，所有标点用英文；参数名不含特殊符号；不用数组角标做参数名 |

### 4.4 失败优先排查

1. 参数越界或单位不一致（mm vs m）
2. 截面方向或接缝不一致
3. 几何维度混用（Vec2/Vec3）
4. 过渡关系不连续导致自交/扭转
5. 重复构造导致性能下降
6. 文件结构违规（含多个 class）

---

## 五、SDK 接口速查（pyp3d API 参考）

> 每个 API 对应 MCP 的一个 symbol，使用前请通过 MCP 获取完整文档，勿凭记忆。

### 5.1 基础几何体

| symbol | 接口签名 | 说明 |
|--------|----------|------|
| `Cube` | `Cube()` / `scale(L,W,H)*Cube()` | 单位立方体（中心在原点），缩放得长方体 |
| `Sphere` | `Sphere()` / `scale(r)*Sphere()` | 球体，只能等比缩放（不支持椭球） |
| `Cone` | `Cone(centerA, centerB, radiusA, radiusB)` | 圆锥/圆台；`radiusA==radiusB` 时为圆柱 |
| `Box` | `Box(baseOrigin, topOrigin, vectorX, vectorY, baseX, baseY, topX, topY)` | 任意朝向四棱台，顶底尺寸相同为棱柱/长方体 |
| `Arc` | `Arc(angle)` / `Arc(startP, midP, endP)` | 单位圆弧（半径1，X轴起点逆时针）或三点圆弧 |
| `Line` | `Line(p1, p2, ...)` | 二维/三维线段（Vec2/Vec3 不混用） |
| `Text` | `Text(content, width, height)` | 二维文字；三维文字用 Sweep 沿 Z 轴线段扫掠 |

### 5.2 复杂造型

| symbol | 接口签名 | 说明 |
|--------|----------|------|
| `Section` | `Section(point1, geom1, point2, ...)` | 装填 Vec2/Line/Arc 作为放样截面；默认在 XOY 平面 |
| `Loft` | `Loft(sec1, sec2, ..., secN)` | 多截面放样（至少2个）；截面须空间分离，方向/开闭/分段一致 |
| `Sweep` | `Sweep(section, path)` | 截面沿轨迹扫掠；**必须旋转截面使法线对齐轨迹**，否则退化为平面 |
| `Combine` | `combine(a, b, ...)` | 组合成组，不做布尔融合，保留各自属性/颜色 |
| `Bool` | `a - b`（减）/ `Intersect(a, b)`（交） | 布尔运算；运算后颜色被抹除需重设 |
| `Linspace` | `linspace(a, b, n)` | 等分点序列（n 个点，n-1 份），支持矢量/数值 |

### 5.3 变换与布置

| symbol | 用法 | 说明 |
|--------|------|------|
| `matrix_interface` | `translate(x,y,z)` / `trans(...)` / `rotate(axis, rad)` / `rotx/roty/rotz(rad)` / `scale(...)` | 变换用 `*` 作用于几何体，**从右到左**执行；角度为**弧度制**；右手坐标系 |
| `PlaceInterface` | `RotationPlace.RotationFunction(g)` / `TwoPointPlace.linearize(g, '长')` | 旋转布置、两点线性布置；线性变量名须与 Attr 名完全一致 |
| `DrivePointInterface` | `self.setDrivenFeaturePoint(name, SnapMode.X, 'X表达式', 'Y表达式', 'Z表达式')` | 驱动点/特征点，支持吸附对齐（`GeometricCenter`/`EndPoint`）；在 `replace()` 前定义。**表达式规则**：禁止 `*0.5`（用 `/2`）、禁止括号 `()`（展开为加减）、三轴必须含 `[定位点X/Y/Z]` |
| `Color` | `geom.color(R, G, B, Alpha)` | RGBA 0~1；链式调用；布尔后需重设 |

### 5.4 变换示例

```python
# 组合变换（先缩放，再平移；从右到左）
testcube = translate(100, 100, 100) * scale(500, 200, 400) * Cube()
rotatecube = rotate(Vec3(0, 0, 1), pi/2) * scale(500, 200, 400) * Cube()
```

---

## 六、自定义组件库（原生 API 无法直接生成，直接复用）

来源：`04_custom_components/`。遇到对应需求时**直接复制复用**。

### 6.1 椭球体（Loft 放样实现）
`custom_Ellipsoid` — 参数：X/Y/Z 半轴、截面数、旋转角度、XYZ 位移。通过逐层计算椭圆截面 + `Loft` 拟合。

### 6.2 圆形截面圆环（Sweep 扫掠实现）
`custom_CircularTorus` — 参数：环半径、截面半径、旋转角度、XYZ。圆形截面沿圆形路径 `Sweep`。关键：`ring_r > tube_r` 避免退化。

### 6.3 方形截面圆环（Sweep 扫掠实现）
`custom_SquareTorus` — 参数：环半径、截面边长、旋转角度、XYZ。方形截面沿圆形路径 `Sweep`。

> 三个组件的完整源码见 `BIMBaseMCP/skill/04_custom_components/*.md`，或通过 MCP `get_skill_doc("custom_Ellipsoid")` 获取。

---

## 七、多组件内联装配

来源：`03_professional_patterns/assembly_guide.md`（MCP symbol：`assembly_guide`）

将多个独立 `.py` 组件合并为**单个总装脚本**时：
- **禁止**跨文件类导入（`from a import A`）
- **禁止**动态加载（`importlib`/`exec`/`eval`/运行时路径加载）
- 两组件建模逻辑必须内联到同一文件，命名冲突用前缀消歧（`comp_a_*`、`comp_b_*`）
- 总装文件结构：公共 import/常量 → 组件A内联区 → 组件B内联区 → 总装定位组合区 → 统一入口

---

## 八、脚本执行环境

AI 生成的脚本由 BIMBase **内嵌 Python** 执行（`frontend/workers/script.py`）：

```
<BIMBase安装目录>\PythonScript\python-3.7.9-embed-amd64\python.exe  <脚本路径>
```

- 执行超时 120 秒，捕获 stdout/stderr 回传前端。
- **注意版本差异**：建模脚本运行在内嵌 **Python 3.7.9**；而 MCP 服务器需 **Python >= 3.10**，两者是不同解释器，不要混用。
- 脚本入口须包含 `if __name__ == "__main__":` 并调用 `place(...)`，才能在 BIMBase 视图中布置结果。

---

## 九、给 AI Agent 的实操清单（TL;DR）

1. **接 MCP**：将 BIMBase MCP Server 挂到 `http://<host>:8888`，Agent 具备 5 个检索工具 + 1 个建模 Prompt。
2. **建模第一步**：`get_summary_document()` → `get_skill_manifest()`。
3. **取文档**：`get_skill_bundle([需要的symbol])`，自动附带 `basic_writing_style` 编码规范。
4. **写代码**：严格遵循「一个 Component 类 + Attr 参数 + @export replace() + place()」结构，单位 mm，弧度制，Vec2/Vec3 不混用。
5. **复杂几何**：椭球/圆环等优先复用 `04_custom_components/` 模板。
6. **执行**：脚本交由 BIMBase 内嵌 Python 3.7.9 运行，`place()` 输出到视图。
7. **不猜函数名**：任何 `pyp3d` API 使用前必须先从 MCP/知识库读到对应文档。

---

*本指南由项目源码解析整理，覆盖 MCP 工具链、Agent 工作流、pyp3d 规范、SDK 接口速查、自定义组件与执行环境，可直接作为 AI Agent 建模的上下文/参考资料。*
