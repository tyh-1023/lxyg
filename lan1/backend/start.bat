@echo off
chcp 65001 >nul
title 蓝心易购后端服务器

echo.
echo ========================================
echo           蓝心易购后端服务器
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 切换到脚本目录
cd /d "%~dp0"

:: 启动服务器
echo 🚀 正在启动服务器...
echo.
echo 服务器地址: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.

python start_server.py

echo.
echo 🛑 服务器已停止
pause 