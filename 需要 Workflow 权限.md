# ⚠️ 需要 Workflow 权限

**问题：** Token 缺少 `workflow` 权限，无法推送 GitHub Actions 工作流文件

---

## 🔍 问题分析

推送被拒绝：
```
refusing to allow a Personal Access Token to create or update workflow 
`.github/workflows/release.yml` without `workflow` scope
```

**原因：** GitHub 要求推送 Actions 工作流文件需要额外的 `workflow` 权限。

---

## ✅ 解决方案

### 方案 1：为现有 Token 添加 workflow 权限（推荐）

#### 步骤 1：编辑 Token 权限

1. 访问：https://github.com/settings/tokens
2. 找到你的 Token（ghp_3INDec...）
3. 点击 "Edit"

#### 步骤 2：添加 workflow 权限

在 Scopes 中勾选：
- ✅ `repo` (Full control of private repositories)
- ✅ `workflow` (Update GitHub Action workflows)

#### 步骤 3：保存并推送

```bash
cd /home/admin/openclaw/workspace/paper-formatter
git push origin main --tags
```

---

### 方案 2：临时移除工作流文件推送

如果不想添加 workflow 权限：

#### 步骤 1：临时移动工作流文件

```bash
cd /home/admin/openclaw/workspace/paper-formatter
mv .github/workflows/release.yml /tmp/
git add -A
git commit -m "temp: remove workflow for push"
```

#### 步骤 2：推送

```bash
git push origin main --tags
```

#### 步骤 3：恢复工作流文件

```bash
mv /tmp/release.yml .github/workflows/
git add -A
git commit -m "chore: restore workflow"
git push origin main
```

---

### 方案 3：创建新 Token 带完整权限

#### 步骤 1：创建新 Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 配置：
   - Note: `paper-formatter-full`
   - Expiration: `No expiration`
   - Scopes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)

#### 步骤 2：使用新 Token 推送

```bash
cd /home/admin/openclaw/workspace/paper-formatter

# 替换为新 token
git remote set-url origin https://ghp_NEW_TOKEN@github.com/taobaoaz/paper-formatter.git

# 推送
git push origin main --tags
```

---

## 🎯 快速方案

**最简单：** 为现有 Token 添加 workflow 权限

1. 访问：https://github.com/settings/tokens
2. 编辑现有 Token
3. 勾选 ✅ `workflow`
4. 保存
5. 重新推送

---

## 📊 当前状态

```
✅ 代码已提交（8 commits）
✅ 版本标签已创建（v2.0.0）
✅ Token 基本权限正常
⏳ 需要添加 workflow 权限
```

---

**请为 Token 添加 workflow 权限后重新推送！** 🚀

---

**开发小助手 · 严谨专业版**  
**© 2024 All Rights Reserved**
