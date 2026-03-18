# 🎉 论文排版优化器 v2.0 - 完全合并版

**所有功能已完全合并！**

---

## 🚀 启动方式

### 推荐方式

```bash
python3 main.py
```

**说明：** main.py 已包含所有功能，包括：
- ✅ 完整的旧版功能
- ✅ 现代化封面配置
- ✅ 模板页面选择器
- ✅ 所有对话框和页面

### 其他启动方式

```bash
# 使用 launcher（指向 main.py）
python3 launcher.py

# Windows
启动.bat

# Linux/Mac
./启动.sh
```

---

## 📦 功能清单

### 核心功能

- ✅ **文档格式化** - 一键完成论文排版
- ✅ **封面和声明页配置** - 可视化配置
- ✅ **模板页面选择** - 上传 Word 模板选择页面
- ✅ **AI 识别** - 自动识别格式要求
- ✅ **模板管理** - 创建、编辑、导入导出
- ✅ **参考文献格式化** - GB/T、APA、MLA、IEEE
- ✅ **章节格式化** - 单独格式化章节
- ✅ **快速生成** - 填写式论文生成

### 对话框

- ✅ TemplateEditDialog - 模板编辑
- ✅ AIDataImportDialog - AI 数据导入
- ✅ StructureItemDialog - 结构项编辑
- ✅ SectionFormatDialog - 章节格式设置
- ✅ QuickSpecParseDialog - 快速规格解析
- ✅ SettingsDialog - 系统设置
- ✅ DocumentCreatorDialog - 文档创建
- ✅ StartupDialog - 启动向导
- ✅ CoverDeclarationConfigDialog - 封面配置（新增）
- ✅ TemplatePageSelectorDialog - 页面选择（新增）

---

## 📊 文件说明

| 文件 | 说明 | 状态 |
|------|------|------|
| `main.py` | **主程序（完全版）** | ✅ 推荐 |
| `main_backup.py` | main.py 备份 | 备份 |
| `main_merged.py` | 合并测试版 | 测试 |
| `main_refactored.py` | 重构版（旧） | 归档 |
| `launcher.py` | 启动器 | ✅ 使用 |

---

## 🎯 使用指南

### 1. 封面配置

**位置：** 菜单 → 工具 → 封面和声明页配置

**功能：**
- 可视化配置封面信息
- 上传 Word 模板选择页面
- 支持 4 种声明页类型
- 配置保存/加载

### 2. 文档格式化

**位置：** 首页 → 快速开始

**步骤：**
1. 选择输入文件
2. 选择输出路径
3. 选择模板
4. 配置封面（可选）
5. 开始格式化

### 3. 模板管理

**位置：** 侧边栏 → 模板设置

**功能：**
- 新建模板
- 导入/导出模板
- 编辑模板规则
- AI 识别模板

---

## ✅ 完成状态

- [x] 所有功能合并到 main.py
- [x] 封面配置功能集成
- [x] 模板页面选择器集成
- [x] 启动入口统一
- [x] 文档完善

---

**所有功能已完全合并！使用 `python3 main.py` 启动即可！** 🎊
