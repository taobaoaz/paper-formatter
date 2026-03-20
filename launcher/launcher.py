#!/usr/bin/env python3
"""
论文排版优化器 v2.0
启动入口 - Entry Point
"""

import sys
import os

# 确保在项目目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 启动主程序（使用完全版 v2.0）
from main import main

if __name__ == '__main__':
    main()
