# BIMBase Python 建模 Skills & Markdown 文件汇总

> 编制日期：2026-08-20
> 维护者：AI Agent
> 用途：当用户要求更新所有相关的 BIMBase 建模 skills、markdown 时，Agent 根据本文件中的路径清单进行对应文件的更新迭代修改。

---

## 目录

1. [一、Skills 技能文件（.trae/skills/）](#一skills-技能文件traeskills)
2. [二、MCP 知识库文件（BIMBaseMCP/skill/）](#二mcp-知识库文件bimbasemcpskill)
3. [三、本地副本 MCP 文件（BIMBaseAPImcp/skill/）](#三本地副本-mcp-文件bimbaseapimcpskill)
4. [四、本地知识库文档（leder_skills/）](#四本地知识库文档leder_skills)
5. [五、根目录知识库文档](#五根目录知识库文档)
6. [六、Skills & Markdown 完整路径清单（更新时必查）](#六skills--markdown-完整路径清单更新时必查)
7. [七、备份路径与同步规则](#七备份路径与同步规则)

---

## 一、Skills 技能文件（.trae/skills/）

**根目录**：`d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\`

每个技能是一个子文件夹，内含 `SKILL.md` 作为技能定义文件。当 Agent 调用 `Skill` 工具时加载对应的 SKILL.md。

### 1.1 bimbase-pyp3d-modeling — pyp3d 建模核心技能

| 项目 | 内容 |
|------|------|
| **路径** | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-pyp3d-modeling\SKILL.md` |
| **功能** | BIMBase pyp3d 参数化建模的总纲级技能，定义建模全流程 |
| **触发条件** | 用户要求创建/编辑/组装 BIMBase 模型时务必加载 |
| **核心内容** | 三级解惑协议、标准结构（Component+Attr+@export+place）、API 速查、变换与布置、自定义组件模板（椭球体/半椭球体/圆形截面圆环/方形截面圆环）、多组件内联装配、输出检查清单 |

### 1.2 bimbase-pyp3d-function-reference — pyp3d 函数参考大全

| 项目 | 内容 |
|------|------|
| **路径** | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-pyp3d-function-reference\SKILL.md` |
| **功能** | 所有 pyp3d 函数的详细用法手册 |
| **触发条件** | Agent 需要查阅具体 pyp3d 函数用法时加载 |
| **核心内容** | 标准结构、Attr 参数规范、9 种基础几何体（Cube/Sphere/Cone/Box/Arc/Line/Text）、6 种复杂造型（Section/Loft/Sweep/Combine/Bool/Linspace）、变换操作、布置接口、驱动点、颜色、自定义组件模板（椭球体/半椭球体/圆形截面圆环/方形截面圆环）、建模决策树、完整示例 |

### 1.3 bimbase-agent-geometry-rules — Agent 几何理解与验证规则

| 项目 | 内容 |
|------|------|
| **路径** | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-agent-geometry-rules\SKILL.md` |
| **功能** | Agent 建模时的推理规则与强制验证流程 |
| **触发条件** | Agent 需要理解用户建模需求、验证几何坐标、或遇到 ≥2 次同类修改时触发复盘流程时加载 |
| **核心内容** | 强制 Skills/MCP 加载流程、建模参数确认表生成规范、API 构建规则（Box/Cone/Sweep 防错）、临时坐标系处理规则、主动复盘规则、方向约定、特征点规则（SnapMode 枚举与选择）、驱动点表达式规则、参数绑定规则 |

### 1.4 bimbase-modeling-agent-interaction — Agent 建模交互规范

| 项目 | 内容 |
|------|------|
| **路径** | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-modeling-agent-interaction\SKILL.md` |
| **功能** | AI Agent 与用户进行 BIMBase pyp3d 建模交互时的行为规范 |
| **触发条件** | 需要与用户进行建模交互时加载 |
| **核心内容** | 不猜测/信息不全必问/一次问清原则、用户信息类型、交互流程（信息提取→缺失提问→检索→代码生成→自检→交付）、参数面板设置表、代码模板、交互示例、执行环境说明、知识库索引 |

### 1.5 bimbase-precise-modeling-interaction — 用户精确建模交互规范

| 项目 | 内容 |
|------|------|
| **路径** | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-precise-modeling-interaction\SKILL.md` |
| **功能** | 面向用户的 BIMBase pyp3d 建模精确交互规范 |
| **触发条件** | 用户需要编写 BIMBase 建模提示词或 Agent 需要理解用户建模意图时加载 |
| **核心内容** | 三段式建模流程（几何体构建→参数化→微调）、精确描述模板（截面原点/拉伸方向/扫掠路径/临时坐标系）、常见歧义速查表、建模参数确认表模板 |

### 1.6 bimbase-skills-mcp-overview — Skills & MCP 配置总览

| 项目 | 内容 |
|------|------|
| **路径** | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-skills-mcp-overview\SKILL.md` |
| **功能** | 汇总当前环境中所有 Skills、MCP 服务、本地知识库文档、参考代码示例的完整配置信息 |
| **触发条件** | Agent 需要了解完整的 BIMBase 建模工具链配置或确定调用哪个资源时加载 |
| **核心内容** | 建模流程调用指南（什么时候调哪个）、MCP 服务详情、Skills 技能详情、本地知识库文档索引、参考代码示例、备份路径与同步规则 |

---

## 二、MCP 知识库文件（BIMBaseMCP/skill/）

**根目录**：`D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\`

通过 MCP 工具 `get_skill_doc` / `get_skill_bundle` 按需检索。该目录下的 `custom_Ellipsoid.md` 等自定义组件文件在更新时需同步修改。

### 2.1 概要

| 文件 | 路径 | 功能 |
|------|------|------|
| summary_skill.md | `.../BIMBaseMCP/skill/summary_skill.md` | 全局概要，列出全部可用 SDK 文档索引 |

### 2.2 SDK 接口指南（01_sdk_interface_guide/）

#### 几何接口（geometric_interface/）

| 文件 | 路径 | 功能 |
|------|------|------|
| property_Attr.md | `.../geometric_interface/property_Attr.md` | 参数定义 Attr（obvious/readonly/combo/show） |
| geometry_Cube.md | `.../geometric_interface/geometry_Cube.md` | 立方体 Cube |
| geometry_Sphere.md | `.../geometric_interface/geometry_Sphere.md` | 球体 Sphere（仅等比缩放） |
| geometry_Cone.md | `.../geometric_interface/geometry_Cone.md` | 圆锥/圆台/圆柱 Cone |
| geometry_Box.md | `.../geometric_interface/geometry_Box.md` | 四棱台/长方体 Box |
| geometry_Arc.md | `.../geometric_interface/geometry_Arc.md` | 圆弧 Arc |
| geometry_Line.md | `.../geometric_interface/geometry_Line.md` | 线段 Line |
| geometry_Text.md | `.../geometric_interface/geometry_Text.md` | 文字 Text |
| geometry_Section.md | `.../geometric_interface/geometry_Section.md` | 截面 Section |
| geometry_Loft.md | `.../geometric_interface/geometry_Loft.md` | 放样 Loft |
| geometry_Sweep.md | `.../geometric_interface/geometry_Sweep.md` | 扫掠 Sweep |
| geometry_Combine.md | `.../geometric_interface/geometry_Combine.md` | 组合 Combine |
| geometry_Bool.md | `.../geometric_interface/geometry_Bool.md` | 布尔运算 Bool |
| geometry_Linspace.md | `.../geometric_interface/geometry_Linspace.md` | 等分点序列 Linspace |
| geometry_Color.md | `.../geometric_interface/geometry_Color.md` | 颜色 Color |

#### 其他接口

| 文件 | 路径 | 功能 |
|------|------|------|
| matrix_interface.md | `.../01_sdk_interface_guide/matrix_interface.md` | 变换接口（translate/rotate/scale） |
| place_interface.md | `.../01_sdk_interface_guide/place_interface.md` | 布置接口（旋转布置、两点线性布置） |
| drive_point_interface.md | `.../01_sdk_interface_guide/drive_point_interface.md` | 驱动点/特征点接口 |

### 2.3 编码规范（02_coding_standards_safety/）

| 文件 | 路径 | 功能 |
|------|------|------|
| basic_writing_style.md | `.../02_coding_standards_safety/basic_writing_style.md` | 基础编写规范（自动附带于 get_skill_bundle） |

### 2.4 专业模式（03_professional_patterns/）

| 文件 | 路径 | 功能 |
|------|------|------|
| assembly_guide.md | `.../03_professional_patterns/assembly_guide.md` | 多组件内联装配指南 |

### 2.5 自定义组件（04_custom_components/）

| 文件 | 路径 | 功能 |
|------|------|------|
| custom_Ellipsoid.md | `.../04_custom_components/custom_Ellipsoid.md` | 椭球体 + 半椭球体（Loft 实现） |
| custom_CircularTorus.md | `.../04_custom_components/custom_CircularTorus.md` | 圆形截面圆环（Sweep 实现） |
| custom_SquareTorus.md | `.../04_custom_components/custom_SquareTorus.md` | 方形截面圆环（Sweep 实现） |

---

## 三、本地副本 MCP 文件（BIMBaseAPImcp/skill/）

**根目录**：`d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\`

与 BIMBaseMCP/skill/ 结构完全一致，为本地副本。更新 MCP 文件时需同时更新此目录下的对应文件。

| 文件 | 路径 | 功能 |
|------|------|------|
| summary_skill.md | `.../BIMBaseAPImcp/skill/summary_skill.md` | 全局概要 |
| property_Attr.md | `.../geometric_interface/property_Attr.md` | 参数定义 Attr |
| geometry_Cube.md | `.../geometric_interface/geometry_Cube.md` | 立方体 |
| geometry_Sphere.md | `.../geometric_interface/geometry_Sphere.md` | 球体 |
| geometry_Cone.md | `.../geometric_interface/geometry_Cone.md` | 圆锥/圆台/圆柱 |
| geometry_Box.md | `.../geometric_interface/geometry_Box.md` | 四棱台/长方体 |
| geometry_Arc.md | `.../geometric_interface/geometry_Arc.md` | 圆弧 |
| geometry_Line.md | `.../geometric_interface/geometry_Line.md` | 线段 |
| geometry_Text.md | `.../geometric_interface/geometry_Text.md` | 文字 |
| geometry_Section.md | `.../geometric_interface/geometry_Section.md` | 截面 |
| geometry_Loft.md | `.../geometric_interface/geometry_Loft.md` | 放样 |
| geometry_Sweep.md | `.../geometric_interface/geometry_Sweep.md` | 扫掠 |
| geometry_Combine.md | `.../geometric_interface/geometry_Combine.md` | 组合 |
| geometry_Bool.md | `.../geometric_interface/geometry_Bool.md` | 布尔运算 |
| geometry_Linspace.md | `.../geometric_interface/geometry_Linspace.md` | 等分点序列 |
| geometry_Color.md | `.../geometric_interface/geometry_Color.md` | 颜色 |
| matrix_interface.md | `.../01_sdk_interface_guide/matrix_interface.md` | 变换接口 |
| place_interface.md | `.../01_sdk_interface_guide/place_interface.md` | 布置接口 |
| drive_point_interface.md | `.../01_sdk_interface_guide/drive_point_interface.md` | 驱动点接口 |
| basic_writing_style.md | `.../02_coding_standards_safety/basic_writing_style.md` | 基础编写规范 |
| assembly_guide.md | `.../03_professional_patterns/assembly_guide.md` | 多组件内联装配指南 |
| custom_Ellipsoid.md | `.../04_custom_components/custom_Ellipsoid.md` | 椭球体 + 半椭球体 |
| custom_CircularTorus.md | `.../04_custom_components/custom_CircularTorus.md` | 圆形截面圆环 |
| custom_SquareTorus.md | `.../04_custom_components/custom_SquareTorus.md` | 方形截面圆环 |

---

## 四、本地知识库文档（leder_skills/）

**根目录**：`d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\`

| 文件 | 路径 | 对应 Skill | 功能 |
|------|------|-----------|------|
| BIMBase_Agent几何理解与验证规则.md | `.../leder_skills/BIMBase_Agent几何理解与验证规则.md` | bimbase-agent-geometry-rules | Agent 几何推理规则、强制验证流程、API 构建规则、主动复盘 |
| BIMBase_AIAgent_建模交互技能.md | `.../leder_skills/BIMBase_AIAgent_建模交互技能.md` | bimbase-modeling-agent-interaction | Agent 与用户交互规范、信息收集、提问模板、代码模板 |
| BIMBase_几何建模精确交互规范.md | `.../leder_skills/BIMBase_几何建模精确交互规范.md` | bimbase-precise-modeling-interaction | 用户提示词编写规范、精确描述模板、歧义速查表 |
| BIMBase_pyp3d_建模方法函数大全.md | `.../leder_skills/BIMBase_pyp3d_建模方法函数大全.md` | bimbase-pyp3d-function-reference | 所有 pyp3d 函数详细用法、建模决策树、完整示例 |
| BIMBase_Skills_MCP_配置总览.md | `.../leder_skills/BIMBase_Skills_MCP_配置总览.md` | bimbase-skills-mcp-overview | Skills & MCP 配置总览（本文件的旧版副本） |

---

## 五、根目录知识库文档

**根目录**：`d:\BIMbase\PythonScript\BFAComponentLib\`

| 文件 | 路径 | 功能 |
|------|------|------|
| SKILL.md | `d:\BIMbase\PythonScript\BFAComponentLib\SKILL.md` | pyp3d 建模核心技能文件（与 bimbase-pyp3d-modeling 同源） |
| BIMBase_AIAgent_建模指南.md | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBase_AIAgent_建模指南.md` | 项目作用、技术栈、数据流、MCP 工具链、pyp3d 规范、SDK 接口速查、多组件装配、执行环境 |
| skills+markdown汇总.md | `d:\BIMbase\PythonScript\BFAComponentLib\skills+markdown汇总.md` | **本文件**：Skills & Markdown 文件路径与功能汇总 |

---

## 六、Skills & Markdown 完整路径清单（更新时必查）

**当用户要求对"所有相关的 BIMBase 建模的 skills、markdown 进行内容更新"时，Agent 必须按以下路径清单逐一更新：**

### 6.1 Skills 技能文件（6 个）

| 序号 | 文件路径 |
|------|---------|
| 1 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-pyp3d-modeling\SKILL.md` |
| 2 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-pyp3d-function-reference\SKILL.md` |
| 3 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-agent-geometry-rules\SKILL.md` |
| 4 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-modeling-agent-interaction\SKILL.md` |
| 5 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-precise-modeling-interaction\SKILL.md` |
| 6 | `d:\BIMbase\PythonScript\BFAComponentLib\.trae\skills\bimbase-skills-mcp-overview\SKILL.md` |

### 6.2 MCP 知识库文件（BIMBaseMCP，24 个）

| 序号 | 文件路径 |
|------|---------|
| 7 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\summary_skill.md` |
| 8 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\property_Attr.md` |
| 9 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Cube.md` |
| 10 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Sphere.md` |
| 11 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Cone.md` |
| 12 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Box.md` |
| 13 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Arc.md` |
| 14 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Line.md` |
| 15 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Text.md` |
| 16 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Section.md` |
| 17 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Loft.md` |
| 18 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Sweep.md` |
| 19 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Combine.md` |
| 20 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Bool.md` |
| 21 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Linspace.md` |
| 22 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\geometric_interface\geometry_Color.md` |
| 23 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\matrix_interface.md` |
| 24 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\place_interface.md` |
| 25 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\01_sdk_interface_guide\drive_point_interface.md` |
| 26 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\02_coding_standards_safety\basic_writing_style.md` |
| 27 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\03_professional_patterns\assembly_guide.md` |
| 28 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\04_custom_components\custom_Ellipsoid.md` |
| 29 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\04_custom_components\custom_CircularTorus.md` |
| 30 | `D:\01\tyafc-master\tyafc-master\BIMBaseMCP\skill\04_custom_components\custom_SquareTorus.md` |

### 6.3 本地副本 MCP 文件（BIMBaseAPImcp，24 个）

| 序号 | 文件路径 |
|------|---------|
| 31 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\summary_skill.md` |
| 32 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\property_Attr.md` |
| 33 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Cube.md` |
| 34 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Sphere.md` |
| 35 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Cone.md` |
| 36 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Box.md` |
| 37 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Arc.md` |
| 38 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Line.md` |
| 39 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Text.md` |
| 40 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Section.md` |
| 41 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Loft.md` |
| 42 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Sweep.md` |
| 43 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Combine.md` |
| 44 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Bool.md` |
| 45 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Linspace.md` |
| 46 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\geometric_interface\geometry_Color.md` |
| 47 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\matrix_interface.md` |
| 48 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\place_interface.md` |
| 49 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\01_sdk_interface_guide\drive_point_interface.md` |
| 50 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\02_coding_standards_safety\basic_writing_style.md` |
| 51 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\03_professional_patterns\assembly_guide.md` |
| 52 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\04_custom_components\custom_Ellipsoid.md` |
| 53 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\04_custom_components\custom_CircularTorus.md` |
| 54 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBaseAPImcp\skill\04_custom_components\custom_SquareTorus.md` |

### 6.4 本地知识库文档（leder_skills/，5 个）

| 序号 | 文件路径 |
|------|---------|
| 55 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_Agent几何理解与验证规则.md` |
| 56 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_AIAgent_建模交互技能.md` |
| 57 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_几何建模精确交互规范.md` |
| 58 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_pyp3d_建模方法函数大全.md` |
| 59 | `d:\BIMbase\PythonScript\BFAComponentLib\leder_skills\BIMBase_Skills_MCP_配置总览.md` |

### 6.5 根目录知识库文档（2 个）

| 序号 | 文件路径 |
|------|---------|
| 60 | `d:\BIMbase\PythonScript\BFAComponentLib\SKILL.md` |
| 61 | `d:\BIMbase\PythonScript\BFAComponentLib\BIMBase_AIAgent_建模指南.md` |

---

## 七、备份路径与同步规则

### 7.1 备份路径

| 序号 | 目录 | 说明 |
|------|------|------|
| 62 | `E:\个人笔记文件备份\notebook\实习\备份skills+mcp+markdown\skills\` | 备份 Skills 目录 |
| 63 | `E:\个人笔记文件备份\notebook\实习\备份skills+mcp+markdown\markdown\` | 备份 Markdown 目录 |
| 64 | `E:\个人笔记文件备份\notebook\实习\目前skills+mcp+md.md` | 当前 skills/mcp/md 汇总文件 |

### 7.2 同步更新规则

**当用户要求更新 Skills、Markdown 或 MCP 内容时，Agent 必须按以下顺序同步更新：**

1. 更新 `.trae\skills\` 下的 6 个 Skill 文件（序号 1-6）
2. 更新 `BIMBaseMCP\skill\` 下的对应文件（序号 7-30）
3. 更新 `BIMBaseAPImcp\skill\` 下的对应文件（序号 31-54）
4. 更新 `leder_skills\` 下的对应文件（序号 55-59）
5. 更新根目录 `SKILL.md` 和 `BIMBase_AIAgent_建模指南.md`（序号 60-61）
6. 更新备份 `skills\` 和 `markdown\` 目录（序号 62-63）
7. 更新 `目前skills+mcp+md.md`（序号 64）
8. 更新本汇总文件 `skills+markdown汇总.md`（如有路径变更）

### 7.3 备份与本地文件的对应关系

| 备份文件 | 本地 Skill 文件 |
|---------|---------------|
| `skills\BIMBase_Agent几何理解与验证规则.md` | `.trae\skills\bimbase-agent-geometry-rules\SKILL.md` |
| `skills\SKILL.md` | `.trae\skills\bimbase-pyp3d-modeling\SKILL.md` |
| `skills\BIMBase_AIAgent_建模交互技能.md` | `.trae\skills\bimbase-modeling-agent-interaction\SKILL.md` |
| `skills\BIMBase_几何建模精确交互规范.md` | `.trae\skills\bimbase-precise-modeling-interaction\SKILL.md` |
| `skills\BIMBase_pyp3d_建模方法函数大全.md` | `.trae\skills\bimbase-pyp3d-function-reference\SKILL.md` |
| `skills\BIMBase_Skills_MCP_配置总览.md` | `.trae\skills\bimbase-skills-mcp-overview\SKILL.md` |
| `markdown\BIMBase_Agent几何理解与验证规则.md` | 同上 |
| `markdown\BIMBase_几何建模精确交互规范.md` | 同上 |
| `markdown\BIMBase_Skills_MCP_配置总览.md` | 同上 |
| `markdown\BIMBase_pyp3d_建模方法函数大全.md` | 同上 |
| `markdown\BIMBase_AIAgent_建模指南.md` | 无对应 Skill（纯本地文档） |

---

> **维护说明**：当新增或删除 Skills、MCP 文件、知识库文档时，请同步更新本汇总文件中的路径清单，确保 Agent 始终拥有完整的最新路径信息。