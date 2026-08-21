# BIMBase Skills & MCP 配置总览

> **冲突优先级规则（最高优先级，必须遵守）**
> 1. **建模技术要求**：本地 skills/markdown 内容若与 `BIMBaseAI2PY_MCPServer` 获取到的建模技术要求（函数签名、参数语义、几何定位语义、编码规范等）发生冲突或解释不同，**以 `BIMBaseAI2PY_MCPServer` 为第一执行准则**。
> 2. **个人建模喜好**：涉及个人建模喜好（建模定位提示词喜好、特殊模型部件调用，如散热片、半椭球体等）时，**以本地 skills/markdown 为第一执行准则**。

## MCP 工具链

| 工具 | 用途 | 调用时机 |
|------|------|---------|
| `get_summary_document()` | 全局 SDK 与文档路径 | 首次建模必调 |
| `get_skill_manifest()` | 结构化 symbol 索引 | 需要定位 API 时 |
| `get_skill_doc(symbol)` | 单个文档正文 | 确认 API 签名时 |
| `get_skill_bundle(symbols)` | 批量获取文档 | 规划完所需 API 后 |
| `get_related_skills(symbol)` | 配套函数查询 | 需要关联 API 时 |

## 运行环境

| 环境 | 路径/地址 | 用途 |
|------|------|------|
| MCP 服务 | `https://dev.pkpm.cn/mcp/`（远程） | 提供官方 SDK 文档，无需本地 Python |
| 建模 Python | `D:\BIMBase KIT official 2026 R1.0\...\python.exe` (3.7.9) | BIMBase 内嵌执行建模脚本 |

## 建模流程调用指南

1. 理解需求 → 2. `get_summary_document()` → 3. `get_skill_manifest()` → 4. 规划 API → 5. `get_skill_bundle()` → 6. 编码 → 7. 自检
