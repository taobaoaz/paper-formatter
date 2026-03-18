# ⚠️ Token 权限问题解决方案

**问题：** 当前 Token 权限不足，推送被拒绝（403）

---

## 🔍 问题分析

你提供的 Token 是 **Fine-grained Personal Access Token**：
- 前缀：`github_pat_...`
- 特点：权限范围有限
- 限制：可能无法推送到某些仓库

---

## ✅ 解决方案

### 方案 1：创建经典 Token（推荐）

#### 步骤 1：访问经典 Token 页面

https://github.com/settings/tokens

**注意：** 不是 Fine-grained tokens 页面

#### 步骤 2：生成经典 Token

1. 点击 **"Generate new token"** (不是 "Generate new token (classic)")
2. 如果看到两个选项，选择 **"Generate new token (classic)"**

#### 步骤 3：配置 Token

- **Note:** `paper-formatter-push`
- **Expiration:** `No expiration`
- **Scopes:** 勾选 ✅ `repo` (Full control of private repositories)

#### 步骤 4：生成并复制

1. 点击 "Generate token"
2. **复制 token**（以 `ghp_` 开头）
3. 保存到一个安全的地方

#### 步骤 5：使用新 Token 推送

```bash
cd /home/admin/openclaw/workspace/paper-formatter

# 使用新 token（替换 ghp_xxxxxxxxxxxx）
git remote set-url origin https://ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/taobaoaz/paper-formatter.git

# 推送
git push origin main --tags
```

---

### 方案 2：为 Fine-grained Token 添加权限

如果你坚持使用当前的 Fine-grained token：

#### 步骤 1：配置 Token 权限

1. 访问：https://github.com/settings/personal-access-tokens
2. 找到你的 token
3. 点击 "Edit"
4. 添加权限：
   - **Repository access:** 选择 `taobaoaz/paper-formatter`
   - **Permissions:**
     - Contents: Read and write
     - Metadata: Read-only

#### 步骤 2：保存并推送

```bash
cd /home/admin/openclaw/workspace/paper-formatter
git push origin main --tags
```

---

### 方案 3：使用 SSH 密钥（永久有效）

#### 步骤 1：生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "taobaoaz@qq.com"
```

按 3 次回车。

#### 步骤 2：查看公钥

```bash
cat ~/.ssh/id_ed25519.pub
```

复制输出内容。

#### 步骤 3：添加到 GitHub

1. 访问：https://github.com/settings/keys
2. 点击 "New SSH key"
3. Title: `paper-formatter`
4. Key: 粘贴公钥
5. 点击 "Add SSH key"

#### 步骤 4：切换为 SSH 并推送

```bash
cd /home/admin/openclaw/workspace/paper-formatter

# 切换为 SSH
git remote set-url origin git@github.com:taobaoaz/paper-formatter.git

# 推送
git push origin main --tags
```

---

## 🎯 快速推送脚本

创建 `quick_push.sh`：

```bash
#!/bin/bash

echo "🔐 请输入你的 GitHub Token (以 ghp_ 开头的经典 Token):"
read -s token

echo ""
cd /home/admin/openclaw/workspace/paper-formatter

# 配置远程 URL
git remote set-url origin https://${token}@github.com/taobaoaz/paper-formatter.git

echo "正在推送..."
git push origin main --tags

if [ $? -eq 0 ]; then
    echo "✅ 推送成功！"
else
    echo "❌ 推送失败"
    echo "请确保使用经典 Token (ghp_ 开头)"
fi
```

使用：
```bash
chmod +x quick_push.sh
./quick_push.sh
```

---

## 📊 Token 类型对比

| 类型 | 前缀 | 权限 | 推荐 |
|------|------|------|------|
| **经典 Token** | `ghp_` | 完整仓库权限 | ✅ 推荐 |
| **Fine-grained** | `github_pat_` | 有限权限 | ⚠️ 需配置 |
| **OAuth** | `gho_` | OAuth 应用 | ❌ 不推荐 |

---

## ✅ 推荐方案

**最简单：** 创建经典 Token（ghp_开头）

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择 `repo` 权限
4. 复制 token
5. 运行推送

**最安全：** 使用 SSH 密钥

1. 生成 SSH 密钥
2. 添加到 GitHub
3. 切换为 SSH 推送
4. 永久有效

---

## 📞 需要帮助？

### GitHub 文档

- 经典 Token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic
- SSH 密钥：https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### 检查当前状态

```bash
cd /home/admin/openclaw/workspace/paper-formatter

# 查看远程仓库
git remote -v

# 查看提交
git log --oneline -5

# 查看标签
git tag -l
```

---

**请使用经典 Token（ghp_开头）重新推送！** 🚀

---

**开发小助手 · 严谨专业版**  
**© 2024 All Rights Reserved**
