@echo off
chcp 65001 >nul
title 论文排版优化器 v2.0
cd /d "%~dp0"
python launcher.py
if errorlevel 1 pause
