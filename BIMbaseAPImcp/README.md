# BIMBase API MCP Server

BIMBase pyp3d 参数化建模技能文档检索 MCP Server，为 AI 智能体（Trae、Cursor、Codex 等）提供 BIMBase 建模 API 文档的结构化检索能力。

## 项目结构

```
BIMbaseAPImcp/
├── install.bat                          # 一键安装配置脚本
├── AI_AGENT_PROMPT.md                   # AI 智能体安装提示词
├── README.md                            # 本文件
├── .gitignore
├── mcpServer/                           # MCP Server 核心
│   ├── MCPServer.py                     # MCP Server 入口（fastmcp）
│   ├── config.py                        # 配置（路径自动解析）
│   ├── monitoring.py                    # 工具调用监控
│   ├── skill_manifest_overrides.json    # 技能清单覆盖配置
│   ├── requirements.txt                 # Python 依赖
│   ├── start_mcp_server.bat             # 启动脚本（安装后自动生成）
│   └── start_mcp_server.ps1             # PowerShell 启动脚本
└── skill/                               # 技能文档库
    ├── summary_skill.md                 # 技能总览
    ├── 01_sdk_interface_guide/          # SDK 接口文档
    │   ├── geometric_interface/         # 几何体 API（Cube/Cone/Sweep 等）
    │   ├── matrix_interface.md          # 变换矩阵
    │   ├── place_interface.md           # 布置接口
    │   └── drive_point_interface.md     # 驱动点接口
    ├── 02_coding_standards_safety/      # 编码规范
    │   └── basic_writing_style.md
    ├── 03_professional_patterns/        # 专业模式
    │   └── assembly_guide.md
    └── 04_custom_components/            # 自定义组件模板
        ├── custom_Ellipsoid.md
        ├── custom_CircularTorus.md
        └── custom_SquareTorus.md
```

## 双 Python 环境说明

本项目涉及两个 Python 解释器，**互不影响**：

| 用途 | 版本要求 | 说明 |
|------|---------|------|
| **BIMBase 建模 Python** | 3.7.9 (嵌入版) | BIMBase 内置，运行 pyp3d 建模脚本，必须在 BIMBase 进程内执行 |
| **MCP 运行 Python** | >= 3.10 | 运行 MCP Server 进程（fastmcp 依赖），独立运行 |

MCP Server 仅使用 MCP Python 运行，不会调用 BIMBase Python。BIMBase Python 仅在 BIMBase 应用内加载 .py 建模脚本时使用。

## 快速安装

### 方式一：一键安装脚本（推荐）

1. 双击 `install.bat`
2. 按提示输入 MCP 运行 Python 路径（需 >= 3.10）
3. 按提示输入 BIMBase 内置 Python 路径
4. 等待依赖安装和 IDE 配置完成
5. 重启 IDE

### 方式二：AI 智能体安装

将 `AI_AGENT_PROMPT.md` 中的提示词粘贴到 AI 对话中，智能体将自动完成安装配置。

### 方式三：手动安装

1. 安装依赖：
   ```bash
   # 使用 MCP Python（非 BIMBase Python）
   D:\Miniconda\python.exe -m pip install fastmcp
   ```

2. 配置 IDE MCP：

   **Trae**: 编辑 `%APPDATA%\Trae CN\User\mcp.json`
   ```json
   {
     "mcpServers": {
       "BIMBaseAI2PY": {
         "command": "D:\\Miniconda\\python.exe",
         "args": ["D:\\path\\to\\BIMbaseAPImcp\\mcpServer\\MCPServer.py"],
         "env": {},
         "description": "BIMBase pyp3d modeling skill retrieval service - requires Python>=3.10"
       }
     }
   }
   ```

   **Cursor**: 编辑 `%APPDATA%\Cursor\mcp.json`，格式同上。

   **VS Code (Copilot)**: 在项目 `.vscode/mcp.json` 中添加相同配置。

3. 重启 IDE

## MCP 工具列表

| 工具名 | 说明 |
|--------|------|
| `get_summary_document()` | 获取建模技能总览文档，首次使用必调 |
| `get_skill_manifest()` | 获取技能文档结构化索引 |
| `get_skill_doc(symbol)` | 按 symbol 获取单个技能文档正文 |
| `get_skill_bundle(symbols)` | 批量获取多个技能文档（含依赖） |
| `get_related_skills(symbol)` | 获取某技能的关联推荐 |

## 常见问题

### Q: 运行 install.bat 时 pip 安装失败？
使用国内镜像：
```bash
D:\Miniconda\python.exe -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastmcp
```

### Q: MCP 在 IDE 中不显示？
1. 确认 `mcp.json` 路径和格式正确
2. 重启 IDE
3. 检查 IDE 设置中 MCP 是否被启用

### Q: 没有 Python >= 3.10？
安装 Miniconda（轻量）：
```bash
# 下载地址
https://docs.conda.io/en/latest/miniconda.html

# 安装后创建环境
conda create -n mcp python=3.13
conda activate mcp
# 然后使用 conda 环境的 python 路径作为 MCP Python
```

### Q: 两个 Python 会冲突吗？
不会。MCP Server 进程独立运行，仅使用 MCP Python。BIMBase Python 仅在 BIMBase 应用内部使用，两者完全隔离。

## 开发与调试

```bash
# 手动启动 MCP Server（用于调试）
D:\Miniconda\python.exe D:\path\to\BIMbaseAPImcp\mcpServer\MCPServer.py

# 查看工具调用日志
type logs\mcp_tool_invocations.jsonl
```

## License

MIT
