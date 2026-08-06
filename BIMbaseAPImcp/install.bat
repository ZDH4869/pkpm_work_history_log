@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM ============================================================
REM  BIMBase MCP Server 一键安装配置脚本
REM  功能：配置 Python 路径、安装依赖、注册 MCP 到 IDE
REM ============================================================

echo.
echo ══════════════════════════════════════════════════════════
echo   BIMBase MCP Server 一键安装配置
echo ══════════════════════════════════════════════════════════
echo.

REM —— 自动检测项目根目录（脚本所在目录的上级）——
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%"
REM 去掉末尾反斜杠
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

echo [信息] 项目目录: %PROJECT_ROOT%
echo.

REM ============================================================
REM 1. 获取 MCP Python 路径（用于运行 MCP Server，需 Python >= 3.10）
REM ============================================================
:INPUT_MCP_PYTHON
set "MCP_PYTHON="
echo ──────────────────────────────────────────────────────────
echo  步骤 1/4: 配置 MCP 运行 Python 解释器
echo  要求: Python ^>= 3.10 (fastmcp 依赖)
echo ──────────────────────────────────────────────────────────
echo.
set /p "MCP_PYTHON=请输入运行 MCP 的 Python 完整路径 (例如 D:\Miniconda\python.exe): "

if "%MCP_PYTHON%"=="" (
    echo [错误] 路径不能为空，请重新输入。
    echo.
    goto INPUT_MCP_PYTHON
)

REM 去掉引号
set "MCP_PYTHON=%MCP_PYTHON:"=%"

if not exist "%MCP_PYTHON%" (
    echo [错误] 文件不存在: %MCP_PYTHON%
    echo.
    goto INPUT_MCP_PYTHON
)

REM 验证 Python 版本 >= 3.10
echo [检查] 验证 Python 版本...
for /f "tokens=*" %%v in ('"%MCP_PYTHON%" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2^>nul') do set "PY_VER=%%v"

if "%PY_VER%"=="" (
    echo [错误] 无法获取 Python 版本，请确认路径正确。
    echo.
    goto INPUT_MCP_PYTHON
)

echo [信息] Python 版本: %PY_VER%

REM 解析主版本号和次版本号
for /f "tokens=1,2 delims=." %%a in ("%PY_VER%") do (
    set "PY_MAJOR=%%a"
    set "PY_MINOR=%%b"
)

if %PY_MAJOR% LSS 3 (
    echo [错误] Python 版本过低 (%PY_VER%)，需要 ^>= 3.10。
    echo.
    goto INPUT_MCP_PYTHON
)

if %PY_MAJOR%==3 if %PY_MINOR% LSS 10 (
    echo [错误] Python 版本过低 (%PY_VER%)，需要 ^>= 3.10。
    echo   建议: 安装 Miniconda (https://docs.conda.io/en/latest/miniconda.html)
    echo   或下载 Python 3.10+ (https://www.python.org/downloads/)
    echo.
    goto INPUT_MCP_PYTHON
)

echo [通过] Python 版本满足要求。
echo.

REM ============================================================
REM 2. 获取 BIMBase 建模 Python 路径（仅用于记录，不影响 MCP 运行）
REM ============================================================
:INPUT_BIM_PYTHON
set "BIM_PYTHON="
echo ──────────────────────────────────────────────────────────
echo  步骤 2/4: 配置 BIMBase 建模脚本 Python 解释器
echo  (仅用于 IDE 运行 .py 建模脚本，与 MCP 运行互不影响)
echo ──────────────────────────────────────────────────────────
echo.
set /p "BIM_PYTHON=请输入 BIMBase 内置 Python 路径 (例如 D:\BIMBase KIT official 2026 R1.0\BIMBase KIT 2026\PythonScript\python-3.7.9-embed-amd64\python.exe): "

if "%BIM_PYTHON%"=="" (
    echo [错误] 路径不能为空，请重新输入。
    echo.
    goto INPUT_BIM_PYTHON
)

set "BIM_PYTHON=%BIM_PYTHON:"=%"

if not exist "%BIM_PYTHON%" (
    echo [警告] 文件不存在: %BIM_PYTHON%
    set /p "CONTINUE=是否继续? (Y/N): "
    if /i not "!CONTINUE!"=="Y" (
        echo.
        goto INPUT_BIM_PYTHON
    )
)

echo [信息] BIMBase Python: %BIM_PYTHON%
echo.

REM ============================================================
REM 3. 安装 MCP Python 依赖
REM ============================================================
echo ──────────────────────────────────────────────────────────
echo  步骤 3/4: 安装 MCP Python 依赖
echo ──────────────────────────────────────────────────────────
echo.
echo [安装] 正在使用 %MCP_PYTHON% 安装依赖...
"%MCP_PYTHON%" -m pip install -r "%PROJECT_ROOT%\mcpServer\requirements.txt"
if errorlevel 1 (
    echo [错误] 依赖安装失败，请检查网络或 pip 配置。
    echo   可手动运行: "%MCP_PYTHON%" -m pip install -r "%PROJECT_ROOT%\mcpServer\requirements.txt"
    echo.
    set /p "CONTINUE=是否继续配置 IDE? (Y/N): "
    if /i not "!CONTINUE!"=="Y" (
        echo [退出] 安装中止。
        pause
        exit /b 1
    )
)
echo [完成] 依赖安装完成。
echo.

REM ============================================================
REM 4. 注册 MCP 到 IDE
REM ============================================================
echo ──────────────────────────────────────────────────────────
echo  步骤 4/4: 注册 MCP 到智能体 IDE
echo ──────────────────────────────────────────────────────────
echo.

set "MCP_SCRIPT=%PROJECT_ROOT%\mcpServer\MCPServer.py"
REM 将路径中的反斜杠替换为双反斜杠（用于 JSON）
set "MCP_SCRIPT_ESC=%MCP_SCRIPT:\=\\%"
set "MCP_PYTHON_ESC=%MCP_PYTHON:\=\\%"

REM —— 注册到 Trae ——
set "TRAE_MCP_DIR=%APPDATA%\Trae CN\User"
set "TRAE_MCP_FILE=%TRAE_MCP_DIR%\mcp.json"

echo [配置] 注册到 Trae IDE...
if exist "%TRAE_MCP_DIR%" (
    if exist "%TRAE_MCP_FILE%" (
        REM 文件已存在，合并配置（用 Python 处理 JSON 合并）
        "%MCP_PYTHON%" -c "import json,sys; f=open(sys.argv[1],'r',encoding='utf-8'); d=json.load(f); f.close(); d.setdefault('mcpServers',{}); d['mcpServers']['BIMBaseAI2PY']={'command':sys.argv[2],'args':[sys.argv[3]],'env':{},'description':'BIMBase pyp3d modeling skill retrieval service - requires Python>=3.10'}; f=open(sys.argv[1],'w',encoding='utf-8'); json.dump(d,f,ensure_ascii=False,indent=2); f.close(); print('OK')" "%TRAE_MCP_FILE%" "%MCP_PYTHON%" "%MCP_SCRIPT%"
        if errorlevel 1 (
            echo [警告] Trae MCP 配置合并失败，请手动配置。
        ) else (
            echo [成功] Trae MCP 配置已更新: %TRAE_MCP_FILE%
        )
    ) else (
        REM 文件不存在，创建新配置
        echo {"mcpServers":{"BIMBaseAI2PY":{"command":"%MCP_PYTHON_ESC%","args":["%MCP_SCRIPT_ESC%"],"env":{},"description":"BIMBase pyp3d modeling skill retrieval service - requires Python>=3.10"}}} > "%TRAE_MCP_FILE%"
        echo [成功] Trae MCP 配置已创建: %TRAE_MCP_FILE%
    )
) else (
    echo [跳过] 未找到 Trae 配置目录: %TRAE_MCP_DIR%
)

REM —— 注册到 Cursor ——
set "CURSOR_MCP_DIR=%APPDATA%\Cursor"
set "CURSOR_MCP_FILE=%CURSOR_MCP_DIR%\mcp.json"

echo [配置] 注册到 Cursor IDE...
if exist "%CURSOR_MCP_DIR%" (
    if exist "%CURSOR_MCP_FILE%" (
        "%MCP_PYTHON%" -c "import json,sys; f=open(sys.argv[1],'r',encoding='utf-8'); d=json.load(f); f.close(); d.setdefault('mcpServers',{}); d['mcpServers']['BIMBaseAI2PY']={'command':sys.argv[2],'args':[sys.argv[3]],'env':{},'description':'BIMBase pyp3d modeling skill retrieval service - requires Python>=3.10'}; f=open(sys.argv[1],'w',encoding='utf-8'); json.dump(d,f,ensure_ascii=False,indent=2); f.close(); print('OK')" "%CURSOR_MCP_FILE%" "%MCP_PYTHON%" "%MCP_SCRIPT%"
        if errorlevel 1 (
            echo [警告] Cursor MCP 配置合并失败，请手动配置。
        ) else (
            echo [成功] Cursor MCP 配置已更新: %CURSOR_MCP_FILE%
        )
    ) else (
        echo {"mcpServers":{"BIMBaseAI2PY":{"command":"%MCP_PYTHON_ESC%","args":["%MCP_SCRIPT_ESC%"],"env":{},"description":"BIMBase pyp3d modeling skill retrieval service - requires Python>=3.10"}}} > "%CURSOR_MCP_FILE%"
        echo [成功] Cursor MCP 配置已创建: %CURSOR_MCP_FILE%
    )
) else (
    echo [跳过] 未找到 Cursor 配置目录: %CURSOR_MCP_DIR%
)

REM —— 注册到 VS Code / Codex ——
echo [信息] VS Code / Codex 用户请手动在 settings.json 中添加 MCP 配置。
echo.

REM ============================================================
REM 5. 生成启动脚本
REM ============================================================
echo [生成] 更新启动脚本...

REM 生成 start_mcp_server.bat
(
echo @echo off
echo REM BIMBase MCP Server 启动器
echo REM 由 install.bat 自动生成
echo set PYTHON_EXE=%MCP_PYTHON%
echo set SCRIPT_PATH=%MCP_SCRIPT%
echo.
echo echo [%%date%% %%time%%] BIMBase MCP Server 启动中...
echo "%%PYTHON_EXE%%" "%%SCRIPT_PATH%%"
echo pause
) > "%PROJECT_ROOT%\mcpServer\start_mcp_server.bat"

REM 生成 start_mcp_server.ps1
(
echo # BIMBase MCP Server 启动器
echo # 由 install.bat 自动生成
echo `$PythonExe = "%MCP_PYTHON%"
echo `$ScriptPath = "%MCP_SCRIPT%"
echo.
echo Write-Host "[$`(Get-Date`)] BIMBase MCP Server 启动中..." -ForegroundColor Cyan
echo.
echo if (-not [System.IO.File]::Exists(`$PythonExe`)^) {
echo     Write-Host "[错误] Python 未找到: `$PythonExe" -ForegroundColor Red
echo     exit 1
echo }
echo.
echo & `$PythonExe `$ScriptPath
) > "%PROJECT_ROOT%\mcpServer\start_mcp_server.ps1"

echo [成功] 启动脚本已更新。
echo.

REM ============================================================
REM 完成
REM ============================================================
echo.
echo ══════════════════════════════════════════════════════════
echo   安装配置完成!
echo ══════════════════════════════════════════════════════════
echo.
echo   MCP Python:    %MCP_PYTHON% (%PY_VER%)
echo   BIMBase Python: %BIM_PYTHON%
echo   MCP 入口脚本:  %MCP_SCRIPT%
echo   项目目录:      %PROJECT_ROOT%
echo.
echo   下一步:
echo   1. 重启 Trae / Cursor / IDE 以加载新的 MCP 配置
echo   2. 在 IDE 中确认 BIMBaseAI2PY MCP 已被识别
echo   3. 使用 AI 智能体时提及 "BIMBase 建模" 即可自动调用
echo.
echo   手动启动: %MCP_PYTHON% %MCP_SCRIPT%
echo.

pause
