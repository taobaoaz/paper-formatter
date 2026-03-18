#!/bin/bash

# 论文排版优化器 - 使用 Token 一键推送
# 使用方法：./push_with_token.sh

echo "========================================"
echo "  🔐 论文排版优化器 v2.0 - 推送到 GitHub"
echo "========================================"
echo ""

echo "📝 请输入你的 GitHub Personal Access Token:"
echo "   获取地址：https://github.com/settings/tokens"
echo "   权限：repo (Full control of private repositories)"
echo ""
read -s token

if [ -z "$token" ]; then
    echo ""
    echo "❌ Token 不能为空"
    exit 1
fi

echo ""
echo ""
echo "正在配置远程仓库..."
cd /home/admin/openclaw/workspace/paper-formatter

# 保存原始 URL（用于恢复）
original_url=$(git remote get-url origin)

# 设置带 Token 的远程地址
git remote set-url origin https://taobaoaz:${token}@github.com/taobaoaz/paper-formatter.git

echo "✅ 配置完成"
echo ""
echo "正在推送到 GitHub..."
echo ""

# 执行推送
if git push origin main --tags; then
    echo ""
    echo "========================================"
    echo "  ✅ 推送成功！"
    echo "========================================"
    echo ""
    echo "📦 推送内容:"
    echo "   - 6 个 commits"
    echo "   - 版本标签 v2.0.0"
    echo "   - 13 个新文件"
    echo "   - ~6,000 行代码"
    echo ""
    echo "🌐 查看仓库:"
    echo "   https://github.com/taobaoaz/paper-formatter"
    echo ""
    echo "📝 创建 Release:"
    echo "   https://github.com/taobaoaz/paper-formatter/releases/new"
    echo ""
else
    echo ""
    echo "========================================"
    echo "  ❌ 推送失败"
    echo "========================================"
    echo ""
    echo "可能的原因:"
    echo "1. Token 错误或已过期"
    echo "2. Token 权限不足（需要 repo 权限）"
    echo "3. 网络连接问题"
    echo ""
    echo "解决方法:"
    echo "1. 访问 https://github.com/settings/tokens"
    echo "2. 删除旧 Token，重新生成"
    echo "3. 确保选择 'repo' 权限"
    echo "4. 重新运行此脚本"
    echo ""
    
    # 恢复原始 URL
    git remote set-url origin "$original_url"
    exit 1
fi

# 恢复原始 URL（移除 Token）
git remote set-url origin "$original_url"

echo "✅ 远程仓库 URL 已恢复（已移除 Token）"
echo ""
