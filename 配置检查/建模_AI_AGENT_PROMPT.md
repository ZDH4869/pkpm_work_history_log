# AI Agent 一键配置提示词 — BIMBase Skills + Markdown 知识库（跨 Agent 快速版）

本文件是给 AI Agent（Trae / Cursor / WorkBuddy / CodeBuddy / Claude / OpenCode 等）阅读的**配置说明书**。用户只需发送一句话，Agent 即可把本项目中的 skills 和 markdown 知识库，按用户所使用的 AI Agent 软件的读取协议，配置到用户自己的 BIMBase 项目里，并出现在对应软件的功能区中。

> 说明：本项目（`skills+markdown一键配置`）是**源项目**；用户通常在自己的 BIMBase 项目目录中打开 Agent 发起配置。

---

## 用户触发提示词（直接复制，任何 AI Agent 通用）

```
请你帮我把这个"skills+markdown一键配置"这个项目中的skills和markdown知识库配置到本地
```

---

## Agent 执行总览

收到提示词后，**先做一次性交互确认（阶段 0），确认完成后才开始任何配置操作**。顺序如下：

**阶段 0 配置前交互确认（一次性提问）→ 阶段 1 定位源项目 → 阶段 2 部署文件 → 阶段 3 写入解释器配置 → 阶段 4 验证并报告**。

核心原则：**在一切配置开始前，用一条消息问清「目标软件、BIMBase Python 路径、建模项目路径」三项，避免反复追问与无效摸索浪费上下文**。

---

## 阶段 0：配置前交互确认（一次性提问，任何配置操作之前，必做）

在开始任何文件操作、探测、复制之前，**先用一条消息一次性向用户确认以下 3 项信息**。能自动识别的先填好默认值让用户确认，缺失项才请用户填写。

```
开始配置前，请一次性确认以下信息（能自动识别的已替你填好，确认或修改即可）：

1. 目标 AI Agent 软件：〔Trae / Cursor / Claude Code / Codex / OpenCode / CodeBuddy / WorkBuddy / 其他，可多选〕
2. BIMBase 内置 Python 路径（建模解释器，后续建模 .py 都用它运行）：〔自动探测结果或空〕
3. 建模项目路径：〔当前 AI Agent 打开的项目目录〕
```

三项说明：

- **目标 AI Agent 软件**：决定 skills/rules 落位到哪个功能区。若用户未明确、但能判断当前运行环境（存在 `.trae/`、`.cursor/`、`.claude/` 等特征），先按当前环境填默认并请确认。确定后按下方「跨 AI Agent Skills 读取协议表」落位；表中没有的软件，用 Web 搜索/官方文档检索 `"{软件名}" skill rules 配置路径`。
- **BIMBase 内置 Python 路径**：这是**建模脚本的运行解释器**（通常 `D:\BIMbase\PythonScript\python-3.7.9-embed-amd64\python.exe`）。若用户给不出，先自动探测（见阶段 1 前的探测命令）再回填确认；确认后写入 `.bimbase_python_path.txt` 作为后续建模默认解释器。
- **建模项目路径**：默认就是当前 AI Agent 打开的项目目录，一般用户无需输入。

> ⚠️ **Python 区分（重要）**：BIMBase 内置 Python（3.7.9）只用于**运行建模 .py 脚本**；MCP（`BIMBaseAI2PY_MCPServer`）为**远程服务**（`https://dev.pkpm.cn/mcp/`），无需本地 Python。本项目只处理建模解释器配置。

---

## 阶段 1：定位源项目 SOURCE_DIR

源项目是名为 `skills+markdown一键配置` 的文件夹（内含 `.trae/skills/`、`skills/`、`markdown/`）。自动搜索，不让用户手打中文路径：

```powershell
$roots = @("$env:USERPROFILE\Desktop", "$env:USERPROFILE\Downloads", "$env:USERPROFILE\Documents", "$env:USERPROFILE")
foreach ($r in $roots) {
  if (Test-Path $r) {
    Get-ChildItem -Path $r -Recurse -Directory -Filter "*skills+markdown一键配置*" -ErrorAction SilentlyContinue -Depth 3 |
      Select-Object -ExpandProperty FullName
  }
}
```

确认候选同时含 `.trae\skills`、`skills`、`markdown` 三个子目录才算有效：

```powershell
Test-Path "{候选}\.trae\skills"; Test-Path "{候选}\skills"; Test-Path "{候选}\markdown"
```

找不到再问用户（拖拽文件夹或说明位置）。

### 附：BIMBase Python 自动探测（阶段 0 用户给不出时执行）

```powershell
$py = $null
foreach ($r in @("D:\BIMbase","D:\BIMBase","C:\BIMbase","C:\BIMBase")) {
  if (Test-Path $r) {
    $c = Get-ChildItem -Path $r -Recurse -Filter "python.exe" -ErrorAction SilentlyContinue |
         Where-Object { $_.FullName -like "*python-3.7.9-embed-amd64*" } |
         Select-Object -First 1 -ExpandProperty FullName
    if ($c) { $py = $c; break }
  }
}
$py
```

## 阶段 2：部署文件（通用文件 + 各软件原生文件）

**禁止 Read+Write 逐文件复制**，用系统命令秒级完成（robocopy 返回码 0~7 均为成功）。

### 2.1 通用文件（任何软件都能读，始终部署）

```powershell
robocopy "{SOURCE_DIR}\skills" "{TARGET_ROOT}\skills" /E /IS /IT
robocopy "{SOURCE_DIR}\markdown" "{TARGET_ROOT}\markdown" /E /IS /IT
copy "{SOURCE_DIR}\skills\SKILL.md" "{TARGET_ROOT}\SKILL.md" /Y
copy "{SOURCE_DIR}\markdown\BIMBase_AIAgent_建模指南.md" "{TARGET_ROOT}\BIMBase_AIAgent_建模指南.md" /Y
```

### 2.2 各软件原生文件（让 skills 出现在对应功能区）

按阶段 0 确定的软件，把源 `.trae/skills/<slug>/SKILL.md`（6 个，slug 即英文文件夹名）落位到对应目录：

| 软件 | 落位目录 | 操作 |
|------|---------|------|
| Trae | `{TARGET_ROOT}\.trae\skills\` | `robocopy "{SOURCE_DIR}\.trae\skills" "{TARGET_ROOT}\.trae\skills" /E /IS /IT` |
| Cursor | `{TARGET_ROOT}\.cursor\rules\` | 每个 skill 转成 `bimbase-<slug>.mdc`，加 frontmatter `---\ndescription: <用途>\nglobs: **/*.py\n---` |
| Claude Code | `{TARGET_ROOT}\.claude\skills\<slug>\SKILL.md` | 复制 `.trae/skills/*` 到 `.claude/skills/*`；另写根 `CLAUDE.md` 引用 |
| Codex / OpenCode | 根 `AGENTS.md` | 写一份指引：强制先读 `SKILL.md`，再按需读 `skills/`、`markdown/` |
| CodeBuddy | `{TARGET_ROOT}\.codebuddy\rules\` | 类似 Cursor，写 `bimbase-<slug>.md` |
| WorkBuddy / 其他 | 检索官方文档 | 搜索 `"{软件名}" skill rules 配置路径` 后落位 |

> 原生文件内容取自源 `skills/` 下对应 `.md`（与 `.trae/skills/*/SKILL.md` 内容一致），仅扩展名/frontmatter 按目标软件要求调整。

## 阶段 3：写入 Python 解释器配置（建模解释器）

```powershell
Set-Content -Path "{TARGET_ROOT}\.bimbase_python_path.txt" -Value "BIMBASE_PYTHON={PYTHON_PATH}" -Encoding UTF8
```

> 该文件记录的是 **BIMBase 建模解释器**路径，后续建模 .py 脚本一律用此解释器运行（MCP 为远程服务，无需本地 Python）。

## 阶段 4：验证并报告

用 `Test-Path` 做存在性检查（不读内容）：

```powershell
Test-Path "{TARGET_ROOT}\.trae\skills\bimbase-pyp3d-modeling\SKILL.md"   # Trae
Test-Path "{TARGET_ROOT}\.cursor\rules"                                  # Cursor（如有）
Test-Path "{TARGET_ROOT}\.claude\skills"                                 # Claude（如有）
Test-Path "{TARGET_ROOT}\AGENTS.md"                                      # Codex/OpenCode（如有）
Test-Path "{TARGET_ROOT}\skills\SKILL.md"
Test-Path "{TARGET_ROOT}\markdown\BIMBase_pyp3d_建模方法函数大全.md"
Test-Path "{TARGET_ROOT}\SKILL.md"
Test-Path "{TARGET_ROOT}\BIMBase_AIAgent_建模指南.md"
Test-Path "{TARGET_ROOT}\.bimbase_python_path.txt"
```

以勾选清单向用户报告，并提示：**重启对应软件后，skills/rules 才会出现在其功能区**。

---

## 跨 AI Agent Skills 读取协议表（速查）

| AI Agent | Skills/Rules 落位 | 说明 |
|----------|-------------------|------|
| Trae | `.trae/skills/<slug>/SKILL.md` | 自动注册到 Skills 面板 |
| Cursor | `.cursor/rules/<slug>.mdc` | 规则面板；需 `description` frontmatter |
| Claude Code | `.claude/skills/<slug>/SKILL.md` | Agent Skills；另写 `CLAUDE.md` 入口 |
| Codex / OpenCode | 根 `AGENTS.md` | 指引读取 `SKILL.md` + `skills/` + `markdown/` |
| CodeBuddy | `.codebuddy/rules/<slug>.md` | 项目规则 |
| WorkBuddy / 其他 | 检索官方文档 | 搜索 `"{软件名}" skill rules 配置路径` |

> 上表为常用软件速查；如软件版本更新导致路径变化，以 Web 搜索/官方文档为准。

---

## 执行原则

| 原则 | 说明 |
|------|------|
| **先确认后配置** | 一切操作前，一次性确认「软件 / BIMBase Python / 项目路径」三项 |
| **Python 区分** | BIMBase 内置 Python(3.7.9) = 建模解释器；MCP 为远程服务（无需本地 Python） |
| **自动定位/探测** | 源项目、BIMBase Python、项目路径优先自动确定 |
| **通用+原生** | 通用文件始终部署，原生文件按软件部署到功能区 |
| **零读取** | 部署阶段不 Read skills/markdown 内容 |
| **系统级复制** | robocopy / copy，秒级完成 |
| **验证仅存在性** | Test-Path，不做内容比对 |

---

> 编制日期：2026-08-19
> 版本：v6.0（配置前一次性确认 + 跨 AI Agent 精准落位版）
