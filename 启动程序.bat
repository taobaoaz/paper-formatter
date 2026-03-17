@echo off
title 论文排版优化工具
chcp 65001 >nul 2>&1

echo.
echo  ========================================================
echo.
echo           论文排版优化工具 v1.0
echo.
echo  ========================================================
echo.

cd /d "%~dp0"

echo  [检查] 正在检查系统环境...
echo.

:: 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [错误] Python 未安装或不在环境变量中！
    echo  [信息] 正在自动下载并安装 Python...
    echo.
    
    :: 使用 PowerShell 下载并安装 Python
    powershell -Command "
        Write-Host '正在下载 Python 3.12...' -ForegroundColor Green
        $pythonInstaller = 'python-3.12.0-amd64.exe'
        $downloadUrl = 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe'
        
        try {
            Invoke-WebRequest -Uri $downloadUrl -OutFile $pythonInstaller -ErrorAction Stop
            Write-Host '下载完成，正在安装...' -ForegroundColor Green
            
            # 静默安装 Python，添加到 PATH
            Start-Process -FilePath $pythonInstaller -ArgumentList '/quiet', 'PrependPath=1', 'Include_test=0' -Wait -ErrorAction Stop
            Write-Host 'Python 安装完成！' -ForegroundColor Green
            
            # 清理安装文件
            Remove-Item $pythonInstaller -ErrorAction SilentlyContinue
        } catch {
            Write-Host '安装失败：' $_.Exception.Message -ForegroundColor Red
            exit 1
        }
    "
    
    if %errorlevel% neq 0 (
        echo  [错误] Python 安装失败！
        echo  [提示] 请手动前往 https://www.python.org/downloads/ 下载并安装
        echo  [提示] 安装时请勾选 "Add Python to PATH"
        echo.
        pause
        exit /b 1
    ) else (
        echo  [成功] Python 安装完成
        echo  [信息] 正在刷新环境变量...
        :: 刷新环境变量
        call "%windir%\System32\cmd.exe" /c "set PATH=%PATH%"
    )
) else (
    echo  [成功] Python 已安装
)

:: 检查依赖包
if exist "requirements.txt" (
    echo  [检查] 正在检查依赖包...
    pip check >nul 2>&1
    if %errorlevel% neq 0 (
        echo  [提示] 依赖包不完整，正在安装...
        pip install -r requirements.txt
        if %errorlevel% neq 0 (
            echo  [错误] 依赖包安装失败！
            echo  [提示] 请检查网络连接后重试
            echo.
            pause
            exit /b 1
        ) else (
            echo  [成功] 依赖包安装完成
        )
    ) else (
        echo  [成功] 依赖包已完整
    )
) else (
    echo  [警告] 未找到 requirements.txt 文件
)

echo.
echo  [信息] 正在启动论文排版优化工具...
echo.

start "论文排版优化工具" /min python main.py

if %errorlevel% neq 0 (
    echo.
    echo  [错误] 程序启动失败！
    echo.
    echo  请手动运行：python main.py
    echo.
    pause
) else (
    echo  [成功] 程序已启动！
    echo.
    echo  提示：本窗口将在3秒后自动关闭...
    timeout /t 3 /nobreak >nul
)
