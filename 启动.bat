@echo off
chcp 65001 >nul
title 论文排版优化器 v2.0

echo ========================================
echo   论文排版优化器 v2.0
echo   Paper Formatter v2.0
echo ========================================
echo.

cd /d "%~dp0"

echo 正在启动...
echo.

python3 run.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   启动失败！
    echo ========================================
    echo.
    echo 可能原因:
    echo 1. Python 未安装
    echo 2. 依赖包未安装
    echo.
    echo 解决方法:
    echo 1. 安装 Python 3.8+
    echo 2. 运行：pip install -r requirements.txt
    echo.
    pause
)
