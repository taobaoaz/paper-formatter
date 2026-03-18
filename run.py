#!/usr/bin/env python3
"""
论文排版优化器 v2.0 - 主启动入口
Paper Formatter v2.0 - Main Entry Point

功能：
- 封面和声明页配置器
- 模板页面选择器
- 现代化 UI 设计
- 文档格式化
- 参考文献处理

使用方法:
    python3 main.py
    
或双击运行此文件
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入主程序（使用重构版）
from main_refactored import main

if __name__ == '__main__':
    main()
