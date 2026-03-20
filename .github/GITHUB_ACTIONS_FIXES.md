# GitHub Actions 问题修复总结

本文档记录了在 Windows 环境下构建中文项目时遇到的所有编码和构建问题及其解决方案。

---

## 🔴 已修复的问题

### 1. UTF-8 编码问题 (cp1252 错误)

**错误信息：**
```
UnicodeEncodeError: 'charmap' codec can't encode characters in position 36-39: 
character maps to <undefined>
```

**原因：**
- Windows GitHub Actions 默认使用 `cp1252` 编码
- 无法处理中文路径、文件名和 emoji 字符

**解决方案：**
```yaml
# 使用 bash shell 代替 PowerShell
defaults:
  run:
    shell: bash
```

**为什么有效：**
- bash 默认使用 UTF-8 编码
- PowerShell 使用系统编码 (Windows 上为 cp1252)

---

### 2. Release Notes 自动生成编码问题

**错误信息：**
同样的 cp1252 编码错误，发生在 `Create Release` 步骤

**原因：**
- `generate_release_notes: true` 会读取 git 标签和提交信息
- 中文提交信息和 emoji 无法用 cp1252 编码

**解决方案：**
```yaml
- name: Create Release
  uses: softprops/action-gh-release@v1
  with:
    generate_release_notes: false  # 禁用自动生成
    body: |                        # 手动编写
      ## 📦 论文排版优化器
      请查看 RELEASE_NOTES 文件获取详细信息。
```

---

### 3. Artifact 名称编码问题

**潜在问题：**
```yaml
with:
  name: 论文排版优化器-Windows  # ❌ 中文名称可能导致问题
```

**解决方案：**
```yaml
with:
  name: paper-formatter-windows  # ✅ 使用英文名称
```

---

### 4. 路径分隔符问题

**潜在问题：**
```yaml
# PowerShell 风格 (反引号续行)
pyinstaller --name="论文排版优化器" `
  --add-data "功能模块;parsers" `
  ./核心模块/main.py
```

**解决方案：**
```yaml
# bash 风格 (反斜杠续行)
pyinstaller --name="论文排版优化器" \
  --add-data "功能模块:parsers" \
  ./核心模块/main.py
```

**注意：**
- bash 使用 `\` 续行
- PowerShell 使用 `` ` `` 续行
- `--add-data` 在 bash 中使用 `:` 分隔，PowerShell 使用 `;`

---

### 5. 环境变量设置问题

**潜在问题：**
```yaml
# PowerShell 风格
$env:PYTHONPATH="功能模块;核心模块;$env:PYTHONPATH"
```

**解决方案：**
```yaml
# 使用 env 关键字
- name: Build EXE
  env:
    PYTHONPATH: "功能模块;核心模块"
  run: |
    pyinstaller ...
```

---

## ✅ 最佳实践总结

### 1. Shell 选择

```yaml
# ✅ 推荐：使用 bash
defaults:
  run:
    shell: bash

# ❌ 避免：PowerShell (Windows 默认)
# 会导致 cp1252 编码问题
```

### 2. 文件命名

```yaml
# ✅ 推荐：英文文件名
name: paper-formatter-windows

# ❌ 避免：中文文件名
name: 论文排版优化器-Windows
```

### 3. 路径处理

```yaml
# ✅ 推荐：Unix 风格路径
./核心模块/main.py
功能模块/parsers

# ✅ 使用 ./ 前缀确保兼容性
```

### 4. Release 创建

```yaml
# ✅ 推荐：手动编写 release body
generate_release_notes: false
body: |
  ## 📦 产品名
  
  请查看 RELEASE_NOTES 文件获取详细信息。

# ❌ 避免：自动生成 (会读取中文提交信息)
generate_release_notes: true
```

### 5. 数据文件路径分隔符

```yaml
# ✅ bash (Linux/macOS/Windows bash)
--add-data "源目录:目标目录"

# ⚠️ PowerShell (仅 Windows)
--add-data "源目录;目标目录"
```

---

## 📋 完整的工作流模板

```yaml
name: Build Windows EXE

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    
    # ✅ 关键：使用 bash shell
    defaults:
      run:
        shell: bash
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyinstaller
        pip install -r ./启动文件/requirements.txt
    
    - name: Build EXE
      env:
        PYTHONPATH: "功能模块;核心模块"
      run: |
        pyinstaller --onefile --windowed \
          --name="app" \
          --add-data "功能模块:parsers" \
          --paths 功能模块 \
          ./核心模块/main.py
    
    - name: Upload EXE
      uses: actions/upload-artifact@v4
      with:
        name: app-windows
        path: dist/app.exe
        retention-days: 30
    
    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: dist/app.exe
        generate_release_notes: false
        draft: true
        body: |
          ## 📦 App Name Windows Version
          
          请查看 RELEASE_NOTES 文件获取详细信息。
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 🔍 故障排查命令

### 检查当前编码
```bash
# 在 GitHub Actions 中运行
python -c "import sys; print(sys.getdefaultencoding())"
python -c "import locale; print(locale.getpreferredencoding())"
```

### 测试 UTF-8 支持
```bash
# 在 GitHub Actions 中运行
echo "测试中文测试 📦"
python -c "print('中文测试 📦')"
```

### 检查文件编码
```bash
# 查看文件编码
file -i filename.py
```

---

## 📚 相关资源

- [GitHub Actions Shell 文档](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#using-a-specific-shell)
- [Python 编码文档](https://docs.python.org/3/library/stdtypes.html#text-encoding)
- [PyInstaller 数据文件路径](https://pyinstaller.org/en/stable/usage.html#what-to-bundle-where-to-search-for-files)
- [softprops/action-gh-release](https://github.com/softprops/action-gh-release)

---

## 📝 修改历史

| 日期 | 版本 | 修改内容 |
|------|------|----------|
| 2026-03-20 | v1.0 | 初始版本，记录所有编码问题修复 |

---

**最后更新：** 2026-03-20  
**维护者：** 开发团队
