@echo off
title 论文排版优化工具 - 自动同步
chcp 65001 >nul 2>&1

echo.
echo  ========================================================
echo.
echo           论文排版优化工具 - 自动同步
echo.
echo  ========================================================
echo.

cd /d "%~dp0"

echo  [检查] 正在检查Git状态...
echo.

:: 检查Git是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [错误] Git 未安装！
    echo  [提示] 请前往 https://git-scm.com/downloads 下载并安装 Git
    echo.
    pause
    exit /b 1
)

:: 检查远程仓库
git remote -v >nul 2>&1
if %errorlevel% neq 0 (
    echo  [错误] 未配置远程仓库！
    echo  [提示] 请先运行 启动程序.bat 初始化仓库
    echo.
    pause
    exit /b 1
)

:: 添加所有修改
echo  [操作] 添加所有修改...
git add .

:: 提交修改
echo  [操作] 提交修改...
git commit -m "Auto sync: %date% %time%"

:: 推送代码
echo  [操作] 推送代码到GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo  [错误] 同步失败！
    echo  [提示] 请检查网络连接或GitHub仓库配置
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo  [成功] 代码已成功同步到GitHub！
    echo.
    echo  提示：本窗口将在3秒后自动关闭...
    timeout /t 3 /nobreak >nul
)