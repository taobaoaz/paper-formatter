#!/bin/bash

# 论文排版优化器 - 一键推送到 GitHub
# 使用方法：./push_to_github.sh

set -e

echo "========================================"
echo "  📤 论文排版优化器 v2.0 - 推送到 GitHub"
echo "========================================"
echo ""

cd /home/admin/openclaw/workspace/paper-formatter

# 检查 Git 状态
echo "[1/5] 检查 Git 状态..."
git status --short
if [ $? -ne 0 ]; then
    echo "❌ Git 状态检查失败"
    exit 1
fi
echo "✅ 状态正常"

# 显示提交历史
echo ""
echo "[2/5] 提交历史:"
git log --oneline -5

# 显示标签
echo ""
echo "[3/5] 版本标签:"
git tag -l

# 选择推送方式
echo ""
echo "[4/5] 选择推送方式:"
echo "1) HTTPS (需要用户名密码)"
echo "2) SSH (需要配置 SSH 密钥)"
echo "3) 仅本地保存（不推送）"
echo ""
read -p "请选择 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "切换到 HTTPS 方式..."
        git remote set-url origin https://github.com/taobaoaz/paper-formatter.git
        echo "✅ 已切换"
        ;;
    2)
        echo ""
        echo "切换到 SSH 方式..."
        git remote set-url origin git@github.com:taobaoaz/paper-formatter.git
        echo "✅ 已切换"
        ;;
    3)
        echo ""
        echo "跳过推送，仅本地保存"
        echo "✅ 完成"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

# 推送
echo ""
echo "[5/5] 推送到 GitHub..."
echo "正在推送提交和标签..."
echo ""

if git push origin main --tags; then
    echo ""
    echo "========================================"
    echo "  ✅ 推送成功！"
    echo "========================================"
    echo ""
    echo "查看仓库："
    echo "https://github.com/taobaoaz/paper-formatter"
    echo ""
    echo "创建 Release："
    echo "https://github.com/taobaoaz/paper-formatter/releases/new"
    echo ""
    echo "标签：v2.0.0"
    echo ""
else
    echo ""
    echo "========================================"
    echo "  ❌ 推送失败"
    echo "========================================"
    echo ""
    echo "可能的原因："
    echo "1. 网络连接问题"
    echo "2. 认证信息错误"
    echo "3. SSH 密钥未配置"
    echo ""
    echo "请查看 推送指南.md 获取帮助"
    echo ""
    exit 1
fi
