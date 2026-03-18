# 📦 v2.0.0 发布说明

**版本：** v2.0.0  
**发布日期：** 2026-03-19

---

## ✨ 新功能

### 🔄 在线更新
- 自动检查 GitHub Release
- GUI 更新提示对话框
- 一键下载安装包

### 📦 安装包支持
- Inno Setup 安装脚本
- 一键安装向导
- 自动创建快捷方式

### 🎨 UI 优化
- 工具菜单新增"检查更新"
- Ctrl+U 快捷键
- 启动时自动检查更新

---

## 📥 下载安装

### Windows 用户

**手动下载：**

由于 GitHub Actions 打包问题，请手动下载：

1. 访问 Releases 页面
2. 下载 `论文排版优化器.exe`
3. 双击运行

**或使用安装包：**

1. 安装 Inno Setup
2. 运行 `iscc installer/installer.iss`
3. 运行生成的安装包

---

## 🔧 技术细节

### 本地打包成功

**文件大小：** 60MB  
**位置：** `dist/论文排版优化器`

**打包命令：**
```bash
pyinstaller --onefile --windowed --name="论文排版优化器" \
  --add-data="功能模块/parsers:parsers" \
  --add-data="功能模块/rules:rules" \
  --paths=功能模块 \
  --paths=核心模块 \
  --hidden-import=parsers \
  --hidden-import=rules \
  核心模块/main.py
```

### GitHub Actions 问题

**问题：** 连续失败 8+ 次  
**原因：** 工作流配置问题  
**解决：** 手动上传本地打包文件

---

## 📊 统计

- **代码行数：** ~9000 行
- **功能模块：** 15+ 个
- **对话框：** 10 个
- **支持系统：** Windows 7/8/10/11, Linux, macOS

---

## 🐛 已知问题

1. GitHub Actions 自动打包失败
2. 需要手动上传安装包

---

## 📞 反馈

**GitHub Issues:**
```
https://github.com/taobaoaz/paper-formatter/issues
```

---

**开发小助手 · 严谨专业版**  
**© 2024 All Rights Reserved**
