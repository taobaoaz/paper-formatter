# 📚 论文排版优化工具

**一款专业的学术论文排版软件 | Powered by AI**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ 特性亮点

- 🎯 **智能格式化** - 一键自动调整论文格式
- 🤖 **AI 识别** - 自动识别论文结构和格式要求
- 📋 **模板管理** - 支持期刊、学位论文等多种模板
- 📘 **封面配置** - 可视化配置封面和声明页
- 📚 **参考文献** - 支持 GB/T 7714、APA、MLA、IEEE 等格式
- 🚀 **批量处理** - 一次处理多个文档
- 🎨 **美观界面** - 基于 PyQt5 + Fluent Widgets 的现代化 UI

---

## 🚀 快速开始

### 方法 1：一键启动（推荐）

```bash
# Windows 用户直接双击
启动程序.bat
```

### 方法 2：手动运行

```bash
# 1. 安装 Python 3.8+
# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python main.py
```

---

## 📦 功能模块

| 模块 | 功能 | 说明 |
|------|------|------|
| **文档格式化** | ✅ | 自动调整字体、字号、行距、段落等 |
| **模板管理** | ✅ | 支持中文期刊、国际期刊、学位论文 |
| **AI 识别** | ✅ | 自动识别论文结构和格式要求 |
| **参考文献** | ✅ | 支持多种引用格式 |
| **批量处理** | ✅ | 一次处理多个文档 |
| **错误处理** | ✅ | 完善的错误检测和提示 |

---

## 📋 系统要求

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 10/11 (64 位) |
| **Python** | 3.8 或更高版本 |
| **内存** | 至少 4GB RAM |
| **硬盘** | 至少 500MB 可用空间 |

---

## 📖 文档

| 文档 | 说明 |
|------|------|
| [用户使用手册](用户使用手册.md) | 完整的使用教程 |
| [常见问题解答](常见问题解答.md) | FAQ 和故障排除 |
| [封面声明页配置指南](封面声明页配置指南.md) | 封面和声明页配置教程 |
| [错误码说明](错误码说明.txt) | 错误代码解释 |

---

## 🎯 使用场景

### 场景 1：本科毕业论文

```
1. 选择模板：学位论文 → 本科毕业论文
2. 导入文档：选择你的论文
3. 应用模板：一键格式化
4. 保存结果：导出格式化后的文档
```

### 场景 2：期刊投稿

```
1. 选择模板：中文期刊/国际期刊
2. 导入文档：选择投稿论文
3. AI 识别：自动识别结构
4. 格式化：应用期刊格式
5. 参考文献：格式化引用
```

### 场景 3：批量处理

```
1. 工具 → 批量处理
2. 选择文件夹：包含所有论文
3. 选择输出目录
4. 开始处理：自动批量格式化
```

---

## 🛠️ 开发相关

### 项目结构

```
paper-formatter/
├── main.py                    # 主程序入口
├── launcher.py                # 启动器
├── formatter.py               # 格式化核心
├── template_manager.py        # 模板管理
├── ai_recognizer.py           # AI 识别
├── reference_formatter.py     # 参考文献格式化
├── document_generator.py      # 文档生成
├── config.py                  # 配置管理
├── error_handler.py           # 错误处理
├── parsers/                   # 文档解析器
├── templates/                 # 模板文件
├── requirements.txt           # 依赖列表
└── 启动程序.bat               # Windows 启动脚本
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 主要依赖

- **PyQt5** - GUI 框架
- **python-docx** - Word 文档处理
- **openpyxl** - Excel 支持
- **Pillow** - 图像处理
- **pyyaml** - YAML 配置解析

---

## 📸 界面预览

### 主界面
```
┌─────────────────────────────────────────┐
│  📚 论文排版优化工具                    │
├─────────────────────────────────────────┤
│                                         │
│  [📁 导入文档]  [💾 保存]  [🖨️ 打印]   │
│                                         │
│  模板选择：[学位论文 ▼]                │
│  子类型：  [本科毕业论文 ▼]            │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │                                 │   │
│  │      文档预览区域               │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [✨ 开始格式化]  [🤖 AI 识别]         │
│                                         │
│  进度：████████████░░░░ 80%            │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🤝 贡献指南

### 提交 Bug

1. 查看是否已有相同 Issue
2. 创建新 Issue，描述问题
3. 提供复现步骤和错误日志

### 提交功能

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

感谢所有贡献者和用户！

---

## 📞 联系方式

- **项目主页**: https://github.com/taobaoaz/paper-formatter
- **Issues**: https://github.com/taobaoaz/paper-formatter/issues
- **邮箱**: [你的邮箱]

---

**Made with ❤️ for researchers and students**

**祝您的论文顺利接受！🎓**
