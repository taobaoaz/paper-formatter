# 🔐 配置 GitHub 认证推送

**快速完成认证并推送到 GitHub**

---

## 📋 当前状态

```
✅ 代码已提交（6 个 commits）
✅ 版本标签已创建（v2.0.0）
✅ 远程仓库已配置
⏳ 需要认证才能推送
```

---

## 🚀 快速推送方案

### 方案 1：使用 GitHub Token（推荐，5 分钟完成）

#### 步骤 1：创建 Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写信息：
   - **Note:** `paper-formatter-push`
   - **Expiration:** `No expiration`（或选择 90 天）
4. 选择权限：
   - ✅ `repo` (Full control of private repositories)
5. 点击 "Generate token"
6. **复制生成的 token**（只显示一次！）

#### 步骤 2：使用 Token 推送

```bash
cd /home/admin/openclaw/workspace/paper-formatter

# 设置凭证（替换 YOUR_TOKEN 为实际 token）
git remote set-url origin https://taobaoaz:YOUR_TOKEN@github.com/taobaoaz/paper-formatter.git

# 推送
git push origin main --tags
```

**示例：**
```bash
git remote set-url origin https://taobaoaz:ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/taobaoaz/paper-formatter.git
git push origin main --tags
```

---

### 方案 2：使用 Git Credential Manager（Windows）

#### Windows 用户

1. 下载并安装：https://github.com/GitCredentialManager/git-credential-manager/releases
2. 运行推送命令：
   ```bash
   cd /home/admin/openclaw/workspace/paper-formatter
   git push origin main --tags
   ```
3. 浏览器会自动打开 GitHub 登录页面
4. 登录后授权
5. 推送自动完成

---

### 方案 3：使用 SSH 密钥（永久有效）

#### 步骤 1：生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "taobaoaz@qq.com"
```

按 3 次回车接受默认设置。

#### 步骤 2：查看公钥

```bash
cat ~/.ssh/id_ed25519.pub
```

复制输出内容（以 `ssh-ed25519` 开头）。

#### 步骤 3：添加到 GitHub

1. 访问：https://github.com/settings/keys
2. 点击 "New SSH key"
3. 填写：
   - **Title:** `paper-formatter-server`
   - **Key:** 粘贴公钥内容
4. 点击 "Add SSH key"

#### 步骤 4：切换为 SSH 并推送

```bash
cd /home/admin/openclaw/workspace/paper-formatter

# 切换为 SSH
git remote set-url origin git@github.com:taobaoaz/paper-formatter.git

# 测试连接
ssh -T git@github.com

# 推送
git push origin main --tags
```

---

## 🎯 一键推送脚本（使用 Token）

创建 `push_with_token.sh`：

```bash
#!/bin/bash

echo "🔐 请输入你的 GitHub Personal Access Token:"
read -s token

echo ""
echo "正在配置..."
cd /home/admin/openclaw/workspace/paper-formatter

# 设置带 Token 的远程地址
git remote set-url origin https://taobaoaz:${token}@github.com/taobaoaz/paper-formatter.git

echo "正在推送..."
git push origin main --tags

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo "查看：https://github.com/taobaoaz/paper-formatter"
else
    echo ""
    echo "❌ 推送失败，请检查 Token 是否正确"
fi
```

使用：
```bash
chmod +x push_with_token.sh
./push_with_token.sh
```

---

## 📊 推送内容

```
提交内容:
✅ 6 个 commits
✅ 版本标签 v2.0.0
✅ 13 个新文件
✅ ~6,000 行新增代码
✅ ~22,000 字文档
```

---

## ✅ 推送后验证

### 1. 查看仓库

访问：https://github.com/taobaoaz/paper-formatter

检查：
- [ ] 最新提交显示在顶部
- [ ] 文件列表包含所有新文件
- [ ] 提交历史完整

### 2. 查看 Tags

访问：https://github.com/taobaoaz/paper-formatter/tags

检查：
- [ ] v2.0.0 标签存在

### 3. 创建 Release

访问：https://github.com/taobaoaz/paper-formatter/releases/new

- 选择标签：v2.0.0
- 标题：`论文排版优化器 v2.0.0`
- 内容：参考 `RELEASE_NOTES.md`
- 点击 "Publish release"

---

## 🐛 故障排除

### 问题 1: "Authentication failed"

**原因：** Token 错误或过期

**解决：**
1. 重新生成 Token
2. 确保复制完整
3. 重新推送

### 问题 2: "Permission denied"

**原因：** Token 权限不足

**解决：**
1. 删除旧 Token
2. 重新生成，确保选择 `repo` 权限
3. 重新推送

### 问题 3: "Could not resolve hostname"

**原因：** 网络连接问题

**解决：**
```bash
# 检查网络
ping github.com

# 检查 DNS
nslookup github.com

# 重试推送
git push origin main --tags
```

---

## 📞 需要帮助？

### GitHub 文档

- 创建 Token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- SSH 连接：https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### 联系方式

- **仓库：** https://github.com/taobaoaz/paper-formatter
- **邮箱：** taobaoaz@qq.com

---

## 🎊 快速开始

**最简单的方式（使用 Token）：**

```bash
# 1. 创建 Token（5 分钟）
# 访问 https://github.com/settings/tokens

# 2. 运行推送脚本
cd /home/admin/openclaw/workspace/paper-formatter
./push_with_token.sh

# 3. 输入 Token
# 粘贴刚才创建的 Token

# 4. 完成！
```

---

**准备好推送了！** 🚀

选择一种方式开始推送吧！

---

**开发小助手 · 严谨专业版**  
**© 2024 All Rights Reserved**
