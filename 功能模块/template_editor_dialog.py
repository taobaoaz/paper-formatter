"""
模板编辑对话框
Template Editor Dialog
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QListWidget, QListWidgetItem, QFileDialog, QMessageBox,
                             QGroupBox, QFormLayout, QLineEdit, QTextEdit, QComboBox,
                             QTabWidget, QWidget)
from PyQt5.QtCore import Qt
from template_editor import TemplateEditor


class TemplateEditorDialog(QDialog):
    """模板编辑对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('模板管理')
        self.setMinimumSize(800, 600)
        
        self.editor = TemplateEditor()
        self.current_template_id = None
        self.current_template_data = None
        
        self.init_ui()
        self.load_templates()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建左右分栏
        main_layout = QHBoxLayout()
        
        # 左侧：模板列表
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # 右侧：模板编辑
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
        
        layout.addLayout(main_layout)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        new_btn = QPushButton('➕ 新建模板')
        new_btn.clicked.connect(self.create_new_template)
        button_layout.addWidget(new_btn)
        
        import_btn = QPushButton('📥 导入模板')
        import_btn.clicked.connect(self.import_template)
        button_layout.addWidget(import_btn)
        
        export_btn = QPushButton('📤 导出模板')
        export_btn.clicked.connect(self.export_template)
        button_layout.addWidget(export_btn)
        
        delete_btn = QPushButton('🗑️ 删除模板')
        delete_btn.clicked.connect(self.delete_template)
        button_layout.addWidget(delete_btn)
        
        close_btn = QPushButton('❌ 关闭')
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def create_left_panel(self):
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 模板列表
        group = QGroupBox('模板列表')
        group_layout = QVBoxLayout(group)
        
        self.template_list = QListWidget()
        self.template_list.currentItemChanged.connect(self.on_template_selected)
        group_layout.addWidget(self.template_list)
        
        layout.addWidget(group)
        
        # 模板统计
        self.count_label = QLabel('模板数：0')
        self.count_label.setStyleSheet('color: #666; font-size: 12px;')
        layout.addWidget(self.count_label)
        
        return panel
    
    def create_right_panel(self):
        """创建右侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.tabs.setEnabled(False)  # 初始禁用
        
        # 基本信息页
        basic_page = self.create_basic_page()
        self.tabs.addTab(basic_page, '📋 基本信息')
        
        # 格式配置页
        format_page = self.create_format_page()
        self.tabs.addTab(format_page, '⚙️ 格式配置')
        
        # 封面配置页
        cover_page = self.create_cover_page()
        self.tabs.addTab(cover_page, '📘 封面配置')
        
        layout.addWidget(self.tabs)
        
        # 保存按钮
        save_btn = QPushButton('💾 保存模板')
        save_btn.setStyleSheet('background-color: #667eea; color: white; padding: 10px; font-size: 14px; font-weight: bold;')
        save_btn.clicked.connect(self.save_template)
        layout.addWidget(save_btn)
        
        return panel
    
    def create_basic_page(self):
        """创建基本信息页"""
        page = QWidget()
        layout = QFormLayout(page)
        layout.setSpacing(10)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # 模板名称
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText('输入模板名称')
        layout.addRow('模板名称:', self.name_edit)
        
        # 适用学校
        self.school_edit = QLineEdit()
        self.school_edit.setPlaceholderText('例如：XX 大学')
        layout.addRow('适用学校:', self.school_edit)
        
        # 模板类型
        self.type_combo = QComboBox()
        self.type_combo.addItem('学位论文', 'thesis')
        self.type_combo.addItem('期刊论文', 'paper')
        self.type_combo.addItem('通用模板', 'general')
        layout.addRow('模板类型:', self.type_combo)
        
        # 描述
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        self.desc_edit.setPlaceholderText('模板描述...')
        layout.addRow('模板描述:', self.desc_edit)
        
        layout.addRow(QWidget())  # 空白行
        
        return page
    
    def create_format_page(self):
        """创建格式配置页"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        info_label = QLabel('💡 提示：格式配置使用全局格式化配置，点击"使用全局配置"按钮即可')
        info_label.setStyleSheet('color: #666; padding: 10px; background-color: #f0f0f0; border-radius: 5px;')
        layout.addWidget(info_label)
        
        use_global_btn = QPushButton('📋 使用全局格式化配置')
        use_global_btn.clicked.connect(self.use_global_format)
        layout.addWidget(use_global_btn)
        
        layout.addStretch()
        
        return page
    
    def create_cover_page(self):
        """创建封面配置页"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        info_label = QLabel('💡 提示：封面配置使用封面配置器，点击"打开封面配置器"按钮')
        info_label.setStyleSheet('color: #666; padding: 10px; background-color: #f0f0f0; border-radius: 5px;')
        layout.addWidget(info_label)
        
        open_cover_btn = QPushButton('📘 打开封面配置器')
        open_cover_btn.clicked.connect(self.open_cover_config)
        layout.addWidget(open_cover_btn)
        
        layout.addStretch()
        
        return page
    
    def load_templates(self):
        """加载模板列表"""
        self.template_list.clear()
        
        templates = self.editor.list_templates()
        
        for template in templates:
            item_text = f"{template['name']}"
            if template.get('school'):
                item_text += f" - {template['school']}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, template['id'])
            item.setToolTip(f"创建时间：{template.get('created_at', 'N/A')}\n类型：{template.get('type', 'general')}")
            self.template_list.addItem(item)
        
        # 更新统计
        self.count_label.setText(f'模板数：{len(templates)}')
    
    def on_template_selected(self, current, previous):
        """模板选择事件"""
        if not current:
            self.current_template_id = None
            self.current_template_data = None
            self.tabs.setEnabled(False)
            return
        
        template_id = current.data(Qt.UserRole)
        self.current_template_id = template_id
        
        # 加载模板数据
        template_data = self.editor.load_template(template_id)
        
        if template_data:
            self.current_template_data = template_data
            self.load_template_to_ui(template_data)
            self.tabs.setEnabled(True)
    
    def load_template_to_ui(self, template_data):
        """加载模板数据到 UI"""
        # 基本信息
        self.name_edit.setText(template_data.get('name', ''))
        self.school_edit.setText(template_data.get('school', ''))
        self.desc_edit.setPlainText(template_data.get('description', ''))
        
        # 模板类型
        template_type = template_data.get('type', 'general')
        index = self.type_combo.findData(template_type)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
    
    def create_new_template(self):
        """创建新模板"""
        # 创建默认模板
        template_id = self.editor.create_template(
            name='新模板',
            description='新创建的模板',
            school='',
            template_type='general'
        )
        
        if template_id:
            # 重新加载列表
            self.load_templates()
            
            # 选中新模板
            for i in range(self.template_list.count()):
                item = self.template_list.item(i)
                if item.data(Qt.UserRole) == template_id:
                    self.template_list.setCurrentItem(item)
                    break
            
            # 聚焦到名称编辑框
            self.name_edit.setFocus()
            self.name_edit.selectAll()
    
    def delete_template(self):
        """删除模板"""
        if not self.current_template_id:
            QMessageBox.warning(self, '警告', '请先选择要删除的模板')
            return
        
        # 确认删除
        reply = QMessageBox.question(
            self,
            '确认删除',
            f'确定要删除模板"{self.current_template_data.get("name", "")}"吗？',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.editor.delete_template(self.current_template_id):
                self.current_template_id = None
                self.current_template_data = None
                self.tabs.setEnabled(False)
                self.load_templates()
                QMessageBox.information(self, '成功', '模板已删除')
    
    def export_template(self):
        """导出模板"""
        if not self.current_template_id:
            QMessageBox.warning(self, '警告', '请先选择要导出的模板')
            return
        
        # 选择保存位置
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '导出模板',
            '',
            '模板文件 (*.json)'
        )
        
        if file_path:
            if self.editor.export_template(self.current_template_id, file_path):
                QMessageBox.information(self, '成功', '模板已导出')
    
    def import_template(self):
        """导入模板"""
        # 选择文件
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '导入模板',
            '',
            '模板文件 (*.json)'
        )
        
        if file_path:
            template_id = self.editor.import_template(file_path)
            if template_id:
                self.load_templates()
                QMessageBox.information(self, '成功', '模板已导入')
    
    def save_template(self):
        """保存模板"""
        if not self.current_template_id:
            return
        
        # 更新模板数据
        self.current_template_data['name'] = self.name_edit.text()
        self.current_template_data['school'] = self.school_edit.text()
        self.current_template_data['description'] = self.desc_edit.toPlainText()
        self.current_template_data['type'] = self.type_combo.currentData()
        
        # 保存
        if self.editor.save_template(self.current_template_id, self.current_template_data):
            QMessageBox.information(self, '成功', '模板已保存')
            self.load_templates()
    
    def use_global_format(self):
        """使用全局格式配置"""
        QMessageBox.information(
            self,
            '使用全局配置',
            '请在主界面打开"格式化配置"对话框进行设置。\n\n'
            '模板会自动使用最新的格式化配置。'
        )
    
    def open_cover_config(self):
        """打开封面配置器"""
        QMessageBox.information(
            self,
            '封面配置',
            '请在主界面打开"封面和声明页配置"对话框进行设置。\n\n'
            '配置完成后，可以在模板中引用。'
        )
