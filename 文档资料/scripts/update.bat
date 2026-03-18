@echo off
chcp 65001 >nul
echo ========================================
echo   论文排版优化器 - 更新到 v2.0
echo ========================================
echo.

echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未检测到 Python 环境
    echo 请先安装 Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python 环境正常

echo.
echo [2/4] 更新依赖包...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo ⚠️ 警告：依赖安装失败，请手动安装
    echo 运行：pip install -r requirements.txt
) else (
    echo ✅ 依赖包更新完成
)

echo.
echo [3/4] 备份旧版本...
if exist main.py.bak (
    echo ⚠️ 备份文件已存在，跳过备份
) else (
    copy main.py main.py.bak >nul
    echo ✅ 已备份 main.py 到 main.py.bak
)

echo.
echo [4/4] 验证新版本...
if exist main_refactored.py (
    echo ✅ 新版本文件存在
) else (
    echo ❌ 错误：新版本文件缺失
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 更新完成！
echo ========================================
echo.
echo 运行方式：
echo   方式 1（推荐）：python main_refactored.py
echo   方式 2（原版）：python main.py
echo.
echo 新功能：
echo   📘 封面和声明页配置器
echo   📄 模板页面选择器
echo   🎨 现代化 UI 设计
echo.
echo 查看帮助：
echo   - 架构说明.md
echo   - 封面声明页配置指南.md
echo   - 上传模板选择页面指南.md
echo.
pause
