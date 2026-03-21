# Paper Formatter 项目结构

本文档详细说明 Paper Formatter 项目的目录结构和代码组织。

## 📁 项目结构概览

```
paper-formatter/
├── .github/                    # GitHub 配置和工作流
├── core/                       # 核心应用程序模块
├── modules/                    # 功能模块
├── docs/                       # 文档网站
├── releases/                   # 发布说明
├── tests/                      # 测试代码
├── templates/                  # 文档模板
├── launcher/                   # 启动器和依赖管理
├── installer/                  # 安装程序资源
├── 文档资料/                   # 中文文档和资料
└── 配置文件                    # 各种配置文件
```

## 📋 详细目录说明

### `.github/` - GitHub 配置
```
.github/
├── workflows/                  # GitHub Actions 工作流
│   ├── build-windows.yml      # Windows EXE 构建
│   ├── build-installer.yml    # 安装程序构建
│   └── test.yml              # 自动化测试
├── ISSUE_TEMPLATE/           # Issue 模板
│   ├── bug_report.md         # Bug 报告模板
│   └── feature_request.md    # 功能请求模板
└── GITHUB_ACTIONS_FIXES.md   # GitHub Actions 问题修复文档
```

### `core/` - 核心模块
```
core/
├── main.py                    # 应用程序主入口
├── main_refactored.py         # 重构版本主入口
├── config.py                  # 配置管理
├── error_handler.py           # 错误处理和日志
└── __init__.py               # 包初始化文件
```

### `modules/` - 功能模块
```
modules/
├── ai_prompt.py              # AI 提示生成
├── ai_recognizer.py          # AI 文档识别
├── auto_backup.py            # 自动备份管理器
├── auto_backup_settings_dialog.py # 备份设置对话框
├── auto_updater.py           # 自动更新器
├── batch_pdf_export_dialog.py # 批量 PDF 导出对话框
├── batch_processor.py        # 批量处理器
├── batch_processor_dialog.py # 批量处理对话框
├── config_snapshot.py        # 配置快照管理
├── config_snapshot_dialog.py # 配置快照对话框
├── cover_declaration_config.py # 封面声明配置
├── document_generator.py     # 文档生成器
├── document_state.py         # 文档状态管理
├── document_state_dialog.py  # 文档状态对话框
├── file_backup.py           # 文件备份
├── file_preview.py          # 文件预览
├── file_preview_dialog.py   # 文件预览对话框
├── font_downloader.py       # 字体下载器
├── font_manager_dialog.py   # 字体管理器对话框
├── format_config.py         # 格式配置
├── format_config_dialog.py  # 格式配置对话框
├── format_processor.py      # 格式处理器
├── history_manager.py       # 历史记录管理
├── image_processor.py       # 图像处理器
├── menu_manager.py          # 菜单管理
├── parsers/                 # 文档解析器
│   ├── docx_parser.py      # DOCX 解析器
│   ├── pdf_parser.py       # PDF 解析器
│   ├── txt_parser.py       # 文本解析器
│   └── __init__.py         # 解析器包
├── pdf_exporter.py          # PDF 导出器
├── reference_manager.py     # 参考文献管理
├── settings_dialog.py       # 设置对话框
├── status_bar.py            # 状态栏
├── template_manager.py      # 模板管理
├── template_manager_dialog.py # 模板管理对话框
├── undo_manager.py          # 撤销管理器
├── utils.py                 # 工具函数
└── version_checker.py       # 版本检查器
```

### `docs/` - 文档网站
```
docs/
├── _config.yml              # Jekyll 配置
├── Gemfile                  # Ruby 依赖
├── index.md                 # 文档首页
├── installation.md         # 安装指南
├── quickstart.md           # 快速开始
├── features.md             # 功能详解
├── faq.md                  # 常见问题
└── .gitkeep                # 保持目录
```

### `releases/` - 发布说明
```
releases/
├── RELEASE_NOTES_v2.1.0.md
├── RELEASE_NOTES_v2.1.1.md
├── RELEASE_NOTES_v2.1.2.md
├── RELEASE_NOTES_v2.1.3.md
├── RELEASE_NOTES_v2.1.4.md
├── RELEASE_NOTES_v2.1.5.md
├── RELEASE_NOTES_v2.1.6.md
├── RELEASE_NOTES_v2.1.7.md
├── RELEASE_NOTES_v2.1.8.md
├── RELEASE_NOTES_v2.1.9.md
├── RELEASE_NOTES_v2.2.0.md
├── RELEASE_NOTES_v2.2.1.md
├── RELEASE_NOTES_v2.2.2.md
├── RELEASE_NOTES_v2.2.3.md
├── RELEASE_NOTES_v2.md
└── .gitkeep
```

### `tests/` - 测试代码
```
tests/
├── test_basic.py           # 基础测试
├── test_modules/          # 模块测试
│   ├── test_auto_backup.py
│   ├── test_config_snapshot.py
│   └── test_document_state.py
├── test_integration/      # 集成测试
│   └── test_workflow.py
└── .gitkeep
```

### `templates/` - 文档模板
```
templates/
├── academic/              # 学术论文模板
├── journal/               # 期刊投稿模板
├── thesis/                # 学位论文模板
├── conference/            # 会议论文模板
└── custom/               # 自定义模板
```

### `launcher/` - 启动器
```
launcher/
├── requirements.txt       # Python 依赖
├── launcher.py           # 启动脚本
└── README.md             # 启动器说明
```

### `installer/` - 安装程序
```
installer/
├── windows/              # Windows 安装程序资源
├── macos/                # macOS 安装程序资源
├── linux/                # Linux 安装程序资源
└── resources/            # 安装程序资源文件
```

### `文档资料/` - 中文文档
```
文档资料/
├── 用户手册.pdf          # 用户手册
├── 开发指南.pdf          # 开发指南
├── API文档.pdf           # API 文档
└── 设计文档.pdf          # 设计文档
```

## 🔧 构建和开发

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/taobaoaz/paper-formatter.git
cd paper-formatter

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 安装依赖
pip install -r launcher/requirements.txt

# 安装开发依赖
pip install pytest pytest-cov black flake8 isort pre-commit

# 安装预提交钩子
pre-commit install
```

### 运行测试
```bash
# 运行所有测试
cd tests
python -m pytest -v

# 运行特定模块测试
python -m pytest test_modules/test_auto_backup.py -v

# 运行测试并生成覆盖率报告
python -m pytest --cov=.. --cov-report=html
```

### 代码质量检查
```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 导入排序
isort .

# 运行所有检查
pre-commit run --all-files
```

### 构建可执行文件
```bash
# 安装 PyInstaller
pip install pyinstaller

# 构建 Windows EXE
pyinstaller --onefile --windowed \
  --name="paper-formatter" \
  --add-data "modules/parsers:parsers" \
  --paths modules \
  --paths core \
  --hidden-import parsers \
  ./core/main.py
```

## 📦 模块依赖关系

### 核心依赖
```
paper-formatter
├── PyQt5 (>=5.15.0)      # GUI 框架
├── python-docx (>=1.0.0) # DOCX 处理
├── PyPDF2 (>=3.0.0)      # PDF 处理
├── requests (>=2.31.0)   # HTTP 请求
├── pillow (>=10.0.0)     # 图像处理
└── openai (>=1.0.0)      # AI 功能
```

### 开发依赖
```
paper-formatter-dev
├── pytest (>=7.0.0)      # 测试框架
├── black (>=23.0.0)      # 代码格式化
├── flake8 (>=6.0.0)      # 代码检查
├── isort (>=5.12.0)      # 导入排序
└── pre-commit (>=3.0.0)  # 预提交钩子
```

## 🚀 发布流程

### 1. 版本管理
```bash
# 更新版本号
# 在 config.py 中更新版本号

# 创建发布分支
git checkout -b release/v2.2.4

# 更新 CHANGELOG.md
# 更新 releases/RELEASE_NOTES_v2.2.4.md
```

### 2. 测试和验证
```bash
# 运行所有测试
python -m pytest tests/ -v

# 代码质量检查
pre-commit run --all-files

# 构建测试
python -m pyinstaller --onefile core/main.py
```

### 3. 创建发布
```bash
# 创建标签
git tag -a v2.2.4 -m "Release v2.2.4"

# 推送标签
git push origin v2.2.4
```

### 4. GitHub Actions 自动构建
- 推送标签时自动触发构建
- 生成 Windows EXE 和安装程序
- 运行自动化测试
- 创建 GitHub Release

## 📚 代码规范

### 命名规范
- **类名**: `CamelCase` (例如: `DocumentState`)
- **函数名**: `snake_case` (例如: `process_document`)
- **变量名**: `snake_case` (例如: `file_path`)
- **常量名**: `UPPER_CASE` (例如: `MAX_RETRIES`)

### 导入顺序
1. 标准库导入
2. 第三方库导入
3. 本地应用导入

### 文档字符串
```python
def process_document(file_path: str, options: dict) -> bool:
    """
    处理文档文件。

    Args:
        file_path (str): 文档文件路径
        options (dict): 处理选项

    Returns:
        bool: 处理是否成功

    Raises:
        FileNotFoundError: 文件不存在时抛出
        ValueError: 文件格式不支持时抛出
    """
    # 函数实现
```

### 错误处理
```python
try:
    result = process_document(file_path, options)
except FileNotFoundError as e:
    logger.error(f"文件不存在: {file_path}")
    raise
except ValueError as e:
    logger.error(f"文件格式不支持: {file_path}")
    raise
except Exception as e:
    logger.error(f"处理文档时发生错误: {e}")
    raise
```

## 🔍 调试和日志

### 日志配置
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('paper_formatter.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 调试模式
```bash
# 启用调试模式
python core/main.py --debug

# 启用详细日志
python core/main.py --verbose

# 启用性能分析
python -m cProfile core/main.py
```

## 🤝 贡献指南

### 开发流程
1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码审查
- 确保代码符合规范
- 添加适当的测试
- 更新文档
- 通过所有 CI 检查

### 提交信息规范
```
类型(范围): 简要描述

详细描述（可选）

关闭 #issue编号
```

**类型**: feat, fix, docs, style, refactor, test, chore
**范围**: 模块名或功能区域

---

**最后更新**: 2026-03-21  
**版本**: v2.2.3