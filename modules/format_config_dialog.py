"""
格式化配置对话框
Format Configuration Dialog
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTabWidget, QWidget, QFormLayout, QLineEdit, QComboBox,
                             QDoubleSpinBox, QSpinBox, QCheckBox, QGroupBox, QMessageBox,
                             QFileDialog)
from PyQt5.QtCore import Qt
from format_config import FormatConfig


class FormatConfigDialog(QDialog):
    """格式化配置对话框"""
    
    # 中文字体列表
    CHINESE_FONTS = [
        '宋体', '黑体', '楷体', '仿宋', '微软雅黑',
        '华文宋体', '华文黑体', '华文楷体', '华文仿宋',
        '方正小标宋', '方正仿宋', '方正楷体'
    ]
    
    # 英文字体列表
    ENGLISH_FONTS = [
        'Times New Roman', 'Arial', 'Calibri', 'Cambria',
        'Georgia', 'Verdana', 'Tahoma', 'Trebuchet MS'
    ]
    
    # 字号列表
    FONT_SIZES = [
        ('初号', 42), ('小初', 36),
        ('一号', 26), ('小一', 24),
        ('二号', 22), ('小二', 18),
        ('三号', 16), ('小三', 15),
        ('四号', 14), ('小四', 12),
        ('五号', 10.5), ('小五', 9),
        ('六号', 7.5), ('小六', 6.5),
        ('七号', 5.5), ('八号', 5)
    ]
    
    # 纸张大小
    PAPER_SIZES = {
        'A4': (21, 29.7),
        'A3': (29.7, 42),
        'B5': (17.6, 25),
        'Letter': (21.59, 27.94),
        'Legal': (21.59, 35.56)
    }
    
    def __init__(self, config=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('格式化配置')
        self.setMinimumSize(600, 500)
        
        self.config = config or FormatConfig()
        
        self.init_ui()
        self.load_config_to_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建标签页
        self.tabs = QTabWidget()
        
        # 字体配置页
        font_page = self.create_font_page()
        self.tabs.addTab(font_page, '📝 字体配置')
        
        # 段落配置页
        para_page = self.create_paragraph_page()
        self.tabs.addTab(para_page, '📄 段落配置')
        
        # 页面配置页
        page_page = self.create_page_page()
        self.tabs.addTab(page_page, '📋 页面配置')
        
        # 标题配置页
        heading_page = self.create_heading_page()
        self.tabs.addTab(heading_page, '📑 标题配置')
        
        layout.addWidget(self.tabs)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton('💾 保存配置')
        save_btn.clicked.connect(self.save_config)
        button_layout.addWidget(save_btn)
        
        export_btn = QPushButton('📤 导出配置')
        export_btn.clicked.connect(self.export_config)
        button_layout.addWidget(export_btn)
        
        import_btn = QPushButton('📥 导入配置')
        import_btn.clicked.connect(self.import_config)
        button_layout.addWidget(import_btn)
        
        reset_btn = QPushButton('🔄 重置默认')
        reset_btn.clicked.connect(self.reset_config)
        button_layout.addWidget(reset_btn)
        
        cancel_btn = QPushButton('❌ 取消')
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def create_font_page(self):
        """创建字体配置页"""
        page = QWidget()
        layout = QFormLayout(page)
        layout.setSpacing(10)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # 中文字体
        self.chinese_font_combo = QComboBox()
        self.chinese_font_combo.addItems(self.CHINESE_FONTS)
        self.chinese_font_combo.setEditable(True)
        layout.addRow('中文字体:', self.chinese_font_combo)
        
        # 英文字体
        self.english_font_combo = QComboBox()
        self.english_font_combo.addItems(self.ENGLISH_FONTS)
        self.english_font_combo.setEditable(True)
        layout.addRow('英文字体:', self.english_font_combo)
        
        # 字号
        self.font_size_combo = QComboBox()
        for name, pt in self.FONT_SIZES:
            self.font_size_combo.addItem(f'{name} ({pt}pt)', pt)
        layout.addRow('正文字号:', self.font_size_combo)
        
        # 行距
        self.line_spacing_spin = QDoubleSpinBox()
        self.line_spacing_spin.setRange(0.5, 3.0)
        self.line_spacing_spin.setSingleStep(0.1)
        self.line_spacing_spin.setDecimals(1)
        layout.addRow('行距倍数:', self.line_spacing_spin)
        
        layout.addRow(QWidget())  # 空白行
        
        return page
    
    def create_paragraph_page(self):
        """创建段落配置页"""
        page = QWidget()
        layout = QFormLayout(page)
        layout.setSpacing(10)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # 首行缩进
        self.first_line_indent_spin = QSpinBox()
        self.first_line_indent_spin.setRange(0, 10)
        self.first_line_indent_spin.setSuffix(' 字符')
        layout.addRow('首行缩进:', self.first_line_indent_spin)
        
        # 段前间距
        self.before_spacing_spin = QSpinBox()
        self.before_spacing_spin.setRange(0, 100)
        self.before_spacing_spin.setSuffix(' 磅')
        layout.addRow('段前间距:', self.before_spacing_spin)
        
        # 段后间距
        self.after_spacing_spin = QSpinBox()
        self.after_spacing_spin.setRange(0, 100)
        self.after_spacing_spin.setSuffix(' 磅')
        layout.addRow('段后间距:', self.after_spacing_spin)
        
        # 行距类型
        self.line_spacing_type_combo = QComboBox()
        self.line_spacing_type_combo.addItem('倍数', 'multi')
        self.line_spacing_type_combo.addItem('固定值', 'exactly')
        self.line_spacing_type_combo.addItem('单倍行距', 'single')
        layout.addRow('行距类型:', self.line_spacing_type_combo)
        
        layout.addRow(QWidget())  # 空白行
        
        return page
    
    def create_page_page(self):
        """创建页面配置页"""
        page = QWidget()
        layout = QFormLayout(page)
        layout.setSpacing(10)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # 纸张大小
        self.paper_size_combo = QComboBox()
        for name, (w, h) in self.PAPER_SIZES.items():
            self.paper_size_combo.addItem(f'{name} ({w}x{h}cm)', name)
        layout.addRow('纸张大小:', self.paper_size_combo)
        
        # 上边距
        self.margin_top_spin = QDoubleSpinBox()
        self.margin_top_spin.setRange(0, 10)
        self.margin_top_spin.setSingleStep(0.1)
        self.margin_top_spin.setSuffix(' cm')
        layout.addRow('上边距:', self.margin_top_spin)
        
        # 下边距
        self.margin_bottom_spin = QDoubleSpinBox()
        self.margin_bottom_spin.setRange(0, 10)
        self.margin_bottom_spin.setSingleStep(0.1)
        self.margin_bottom_spin.setSuffix(' cm')
        layout.addRow('下边距:', self.margin_bottom_spin)
        
        # 左边距
        self.margin_left_spin = QDoubleSpinBox()
        self.margin_left_spin.setRange(0, 10)
        self.margin_left_spin.setSingleStep(0.1)
        self.margin_left_spin.setSuffix(' cm')
        layout.addRow('左边距:', self.margin_left_spin)
        
        # 右边距
        self.margin_right_spin = QDoubleSpinBox()
        self.margin_right_spin.setRange(0, 10)
        self.margin_right_spin.setSingleStep(0.1)
        self.margin_right_spin.setSuffix(' cm')
        layout.addRow('右边距:', self.margin_right_spin)
        
        layout.addRow(QWidget())  # 空白行
        
        return page
    
    def create_heading_page(self):
        """创建标题配置页"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 一级标题
        level1_group = self.create_heading_group('一级标题', 'level_1')
        layout.addWidget(level1_group)
        
        # 二级标题
        level2_group = self.create_heading_group('二级标题', 'level_2')
        layout.addWidget(level2_group)
        
        # 三级标题
        level3_group = self.create_heading_group('三级标题', 'level_3')
        layout.addWidget(level3_group)
        
        layout.addStretch()
        
        return page
    
    def create_heading_group(self, title, level_key):
        """创建标题配置组"""
        group = QGroupBox(title)
        layout = QFormLayout(group)
        layout.setSpacing(8)
        
        # 字号
        font_size_combo = QComboBox()
        for name, pt in self.FONT_SIZES:
            font_size_combo.addItem(f'{name} ({pt}pt)', pt)
        setattr(self, f'{level_key}_font_size', font_size_combo)
        layout.addRow('字号:', font_size_combo)
        
        # 加粗
        bold_check = QCheckBox('加粗')
        bold_check.setChecked(True)
        setattr(self, f'{level_key}_bold', bold_check)
        layout.addRow('加粗:', bold_check)
        
        # 编号格式
        numbering_edit = QLineEdit()
        setattr(self, f'{level_key}_numbering', numbering_edit)
        layout.addRow('编号格式:', numbering_edit)
        
        return group
    
    def load_config_to_ui(self):
        """从配置加载到 UI"""
        # 字体配置
        font = self.config.get_config('font')
        if font:
            idx = self.chinese_font_combo.findText(font.get('chinese_font', '宋体'))
            if idx >= 0:
                self.chinese_font_combo.setCurrentIndex(idx)
            
            idx = self.english_font_combo.findText(font.get('english_font', 'Times New Roman'))
            if idx >= 0:
                self.english_font_combo.setCurrentIndex(idx)
            
            self.font_size_combo.setCurrentIndex(
                self.font_size_combo.findData(font.get('font_size_pt', 12))
            )
            self.line_spacing_spin.setValue(font.get('line_spacing', 1.5))
        
        # 段落配置
        para = self.config.get_config('paragraph')
        if para:
            self.first_line_indent_spin.setValue(para.get('first_line_indent', 2))
            self.before_spacing_spin.setValue(para.get('before_spacing', 0))
            self.after_spacing_spin.setValue(para.get('after_spacing', 0))
            
            idx = self.line_spacing_type_combo.findData(para.get('line_spacing_type', 'multi'))
            if idx >= 0:
                self.line_spacing_type_combo.setCurrentIndex(idx)
        
        # 页面配置
        page = self.config.get_config('page')
        if page:
            idx = self.paper_size_combo.findData(page.get('paper_size', 'A4'))
            if idx >= 0:
                self.paper_size_combo.setCurrentIndex(idx)
            
            self.margin_top_spin.setValue(page.get('margin_top_cm', 2.54))
            self.margin_bottom_spin.setValue(page.get('margin_bottom_cm', 2.54))
            self.margin_left_spin.setValue(page.get('margin_left_cm', 3.17))
            self.margin_right_spin.setValue(page.get('margin_right_cm', 3.17))
        
        # 标题配置
        heading = self.config.get_config('heading')
        if heading:
            for level in ['level_1', 'level_2', 'level_3']:
                level_config = heading.get(level, {})
                
                font_size_combo = getattr(self, f'{level}_font_size')
                font_size_combo.setCurrentIndex(
                    font_size_combo.findData(level_config.get('font_size_pt', 12))
                )
                
                bold_check = getattr(self, f'{level}_bold')
                bold_check.setChecked(level_config.get('bold', False))
                
                numbering_edit = getattr(self, f'{level}_numbering')
                numbering_edit.setText(level_config.get('numbering', ''))
    
    def save_config_from_ui(self):
        """从 UI 保存配置"""
        # 字体配置
        self.config.set_config('font', 'chinese_font', self.chinese_font_combo.currentText())
        self.config.set_config('font', 'english_font', self.english_font_combo.currentText())
        self.config.set_config('font', 'font_size_pt', self.font_size_combo.currentData())
        self.config.set_config('font', 'font_size', self.font_size_combo.currentText().split()[0])
        self.config.set_config('font', 'line_spacing', self.line_spacing_spin.value())
        
        # 段落配置
        self.config.set_config('paragraph', 'first_line_indent', self.first_line_indent_spin.value())
        self.config.set_config('paragraph', 'before_spacing', self.before_spacing_spin.value())
        self.config.set_config('paragraph', 'after_spacing', self.after_spacing_spin.value())
        self.config.set_config('paragraph', 'line_spacing_type', self.line_spacing_type_combo.currentData())
        self.config.set_config('paragraph', 'line_spacing_value', self.line_spacing_spin.value())
        
        # 页面配置
        self.config.set_config('page', 'paper_size', self.paper_size_combo.currentData())
        self.config.set_config('page', 'margin_top_cm', self.margin_top_spin.value())
        self.config.set_config('page', 'margin_bottom_cm', self.margin_bottom_spin.value())
        self.config.set_config('page', 'margin_left_cm', self.margin_left_spin.value())
        self.config.set_config('page', 'margin_right_cm', self.margin_right_spin.value())
        
        # 标题配置
        for level in ['level_1', 'level_2', 'level_3']:
            font_size_combo = getattr(self, f'{level}_font_size')
            bold_check = getattr(self, f'{level}_bold')
            numbering_edit = getattr(self, f'{level}_numbering')
            
            self.config.set_config('heading', f'{level}/font_size_pt', font_size_combo.currentData())
            self.config.set_config('heading', f'{level}/bold', bold_check.isChecked())
            self.config.set_config('heading', f'{level}/numbering', numbering_edit.text())
    
    def save_config(self):
        """保存配置"""
        self.save_config_from_ui()
        
        valid, errors = self.config.validate_config()
        if not valid:
            QMessageBox.warning(
                self,
                '配置验证失败',
                '\n'.join(errors)
            )
            return
        
        if self.config.save_config():
            QMessageBox.information(self, '成功', '配置已保存！')
            self.accept()
    
    def export_config(self):
        """导出配置"""
        self.save_config_from_ui()
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '导出配置',
            '',
            '配置文件 (*.json)'
        )
        
        if file_path:
            if self.config.export_config(file_path):
                QMessageBox.information(self, '成功', '配置已导出！')
    
    def import_config(self):
        """导入配置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '导入配置',
            '',
            '配置文件 (*.json)'
        )
        
        if file_path:
            if self.config.import_config(file_path):
                self.load_config_to_ui()
                QMessageBox.information(self, '成功', '配置已导入！')
    
    def reset_config(self):
        """重置配置"""
        reply = QMessageBox.question(
            self,
            '确认重置',
            '确定要重置为默认配置吗？',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.config.reset_to_default()
            self.load_config_to_ui()
            QMessageBox.information(self, '成功', '已重置为默认配置')
