@echo off
rem ============================================================
rem  run_pyp3d.cmd
rem  Auto-locate BIMBase embedded Python 3.7.9 and run a pyp3d
rem  script with it. Pure batch (cmd) replacement for run_pyp3d.ps1.
rem
rem  Usage:
rem      run_pyp3d.cmd <script.py> [args...]
rem      run_pyp3d.cmd -PrintPython
rem      run_pyp3d.cmd -Refresh <script.py>
rem ============================================================
setlocal EnableDelayedExpansion

set "EMBED_SUBPATH=PythonScript\python-3.7.9-embed-amd64\python.exe"
set "CACHE_DIR=%LOCALAPPDATA%\bimbase-run"
set "CACHE_FILE=%CACHE_DIR%\python_path.txt"

rem ---------- parse arguments ----------
set "SCRIPT="
set "PRINT_PYTHON=0"
set "REFRESH=0"
set "ARGS="
:parse
if "%~1"=="" goto :parse_done
if /i "%~1"=="-PrintPython" ( set "PRINT_PYTHON=1" & shift & goto :parse )
if /i "%~1"=="-Refresh"    ( set "REFRESH=1"    & shift & goto :parse )
if not defined SCRIPT ( set "SCRIPT=%~1" ) else ( set "ARGS=!ARGS! %~1" )
shift
goto :parse
:parse_done

rem fallback: take script path from env var. Some shells pass Chinese args
rem to cmd in a way that mangles the bytes; env vars are Unicode-safe.
if not defined SCRIPT if defined PYP3D_SCRIPT set "SCRIPT=%PYP3D_SCRIPT%"

set "PY="

rem 0) explicit env var: BIMBASE_PYTHON points directly to python.exe
if not defined PY if defined BIMBASE_PYTHON if exist "%BIMBASE_PYTHON%" set "PY=%BIMBASE_PYTHON%"

rem 1) cached result from a previous run
if not defined PY if "!REFRESH!"=="0" if exist "%CACHE_FILE%" (
    set "CACHED="
    set /p "CACHED=" < "%CACHE_FILE%"
    if defined CACHED if exist "!CACHED!" set "PY=!CACHED!"
)

rem 2) BIMBASE_HOME env var (install dir)
if not defined PY if defined BIMBASE_HOME if exist "%BIMBASE_HOME%\%EMBED_SUBPATH%" set "PY=%BIMBASE_HOME%\%EMBED_SUBPATH%"

rem 3) registry: PKPM install keys
if not defined PY call :scan_registry

rem 4) running BIMBase process (best-effort via wmic)
if not defined PY call :scan_process

rem 5) disk scan fallback (directory-name based, 2 levels)
if not defined PY call :scan_disk

if not defined PY (
    echo [ERROR] Cannot locate BIMBase embedded Python interpreter.
    echo Set BIMBASE_PYTHON to "...\PythonScript\python-3.7.9-embed-amd64\python.exe",
    echo or BIMBASE_HOME to the BIMBase install directory, then retry.
    echo Do NOT fall back to system python - pyp3d only exists in the embedded interpreter.
    exit /b 3
)

rem persist cache for next time
if not exist "%CACHE_DIR%" mkdir "%CACHE_DIR%" >nul 2>&1
>"%CACHE_FILE%" echo !PY!

if "!PRINT_PYTHON!"=="1" goto :show
if not defined SCRIPT goto :show
goto :run

:show
echo !PY!
exit /b 0

:run
if not exist "%SCRIPT%" (
    echo [ERROR] Target script not found: %SCRIPT%
    exit /b 4
)

"%PY%" "%SCRIPT%" !ARGS!
exit /b %errorlevel%

rem ---------- subroutines ----------

:scan_registry
if defined PY exit /b 0
for %%K in ("HKLM\SOFTWARE\PKPM" "HKLM\SOFTWARE\WOW6432Node\PKPM" "HKCU\SOFTWARE\PKPM") do (
    for %%V in (InstallPath InstallLocation Path Home InstallDir) do (
        for /f "skip=1 tokens=2,*" %%A in ('reg query "%%~K" /v %%V 2^>nul') do (
            if not defined PY (
                set "loc=%%B"
                if defined loc if exist "!loc!\%EMBED_SUBPATH%" set "PY=!loc!\%EMBED_SUBPATH%"
            )
        )
    )
)
exit /b 0

:scan_process
if defined PY exit /b 0
where wmic >nul 2>&1
if errorlevel 1 exit /b 0
for /f "skip=1 delims=" %%A in ('wmic process where "name like '%%bim%%'" get ExecutablePath 2^>nul') do (
    if not defined PY (
        set "ep=%%A"
        set "ep=!ep: =!"
        if not "!ep!"=="" for %%p in ("!ep!") do if exist "%%~dpp%EMBED_SUBPATH%" set "PY=%%~dpp%EMBED_SUBPATH%"
    )
)
exit /b 0

:scan_disk
if defined PY exit /b 0
for %%D in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if not defined PY if exist "%%D:\" (
        for /d %%A in ("%%D:\*") do (
            if not defined PY call :check_dir "%%A"
        )
    )
)
exit /b 0

:check_dir
if defined PY exit /b 0
set "d=%~1"
set "n=%~nx1"
echo !n! | findstr /i "bim pkpm" >nul
if errorlevel 1 exit /b 0
if exist "!d!\%EMBED_SUBPATH%" set "PY=!d!\%EMBED_SUBPATH%"
if defined PY exit /b 0
for /d %%B in ("!d!\*") do (
    if not defined PY if exist "%%B\%EMBED_SUBPATH%" set "PY=%%B\%EMBED_SUBPATH%"
)
exit /b 0
