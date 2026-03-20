#!/bin/bash
# GitHub Release 自动创建脚本
# 使用方法：
# 1. 先运行 gh auth login 登录
# 2. 运行此脚本：bash create-releases.sh

set -e

echo "🚀 开始创建 GitHub Releases..."
echo ""

# 检查是否已登录
if ! gh auth status > /dev/null 2>&1; then
    echo "❌ 未登录 GitHub"
    echo "请先运行：gh auth login"
    exit 1
fi

echo "✅ GitHub 登录成功"
echo ""

# 创建 Release 列表
releases=(
    "v2.1.8:v2.1.8 - 自动备份和智能清理:RELEASE_NOTES_v2.1.8.md"
    "v2.1.9:v2.1.9 - 自动备份 GUI 和重要性标记:RELEASE_NOTES_v2.1.9.md"
    "v2.2.0:v2.2.0 - PDF 导出和帮助系统:RELEASE_NOTES_v2.2.0.md"
    "v2.2.1:v2.2.1 - 批量 PDF 导出和中文字体:RELEASE_NOTES_v2.2.1.md"
    "v2.2.2:v2.2.2 - 字体搜索下载和管理:RELEASE_NOTES_v2.2.2.md"
)

# 遍历创建
for release in "${releases[@]}"; do
    IFS=':' read -r tag title notes_file <<< "$release"
    
    echo "📦 创建 Release: $tag"
    echo "   标题：$title"
    echo "   说明：$notes_file"
    
    # 检查 tag 是否存在
    if ! git rev-parse "$tag" >/dev/null 2>&1; then
        echo "   ⚠️  Tag $tag 不存在，跳过"
        continue
    fi
    
    # 检查 Release 是否已存在
    if gh release view "$tag" > /dev/null 2>&1; then
        echo "   ⚠️  Release 已存在，跳过"
        continue
    fi
    
    # 创建 Release
    if [ "$tag" == "v2.2.2" ]; then
        # 最新版
        gh release create "$tag" --title "$title" --notes-file "$notes_file"
    else
        gh release create "$tag" --title "$title" --notes-file "$notes_file"
    fi
    
    echo "   ✅ 创建成功"
    echo ""
done

echo "🎉 所有 Release 创建完成！"
echo ""
echo "查看 Releases: https://github.com/taobaoaz/paper-formatter/releases"
