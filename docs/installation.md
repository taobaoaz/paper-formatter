---
layout: default
title: 安装指南
parent: 用户指南
nav_order: 2
---

# 安装指南

本文档介绍如何在不同的操作系统上安装 Paper Formatter。

## 系统要求

### 最低要求
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+ 或其他 Linux 发行版
- **内存**: 4 GB RAM
- **存储空间**: 500 MB 可用空间
- **Python**: 3.8 或更高版本（仅开发版本需要）

### 推荐配置
- **操作系统**: Windows 11, macOS 12+, Ubuntu 20.04+
- **内存**: 8 GB RAM 或更高
- **存储空间**: 1 GB 可用空间
- **显示器**: 1920x1080 分辨率或更高

## 📦 安装方式

### 方式一：Windows 安装程序（推荐）

#### 下载安装包
1. 访问 [GitHub Releases](https://github.com/taobaoaz/paper-formatter/releases)
2. 下载最新版本的 `.exe` 安装程序
3. 文件名为 `paper-formatter-vX.X.X-setup.exe`

#### 安装步骤
1. **双击安装程序**：运行下载的 `.exe` 文件
2. **选择安装位置**：默认安装在 `C:\Program Files\Paper Formatter\`
3. **创建快捷方式**：选择是否创建桌面快捷方式和开始菜单项
4. **完成安装**：点击"完成"按钮

#### 验证安装
1. 从开始菜单或桌面快捷方式启动 Paper Formatter
2. 如果看到主界面，说明安装成功

### 方式二：macOS 安装

#### 下载安装包
1. 访问 [GitHub Releases](https://github.com/taobaoaz/paper-formatter/releases)
2. 下载最新版本的 `.dmg` 文件
3. 文件名为 `paper-formatter-vX.X.X.dmg`

#### 安装步骤
1. **打开 DMG 文件**：双击下载的 `.dmg` 文件
2. **拖拽到应用程序**：将 Paper Formatter 图标拖到"应用程序"文件夹
3. **首次运行**：在"应用程序"中找到并运行 Paper Formatter
4. **安全警告**：如果出现安全警告，请前往"系统偏好设置" → "安全性与隐私" → "通用"中允许运行

### 方式三：Linux 安装

#### 下载安装包
1. 访问 [GitHub Releases](https://github.com/taobaoaz/paper-formatter/releases)
2. 下载对应 Linux 发行版的安装包
   - `.deb` 文件（适用于 Ubuntu/Debian）
   - `.rpm` 文件（适用于 Fedora/RHEL）
   - `.AppImage` 文件（适用于所有 Linux 发行版）

#### 安装步骤

##### Debian/Ubuntu (.deb)
```bash
# 下载 .deb 文件
wget https://github.com/taobaoaz/paper-formatter/releases/download/vX.X.X/paper-formatter_vX.X.X_amd64.deb

# 安装
sudo dpkg -i paper-formatter_vX.X.X_amd64.deb

# 修复依赖（如果需要）
sudo apt-get install -f
```

##### Fedora/RHEL (.rpm)
```bash
# 下载 .rpm 文件
wget https://github.com/taobaoaz/paper-formatter/releases/download/vX.X.X/paper-formatter-vX.X.X.x86_64.rpm

# 安装
sudo rpm -i paper-formatter-vX.X.X.x86_64.rpm
```

##### 通用 Linux (.AppImage)
```bash
# 下载 AppImage 文件
wget https://github.com/taobaoaz/paper-formatter/releases/download/vX.X.X/paper-formatter-vX.X.X-x86_64.AppImage

# 添加执行权限
chmod +x paper-formatter-vX.X.X-x86_64.AppImage

# 运行
./paper-formatter-vX.X.X-x86_64.AppImage
```

### 方式四：从源代码安装（开发者）

#### 前提条件
- Python 3.8+
- Git
- pip

#### 安装步骤
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

# 运行应用
python -m core.main
```

## 🔧 安装后配置

### 首次运行设置
1. **语言选择**：首次运行时选择界面语言（中文/英文）
2. **主题选择**：选择亮色或暗色主题
3. **默认格式**：设置默认的论文格式模板
4. **备份设置**：配置自动备份选项

### 文件关联（Windows）
安装程序会自动关联以下文件类型：
- `.docx` - Microsoft Word 文档
- `.doc` - 旧版 Word 文档
- `.txt` - 纯文本文件
- `.md` - Markdown 文件

如果需要手动关联：
1. 右键点击文件 → "打开方式" → "选择其他应用"
2. 浏览到 Paper Formatter 安装目录
3. 选择 `paper-formatter.exe`
4. 勾选"始终使用此应用打开"

### 卸载程序

#### Windows
1. 打开"设置" → "应用" → "应用和功能"
2. 找到"Paper Formatter"
3. 点击"卸载"

#### macOS
1. 打开"应用程序"文件夹
2. 将 Paper Formatter 拖到废纸篓
3. 清空废纸篓

#### Linux
```bash
# Debian/Ubuntu
sudo apt remove paper-formatter

# Fedora/RHEL
sudo dnf remove paper-formatter

# 手动删除 AppImage
rm paper-formatter-vX.X.X-x86_64.AppImage
```

## ❓ 常见安装问题

### 问题1：安装程序无法运行
**解决方案**：
- 确保下载的文件完整
- 检查杀毒软件是否阻止安装
- 以管理员身份运行安装程序

### 问题2：缺少依赖库
**解决方案**：
- 安装 Microsoft Visual C++ Redistributable
- 更新系统到最新版本
- 重新安装应用

### 问题3：权限问题
**解决方案**：
- 确保有安装目录的写入权限
- 关闭所有正在运行的 Paper Formatter 实例
- 重启系统后重试

### 问题4：启动时崩溃
**解决方案**：
1. 检查日志文件：`%APPDATA%\Paper Formatter\logs\` (Windows) 或 `~/.paper-formatter/logs/` (Linux/macOS)
2. 重新安装最新版本
3. 提交问题到 [GitHub Issues](https://github.com/taobaoaz/paper-formatter/issues)

## 📞 获取帮助

如果遇到安装问题，请：
1. 查看 [常见问题](/faq)
2. 在 [GitHub Issues](https://github.com/taobaoaz/paper-formatter/issues) 中搜索类似问题
3. 创建新的 issue 并附上详细错误信息

## 🔄 更新应用

### 自动更新
Paper Formatter 支持自动更新：
1. 打开应用 → "帮助" → "检查更新"
2. 如果有新版本，点击"立即更新"
3. 按照提示完成更新

### 手动更新
1. 下载最新版本安装包
2. 运行安装程序（会覆盖旧版本）
3. 重启应用

---

**注意**：安装过程中请确保网络连接稳定，以便下载必要的组件。如果遇到任何问题，请参考上述解决方案或联系支持。