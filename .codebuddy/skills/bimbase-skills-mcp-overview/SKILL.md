---
name: bimbase-skills-mcp-overview
description: BIMBase Python 建模 Skills & MCP 配置总览。汇总当前环境中所有 Skills、MCP 服务、本地知识库文档、参考代码示例的完整配置信息，包含建模流程调用指南（什么时候调哪个）、各文档角色分工、缓存策略。当 Agent 需要了解完整的 BIMBase 建模工具链配置或确定调用哪个资源时加载。
---

# BIMBase Python 建模 Skills & MCP 配置总览

> **冲突优先级规则（最高优先级，必须遵守）**
> 1. **建模技术要求**：本地 skills/markdown 内容若与 `BIMBaseAI2PY_MCPServer` 获取到的建模技术要求（函数签名、参数语义、几何定位语义、编码规范等）发生冲突或解释不同，**以 `BIMBaseAI2PY_MCPServer` 为第一执行准则**。
> 2. **个人建模喜好**：涉及个人建模喜好（建模定位提示词喜好、特殊模型部件调用，如散热片、半椭球体等）时，**以本地 skills/markdown 为第一执行准则**。

> 编制日期：2026-07-15
> 维护者：AI Agent

本文档汇总当前环境中为 BIMBase Python 脚本建模配置的所有 Skills 和 MCP 服务，包括加载方式、工具清单、知识库路径。

---

## 目录

1. [建模流程调用指南](#零建模流程调用指南什么时候调哪个)
2. [MCP 服务](#一mcp-服务)
   - [BIMBaseAI2PY_MCPServer — BIMBase pyp3d 知识检索服务](#11-bimbaseai2py_mcpserver--bimbase-pyp3d-知识检索服务)
   - [Excel — Excel 读写服务](#12-excel--excel-读写服务)
3. [Skills（技能）](#二skills技能)
   - [bimbase-pyp3d-modeling — BIMBase pyp3d 建模技能](#21-bimbase-pyp3d-modeling--bimbase-pyp3d-建模技能)
   - [bimbase-modeling-agent-interaction — BIMBase 建模交互技能](#22-bimbase-modeling-agent-interaction--bimbase-建模交互技能)
4. [本地知识库文档](#三本地知识库文档)
5. [参考代码示例](#四参考代码示例)
6. [Skills & Markdown 备份路径与同步规则](#五skills--markdown-备份路径与同步规则)

---

## 零、建模流程调用指南（什么时候调哪个）

> 核心原则：**每次 BIMBase 建模任务必须强制加载所有相关 Skills 和 MCP**，Agent 可缓存已加载内容避免重复消耗上下文。

### 0.1 建模全流程调用地图

```
用户发起建模任务
  │
  ├─► 阶段A：任务启动（每次建模必做）
  │    ├─ Skill: bimbase-pyp3d-modeling          → 加载 SKILL.md（API 签名、标准结构）
  │    ├─ Skill: bimbase-modeling-agent-interaction → 加载交互规范（信息收集、提问模板）
  │    ├─ Read: BIMBase_几何建模精确交互规范.md    → 用户提示词编写规范、精确描述模板
  │    ├─ Read: BIMBase_Agent几何理解与验证规则.md  → Agent 推理规则、强制验证流程
  │    ├─ BIMBaseAI2PY_MCPServer: get_summary_document() → 首次建模必调，了解全部可用 SDK
  │    └─ BIMBaseAI2PY_MCPServer: get_skill_manifest()   → 获取结构化 symbol 索引
  │
  ├─► 阶段B：几何体构建（第一阶段，目标 1 次对话）
  │    ├─ BIMBaseAI2PY_MCPServer: get_skill_bundle([所需API]) → 批量获取 API 文档（自动带编码规范）
  │    ├─ Read: BIMBase_pyp3d_建模方法函数大全.md   → 函数详细用法与示例
  │    ├─ Read: BIMBase_AIAgent_建模指南.md         → 完整技术参考
  │    ├─ 【输出建模参数确认表】                    → 用户确认后再生成代码
  │    └─ Write: 生成 Python 代码
  │
  ├─► 阶段C：参数化与特征点（第二阶段，目标 1 次对话）
  │    ├─ BIMBaseAI2PY_MCPServer: get_skill_doc("Attr")      → Attr 参数规范
  │    ├─ BIMBaseAI2PY_MCPServer: get_skill_doc("DrivePointInterface") → 驱动点接口
  │    ├─ Read: SKILL.md（Attr 参数规范章节）       → obvious/readonly/combo
  │    └─ Edit: 将硬编码替换为 Attr，添加驱动点
  │
  ├─► 阶段D：精细化微调（第三阶段，目标 1 次对话）
  │    ├─ Read: 相关 py 参考代码                   → 参考已有组件实现
  │    └─ Edit: 调整默认值、新增/删除部件、微调位置
  │
  └─► 触发：主动复盘（≥2 次同类修改时）
       ├─ 暂停修改
       ├─ 复盘列出不确定的坐标/起点/终点
       └─ 以表格向用户确认后再修改
```

### 0.2 按建模任务类型速查

| 任务类型 | 必须调用的 Skill | 必须调用的 MCP | 必须读取的本地文档 |
|---------|-----------------|---------------|------------------|
| **新建模型**（从零开始） | bimbase-pyp3d-modeling + bimbase-modeling-agent-interaction | get_summary_document + get_skill_manifest + get_skill_bundle | 全部 5 份知识库文档 |
| **修改已有模型** | bimbase-pyp3d-modeling | get_skill_bundle（按需） | 几何建模精确交互规范 + Agent几何理解与验证规则 |
| **添加新部件** | bimbase-pyp3d-modeling | get_skill_bundle([新部件所需API]) | BIMBase_pyp3d_建模方法函数大全 |
| **调整参数/特征点** | bimbase-pyp3d-modeling | get_skill_doc("Attr") 或 get_skill_doc("DrivePointInterface") | SKILL.md（Attr 章节） |
| **调试几何位置错误** | 无需额外 Skill | 无需额外 MCP | Agent几何理解与验证规则（主动复盘规则） |
| **参考已有组件** | 无需额外 Skill | 无需额外 MCP | 参考代码示例目录 |

### 0.3 各文档/服务的作用分工

| 资源 | 角色 | 核心解决的问题 |
|------|------|-------------|
| **SKILL.md** (bimbase-pyp3d-modeling) | 建模总纲 | API 签名、标准结构、变换规则、自定义组件模板 |
| **BIMBase_AIAgent_建模交互技能.md** | 交互流程 | 信息收集、提问模板、参数面板设置、代码模板 |
| **BIMBase_几何建模精确交互规范.md** | 用户侧规范 | 提示词怎么写（截面原点、拉伸方向、临时坐标系） |
| **BIMBase_Agent几何理解与验证规则.md** | Agent 侧规则 | 推理规则、建模参数确认表、主动复盘、API 构建规则 |
| **BIMBase_AIAgent_建模指南.md** | 技术大全 | 完整技术参考、SDK 接口速查、多组件装配、执行环境 |
| **BIMBase_pyp3d_建模方法函数大全.md** | 函数手册 | 每个 pyp3d 函数的详细用法、参数说明、代码示例 |
| **BIMBaseAI2PY_MCPServer get_summary_document** | SDK 索引 | 全部可用 SDK 文档的概要 |
| **BIMBaseAI2PY_MCPServer get_skill_manifest** | 结构化索引 | 所有 symbol 的路径、分类、别名、关键词、依赖 |
| **BIMBaseAI2PY_MCPServer get_skill_bundle** | 批量文档 | 按需获取具体 API 文档（自动带编码规范） |
| **BIMBaseAI2PY_MCPServer get_skill_doc** | 单文档 | 获取单个 API 文档 |
| **BIMBaseAI2PY_MCPServer get_related_skills** | 关联查询 | 查配套函数与必载依赖 |

### 0.4 缓存策略

> Agent 在同一次会话中缓存已加载的 Skills/MCP 内容，避免重复消耗上下文。但当用户切换到**新的建模任务**（新文件）时，应重新调用 MCP 确认 API 签名。

---

## 一、MCP 服务

MCP（Model Context Protocol）服务通过工具接口为 AI Agent 提供能力支撑。

### 配置文件

项目 MCP 配置文件：`d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\mcp.json`

```json
{
  "mcpServers": {
    "BIMBaseAI2PY_MCPServer": {
      "url": "https://dev.pkpm.cn/mcp/"
    }
  }
}
```

---

### 1.1 BIMBaseAI2PY_MCPServer — BIMBase pyp3d 知识检索服务

| 项目 | 内容 |
|------|------|
| **类型** | 远程 MCP 服务（HTTP/SSE） |
| **配置方式** | `mcp.json` 文件配置 |
| **服务地址** | `https://dev.pkpm.cn/mcp/` |
| **权威性** | BIMBase 建模 SDK 官方技术文档，**建模技术要求以此为准** |

#### 提供的工具（5 个）

| 工具名 | 参数 | 功能 |
|--------|------|------|
| `get_summary_document` | 无 | 返回知识库概要（全部可用 SDK 文档索引），**首次建模必调** |
| `get_skill_manifest` | `include_reference=False, force_refresh=False, agent_input=""` | 返回结构化 JSON 索引：所有 symbol、路径、分类、别名、关键词、依赖 |
| `get_skill_doc` | `symbol, include_reference=False, agent_input=""` | 按 symbol 获取**单个**文档正文 |
| `get_skill_bundle` | `symbols, include_reference=False, include_dependencies=True, agent_input=""` | **批量**获取多个文档正文，自动附带 `basic_writing_style` 编码规范 |
| `get_related_skills` | `symbol, include_reference=False, agent_input=""` | 返回该 symbol 的配套函数与必载依赖 |

#### 官方 SDK symbol 清单（通过 `get_skill_manifest()` / `get_summary_document()` 查询）

| 分类 | symbol |
|------|--------|
| 几何体 | Cube、Sphere、Cone、Box、Arc、Line、Text、Section、Loft、Sweep、Combine、Bool、Linspace、Extrusion、ExtrusionPlus、RotationalSweep、FilletPipe |
| 曲线/网格 | SplineCurve、ParametricEquation、Polyface |
| 属性/颜色 | Attr、Color |
| 变换/布置 | matrix_interface、PlaceInterface |
| 驱动点 | DrivePointInterface |
| 向量 | GeVec3d |
| 编码规范 | basic_writing_style |
| 专业模式 | assembly_guide |
| 自定义组件 | custom_Ellipsoid、custom_CircularTorus、custom_SquareTorus |

> 完整 symbol 索引以 `BIMBaseAI2PY_MCPServer` 的 `get_skill_manifest()` 返回为准。

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
| **几何建模精确交互规范** | `D:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_几何建模精确交互规范.md` | 用户提示词编写规范：三段式建模流程、精确描述模板（截面原点/拉伸方向/扫掠路径）、常见歧义速查表、建模参数确认表模板 |
| **Agent几何理解与验证规则** | `D:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_Agent几何理解与验证规则.md` | Agent 推理规则：强制 Skills/MCP 加载流程、API 构建规则（Box/Cone/Sweep）、主动复盘规则、方向约定、参数绑定规则 |
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

## 五、Skills & Markdown 完整文件路径清单（更新时必查）

> **当用户要求对"所有相关的 BIMBase 建模的 skills、markdown 进行内容更新"时，Agent 必须按以下编号路径逐一更新对应文件。**

> 完整汇总文件见：`d:\BIMbase\PythonScript\BFAComponentLib\skills+markdown汇总.md`

### 5.1 Skills 技能文件（6 个，.trae/skills/）

| 编号 | 文件路径 |
|------|---------|
| S1 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-pyp3d-modeling\SKILL.md` |
| S2 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-pyp3d-function-reference\SKILL.md` |
| S3 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-agent-geometry-rules\SKILL.md` |
| S4 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-modeling-agent-interaction\SKILL.md` |
| S5 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-precise-modeling-interaction\SKILL.md` |
| S6 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-skills-mcp-overview\SKILL.md` |

### 5.2 MCP 官方 SDK 文档（通过 BIMBaseAI2PY_MCPServer 查询）

不再维护本地 MCP 知识库文件。全部 SDK 文档由 `BIMBaseAI2PY_MCPServer`（远程 `https://dev.pkpm.cn/mcp/`）统一提供，通过 `get_skill_doc` / `get_skill_bundle` 按 symbol 查询。完整 symbol 清单见上文「官方 SDK symbol 清单」。

### 5.3 本地知识库文档（5 个，leder_skills/）

| 编号 | 文件路径 |
|------|---------|
| L1 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_Agent几何理解与验证规则.md` |
| L2 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_AIAgent_建模交互技能.md` |
| L3 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_几何建模精确交互规范.md` |
| L4 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_pyp3d_建模方法函数大全.md` |
| L5 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_Skills_MCP_配置总览.md` |

### 5.4 根目录知识库文档（2 个）

| 编号 | 文件路径 |
|------|---------|
| R1 | `d:\BIMbase\PythonScript\BFAComponentLib\SKILL.md` |
| R2 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBase_AIAgent_建模指南.md` |

### 5.5 备份路径

| 编号 | 路径 | 说明 |
|------|------|------|
| B1 | `E:\个人笔记文件备份\notebook\实习\备份skills+mcp+markdown\skills\` | 备份 Skills 目录 |
| B2 | `E:\个人笔记文件备份\notebook\实习\备份skills+mcp+markdown\markdown\` | 备份 Markdown 目录 |
| B3 | `E:\个人笔记文件备份\notebook\实习\目前skills+mcp+md.md` | 当前 skills/mcp/md 汇总文件 |

### 5.6 同步更新规则（必须遵守）

**当用户要求更新 Skills、Markdown 或 MCP 内容时，Agent 必须按以下顺序同步更新：**

1. 更新 `.trae\skills\` 下的 6 个 Skill 文件（编号 S1-S6）
2. 更新 `leder_skills\` 下的对应文件（编号 L1-L5）
3. 更新根目录 `SKILL.md` 和 `BIMBase_AIAgent_建模指南.md`（编号 R1-R2）
4. 更新备份 `skills\` 和 `markdown\` 目录（编号 B1-B2）
5. 更新 `目前skills+mcp+md.md`（编号 B3）
6. 更新 `skills+markdown汇总.md`（如有路径变更）

### 5.7 备份文件与本地文件的对应关系

| 备份文件 | 本地 Skill 文件 |
|---------|---------------|
| `skills\BIMBase_Agent几何理解与验证规则.md` | `.trae\skills\bimbase-agent-geometry-rules\SKILL.md` (S3) |
| `skills\SKILL.md` | `.trae\skills\bimbase-pyp3d-modeling\SKILL.md` (S1) |
| `skills\BIMBase_AIAgent_建模交互技能.md` | `.trae\skills\bimbase-modeling-agent-interaction\SKILL.md` (S4) |
| `skills\BIMBase_几何建模精确交互规范.md` | `.trae\skills\bimbase-precise-modeling-interaction\SKILL.md` (S5) |
| `skills\BIMBase_pyp3d_建模方法函数大全.md` | `.trae\skills\bimbase-pyp3d-function-reference\SKILL.md` (S2) |
| `skills\BIMBase_Skills_MCP_配置总览.md` | `.trae\skills\bimbase-skills-mcp-overview\SKILL.md` (S6) |
| `markdown\BIMBase_Agent几何理解与验证规则.md` | 同上 |
| `markdown\BIMBase_几何建模精确交互规范.md` | 同上 |
| `markdown\BIMBase_Skills_MCP_配置总览.md` | 同上 |
| `markdown\BIMBase_pyp3d_建模方法函数大全.md` | 同上 |
| `markdown\BIMBase_AIAgent_建模指南.md` | 无对应 Skill（纯本地文档 R2） |

---

## 配置关系图

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent 建模配置                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ mcp.json 文件配置 ─────────────────────────────────┐    │
│  │                                                      │    │
│  │  BIMBaseAI2PY_MCPServer (远程 HTTP/SSE)              │    │
│  │  ├─ 地址: https://dev.pkpm.cn/mcp/                   │    │
│  │  ├─ 知识库: 官方 SDK 文档（按 symbol 查询）           │    │
│  │  ├─ 工具: get_summary_document / get_skill_manifest  │    │
│  │  │        get_skill_doc / get_skill_bundle /         │    │
│  │  │        get_related_skills                          │    │
│  │  └─ 权威性: 建模技术要求以此为准                      │    │
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
│  │  BIMBase_几何建模精确交互规范.md                      │    │
│  │  BIMBase_Agent几何理解与验证规则.md                   │    │
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
> - BIMBase 建模脚本运行在 **内嵌 Python 3.7.9** (`D:\BIMBase KIT official 2026 R1.0\BIMBase KIT 2026\PythonScript\python-3.7.9-embed-amd64\python.exe`)
> - MCP 服务 `BIMBaseAI2PY_MCPServer` 为远程服务（`https://dev.pkpm.cn/mcp/`），无需本地 Python 环境
> - 本文件由 AI Agent 自动生成，随配置变更应同步更新