# BIMBase Python 建模 Skills & MCP 配置总览

> 编制日期：2026-07-13
> 维护者：AI Agent

本文档汇总当前环境中为 BIMBase Python 脚本建模配置的所有 Skills 和 MCP 服务，包括加载方式、工具清单、知识库路径。

---

## 目录

1. [MCP 服务](#一mcp-服务)
   - [BIMBaseAI2PY — BIMBase pyp3d 知识检索服务](#11-bimbaseai2py--bimbase-pyp3d-知识检索服务)
   - [Excel — Excel 读写服务](#12-excel--excel-读写服务)
2. [Skills（技能）](#二skills技能)
   - [bimbase-pyp3d-modeling — BIMBase pyp3d 建模技能](#21-bimbase-pyp3d-modeling--bimbase-pyp3d-建模技能)
   - [bimbase-modeling-agent-interaction — BIMBase 建模交互技能](#22-bimbase-modeling-agent-interaction--bimbase-建模交互技能)
3. [本地知识库文档](#三本地知识库文档)
4. [参考代码示例](#四参考代码示例)

---

## 一、MCP 服务

MCP（Model Context Protocol）服务通过工具接口为 AI Agent 提供能力支撑。

### 配置文件

```
C:\Users\张德海（Jack）\AppData\Roaming\Trae CN\User\mcp.json
```

```json
{
  "mcpServers": {
    "Excel": {
      "command": "npx",
      "args": ["--yes", "@negokaz/excel-mcp-server"],
      "env": {
        "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
      },
      "fromGalleryId": "byted-mcp-volcengine.excel"
    },
    "BIMBaseAI2PY": {
      "command": "D:\\Miniconda\\python.exe",
      "args": ["D:\\01\\tyafc-master\\tyafc-master\\BIMBaseMCP\\mcpServer\\MCPServer.py"],
      "env": {},
      "description": "BIMBase pyp3d 建模技能文档检索服务 ⚠ 需 Python>=3.10 (fastmcp 依赖)"
    }
  }
}
```

---

### 1.1 BIMBaseAI2PY — BIMBase pyp3d 知识检索服务

| 项目 | 内容 |
|------|------|
| **类型** | MCP Command 服务（stdio 传输） |
| **配置方式** | `mcp.json` 文件配置 |
| **Python 解释器** | `D:\Miniconda\python.exe`（Python 3.13.12，需 >= 3.10） |
| **服务脚本** | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\mcpServer\MCPServer.py` |
| **知识库根目录** | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\` |
| **核心依赖** | `fastmcp`（MCP 框架）、YAML frontmatter 解析 |

#### 提供的工具（5 个）

| 工具名 | 参数 | 功能 |
|--------|------|------|
| `get_summary_document` | 无 | 返回知识库概要（全部可用 SDK 文档索引），**首次建模必调** |
| `get_skill_manifest` | `include_reference=False, force_refresh=False, agent_input=""` | 返回结构化 JSON 索引：所有 symbol、路径、分类、别名、关键词、依赖 |
| `get_skill_doc` | `symbol, include_reference=False, agent_input=""` | 按 symbol 获取**单个**文档正文 |
| `get_skill_bundle` | `symbols, include_reference=False, include_dependencies=True, agent_input=""` | **批量**获取多个文档正文，自动附带 `basic_writing_style` 编码规范 |
| `get_related_skills` | `symbol, include_reference=False, agent_input=""` | 返回该 symbol 的配套函数与必载依赖 |

#### 知识库结构

```
D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\
├── summary_skill.md                           # 全局概要
├── 01_sdk_interface_guide/                    # SDK 接口指南
│   ├── geometric_interface/                   #   几何接口
│   │   ├── property_Attr.md                   #     参数定义 Attr
│   │   ├── geometry_Cube.md                   #     立方体
│   │   ├── geometry_Sphere.md                 #     球体
│   │   ├── geometry_Cone.md                   #     圆锥/圆台/圆柱
│   │   ├── geometry_Box.md                    #     四棱台/长方体
│   │   ├── geometry_Arc.md                    #     圆弧
│   │   ├── geometry_Line.md                   #     线段
│   │   ├── geometry_Text.md                   #     文字
│   │   ├── geometry_Section.md                #     截面
│   │   ├── geometry_Loft.md                   #     放样
│   │   ├── geometry_Sweep.md                  #     扫掠
│   │   ├── geometry_Combine.md                #     组合
│   │   ├── geometry_Bool.md                   #     布尔运算
│   │   ├── geometry_Linspace.md               #     等分点序列
│   │   └── geometry_Color.md                  #     颜色
│   ├── matrix_interface.md                    #   变换接口
│   ├── place_interface.md                     #   布置接口
│   └── drive_point_interface.md               #   驱动点接口
├── 02_coding_standards_safety/                # 编码规范
│   └── basic_writing_style.md                 #   基础编写规范（自动附带）
├── 03_professional_patterns/                  # 专业模式
│   └── assembly_guide.md                      #   多组件内联装配指南
└── 04_custom_components/                      # 自定义组件模板
    ├── custom_Ellipsoid.md                    #   椭球体（Loft 实现）
    ├── custom_CircularTorus.md                #   圆形截面圆环（Sweep 实现）
    └── custom_SquareTorus.md                  #   方形截面圆环（Sweep 实现）
```

#### 推荐调用序列

```
1. get_summary_document()                           # 了解全局
2. get_skill_manifest()                              # 获取结构化 symbol 索引
3. 规划需要的 symbol（如 Cube / Sweep / Bool）
4. get_skill_bundle(["Cube", "Sweep", "Bool"])       # 批量取文档（自动带编码规范）
   （可选）get_related_skills("Sweep")               # 找配套函数
5. 依据文档生成 pyp3d 代码
```

---

### 1.2 Excel — Excel 读写服务

| 项目 | 内容 |
|------|------|
| **类型** | MCP Command 服务（npx） |
| **配置方式** | `mcp.json` 文件配置（Gallery 导入） |
| **服务包** | `@negokaz/excel-mcp-server` |
| **用途** | 非 BIMBase 建模直接相关，但可用于辅助数据处理（读取参数表、统计明细等） |

#### 提供的工具（7 个）

| 工具名 | 功能 |
|--------|------|
| `excel_read_sheet` | 读取工作表数据 |
| `excel_write_to_sheet` | 写入数据到工作表 |
| `excel_create_table` | 创建表格 |
| `excel_describe_sheets` | 获取工作表结构描述 |
| `excel_format_range` | 格式化单元格区域 |
| `excel_copy_sheet` | 复制工作表 |
| `excel_screen_capture` | 截取工作表截图 |

---

## 二、Skills（技能）

Skills 是 AI Agent 的提示词扩展，通过 markdown 文件导入，对 Agent 的建模行为进行规范和指导。

### 2.1 bimbase-pyp3d-modeling — BIMBase pyp3d 建模技能

| 项目 | 内容 |
|------|------|
| **类型** | 技能（Skill） |
| **加载方式** | 项目内 markdown 文件自动导入 |
| **文件路径** | `D:\BIMbase\PythonScript\BFAComponentLib\SKILL.md` |
| **适用范围** | 用户要求创建/编辑/组装 BIMBase 模型时需加载 |

#### 核心内容

| 章节 | 内容说明 |
|------|----------|
| **最高准则** | 先准确理解再编码；三级解惑协议（检索→推断→提问） |
| **核心原则** | 不凭记忆猜 API、单位 mm、弧度制、单 Component 类、Vec2/Vec3 不混用 |
| **标准结构** | Component + Attr + @export replace() + place() 模板代码 |
| **Attr 参数规范** | `obvious` 可见性（默认 False）、`readonly` 置灰不可调（默认 False）、`combo` 下拉 |
| **API 速查** | Cube/Sphere/Cone/Box/Section/Loft/Sweep/Combine/Bool 等接口签名 |
| **变换与布置** | translate/rotate/scale 从右到左执行、驱动点、两点/旋转布置 |
| **自定义组件模板** | 椭球体（Loft）、圆形/方形截面圆环（Sweep） |
| **多组件内联装配** | 禁止跨文件导入，内联到同一文件 |
| **输出检查清单** | 11 条规则确保代码规范性 |

---

### 2.2 bimbase-modeling-agent-interaction — BIMBase 建模交互技能

| 项目 | 内容 |
|------|------|
| **类型** | 技能（Skill） |
| **加载方式** | 项目内 markdown 文件自动导入 |
| **文件路径** | `D:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_AIAgent_建模交互技能.md` |
| **适用范围** | AI Agent 与用户交互建模时的行为规范 |

#### 核心内容

| 章节 | 内容说明 |
|------|----------|
| **核心原则** | 不猜测、信息不全必问、一次问清、遵循标准结构 |
| **第一部分：用户信息** | 用户会告诉 Agent 的信息类型（建模顺序、尺寸、参数面板、特征点） |
| **第二部分：交互流程** | 信息提取校验 → 缺失提问 → 知识库检索 → 代码生成 → 自检 → 交付 |
| **参数面板设置表** | `obvious=True` 可见可调、`combo` 下拉、`readonly=True` 置灰不可调、`show` 输出 |
| **代码模板** | 完整可复制的 pyp3d 代码框架 |
| **交互示例** | 信息齐全时 / 信息不全时的对话范例 |
| **执行环境** | Python 3.7.9 内嵌解释器路径、pip 安装方法 |
| **知识库索引** | 所有本地文档和参考示例路径汇总 |

---

## 三、本地知识库文档

除 MCP 和 Skills 外，以下本地 markdown 文档构成额外的知识源：

| 文档 | 路径 | 内容说明 |
|------|------|----------|
| **AI Agent 建模指南** | `D:\BIMbase\PythonScript\BFAComponentLib\BIMBase_AIAgent_建模指南.md` | 项目作用、技术栈、数据流、MCP 工具链、pyp3d 规范、SDK 接口速查、多组件装配、执行环境 |
| **建模方法函数大全** | `D:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_pyp3d_建模方法函数大全.md` | pyp3d 所有函数详细用法：标准结构、Attr、9 种基础几何体、6 种复杂造型、变换、布置、驱动点、颜色、3 种自定义组件、建模决策树、完整示例 |
| **建模交互技能** | `D:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_AIAgent_建模交互技能.md` | 同 Skills 2.2，是 Skill 对应的源文件 |
| **通用建模模板** | `D:\BIMbase\PythonScript\BFAComponentLib\参数化组件样例\自建\通用Python建模模版.py` | 12 个板块的完整 Python 模板，可直接复制修改 |

---

## 四、参考代码示例

以下目录存放已实现的 Python 建模示例，可作为编码参考：

| 目录 | 路径 | 示例内容 |
|------|------|----------|
| **基本体教学** | `D:\BIMbase\PythonScript\BFAComponentLib\参数化组件样例\基本体教学\` | Loft、Sweep、Combine、Section、Cube、Fusion、Intersect、两点布置、旋转平移 |
| **造型构件** | `D:\BIMbase\PythonScript\BFAComponentLib\参数化组件样例\造型构件\` | 弹簧、月饼等复杂造型 |
| **场布内置** | `D:\BIMbase\PythonScript\BFAComponentLib\场布内置\` | 内置场布组件参考 |
| **已有组件参考** | `D:\BIMbase\PythonScript\BFAComponentLib\已有Py组件参考\` | 椭球等已验证组件 |
| **自建组件** | `D:\BIMbase\PythonScript\BFAComponentLib\参数化组件样例\自建\` | 小蛮腰、螺钉、扭面等自建示例 |
| **热水器** | `D:\BIMbase\PythonScript\BFAComponentLib\参数化组件样例\热水器\` | 太阳能集热器、基础热水器等设备模型 |

---

## 配置关系图

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent 建模配置                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ mcp.json 文件配置 ─────────────────────────────────┐    │
│  │                                                      │    │
│  │  BIMBaseAI2PY (MCP Command)                          │    │
│  │  ├─ 运行: Miniconda Python → MCPServer.py            │    │
│  │  ├─ 知识库: BIMBaseMCP/skill/*.md                    │    │
│  │  ├─ 工具: get_summary_document / get_skill_manifest  │    │
│  │  │        get_skill_doc / get_skill_bundle /         │    │
│  │  │        get_related_skills                          │    │
│  │  └─ Prompt: bimbase_modeling_guide()                 │    │
│  │                                                      │    │
│  │  Excel (MCP Command, 辅助)                            │    │
│  │  └─ 7 个 Excel 读写工具                               │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─ Skills (markdown 自动导入) ────────────────────────┐    │
│  │                                                      │    │
│  │  SKILL.md → bimbase-pyp3d-modeling                   │    │
│  │  ├─ pyp3d 建模最高准则与标准结构                      │    │
│  │  ├─ API 速查、变换、布置、驱动点                     │    │
│  │  └─ 自定义组件模板（椭球/圆环）                       │    │
│  │                                                      │    │
│  │  BIMBase_AIAgent_建模交互技能.md                     │    │
│  │   → bimbase-modeling-agent-interaction               │    │
│  │  ├─ 信息收集、提问模板、代码生成规范                  │    │
│  │  └─ 完整交互示例与自检清单                            │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─ 本地知识库文档 ────────────────────────────────────┐    │
│  │                                                      │    │
│  │  BIMBase_AIAgent_建模指南.md                          │    │
│  │  BIMBase_pyp3d_建模方法函数大全.md                    │    │
│  │  通用Python建模模版.py                                │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─ 参考代码示例 ──────────────────────────────────────┐    │
│  │  基本体教学 / 造型构件 / 场布内置 / 已有组件参考      │    │
│  │  自建 / 热水器                                        │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

> **技术备注：**
> - BIMBase 建模脚本运行在 **内嵌 Python 3.7.9** (`D:\BIMbase\PythonScript\python-3.7.9-embed-amd64\python.exe`)
> - MCP 服务器需要 **Python >= 3.10** (`D:\Miniconda\python.exe`)，两者是不同的解释器
> - 本文件由 AI Agent 自动生成，随配置变更应同步更新
