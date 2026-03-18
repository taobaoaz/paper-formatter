#!/bin/bash

echo "========================================"
echo "  论文排版优化器 - 更新到 v2.0"
echo "========================================"
echo ""

echo "[1/4] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未检测到 Python3 环境"
    echo "请先安装 Python 3.8+"
    exit 1
fi
echo "✅ Python 环境正常 ($(python3 --version))"

echo ""
echo "[2/4] 更新依赖包..."
pip3 install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "⚠️ 警告：依赖安装失败，请手动安装"
    echo "运行：pip3 install -r requirements.txt"
else
    echo "✅ 依赖包更新完成"
fi

echo ""
echo "[3/4] 备份旧版本..."
if [ -f main.py.bak ]; then
    echo "⚠️ 备份文件已存在，跳过备份"
else
    cp main.py main.py.bak
    echo "✅ 已备份 main.py 到 main.py.bak"
fi

echo ""
echo "[4/4] 验证新版本..."
if [ -f main_refactored.py ]; then
    echo "✅ 新版本文件存在"
else
    echo "❌ 错误：新版本文件缺失"
    exit 1
fi

echo ""
echo "========================================"
echo "  ✅ 更新完成！"
echo "========================================"
echo ""
echo "运行方式："
echo "  方式 1（推荐）：python3 main_refactored.py"
echo "  方式 2（原版）：python3 main.py"
echo ""
echo "新功能："
echo "  📘 封面和声明页配置器"
echo "  📄 模板页面选择器"
echo "  🎨 现代化 UI 设计"
echo ""
echo "查看帮助："
echo "  - 架构说明.md"
echo "  - 封面声明页配置指南.md"
echo "  - 上传模板选择页面指南.md"
echo ""
