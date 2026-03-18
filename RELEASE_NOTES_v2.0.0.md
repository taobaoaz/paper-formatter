# 🎉 论文排版优化器 v2.0.0

**发布日期：** 2026-03-19

---

## ✨ 新功能

### 📦 安装包功能

- ✅ 专业 Inno Setup 安装向导
- ✅ 一键安装，无需配置
- ✅ 自动创建桌面快捷方式
- ✅ 开始菜单集成
- ✅ 完整卸载功能

### 🔄 在线更新

- ✅ 自动检查 GitHub Release
- ✅ 智能版本号比较
- ✅ GUI 更新提示对话框
- ✅ 自动下载更新包
- ✅ 启动时自动检查更新

### 🤖 自动化打包

- ✅ GitHub Actions 自动打包
- ✅ 推送标签自动创建 Release
- ✅ 自动上传安装包

---

## 🔧 改进

### UI 优化

- ✅ 工具菜单添加"检查更新"
- ✅ Ctrl+U 快捷键
- ✅ 托盘通知提示

### 项目结构

- ✅ 简化文件夹结构
- ✅ 启动文件单独放置
- ✅ 功能模块分类清晰

---

## 📝 使用说明

### 安装包制作

**手动制作：**
```bash
# 安装 Inno Setup
https://jrsoftware.org/isdl.php

# 编译安装包
iscc installer/installer.iss
```

**自动打包：**
```bash
# 推送标签
git tag v2.0.0
git push origin v2.0.0

# GitHub Actions 自动打包
```

### 检查更新

**GUI 方式：**
- 工具 → 检查更新
- 或按 Ctrl+U

**命令行：**
```bash
cd 功能模块
python auto_updater.py
```

---

## 📊 统计

- **代码行数：** ~9000 行
- **功能模块：** 15+ 个
- **对话框：** 10 个
- **支持系统：** Windows 7/8/10/11, Linux, macOS

---

## 🎯 下一步

- [ ] 收集用户反馈
- [ ] 修复发现的问题
- [ ] 持续优化性能

---

## 📞 反馈

**GitHub Issues:**
```
https://github.com/taobaoaz/paper-formatter/issues
```

**仓库地址:**
```
https://github.com/taobaoaz/paper-formatter
```

---

**开发小助手 · 严谨专业版**  
**© 2024 All Rights Reserved**
