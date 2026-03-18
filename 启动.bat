@echo off
chcp 65001 >nul
title 论文排版优化器 v2.0
cd /d "%~dp0"

:: 启动程序（不等待程序结束）
start "" python launcher.py

:: 立即退出批处理文件
exit
