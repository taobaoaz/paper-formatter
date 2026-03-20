"""
帮助系统对话框
Help System Dialog

版本：v2.2.0
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTreeWidget, QTreeWidgetItem, QTextBrowser, QSplitter,
                             QGroupBox, QFileDialog)
from PyQt5.QtCore import Qt


class HelpDialog(QDialog):
    """帮助系统对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('📖 帮助文档')
        self.setMinimumSize(800, 600)
        
        self.init_ui()
        self.load_content()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 主内容区（分割器）
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：目录树
        left_panel = self.create_toc_panel()
        splitter.addWidget(left_panel)
        
        # 右侧：内容显示
        right_panel = self.create_content_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([200, 600])
        
        layout.addWidget(splitter)
        
        # 底部按钮
        button_layout = self.create_button_layout()
        layout.addLayout(button_layout)
    
    def create_toc_panel(self):
        """创建目录面板"""
        group = QGroupBox('📑 目录')
        layout = QVBoxLayout(group)
        
        self.toc_tree = QTreeWidget()
        self.toc_tree.setHeaderLabels(['主题'])
        self.toc_tree.setColumnWidth(0, 180)
        self.toc_tree.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.toc_tree)
        
        return group
    
    def create_content_panel(self):
        """创建内容面板"""
        group = QGroupBox('📄 内容')
        layout = QVBoxLayout(group)
        
        self.content_browser = QTextBrowser()
        self.content_browser.setOpenExternalLinks(True)
        self.content_browser.setHtml(self.get_welcome_html())
        layout.addWidget(self.content_browser)
        
        return group
    
    def create_button_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        layout.addStretch()
        
        # 关于
        about_btn = QPushButton('ℹ️ 关于')
        about_btn.clicked.connect(self.show_about)
        layout.addWidget(about_btn)
        
        # 快捷键
        shortcut_btn = QPushButton('⌨️ 快捷键')
        shortcut_btn.clicked.connect(self.show_shortcuts)
        layout.addWidget(shortcut_btn)
        
        # 关闭
        close_btn = QPushButton('❌ 关闭')
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)
        
        return layout
    
    def load_content(self):
        """加载目录内容"""
        self.toc_tree.clear()
        
        # 快速入门
        item = QTreeWidgetItem(self.toc_tree, ['🚀 快速入门'])
        item.addChild(QTreeWidgetItem(item, ['欢迎使用']))
        item.addChild(QTreeWidgetItem(item, ['界面介绍']))
        item.addChild(QTreeWidgetItem(item, ['基本操作']))
        
        # 功能说明
        item = QTreeWidgetItem(self.toc_tree, ['📋 功能说明'])
        item.addChild(QTreeWidgetItem(item, ['文件预览']))
        item.addChild(QTreeWidgetItem(item, ['模板管理']))
        item.addChild(QTreeWidgetItem(item, ['格式化配置']))
        item.addChild(QTreeWidgetItem(item, ['PDF 导出']))
        item.addChild(QTreeWidgetItem(item, ['自动备份']))
        
        # 高级功能
        item = QTreeWidgetItem(self.toc_tree, ['⚙️ 高级功能'])
        item.addChild(QTreeWidgetItem(item, ['AI 识别']))
        item.addChild(QTreeWidgetItem(item, ['批量处理']))
        item.addChild(QTreeWidgetItem(item, ['快照管理']))
        
        # 常见问题
        item = QTreeWidgetItem(self.toc_tree, ['❓ 常见问题'])
        item.addChild(QTreeWidgetItem(item, ['安装问题']))
        item.addChild(QTreeWidgetItem(item, ['使用问题']))
        item.addChild(QTreeWidgetItem(item, ['错误处理']))
        
        # 快捷键
        item = QTreeWidgetItem(self.toc_tree, ['⌨️ 快捷键列表'])
        
        self.toc_tree.expandAll()
    
    def on_item_clicked(self, item, column):
        """目录项点击事件"""
        text = item.text(column)
        
        if '欢迎' in text:
            self.content_browser.setHtml(self.get_welcome_html())
        elif '界面' in text:
            self.content_browser.setHtml(self.get_interface_html())
        elif '基本' in text:
            self.content_browser.setHtml(self.get_basic_html())
        elif 'PDF' in text:
            self.content_browser.setHtml(self.get_pdf_html())
        elif '备份' in text:
            self.content_browser.setHtml(self.get_backup_html())
        elif '快捷' in text:
            self.show_shortcuts()
    
    def get_welcome_html(self):
        """欢迎页面"""
        return '''
        <h1>🚀 欢迎使用论文排版优化工具</h1>
        
        <h2>软件版本</h2>
        <p>版本：v2.2.0</p>
        <p>更新日期：2026-03-20</p>
        
        <h2>主要功能</h2>
        <ul>
            <li>📄 支持 Word (.docx) 和 LaTeX (.tex) 文档</li>
            <li>🎨 内置多种期刊和学位论文模板</li>
            <li>🤖 AI 自动识别文档模板</li>
            <li>⚙️ 可自定义模板规则</li>
            <li>✨ 一键优化文档排版格式</li>
            <li>📑 论文快速生成（填写式）</li>
            <li>📄 PDF 导出功能</li>
            <li>💾 自动备份和快照管理</li>
        </ul>
        
        <h2>快速开始</h2>
        <ol>
            <li>点击"打开文件"加载文档</li>
            <li>选择或识别模板</li>
            <li>点击"格式化文档"</li>
            <li>保存或导出为 PDF</li>
        </ol>
        
        <h2>获取帮助</h2>
        <p>如需更多帮助，请：</p>
        <ul>
            <li>查看左侧目录树</li>
            <li>点击"快捷键"按钮查看快捷键列表</li>
            <li>访问 GitHub 仓库提交 Issue</li>
        </ul>
        '''
    
    def get_interface_html(self):
        """界面介绍"""
        return '''
        <h1>🖥️ 界面介绍</h1>
        
        <h2>主界面布局</h2>
        <ul>
            <li><strong>顶部菜单栏：</strong>文件、编辑、视图、设置、工具、帮助</li>
            <li><strong>左侧面板：</strong>文件信息、模板选择</li>
            <li><strong>中间区域：</strong>文档预览、格式化结果</li>
            <li><strong>底部状态栏：</strong>快照数量、自动备份状态</li>
        </ul>
        
        <h2>状态栏说明</h2>
        <ul>
            <li>📸 X 个快照：点击打开快照管理</li>
            <li>🔄 自动备份：X 分钟后 - 点击打开备份设置</li>
        </ul>
        '''
    
    def get_basic_html(self):
        """基本操作"""
        return '''
        <h1>📖 基本操作</h1>
        
        <h2>打开文档</h2>
        <ol>
            <li>点击"文件" → "打开"</li>
            <li>或使用快捷键 Ctrl+O</li>
            <li>选择 Word 或 LaTeX 文件</li>
        </ol>
        
        <h2>选择模板</h2>
        <ol>
            <li>在左侧模板列表中选择</li>
            <li>或使用 AI 识别（Ctrl+R）</li>
        </ol>
        
        <h2>格式化文档</h2>
        <ol>
            <li>确保已选择模板</li>
            <li>点击"格式化文档"按钮</li>
            <li>等待处理完成</li>
            <li>查看格式化结果</li>
        </ol>
        
        <h2>保存和导出</h2>
        <ul>
            <li>保存：Ctrl+S</li>
            <li>导出 PDF：Ctrl+Alt+P</li>
        </ul>
        '''
    
    def get_pdf_html(self):
        """PDF 导出"""
        return '''
        <h1>📄 PDF 导出</h1>
        
        <h2>导出步骤</h2>
        <ol>
            <li>打开要导出的文档</li>
            <li>点击"工具" → "导出为 PDF"</li>
            <li>或使用快捷键 Ctrl+Alt+P</li>
            <li>选择导出选项</li>
            <li>点击"导出 PDF"</li>
        </ol>
        
        <h2>导出选项</h2>
        <ul>
            <li><strong>页面大小：</strong>A4/A3/B5/Letter/Legal</li>
            <li><strong>导出质量：</strong>标准/高质量/最小文件</li>
            <li><strong>压缩：</strong>减小文件大小</li>
            <li><strong>嵌入字体：</strong>确保正确显示</li>
        </ul>
        
        <h2>提示</h2>
        <ul>
            <li>标准质量适合屏幕阅读和打印</li>
            <li>高质量适合专业打印</li>
            <li>最小文件适合网络传输</li>
        </ul>
        '''
    
    def get_backup_html(self):
        """自动备份"""
        return '''
        <h1>💾 自动备份</h1>
        
        <h2>启用自动备份</h2>
        <ol>
            <li>点击"设置" → "自动备份设置"</li>
            <li>或使用快捷键 Ctrl+Alt+B</li>
            <li>勾选"启用自动备份"</li>
            <li>设置备份间隔（建议 10-15 分钟）</li>
            <li>点击"保存"</li>
        </ol>
        
        <h2>快照管理</h2>
        <ul>
            <li>点击状态栏"📸 X 个快照"</li>
            <li>或使用快捷键 Ctrl+Alt+S</li>
            <li>查看、恢复、删除快照</li>
            <li>标记重要快照（⭐）</li>
        </ul>
        
        <h2>重要性标记</h2>
        <ul>
            <li>选择快照</li>
            <li>点击"⭐ 标记为重要"</li>
            <li>重要快照不会被自动清理</li>
            <li>黄色高亮显示</li>
        </ul>
        '''
    
    def show_shortcuts(self):
        """显示快捷键"""
        html = '''
        <h1>⌨️ 快捷键列表</h1>
        
        <h2>文件操作</h2>
        <table border="1" cellpadding="5">
            <tr><th>快捷键</th><th>功能</th></tr>
            <tr><td>Ctrl+O</td><td>打开文件</td></tr>
            <tr><td>Ctrl+S</td><td>保存文件</td></tr>
            <tr><td>Ctrl+Alt+P</td><td>导出为 PDF</td></tr>
        </table>
        
        <h2>编辑操作</h2>
        <table border="1" cellpadding="5">
            <tr><th>快捷键</th><th>功能</th></tr>
            <tr><td>Ctrl+Z</td><td>撤销</td></tr>
            <tr><td>Ctrl+Y</td><td>重做</td></tr>
            <tr><td>Ctrl+Alt+S</td><td>文档快照管理</td></tr>
        </table>
        
        <h2>视图操作</h2>
        <table border="1" cellpadding="5">
            <tr><th>快捷键</th><th>功能</th></tr>
            <tr><td>Ctrl+T</td><td>窗口置顶</td></tr>
            <tr><td>Ctrl+R</td><td>AI 识别模板</td></tr>
        </table>
        
        <h2>工具操作</h2>
        <table border="1" cellpadding="5">
            <tr><th>快捷键</th><th>功能</th></tr>
            <tr><td>Ctrl+B</td><td>批量处理</td></tr>
            <tr><td>Ctrl+Alt+F</td><td>格式化配置</td></tr>
            <tr><td>Ctrl+Alt+K</td><td>配置快照管理</td></tr>
            <tr><td>Ctrl+Alt+B</td><td>自动备份设置</td></tr>
        </table>
        '''
        self.content_browser.setHtml(html)
    
    def show_about(self):
        """显示关于"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            '关于',
            '''
            <h2>论文排版优化工具</h2>
            <p>版本：v2.2.0</p>
            <p>更新日期：2026-03-20</p>
            
            <h3>主要功能</h3>
            <ul>
                <li>Word/LaTeX文档处理</li>
                <li>模板管理和 AI 识别</li>
                <li>一键格式化</li>
                <li>PDF 导出</li>
                <li>自动备份和快照</li>
            </ul>
            
            <p><b>开发者：</b>夕岸摇</p>
            <p><b>GitHub：</b>github.com/taobaoaz/paper-formatter</p>
            '''
        )
