#!/bin/bash

# 论文排版优化器 v2.0 - Linux/Mac 启动脚本

echo "========================================"
echo "  论文排版优化器 v2.0"
echo "  Paper Formatter v2.0"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "正在启动..."
echo ""

python3 run.py

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "  启动失败！"
    echo "========================================"
    echo ""
    echo "可能原因:"
    echo "1. Python 未安装"
    echo "2. 依赖包未安装"
    echo ""
    echo "解决方法:"
    echo "1. 安装 Python 3.8+"
    echo "2. 运行：pip3 install -r requirements.txt"
    echo ""
    exit 1
fi
