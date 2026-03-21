---
layout: default
title: API 参考
parent: 开发者文档
nav_order: 2
---

# API 参考

本文档详细说明 Paper Formatter 的 API 接口和模块。

## 📋 核心模块 API

### `core.main` - 主应用程序

#### `MainWindow` 类
主窗口类，负责应用程序的主要界面和功能。

**构造函数**
```python
def __init__(self):
    """
    初始化主窗口。
    """
```

**方法**
```python
def setup_ui(self) -> None:
    """设置用户界面。"""

def setup_connections(self) -> None:
    """设置信号槽连接。"""

def load_settings(self) -> None:
    """加载应用程序设置。"""

def save_settings(self) -> None:
    """保存应用程序设置。"""

def closeEvent(self, event: QCloseEvent) -> None:
    """处理窗口关闭事件。"""
```

### `core.config` - 配置管理

#### `Config` 类
配置管理类，负责加载、保存和管理应用程序配置。

**属性**
```python
config_path: str  # 配置文件路径
settings: dict    # 配置字典
```

**方法**
```python
@classmethod
def get_instance(cls) -> 'Config':
    """获取配置单例实例。"""

def load(self) -> None:
    """从文件加载配置。"""

def save(self) -> None:
    """保存配置到文件。"""

def get(self, key: str, default=None) -> Any:
    """获取配置值。"""

def set(self, key: str, value: Any) -> None:
    """设置配置值。"""

def update(self, updates: dict) -> None:
    """批量更新配置。"""
```

### `core.error_handler` - 错误处理

#### `ErrorHandler` 类
错误处理类，负责捕获、记录和处理应用程序错误。

**方法**
```python
@staticmethod
def setup_global_exception_handler() -> None:
    """设置全局异常处理器。"""

@staticmethod
def log_error(error: Exception, context: str = "") -> None:
    """记录错误到日志文件。"""

@staticmethod
def show_error_dialog(error: Exception, parent=None) -> None:
    """显示错误对话框。"""

@staticmethod
def handle_critical_error(error: Exception) -> None:
    """处理致命错误。"""
```

## 📦 功能模块 API

### `modules.document_state` - 文档状态管理

#### `DocumentState` 类
文档状态管理类，负责保存和恢复文档状态。

**属性**
```python
document_path: str      # 文档路径
state_data: dict        # 状态数据
timestamp: datetime     # 时间戳
importance: int         # 重要性等级 (1-5)
```

**方法**
```python
@classmethod
def from_document(cls, document_path: str) -> 'DocumentState':
    """从文档创建状态。"""

def save(self, file_path: str) -> None:
    """保存状态到文件。"""

@classmethod
def load(cls, file_path: str) -> 'DocumentState':
    """从文件加载状态。"""

def restore(self) -> bool:
    """恢复文档状态。"""

def compare(self, other: 'DocumentState') -> dict:
    """比较两个状态。"""
```

### `modules.config_snapshot` - 配置快照

#### `ConfigSnapshot` 类
配置快照管理类，负责保存和恢复配置快照。

**属性**
```python
config_data: dict       # 配置数据
snapshot_name: str      # 快照名称
description: str        # 描述
created_at: datetime    # 创建时间
```

**方法**
```python
@classmethod
def create(cls, config_data: dict, name: str = None) -> 'ConfigSnapshot':
    """创建配置快照。"""

def save(self, file_path: str) -> None:
    """保存快照到文件。"""

@classmethod
def load(cls, file_path: str) -> 'ConfigSnapshot':
    """从文件加载快照。"""

def apply(self) -> None:
    """应用配置快照。"""

def export(self, format: str = "json") -> str:
    """导出快照为指定格式。"""
```

### `modules.auto_backup` - 自动备份

#### `AutoBackupManager` 类
自动备份管理器，负责管理文档的自动备份。

**属性**
```python
backup_dir: str         # 备份目录
max_backups: int        # 最大备份数量
backup_interval: int    # 备份间隔（分钟）
```

**方法**
```python
def __init__(self, backup_dir: str = None):
    """初始化备份管理器。"""

def setup(self, config: dict) -> None:
    """设置备份配置。"""

def backup_document(self, document_path: str) -> str:
    """备份文档。"""

def get_backups(self, document_path: str) -> List[str]:
    """获取文档的备份列表。"""

def restore_backup(self, backup_path: str, target_path: str) -> bool:
    """从备份恢复文档。"""

def cleanup_old_backups(self) -> None:
    """清理旧备份。"""
```

### `modules.font_downloader` - 字体下载器

#### `FontDownloader` 类
字体下载器，负责从在线字体库下载和安装字体。

**属性**
```python
font_library_url: str   # 字体库 URL
download_dir: str       # 下载目录
installed_fonts: list   # 已安装字体列表
```

**方法**
```python
def search_fonts(self, query: str, language: str = "zh") -> List[dict]:
    """搜索字体。"""

def download_font(self, font_id: str, variants: List[str] = None) -> str:
    """下载字体。"""

def install_font(self, font_path: str) -> bool:
    """安装字体。"""

def get_installed_fonts(self) -> List[str]:
    """获取已安装字体列表。"""

def uninstall_font(self, font_name: str) -> bool:
    """卸载字体。"""
```

## 🔌 插件系统 API

### 插件接口

#### `BasePlugin` 类
所有插件必须继承的基类。

**方法**
```python
class BasePlugin:
    """插件基类。"""
    
    def __init__(self, app):
        """初始化插件。"""
        self.app = app
        self.name = "未命名插件"
        self.version = "1.0.0"
        self.author = "未知作者"
        self.description = "插件描述"
    
    def initialize(self) -> bool:
        """初始化插件。"""
        return True
    
    def cleanup(self) -> None:
        """清理插件资源。"""
    
    def get_menu_items(self) -> List[dict]:
        """获取菜单项。"""
        return []
    
    def get_toolbar_buttons(self) -> List[dict]:
        """获取工具栏按钮。"""
        return []
    
    def get_settings_widget(self) -> QWidget:
        """获取设置窗口部件。"""
        return None
```

### 插件管理器

#### `PluginManager` 类
插件管理器，负责加载、管理和卸载插件。

**方法**
```python
class PluginManager:
    """插件管理器。"""
    
    def __init__(self, plugin_dir: str):
        """初始化插件管理器。"""
    
    def load_plugins(self) -> List[BasePlugin]:
        """加载所有插件。"""
    
    def load_plugin(self, plugin_path: str) -> BasePlugin:
        """加载单个插件。"""
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件。"""
    
    def get_plugin(self, plugin_name: str) -> BasePlugin:
        """获取插件实例。"""
    
    def get_all_plugins(self) -> List[BasePlugin]:
        """获取所有插件。"""
```

## 📄 文档解析器 API

### 解析器接口

#### `BaseParser` 类
文档解析器基类。

**方法**
```python
class BaseParser:
    """文档解析器基类。"""
    
    def __init__(self, file_path: str):
        """初始化解析器。"""
    
    def parse(self) -> Document:
        """解析文档。"""
    
    def get_metadata(self) -> dict:
        """获取文档元数据。"""
    
    def get_content(self) -> str:
        """获取文档内容。"""
    
    def get_structure(self) -> List[dict]:
        """获取文档结构。"""
    
    def get_formatting(self) -> dict:
        """获取文档格式信息。"""
```

### 具体解析器

#### `DocxParser` 类
DOCX 文档解析器。

```python
class DocxParser(BaseParser):
    """DOCX 文档解析器。"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
    
    def parse(self) -> Document:
        """解析 DOCX 文档。"""
    
    def get_styles(self) -> List[dict]:
        """获取文档样式。"""
    
    def get_images(self) -> List[dict]:
        """获取文档中的图片。"""
    
    def get_tables(self) -> List[dict]:
        """获取文档中的表格。"""
```

#### `PdfParser` 类
PDF 文档解析器。

```python
class PdfParser(BaseParser):
    """PDF 文档解析器。"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
    
    def parse(self) -> Document:
        """解析 PDF 文档。"""
    
    def get_pages(self) -> List[dict]:
        """获取页面信息。"""
    
    def extract_text(self, page_num: int) -> str:
        """提取页面文本。"""
    
    def extract_images(self, page_num: int) -> List[bytes]:
        """提取页面图片。"""
```

## 🎨 GUI 组件 API

### 对话框组件

#### `BaseDialog` 类
对话框基类。

```python
class BaseDialog(QDialog):
    """对话框基类。"""
    
    def __init__(self, parent=None):
        """初始化对话框。"""
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self) -> None:
        """设置用户界面。"""
    
    def setup_connections(self) -> None:
        """设置信号槽连接。"""
    
    def accept(self) -> None:
        """接受对话框。"""
        super().accept()
    
    def reject(self) -> None:
        """拒绝对话框。"""
        super().reject()
```

### 自定义组件

#### `DocumentPreview` 类
文档预览组件。

```python
class DocumentPreview(QWidget):
    """文档预览组件。"""
    
    def __init__(self, parent=None):
        """初始化预览组件。"""
    
    def load_document(self, file_path: str) -> bool:
        """加载文档。"""
    
    def render_page(self, page_num: int) -> QPixmap:
        """渲染页面。"""
    
    def zoom_in(self) -> None:
        """放大。"""
    
    def zoom_out(self) -> None:
        """缩小。"""
    
    def fit_to_width(self) -> None:
        """适应宽度。"""
    
    def fit_to_page(self) -> None:
        """适应页面。"""
```

## 🔧 工具函数 API

### 文件工具

```python
def safe_delete(file_path: str) -> bool:
    """安全删除文件。"""

def create_backup(file_path: str) -> str:
    """创建文件备份。"""

def get_file_hash(file_path: str) -> str:
    """计算文件哈希值。"""

def validate_file_path(file_path: str) -> bool:
    """验证文件路径。"""

def get_file_info(file_path: str) -> dict:
    """获取文件信息。"""
```

### 字符串工具

```python
def truncate_string(text: str, max_length: int) -> str:
    """截断字符串。"""

def sanitize_filename(filename: str) -> str:
    """清理文件名。"""

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小。"""

def format_timestamp(timestamp: float) -> str:
    """格式化时间戳。"""

def generate_id() -> str:
    """生成唯一ID。"""
```

### 网络工具

```python
def download_file(url: str, save_path: str) -> bool:
    """下载文件。"""

def check_internet_connection() -> bool:
    """检查网络连接。"""

def get_http_status(url: str) -> int:
    """获取HTTP状态码。"""

def make_api_request(url: str, method: str = "GET", **kwargs) -> dict:
    """发送API请求。"""
```

## 🧪 测试工具 API

### 测试基类

```python
class BaseTestCase(unittest.TestCase):
    """测试用例基类。"""
    
    def setUp(self) -> None:
        """测试前准备。"""
    
    def tearDown(self) -> None:
        """测试后清理。"""
    
    def assert_file_exists(self, file_path: str) -> None:
        """断言文件存在。"""
    
    def assert_file_content(self, file_path: str, expected_content: str) -> None:
        """断言文件内容。"""
    
    def create_test_file(self, content: str = "") -> str:
        """创建测试文件。"""
```

### 模拟对象

```python
class MockDocument:
    """模拟文档对象。"""
    
    def __init__(self, content: str = ""):
        self.content = content
        self.metadata = {}
    
    def save(self, file_path: str) -> None:
        """模拟保存文档。"""
    
    def load(self, file_path: str) -> None:
        """模拟加载文档。"""

class MockConfig:
    """模拟配置对象。"""
    
    def __init__(self):
        self.settings = {}
    
    def get(self, key: str, default=None):
        """模拟获取配置。"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value) -> None:
        """模拟设置配置。"""
        self.settings[key] = value
```

## 📊 事件系统 API

### 事件定义

```python
class Event:
    """事件基类。"""
    
    def __init__(self, name: str, data: dict = None):
        self.name = name
        self.data = data or {}
        self.timestamp = time.time()
        self.handled = False
    
    def mark_handled(self) -> None:
        """标记事件已处理。"""
        self.handled = True

class DocumentOpenedEvent(Event):
    """文档打开事件。"""
    
    def __init__(self, file_path: str):
        super().__init__("document_opened", {"file_path": file_path})

class DocumentSavedEvent(Event):
    """文档保存事件。"""
    
    def __init__(self, file_path: str):
        super().__init__("document_saved", {"file_path": file_path})
```

### 事件总线

```python
class EventBus:
    """事件总线。"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._handlers = {}
        return cls._instance
    
    def subscribe(self, event_name: str, handler: callable) -> None:
        """订阅事件。"""
    
    def unsubscribe(self, event_name: str, handler: callable) -> None:
        """取消订阅事件。"""
    
    def publish(self, event: Event) -> None:
        """发布事件。"""
    
    def clear(self) -> None:
        """清除所有处理器。"""
```

## 🔐 安全 API

### 加密工具

```python
def encrypt_data(data: bytes, key: str) -> bytes:
    """加密数据。"""

def decrypt_data(encrypted_data: bytes, key: str) -> bytes:
    """解密数据。"""

def hash_password(password: str) -> str:
    """哈希密码。"""

def verify_password(password: str, hashed: str) -> bool:
    """验证密码。"""

def generate_api_key() -> str:
    """生成API密钥。"""
```

### 权限检查

```python
def check_file_permission(file_path: str, permission: str) -> bool:
    """检查文件权限。"""

def validate_user_input(input_str: str, pattern: str) -> bool:
    """验证用户输入。"""

def sanitize_html(html: str) -> str:
    """清理HTML。"""

def prevent_xss(input_str: str) -> str:
    """防止XSS攻击。"""
```

## 📈 性能监控 API

### 性能计数器

```python
class PerformanceCounter:
    """性能计数器。"""
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.memory_usage = None
    
    def start(self) -> None:
        """开始计时。"""
    
    def stop(self) -> None:
        """停止计时。"""
    
    def get_duration(self) -> float:
        """获取持续时间。"""
    
    def get_memory_usage(self) -> float:
        """获取内存使用量。"""
    
    def reset(self) -> None:
        """重置计数器。"""
```

### 资源监控

```python
class ResourceMonitor:
    """资源监控器。"""
    
    def __init__(self):
        self.metrics = {}
    
    def start_monitoring(self) -> None:
        """开始监控。"""
    
    def stop_monitoring(self) -> None:
        """停止监控。"""
    
    def get_cpu_usage(self) -> float:
        """获取CPU使用率。"""
    
    def get_memory_usage(self) -> float:
        """获取内存使用率。"""
    
    def get_disk_usage(self) -> float:
        """获取磁盘使用率。"""
    
    def generate_report(self) -> dict:
        """生成监控报告。"""
```

## 🔗 外部集成 API

### GitHub 集成

```python
class GitHubIntegration:
    """GitHub 集成。"""
    
    def __init__(self, token: str = None):
        self.token = token
        self.client = None
    
    def authenticate(self) -> bool:
        """认证。"""
    
    def create_issue(self, title: str, body: str, labels: List[str] = None) -> dict:
        """创建Issue。"""
    
    def get_releases(self) -> List[dict]:
        """获取发布版本。"""
    
    def check_for_updates(self) -> dict:
        """检查更新。"""
    
    def download_release(self, release_tag: str, asset_name: str) -> str:
        """下载发布版本。"""
```

### 云存储集成

```python
class CloudStorage:
    """云存储集成。"""
    
    def __init__(self, provider: str, credentials: dict):
        self.provider = provider
        self.credentials = credentials
    
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """上传文件。"""
    
    def download_file(self, remote_path: str, local_path: str) -> bool:
        """下载文件。"""
    
    def list_files(self, path: str) -> List[str]:
        """列出文件。"""
    
    def delete_file(self, path: str) -> bool:
        """删除文件。"""
```

---

**注意**: 这是 Paper Formatter 的 API 参考文档。实际实现可能有所不同，请参考源代码获取最新信息。

**版本**: v2.2.3  
**最后更新**: 2026-03-21