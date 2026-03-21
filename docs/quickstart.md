---
layout: default
title: 快速开始
parent: 用户指南
nav_order: 3
---

# 快速开始指南

本文档将帮助你在 5 分钟内快速上手 Paper Formatter。

## 🎯 第一步：安装

### Windows 用户
1. 访问 [GitHub Releases](https://github.com/taobaoaz/paper-formatter/releases)
2. 下载 `paper-formatter-vX.X.X-setup.exe`
3. 双击安装程序并按照提示完成安装
4. 从开始菜单启动 Paper Formatter

### macOS 用户
1. 访问 [GitHub Releases](https://github.com/taobaoaz/paper-formatter/releases)
2. 下载 `paper-formatter-vX.X.X.dmg`
3. 打开 DMG 文件并将应用拖到"应用程序"文件夹
4. 从"应用程序"文件夹启动

### Linux 用户
```bash
# 下载 AppImage（推荐）
wget https://github.com/taobaoaz/paper-formatter/releases/download/v2.2.3/paper-formatter-v2.2.3-x86_64.AppImage
chmod +x paper-formatter-v2.2.3-x86_64.AppImage
./paper-formatter-v2.2.3-x86_64.AppImage
```

## 🚀 第二步：首次运行

### 1. 启动应用
- Windows: 从开始菜单或桌面快捷方式
- macOS: 从"应用程序"文件夹
- Linux: 双击 AppImage 或运行命令

### 2. 初始设置
首次运行时，你会看到：
- **语言选择**：选择中文或英文界面
- **主题选择**：选择亮色或暗色主题
- **默认格式**：设置常用的论文格式
- **备份设置**：配置自动备份选项

### 3. 主界面介绍
```
┌─────────────────────────────────────┐
│  Paper Formatter                    │
├─────────────────────────────────────┤
│  📂 文件菜单                         │
│  📝 编辑菜单                         │
│  ⚙️  设置菜单                         │
│  ❓ 帮助菜单                         │
├─────────────────────────────────────┤
│  [打开文档] [选择格式] [格式化] [保存] │
│  ┌──────────────────────────────┐  │
│  │  文档预览区域                 │  │
│  │                              │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│  📊 状态栏：就绪                    │
└─────────────────────────────────────┘
```

## 📄 第三步：格式化你的第一篇论文

### 示例：格式化学术论文

1. **打开文档**
   - 点击"打开"按钮或使用快捷键 `Ctrl+O`
   - 选择你的 Word 文档（.docx 或 .doc）
   - 支持的文件格式：.docx, .doc, .txt, .md

2. **选择格式模板**
   - 点击"选择格式"按钮
   - 从预设模板中选择：
     - **学术论文**：标准学术格式
     - **期刊投稿**：期刊要求格式
     - **学位论文**：学位论文格式
     - **会议论文**：会议投稿格式
     - **自定义格式**：创建自己的模板

3. **配置格式选项**
   ```
   📋 格式配置
   ├── 页面设置
   │   ├── 纸张大小：A4
   │   ├── 页边距：上 2.5cm，下 2.5cm，左 3cm，右 2.5cm
   │   └── 页眉页脚：启用
   │
   ├── 字体设置
   │   ├── 正文字体：宋体，小四
   │   ├── 标题字体：黑体，三号
   │   └── 英文字体：Times New Roman
   │
   ├── 段落设置
   │   ├── 行距：1.5倍
   │   ├── 首行缩进：2字符
   │   └── 段前段后：0.5行
   │
   └── 其他设置
       ├── 自动编号：启用
       ├── 目录生成：启用
       └── 参考文献：自动格式化
   ```

4. **开始格式化**
   - 点击"格式化"按钮或使用快捷键 `Ctrl+F`
   - 等待处理完成（进度条显示）
   - 处理过程中可以取消

5. **保存结果**
   - 点击"保存"按钮或使用快捷键 `Ctrl+S`
   - 选择保存位置和文件名
   - 建议使用新文件名，如 `论文_格式化后.docx`

## ⚡ 常用快捷键

### 文件操作
- `Ctrl+N` - 新建文档
- `Ctrl+O` - 打开文档
- `Ctrl+S` - 保存文档
- `Ctrl+Shift+S` - 另存为
- `Ctrl+P` - 打印

### 编辑操作
- `Ctrl+Z` - 撤销
- `Ctrl+Y` - 重做
- `Ctrl+F` - 格式化文档
- `Ctrl+B` - 批量处理
- `Ctrl+R` - 刷新预览

### 视图操作
- `Ctrl+1` - 切换到预览模式
- `Ctrl+2` - 切换到编辑模式
- `Ctrl+3` - 切换到对比模式
- `F11` - 全屏切换

## 🔧 高级功能快速使用

### 批量处理多个文档
1. 点击"批量处理"按钮或使用 `Ctrl+B`
2. 选择多个文档
3. 选择输出格式
4. 点击"开始处理"
5. 处理完成后会显示结果报告

### 自动备份管理
- **自动备份**：每次保存时自动创建备份
- **手动备份**：点击"备份"按钮或使用 `Ctrl+Shift+B`
- **恢复备份**：从"文件"→"恢复备份"中选择
- **备份设置**：在设置中配置备份策略

### 文档状态快照
- **创建快照**：`Ctrl+Shift+S` 保存当前状态
- **恢复快照**：从"历史"菜单中选择
- **管理快照**：查看、删除、标记重要快照

## 🎮 交互式教程

### 教程 1：格式化一篇简单的论文
1. 下载示例文档：[示例论文.docx](https://github.com/taobaoaz/paper-formatter/raw/main/examples/sample_paper.docx)
2. 用 Paper Formatter 打开
3. 选择"学术论文"模板
4. 点击"格式化"
5. 保存为 `示例论文_格式化后.docx`

### 教程 2：批量处理多篇文档
1. 准备多个文档到一个文件夹
2. 点击"批量处理"
3. 选择文件夹
4. 选择输出格式
5. 查看处理报告

### 教程 3：自定义格式模板
1. 点击"设置"→"格式模板"
2. 点击"新建模板"
3. 配置各项参数
4. 保存为"我的模板"
5. 应用自定义模板

## ❓ 遇到问题？

### 常见问题快速解决

#### 问题：打开文档失败
**解决方案：**
1. 确保文档不是只读状态
2. 检查文件权限
3. 尝试另存为其他格式再打开

#### 问题：格式化后样式不对
**解决方案：**
1. 检查文档是否包含特殊格式
2. 尝试不同的模板
3. 在设置中调整格式参数

#### 问题：程序崩溃或无响应
**解决方案：**
1. 重启应用
2. 检查日志文件：`%APPDATA%\Paper Formatter\logs\` (Windows) 或 `~/.paper-formatter/logs/` (Linux/macOS)
3. 提交问题到 [GitHub Issues](https://github.com/taobaoaz/paper-formatter/issues)

### 获取更多帮助
- 📖 **完整文档**：[用户指南](https://taobaoaz.github.io/paper-formatter/)
- 🐛 **报告问题**：[GitHub Issues](https://github.com/taobaoaz/paper-formatter/issues)
- 💬 **讨论交流**：[GitHub Discussions](https://github.com/taobaoaz/paper-formatter/discussions)
- 📧 **联系支持**：taobaoaz@users.noreply.github.com

## 🎉 恭喜！

你已经成功完成了 Paper Formatter 的快速入门。现在你可以：

1. ✅ 格式化你的第一篇论文
2. ✅ 使用批量处理功能
3. ✅ 创建自定义模板
4. ✅ 管理文档备份

**下一步建议：**
- 查看 [功能详解](/features) 了解所有功能
- 阅读 [常见问题](/faq) 解决遇到的问题
- 参与 [社区讨论](https://github.com/taobaoaz/paper-formatter/discussions) 分享经验

---

**提示**：Paper Formatter 会自动保存你的设置和偏好。如果你有任何建议或发现问题，请随时反馈！