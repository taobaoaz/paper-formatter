@echo off
chcp 65001 >nul
title 论文排版优化器 - 打包工具

echo ========================================
echo   论文排版优化器 - 打包成 EXE
echo ========================================
echo.

echo [1/4] 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
) else (
    echo ✅ PyInstaller 已安装
)

echo.
echo [2/4] 清理旧文件...
rmdir /s /q build dist 2>nul
del *.spec 2>nul
echo ✅ 清理完成

echo.
echo [3/4] 开始打包...
echo 这可能需要 2-5 分钟...
echo.

pyinstaller --onefile --windowed ^
  --name "论文排版优化器" ^
  --icon icon.ico ^
  --add-data "docs;docs" ^
  --hidden-import PyQt5 ^
  --hidden-import python-docx ^
  main.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   ❌ 打包失败！
    echo ========================================
    echo.
    echo 请检查错误信息
    pause
    exit /b 1
)

echo.
echo [4/4] 打包完成！
echo.
echo ========================================
echo   ✅ 打包成功！
echo ========================================
echo.
echo 📦 可执行文件位置:
echo   dist\论文排版优化器.exe
echo.
echo 📁 目录结构:
echo   dist/
echo   └── 论文排版优化器.exe  ← 发给用户这个！
echo.
echo 🎉 完成！
echo.
pause
