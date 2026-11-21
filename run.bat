@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist ".venv" (
    echo 首次运行，正在创建虚拟环境并安装依赖，请稍候...
    python -m venv .venv
    if errorlevel 1 (
        echo 创建虚拟环境失败，请确认已安装 Python 3.10+ 并加入 PATH。
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" -m pip install --quiet "flet>=0.28,<0.29"
    if errorlevel 1 (
        echo 安装依赖失败，请检查网络连接。
        pause
        exit /b 1
    )
)
start "" ".venv\Scripts\pythonw.exe" main.py
