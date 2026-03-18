#!/usr/bin/env python3
"""
论文排版优化工具 - 启动器
启动版本：v2.0
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用重构版主程序（v2.0）
from main_refactored import main

if __name__ == '__main__':
    main()
