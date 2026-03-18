# 📥 论文排版优化器 - 安装指南

**版本：** v2.0  
**更新日期：** 2024-03-18

---

## 🚀 快速开始

### 方式 1：使用打包版（推荐）⭐⭐⭐⭐⭐

**无需安装 Python，双击即可运行！**

**步骤：**

1. **下载程序**
   - 下载 `论文排版优化器.exe`

2. **运行程序**
   - 双击 `论文排版优化器.exe`

3. **完成！**
   - 程序自动启动

**优点：**
- ✅ 无需安装 Python
- ✅ 无需配置环境
- ✅ 双击即可运行
- ✅ 像普通软件一样

---

### 方式 2：源码运行（技术人员）⭐⭐⭐

**需要安装 Python**

#### 步骤 1：安装 Python

1. 访问：https://www.python.org/downloads/
2. 下载 **Python 3.8+**
3. 运行安装程序
4. ✅ **重要：** 勾选 "Add Python to PATH"
5. 点击 "Install Now"

**验证安装：**
```bash
python --version
```
应该显示：`Python 3.x.x`

---

#### 步骤 2：下载程序

```bash
git clone https://github.com/taobaoaz/paper-formatter.git
cd paper-formatter
```

或下载 ZIP 文件解压。

---

#### 步骤 3：安装依赖

```bash
pip install -r requirements.txt
```

**依赖列表：**
```txt
PyQt5>=5.15.0
python-docx>=0.8.11
```

---

#### 步骤 4：启动程序

**Windows:**
```
双击 启动.bat
```

**或命令行:**
```bash
python main.py
```

**Linux/Mac:**
```bash
./启动.sh
python3 main.py
```

---

## 📦 打包版说明

### 打包版包含

- ✅ 完整的程序
- ✅ Python 运行环境
- ✅ 所有依赖库
- ✅ 文档文件

### 文件大小

- **打包版：** ~50MB
- **源码版：** ~1MB（不含 Python）

### 系统要求

- **操作系统：** Windows 7/8/10/11
- **内存：** 至少 2GB
- **磁盘空间：** 至少 100MB

---

## 🔧 常见问题

### Q1: 双击没反应？

**可能原因：**
- 程序正在启动，等待几秒
- 被杀毒软件拦截

**解决方法：**
1. 等待 10 秒
2. 检查任务管理器
3. 临时关闭杀毒软件
4. 添加到杀毒软件白名单

---

### Q2: 提示缺少 Python？

**原因：** 使用了源码版但未安装 Python

**解决：**
- **方案 A：** 下载打包版（推荐）
- **方案 B：** 安装 Python（见上方）

---

### Q3: 杀毒软件报毒？

**原因：** PyInstaller 打包的程序可能误报

**解决：**
1. 添加到杀毒软件白名单
2. 临时关闭杀毒软件
3. 联系开发者获取签名版本

**说明：** 程序是安全的，这是误报。

---

### Q4: 运行时提示错误？

**常见错误：**

**错误 1：找不到模块**
```
ModuleNotFoundError: No module named 'xxx'
```
**解决：** 重新安装依赖
```bash
pip install -r requirements.txt
```

**错误 2：Python 版本过低**
```
Python 3.8+ is required
```
**解决：** 升级 Python 到 3.8+

---

## 📞 获取帮助

### 文档资源

- `README.md` - 项目说明
- `快速入门.md` - 使用教程
- `常见问题解答.md` - FAQ

### 在线资源

- **GitHub:** https://github.com/taobaoaz/paper-formatter
- **Issues:** https://github.com/taobaoaz/paper-formatter/issues

---

## ✅ 检查清单

### 打包版用户

- [ ] 下载了 .exe 文件
- [ ] 双击可以运行
- [ ] 程序正常显示
- [ ] 功能可以使用

### 源码版用户

- [ ] 安装了 Python 3.8+
- [ ] Python 已添加到 PATH
- [ ] 安装了依赖包
- [ ] 可以运行程序

---

## 🎊 推荐

**强烈推荐使用打包版！**

**理由：**
- ✅ 无需安装 Python
- ✅ 无需配置环境
- ✅ 双击即可运行
- ✅ 适合所有用户

**下载：** `论文排版优化器.exe`

---

**开发小助手 · 严谨专业版**  
**© 2024 All Rights Reserved**
