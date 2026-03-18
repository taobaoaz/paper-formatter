"""
文件预览对话框
File Preview Dialog
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QSplitter, QTreeWidget, QTreeWidgetItem, QTextBrowser,
                             QGroupBox, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from file_preview import FilePreview


class FilePreviewDialog(QDialog):
    """文件预览对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('文件预览')
        self.setMinimumSize(900, 700)
        
        self.preview = FilePreview()
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 顶部工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 主内容区（分割器）
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：文档结构
        left_panel = self.create_structure_panel()
        splitter.addWidget(left_panel)
        
        # 右侧：预览内容
        right_panel = self.create_preview_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([250, 650])
        
        layout.addWidget(splitter)
        
        # 底部状态栏
        status_bar = self.create_status_bar()
        layout.addWidget(status_bar)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QGroupBox('工具栏')
        layout = QHBoxLayout(toolbar)
        
        # 打开文件
        open_btn = QPushButton('📂 打开文件')
        open_btn.clicked.connect(self.open_file)
        layout.addWidget(open_btn)
        
        # 刷新
        refresh_btn = QPushButton('🔄 刷新')
        refresh_btn.clicked.connect(self.refresh_preview)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
        
        # 关闭
        close_btn = QPushButton('❌ 关闭')
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)
        
        return toolbar
    
    def create_structure_panel(self):
        """创建结构面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        group = QGroupBox('文档结构')
        group_layout = QVBoxLayout(group)
        
        self.structure_tree = QTreeWidget()
        self.structure_tree.setHeaderLabels(['标题'])
        self.structure_tree.setColumnWidth(0, 200)
        self.structure_tree.itemClicked.connect(self.on_structure_item_clicked)
        group_layout.addWidget(self.structure_tree)
        
        layout.addWidget(group)
        
        return panel
    
    def create_preview_panel(self):
        """创建预览面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        group = QGroupBox('预览')
        group_layout = QVBoxLayout(group)
        
        self.preview_browser = QTextBrowser()
        self.preview_browser.setOpenExternalLinks(True)
        self.preview_browser.setHtml(self.get_welcome_html())
        group_layout.addWidget(self.preview_browser)
        
        layout.addWidget(group)
        
        return panel
    
    def create_status_bar(self):
        """创建状态栏"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 文件信息
        self.file_label = QLabel('文件：未选择')
        self.file_label.setStyleSheet('color: #666;')
        layout.addWidget(self.file_label)
        
        layout.addStretch()
        
        # 统计信息
        self.stats_label = QLabel('统计：-')
        self.stats_label.setStyleSheet('color: #666;')
        layout.addWidget(self.stats_label)
        
        return panel
    
    def open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '选择文件',
            '',
            'Word 文件 (*.docx);;所有文件 (*)'
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path: str):
        """加载文件"""
        if self.preview.load_file(file_path):
            # 更新状态栏
            self.file_label.setText(f'文件：{file_path}')
            
            # 加载结构
            self.load_structure()
            
            # 加载预览
            self.load_preview()
            
            # 更新统计
            self.update_statistics()
        else:
            QMessageBox.warning(self, '警告', '无法加载文件')
    
    def load_structure(self):
        """加载文档结构"""
        self.structure_tree.clear()
        
        structure = self.preview.get_structure()
        
        # 按级别组织
        root_items = {}
        
        for item in structure:
            if item['is_heading']:
                level = item['level']
                
                # 创建树节点
                tree_item = QTreeWidgetItem()
                tree_item.setText(0, item['text'])
                tree_item.setData(0, Qt.UserRole, item['index'])
                
                # 根据级别设置图标和字体
                if level == 1:
                    tree_item.setFont(0, self.font())
                    # 添加到根
                    self.structure_tree.addTopLevelItem(tree_item)
                    root_items[level] = tree_item
                elif level == 2:
                    # 添加到最近的一级标题
                    parent = root_items.get(1)
                    if parent:
                        parent.addChild(tree_item)
                    else:
                        self.structure_tree.addTopLevelItem(tree_item)
                elif level == 3:
                    # 添加到最近的二级标题
                    parent = root_items.get(2)
                    if parent and parent.childCount() > 0:
                        parent.child(parent.childCount() - 1).addChild(tree_item)
                    else:
                        self.structure_tree.addTopLevelItem(tree_item)
    
    def load_preview(self):
        """加载预览"""
        html = self.preview.get_preview_html()
        self.preview_browser.setHtml(html)
    
    def update_statistics(self):
        """更新统计信息"""
        stats = self.preview.get_statistics()
        
        if stats:
            text = f"字数：{stats.get('total_chars', 0)} | "
            text += f"段落：{stats.get('paragraph_count', 0)} | "
            text += f"标题：{stats.get('headings', {}).get('level_1', 0) + stats.get('headings', {}).get('level_2', 0) + stats.get('headings', {}).get('level_3', 0)}"
            self.stats_label.setText(f'统计：{text}')
    
    def refresh_preview(self):
        """刷新预览"""
        if self.preview.file_path:
            self.load_file(self.preview.file_path)
    
    def on_structure_item_clicked(self, item, column):
        """结构项点击事件"""
        # 这里可以跳转到对应位置
        # 由于 QTextBrowser 不支持直接跳转，暂时只显示提示
        index = item.data(0, Qt.UserRole)
        if index is not None:
            print(f'跳转到段落 {index}')
    
    def get_welcome_html(self):
        """获取欢迎 HTML"""
        return '''
        <div style="font-family: Arial, sans-serif; padding: 40px; text-align: center; color: #666;">
            <h2 style="color: #667eea;">📄 文件预览</h2>
            <p>点击"打开文件"按钮选择要预览的 Word 文档</p>
            <p style="margin-top: 20px; font-size: 12px;">
                支持格式：.docx<br>
                功能：文档结构、内容预览、统计信息
            </p>
        </div>
        '''
    
    def closeEvent(self, event):
        """关闭事件"""
        self.preview.close()
        event.accept()


# 为了方便，定义一个空的 QWidget
class QWidget:
    pass

# 实际使用时需要正确导入
from PyQt5.QtWidgets import QWidget
