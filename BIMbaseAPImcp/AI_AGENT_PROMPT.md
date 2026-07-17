# AI 智能体安装提示词 (AI Agent Installation Prompt)

将以下内容粘贴到 Trae / Cursor / Codex 等 AI 智能体的对话中，智能体即可自动完成 MCP Server 的安装配置。

---

## 提示词模板

```
请帮我安装配置 BIMBase MCP Server，项目路径：{项目本地路径或GitHub链接}

我的环境信息：
- BIMBase 内置 Python 路径：{BIMBase Python 路径，如 D:\BIMbase\PythonScript\python-3.7.9-embed-amd64\python.exe}
- MCP 运行 Python 路径：{MCP Python 路径，如 D:\Miniconda\python.exe}（需要 Python >= 3.10）

请按照项目中的 install.bat 脚本逻辑完成以下步骤：
1. 验证两个 Python 路径是否有效
2. 使用 MCP Python 安装依赖 fastmcp
3. 将 MCP Server 注册到当前 IDE 的 MCP 配置中
4. 生成启动脚本
```

---

## 智能体执行指南

当用户要求安装 BIMBase MCP Server 时，请按以下步骤执行：

### 步骤 1: 收集必要信息

必须从用户获取：
1. **项目路径**: BIMbaseAPImcp 项目的本地路径或 GitHub 仓库链接
2. **BIMBase Python 路径**: BIMBase 内置的 Python 解释器路径（通常是 `python-3.7.9-embed-amd64\python.exe`）
3. **MCP Python 路径**: 用于运行 MCP Server 的 Python >= 3.10 解释器路径

如果用户没有提供 MCP Python 路径（Python >= 3.10），请询问：
- "MCP Server 需要 Python >= 3.10 才能运行（fastmcp 依赖），您的电脑上是否有 Miniconda 或 Python 3.10+ 的安装路径？"
- 如果用户没有合适的 Python 版本，建议安装 Miniconda：https://docs.conda.io/en/latest/miniconda.html

### 步骤 2: 如果是 GitHub 链接，先克隆项目

```bash
git clone {GitHub URL} {本地路径}
cd {本地路径}
```

### 步骤 3: 运行一键安装脚本

```bash
cd {项目路径}
install.bat
```

然后按照提示输入两个 Python 路径。

或者，如果智能体有文件操作权限，可以直接执行配置：

### 步骤 3（替代方案）: 手动配置

1. **安装依赖**:
   ```bash
   {MCP Python路径} -m pip install fastmcp
   ```

2. **配置 Trae IDE**:
   编辑 `%APPDATA%\Trae CN\User\mcp.json`，在 `mcpServers` 中添加：
   ```json
   {
     "BIMBaseAI2PY": {
       "command": "{MCP Python路径}",
       "args": ["{项目路径}\\mcpServer\\MCPServer.py"],
       "env": {},
       "description": "BIMBase pyp3d modeling skill retrieval service - requires Python>=3.10"
     }
   }
   ```

3. **配置 Cursor IDE**:
   编辑 `%APPDATA%\Cursor\mcp.json`，添加相同的配置。

4. **配置 VS Code (Copilot/Codex)**:
   在 `.vscode/mcp.json` 或用户 settings.json 中添加 MCP 配置。

### 步骤 4: 验证

1. 让用户重启 IDE
2. 在 IDE 设置中确认 BIMBaseAI2PY MCP Server 已被识别
3. 测试调用 `get_summary_document()` 工具是否返回内容

### 关键注意事项

- **两个 Python 互不影响**: BIMBase 内置 Python (3.7.9) 仅用于运行 pyp3d 建模脚本（必须在 BIMBase 环境内执行），MCP Python (>=3.10) 仅用于运行 MCP Server 进程
- **路径中的反斜杠**: JSON 配置中 Windows 路径需要使用双反斜杠 `\\` 或正斜杠 `/`
- **重启 IDE**: 修改 MCP 配置后必须重启 IDE 才能生效
- **pip 安装网络问题**: 如果 pip 安装失败，建议使用国内镜像：
  ```bash
  {MCP Python路径} -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastmcp
  ```
