# GitHub Release 创建指南

由于 GitHub CLI 未安装，请手动在 GitHub Web 界面创建 Release。

## 创建步骤

1. 访问：https://github.com/taobaoaz/paper-formatter/releases
2. 点击 "Draft a new release"
3. 选择对应的 tag
4. 输入 Release title
5. 粘贴下方的 Release notes
6. 点击 "Publish release"

---

## v2.2.2 (最新)

**Tag:** v2.2.2  
**Title:** v2.2.2 - 字体搜索下载和管理

**Release Notes:**
```markdown
## 🎉 新功能

### 🔤 字体包搜索下载
- ✅ 在线字体库搜索（支持中文字体）
- ✅ 字体包下载（多线程）
- ✅ 自动安装字体（Windows/macOS/Linux）
- ✅ 实时下载进度显示

### 📦 字体管理器
- ✅ 已安装字体列表
- ✅ 字体导入/导出
- ✅ 字体卸载
- ✅ API 密钥管理

### 📖 使用方式
- 菜单：帮助 → 🔤 字体管理
- 快捷键：Ctrl+Alt+F

## 📦 安装
下载 `paper-formatter-windows.exe` 或 `paper-formatter-installer.exe`

## 🐛 已知问题
- Google Fonts API 需要手动获取密钥
- 字体预览功能将在未来版本实现

## 📚 完整文档
查看项目中的 `RELEASE_NOTES_v2.2.2.md` 获取详细信息。
```

---

## v2.2.1

**Tag:** v2.2.1  
**Title:** v2.2.1 - 批量 PDF 导出和中文字体

**Release Notes:**
```markdown
## 🎉 新功能

### 📦 批量 PDF 导出
- ✅ 批量选择多个 Word 文档
- ✅ 一键导出所有文档为 PDF
- ✅ 实时进度条显示
- ✅ 导出结果统计
- ✅ 快捷键：Ctrl+Shift+P

### 🀄 中文字体支持
- ✅ SimSun（宋体）
- ✅ SimHei（黑体）
- ✅ KaiTi（楷体）
- ✅ 自动注册

## 📦 安装
下载 `paper-formatter-windows.exe` 或 `paper-formatter-installer.exe`

## 📚 完整文档
查看项目中的 `RELEASE_NOTES_v2.2.1.md` 获取详细信息。
```

---

## v2.2.0

**Tag:** v2.2.0  
**Title:** v2.2.0 - PDF 导出和帮助系统

**Release Notes:**
```markdown
## 🎉 新功能

### 📄 PDF 导出
- ✅ Word 文档导出为 PDF
- ✅ 多种页面大小（A4/A3/B5/Letter/Legal）
- ✅ 导出质量选择（标准/高质量/最小）
- ✅ 压缩选项
- ✅ 嵌入字体选项
- ✅ 快捷键：Ctrl+Alt+P

### 📖 帮助系统
- ✅ 目录树导航
- ✅ HTML 内容显示
- ✅ 快速入门指南
- ✅ 快捷键列表
- ✅ 关于对话框

## 📦 安装
下载 `paper-formatter-windows.exe` 或 `paper-formatter-installer.exe`

## 📚 完整文档
查看项目中的 `RELEASE_NOTES_v2.2.0.md` 获取详细信息。
```

---

## v2.1.9

**Tag:** v2.1.9  
**Title:** v2.1.9 - 自动备份 GUI 和重要性标记

**Release Notes:**
```markdown
## 🎉 新功能

### ⚙️ 自动备份 GUI 设置
- ✅ 启用/禁用开关
- ✅ 备份间隔选择（5-60 分钟）
- ✅ 清理策略设置
- ✅ 重要快照保护
- ✅ 快捷键：Ctrl+Alt+B

### 🔄 主程序集成
- ✅ PyQt 定时器（每分钟检查）
- ✅ 后台自动备份
- ✅ 状态栏实时显示

### ⭐ 快照重要性标记 UI
- ✅ 标记为重要按钮
- ✅ 取消重要标记按钮
- ✅ 只看重要筛选
- ✅ 重要快照黄色高亮

## 📦 安装
下载 `paper-formatter-windows.exe` 或 `paper-formatter-installer.exe`

## 📚 完整文档
查看项目中的 `RELEASE_NOTES_v2.1.9.md` 获取详细信息。
```

---

## v2.1.8

**Tag:** v2.1.8  
**Title:** v2.1.8 - 自动备份和智能清理

**Release Notes:**
```markdown
## 🎉 新功能

### 🤖 自动备份管理器
- ✅ 可配置备份间隔（默认 10 分钟）
- ✅ 后台自动备份
- ✅ 备份状态追踪
- ✅ 持久化备份历史

### 🧹 智能清理策略
- ✅ 保留重要快照
- ✅ 保留最近 N 个（默认 20）
- ✅ 保留 N 小时内（默认 24 小时）
- ✅ 智能合并规则

### 📌 快照重要性标记
- ✅ 标记快照为"重要"
- ✅ 设置标记原因
- ✅ 记录标记时间
- ✅ 取消重要标记

## 📦 安装
下载 `paper-formatter-windows.exe` 或 `paper-formatter-installer.exe`

## 📚 完整文档
查看项目中的 `RELEASE_NOTES_v2.1.8.md` 获取详细信息。
```

---

## 快速创建所有 Release

按以下顺序创建：
1. v2.1.8
2. v2.1.9
3. v2.2.0
4. v2.2.1
5. v2.2.2（最新版）

每个 Release 都设置为：
- ✅ Set as the latest release（仅 v2.2.2）
- ✅ Create a discussion for this release（可选）
