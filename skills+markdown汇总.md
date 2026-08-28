# BIMBase Python 建模 Skills & Markdown 文件汇总

> 编制日期：2026-08-20
> 更新日期：2026-08-28
> 维护者：AI Agent
> 用途：当用户要求更新所有相关的 BIMBase 建模 skills、markdown 时，Agent 根据本文件中的路径清单进行对应文件的更新迭代修改。
>
> **本次更新（2026-08-28）**：在所有交互类 skills/markdown 中新增「建模前需求对齐与复杂度确认」环节——① 部件理解对齐（图片解析/提示词拆解，识别不清处盘问确认，参考 grill-me 逻辑）；② 建模精细/复杂程度确认（是否简化，给出简化方案供选；用户明确要求"复刻/按图片尺寸/按建模提示词"时跳过）。同步更新核心工作流为：输入(图片/文字) → 部件理解 → 盘问对齐 → 复杂度确认 → 建模参数确认表 → 编码。
>
> **二次更新（2026-08-28）**：细化落地，新增三套模板——① 图片识别结果汇报模板（6 段：总体信息/尺寸表格/建模部件清单/尺寸信息/属性业务信息/疑惑点）；② 复杂度确认话术（建模范围多选+各部件精细度 2~4 档+缺失尺寸可调默认值）；③ 结构化提问话术（header + options(label+description) + multiSelect，一次问清）。

> **冲突优先级规则（最高优先级，必须遵守）**
> 1. **建模技术要求**：本地 skills/markdown 内容若与 `BIMBaseAI2PY_MCPServer` 获取到的建模技术要求（函数签名、参数语义、几何定位语义、编码规范等）发生冲突或解释不同，**以 `BIMBaseAI2PY_MCPServer` 为第一执行准则**。
> 2. **个人建模喜好**：涉及个人建模喜好（建模定位提示词喜好、特殊模型部件调用，如散热片、半椭球体等）时，**以本地 skills/markdown 为第一执行准则**。

---

## 目录

1. [一、Skills 技能文件](#一skills-技能文件)
2. [二、MCP 官方 SDK 文档（BIMBaseAI2PY_MCPServer）](#二mcp-官方-sdk-文档bimbaseai2py_mcpserver)
3. [三、本地知识库文档（leder_skills/）](#三本地知识库文档leder_skills)
4. [四、根目录知识库文档](#四根目录知识库文档)
5. [五、Skills & Markdown 完整路径清单（更新时必查）](#五skills--markdown-完整路径清单更新时必查)
6. [六、备份路径与同步规则](#六备份路径与同步规则)

---

## 一、Skills 技能文件

每个技能是一个子文件夹，内含 `SKILL.md` 作为技能定义文件。当 Agent 调用 `Skill` 工具时加载对应的 SKILL.md。

**技能存在两处同源副本**：
- `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\skills\`
- `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\`

另在 `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\rules\` 下有同名规则的 `.md` 精要副本（6 个）。

### 1.1 bimbase-pyp3d-modeling — pyp3d 建模核心技能

| 项目 | 内容 |
|------|------|
| **路径** | `.codebuddy\skills\bimbase-pyp3d-modeling\SKILL.md` / `.trae\skills\bimbase-pyp3d-modeling\SKILL.md` |
| **功能** | BIMBase pyp3d 参数化建模的总纲级技能，定义建模全流程 |
| **触发条件** | 用户要求创建/编辑/组装 BIMBase 模型时务必加载 |
| **核心内容** | 三级解惑协议、标准结构（Component+Attr+@export+place）、API 速查、变换与布置、自定义组件模板（椭球体/半椭球体/圆形截面圆环/方形截面圆环）、多组件内联装配、输出检查清单 |

### 1.2 bimbase-pyp3d-function-reference — pyp3d 函数参考大全

| 项目 | 内容 |
|------|------|
| **路径** | `.codebuddy\skills\bimbase-pyp3d-function-reference\SKILL.md` / `.trae\skills\bimbase-pyp3d-function-reference\SKILL.md` |
| **功能** | 所有 pyp3d 函数的详细用法手册 |
| **触发条件** | Agent 需要查阅具体 pyp3d 函数用法时加载 |
| **核心内容** | 标准结构、Attr 参数规范、基础几何体（Cube/Sphere/Cone/Box/Arc/Line/Text）、复杂造型（Section/Loft/Sweep/Combine/Bool/Linspace）、变换操作、布置接口、驱动点、颜色、自定义组件模板、建模决策树、完整示例 |

### 1.3 bimbase-agent-geometry-rules — Agent 几何理解与验证规则

| 项目 | 内容 |
|------|------|
| **路径** | `.codebuddy\skills\bimbase-agent-geometry-rules\SKILL.md` / `.trae\skills\bimbase-agent-geometry-rules\SKILL.md` |
| **功能** | Agent 建模时的推理规则与强制验证流程 |
| **触发条件** | Agent 需要理解用户建模需求、验证几何坐标、或遇到 ≥2 次同类修改时触发复盘流程时加载 |
| **核心内容** | 强制 Skills/MCP 加载流程、建模参数确认表生成规范、API 构建规则（Box/Cone/Sweep 防错）、临时坐标系处理规则、主动复盘规则、方向约定、特征点规则、驱动点表达式规则、参数绑定规则 |

### 1.4 bimbase-modeling-agent-interaction — Agent 建模交互规范

| 项目 | 内容 |
|------|------|
| **路径** | `.codebuddy\skills\bimbase-modeling-agent-interaction\SKILL.md` / `.trae\skills\bimbase-modeling-agent-interaction\SKILL.md` |
| **功能** | AI Agent 与用户进行 BIMBase pyp3d 建模交互时的行为规范 |
| **触发条件** | 需要与用户进行建模交互时加载 |
| **核心内容** | 不猜测/信息不全必问/一次问清原则、用户信息类型、交互流程、参数面板设置表、代码模板、交互示例、执行环境说明、知识库索引 |

### 1.5 bimbase-precise-modeling-interaction — 用户精确建模交互规范

| 项目 | 内容 |
|------|------|
| **路径** | `.codebuddy\skills\bimbase-precise-modeling-interaction\SKILL.md` / `.trae\skills\bimbase-precise-modeling-interaction\SKILL.md` |
| **功能** | 面向用户的 BIMBase pyp3d 建模精确交互规范 |
| **触发条件** | 用户需要编写 BIMBase 建模提示词或 Agent 需要理解用户建模意图时加载 |
| **核心内容** | 三段式建模流程、精确描述模板、常见歧义速查表、建模参数确认表模板 |

### 1.6 bimbase-skills-mcp-overview — Skills & MCP 配置总览

| 项目 | 内容 |
|------|------|
| **路径** | `.codebuddy\skills\bimbase-skills-mcp-overview\SKILL.md` / `.trae\skills\bimbase-skills-mcp-overview\SKILL.md` |
| **功能** | 汇总当前环境中所有 Skills、MCP 服务、本地知识库文档、参考代码示例的完整配置信息 |
| **触发条件** | Agent 需要了解完整的 BIMBase 建模工具链配置或确定调用哪个资源时加载 |
| **核心内容** | 建模流程调用指南、MCP 服务详情、Skills 技能详情、本地知识库文档索引、参考代码示例、备份路径与同步规则 |

---

## 二、MCP 官方 SDK 文档（BIMBaseAI2PY_MCPServer）

**服务地址**：`https://dev.pkpm.cn/mcp/`（远程 HTTP/SSE，无需本地 Python 环境）。

基础命令（立方体/圆柱/球/圆锥/圆环/椭球/放样/扫掠/布尔运算等）的准确用法，统一通过 `BIMBaseAI2PY_MCPServer` 查询官方 SDK 技术文档获得。**仅「有本地 `.py` 教学文件」的命令保留本地描述**；无本地 `.py` 的命令（如 Box）必须改查 MCP。

### 2.1 MCP 工具（Tools）

| 工具 | 作用 |
|------|------|
| `get_summary_document()` | 首次建模必调，返回知识库全局概要 |
| `get_skill_manifest()` | 返回结构化 symbol 索引（路径/别名/关键词/依赖） |
| `get_skill_doc(symbol)` | 获取单个 symbol 的文档正文 |
| `get_skill_bundle(symbols)` | 批量获取多个文档正文 |
| `get_related_skills(symbol)` | 获取配套函数与必载依赖 |

### 2.2 官方 symbol 清单（共 31 个）

#### 基础几何体

| symbol | 说明 |
|--------|------|
| `Cube` | 单位立方体/指定尺寸立方体（角点在原点，非中心定位） |
| `Sphere` | 单位球体/指定半径球体 |
| `Cone` | 圆锥/圆台/圆柱（两端半径相等时） |
| `Box` | 任意朝向四棱台（含长方体、棱柱）；origin 是底/顶面角点而非中心 |
| `Arc` | 单位圆弧或三点圆弧 |
| `Line` | 二维/三维线段 |
| `Text` | 二维/三维文字几何体 |

#### 复杂造型

| symbol | 说明 |
|--------|------|
| `Section` | 装填二维几何体作为放样截面 |
| `Loft` | 多截面放样 |
| `Sweep` | 截面沿轨迹扫掠 |
| `Extrusion` | 拉伸体（直线放样） |
| `ExtrusionPlus` | 复杂拉伸体（外轮廓含圆弧/椭圆 + 内孔） |
| `RotationalSweep` | 旋转扫描（回转体/revolve） |
| `FilletPipe` | 圆角弯管 |
| `Bool` | 布尔减（差集）、交（交集）；并集/合并改用 Combine |
| `Combine` | 组合成组 |
| `Linspace` | 等分点序列 |
| `SplineCurve` | 准均匀 B 样条曲线（扫掠/放样光滑路径） |
| `ParametricEquation` | 参数方程曲线 |
| `Polyface` | 三角面片网格原语 |

#### 属性 / 变换 / 布置 / 驱动

| symbol | 说明 |
|--------|------|
| `Attr` | 组件属性、分组及下拉框选项 |
| `Color` | 颜色与透明度（RGBA） |
| `matrix_interface` | 几何体变换（平移/旋转/缩放） |
| `PlaceInterface` | 布置接口（旋转、两点线性） |
| `DrivePointInterface` | 驱动点（特征点）设置与联动 |
| `GeVec3d` | 三维向量/点类型（Vec3 同义别名） |

#### 编码规范 / 专业模式 / 自定义组件

| symbol | 说明 |
|--------|------|
| `basic_writing_style` | 参数化组件开发指导（编码规范） |
| `assembly_guide` | 多组件内联装配指南 |
| `custom_Ellipsoid` | 椭球体 + 半椭球体（Loft+Section 组合） |
| `custom_CircularTorus` | 圆形截面圆环（Sweep 实现） |
| `custom_SquareTorus` | 方形截面圆环（Sweep 实现） |

---

## 三、本地知识库文档（leder_skills/）

**根目录**：`d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\`

| 文件 | 对应 Skill | 功能 |
|------|-----------|------|
| BIMBase_Agent几何理解与验证规则.md | bimbase-agent-geometry-rules | Agent 几何推理规则、强制验证流程、API 构建规则、主动复盘 |
| BIMBase_AIAgent_建模交互技能.md | bimbase-modeling-agent-interaction | Agent 与用户交互规范、信息收集、提问模板、代码模板 |
| BIMBase_几何建模精确交互规范.md | bimbase-precise-modeling-interaction | 用户提示词编写规范、精确描述模板、歧义速查表 |
| BIMBase_pyp3d_建模方法函数大全.md | bimbase-pyp3d-function-reference | 所有 pyp3d 函数详细用法、建模决策树、完整示例 |
| BIMBase_Skills_MCP_配置总览.md | bimbase-skills-mcp-overview | Skills & MCP 配置总览 |

---

## 四、根目录知识库文档

**根目录**：`d:\BIMbase\PythonScript\BFAComponentLib\`

| 文件 | 功能 |
|------|------|
| SKILL.md | pyp3d 建模核心技能文件（与 bimbase-pyp3d-modeling 同源） |
| BIMBase_AIAgent_建模指南.md | 项目作用、技术栈、数据流、MCP 工具链、pyp3d 规范、SDK 接口速查、多组件装配、执行环境 |
| skills+markdown汇总.md | **本文件**：Skills & Markdown 文件路径与功能汇总 |

---

## 五、Skills & Markdown 完整路径清单（更新时必查）

**当用户要求对"所有相关的 BIMBase 建模的 skills、markdown 进行内容更新"时，Agent 必须按以下路径清单逐一更新：**

### 5.1 Skills 技能文件（.codebuddy/skills/，6 个）

| 序号 | 文件路径 |
|------|---------|
| 1 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\skills\bimbase-pyp3d-modeling\SKILL.md` |
| 2 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\skills\bimbase-pyp3d-function-reference\SKILL.md` |
| 3 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\skills\bimbase-agent-geometry-rules\SKILL.md` |
| 4 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\skills\bimbase-modeling-agent-interaction\SKILL.md` |
| 5 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\skills\bimbase-precise-modeling-interaction\SKILL.md` |
| 6 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\skills\bimbase-skills-mcp-overview\SKILL.md` |

### 5.2 Skills 技能文件（.trae/skills/，6 个，与 5.1 同源）

| 序号 | 文件路径 |
|------|---------|
| 7 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-pyp3d-modeling\SKILL.md` |
| 8 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-pyp3d-function-reference\SKILL.md` |
| 9 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-agent-geometry-rules\SKILL.md` |
| 10 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-modeling-agent-interaction\SKILL.md` |
| 11 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-precise-modeling-interaction\SKILL.md` |
| 12 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-skills-mcp-overview\SKILL.md` |

### 5.3 Rules 规则文件（.codebuddy/rules/，6 个）

| 序号 | 文件路径 |
|------|---------|
| 13 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\rules\bimbase-pyp3d-modeling.md` |
| 14 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\rules\bimbase-pyp3d-function-reference.md` |
| 15 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\rules\bimbase-agent-geometry-rules.md` |
| 16 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\rules\bimbase-modeling-agent-interaction.md` |
| 17 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\rules\bimbase-precise-modeling-interaction.md` |
| 18 | `d:\BIMbase\PythonScript\BFAComponentLib\.codebuddy\rules\bimbase-skills-mcp-overview.md` |

### 5.4 本地知识库文档（leder_skills/，5 个）

| 序号 | 文件路径 |
|------|---------|
| 19 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_Agent几何理解与验证规则.md` |
| 20 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_AIAgent_建模交互技能.md` |
| 21 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_几何建模精确交互规范.md` |
| 22 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_pyp3d_建模方法函数大全.md` |
| 23 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_Skills_MCP_配置总览.md` |

### 5.5 根目录知识库文档（3 个）

| 序号 | 文件路径 |
|------|---------|
| 24 | `d:\BIMbase\PythonScript\BFAComponentLib\SKILL.md` |
| 25 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBase_AIAgent_建模指南.md` |
| 26 | `d:\BIMbase\PythonScript\BFAComponentLib\skills+markdown汇总.md` |

---

## 六、备份路径与同步规则

### 6.1 备份路径

| 序号 | 目录 | 说明 |
|------|------|------|
| 27 | `E:\个人笔记文件备份\notebook\实习\备份skills+mcp+markdown\skills\` | 备份 Skills 目录 |
| 28 | `E:\个人笔记文件备份\notebook\实习\备份skills+mcp+markdown\markdown\` | 备份 Markdown 目录 |
| 29 | `E:\个人笔记文件备份\notebook\实习\目前skills+mcp+md.md` | 当前 skills/mcp/md 汇总文件 |

### 6.2 同步更新规则

**当用户要求更新 Skills、Markdown 内容时，Agent 必须按以下顺序同步更新：**

1. 更新 `.codebuddy\skills\` 下的 6 个 Skill 文件（序号 1-6）
2. 更新 `.trae\skills\` 下的 6 个 Skill 文件（序号 7-12，与上一步同源）
3. 更新 `.codebuddy\rules\` 下的 6 个规则文件（序号 13-18）
4. 更新 `leder_skills\` 下的对应文件（序号 19-23）
5. 更新根目录 `SKILL.md`、`BIMBase_AIAgent_建模指南.md`（序号 24-25）
6. 更新备份 `skills\` 和 `markdown\` 目录（序号 27-28）
7. 更新 `目前skills+mcp+md.md`（序号 29）
8. 更新本汇总文件 `skills+markdown汇总.md`（如有路径变更）

> 基础命令的准确用法统一通过 `BIMBaseAI2PY_MCPServer` 查询官方 SDK 文档，无需在本项目内维护本地 MCP 知识库文件。

### 6.3 备份与本地文件的对应关系

| 备份文件 | 本地 Skill 文件 |
|---------|---------------|
| `skills\BIMBase_Agent几何理解与验证规则.md` | `.codebuddy\skills\bimbase-agent-geometry-rules\SKILL.md` |
| `skills\SKILL.md` | `.codebuddy\skills\bimbase-pyp3d-modeling\SKILL.md` |
| `skills\BIMBase_AIAgent_建模交互技能.md` | `.codebuddy\skills\bimbase-modeling-agent-interaction\SKILL.md` |
| `skills\BIMBase_几何建模精确交互规范.md` | `.codebuddy\skills\bimbase-precise-modeling-interaction\SKILL.md` |
| `skills\BIMBase_pyp3d_建模方法函数大全.md` | `.codebuddy\skills\bimbase-pyp3d-function-reference\SKILL.md` |
| `skills\BIMBase_Skills_MCP_配置总览.md` | `.codebuddy\skills\bimbase-skills-mcp-overview\SKILL.md` |
| `markdown\BIMBase_Agent几何理解与验证规则.md` | 同上 |
| `markdown\BIMBase_几何建模精确交互规范.md` | 同上 |
| `markdown\BIMBase_Skills_MCP_配置总览.md` | 同上 |
| `markdown\BIMBase_pyp3d_建模方法函数大全.md` | 同上 |
| `markdown\BIMBase_AIAgent_建模指南.md` | 无对应 Skill（纯本地文档） |

---

> **维护说明**：当新增或删除 Skills、MCP 文件、知识库文档时，请同步更新本汇总文件中的路径清单，确保 Agent 始终拥有完整的最新路径信息。
