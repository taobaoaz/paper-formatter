"""
PDF 导出对话框
PDF Export Dialog

版本：v2.2.0
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QGroupBox, QFileDialog, QFormLayout, QComboBox,
                             QCheckBox, QSpinBox, QMessageBox, QProgressBar,
                             QTextEdit)
from PyQt5.QtCore import Qt
from pdf_exporter import PDFExporter, PDFExportOptions


class PDFExportDialog(QDialog):
    """PDF 导出对话框"""
    
    PAGE_SIZES = {
        'A4': 'A4 (210 × 297 mm)',
        'A3': 'A3 (297 × 420 mm)',
        'B5': 'B5 (176 × 250 mm)',
        'Letter': 'Letter (8.5 × 11 inch)',
        'Legal': 'Legal (8.5 × 14 inch)'
    }
    
    QUALITY_OPTIONS = {
        'standard': '标准质量',
        'high': '高质量',
        'minimum': '最小文件'
    }
    
    def __init__(self, file_path: str = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('📄 导出为 PDF')
        self.setMinimumSize(500, 400)
        
        self.file_path = file_path
        self.exporter = PDFExporter()
        self.export_options = PDFExportOptions()
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 文件选择
        file_group = self.create_file_group()
        layout.addWidget(file_group)
        
        # 导出选项
        options_group = self.create_options_group()
        layout.addWidget(options_group)
        
        # 进度显示
        progress_group = self.create_progress_group()
        layout.addWidget(progress_group)
        
        # 底部按钮
        button_layout = self.create_button_layout()
        layout.addLayout(button_layout)
    
    def create_file_group(self):
        """创建文件选择组"""
        group = QGroupBox('📁 文件选择')
        layout = QFormLayout(group)
        
        # 源文件
        self.source_file_edit = QLabel(self.file_path or '未选择文件')
        self.source_file_edit.setStyleSheet('color: #666;')
        layout.addRow('源文件:', self.source_file_edit)
        
        # 选择文件按钮
        select_btn = QPushButton('📂 选择文件')
        select_btn.clicked.connect(self.select_file)
        layout.addRow(select_btn)
        
        # 目标文件
        target_layout = QHBoxLayout()
        self.target_file_edit = QLabel('')
        self.target_file_edit.setStyleSheet('color: #666;')
        target_layout.addWidget(self.target_file_edit)
        
        browse_btn = QPushButton('浏览...')
        browse_btn.clicked.connect(self.browse_target)
        target_layout.addWidget(browse_btn)
        
        layout.addRow('目标文件:', target_layout)
        
        return group
    
    def create_options_group(self):
        """创建导出选项组"""
        group = QGroupBox('⚙️ 导出选项')
        layout = QFormLayout(group)
        
        # 页面大小
        self.page_size_combo = QComboBox()
        for size, desc in self.PAGE_SIZES.items():
            self.page_size_combo.addItem(desc, size)
        self.page_size_combo.setCurrentText(self.PAGE_SIZES['A4'])
        layout.addRow('页面大小:', self.page_size_combo)
        
        # 导出质量
        self.quality_combo = QComboBox()
        for quality, desc in self.QUALITY_OPTIONS.items():
            self.quality_combo.addItem(desc, quality)
        self.quality_combo.setCurrentText(self.QUALITY_OPTIONS['standard'])
        layout.addRow('导出质量:', self.quality_combo)
        
        # 压缩选项
        self.compress_checkbox = QCheckBox('启用压缩（减小文件大小）')
        self.compress_checkbox.setChecked(True)
        layout.addRow(self.compress_checkbox)
        
        # 嵌入字体
        self.embed_fonts_checkbox = QCheckBox('嵌入字体（推荐）')
        self.embed_fonts_checkbox.setChecked(True)
        layout.addRow(self.embed_fonts_checkbox)
        
        # 说明
        desc_label = QLabel(
            '💡 提示：\n'
            '• 标准质量：适合屏幕阅读和打印\n'
            '• 高质量：适合专业打印\n'
            '• 最小文件：适合网络传输'
        )
        desc_label.setStyleSheet('color: #666; font-size: 11px;')
        desc_label.setWordWrap(True)
        layout.addRow(desc_label)
        
        return group
    
    def create_progress_group(self):
        """创建进度显示组"""
        group = QGroupBox('📊 导出进度')
        layout = QVBoxLayout(group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # 状态文本
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        self.status_text.setStyleSheet('background-color: #f5f5f5; font-family: monospace;')
        layout.addWidget(self.status_text)
        
        return group
    
    def create_button_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        layout.addStretch()
        
        # 取消
        cancel_btn = QPushButton('❌ 取消')
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        # 导出
        export_btn = QPushButton('💾 导出 PDF')
        export_btn.setStyleSheet('background-color: #4CAF50; color: white; padding: 8px 16px;')
        export_btn.clicked.connect(self.export_pdf)
        layout.addWidget(export_btn)
        
        return layout
    
    def select_file(self):
        """选择源文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '选择 Word 文档',
            '',
            'Word 文档 (*.docx);;所有文件 (*)'
        )
        
        if file_path:
            self.file_path = file_path
            self.source_file_edit.setText(file_path)
            self.target_file_edit.setText('')  # 清空目标文件
    
    def browse_target(self):
        """浏览目标文件"""
        if not self.file_path:
            QMessageBox.warning(self, '警告', '请先选择源文件')
            return
        
        # 默认文件名
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        default_name = f"{base_name}.pdf"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '保存 PDF 文件',
            default_name,
            'PDF 文件 (*.pdf)'
        )
        
        if file_path:
            self.export_options.target_path = file_path
            self.target_file_edit.setText(file_path)
    
    def get_export_options(self) -> PDFExportOptions:
        """获取导出选项"""
        options = PDFExportOptions()
        options.page_size = self.page_size_combo.currentData()
        options.quality = self.quality_combo.currentData()
        options.compress = self.compress_checkbox.isChecked()
        options.embed_fonts = self.embed_fonts_checkbox.isChecked()
        return options
    
    def log_message(self, message: str):
        """记录日志消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.status_text.append(f"[{timestamp}] {message}")
    
    def export_pdf(self):
        """导出 PDF"""
        if not self.file_path:
            QMessageBox.warning(self, '警告', '请先选择源文件')
            return
        
        # 获取目标路径
        target_path = getattr(self.export_options, 'target_path', None)
        if not target_path:
            # 自动生成目标路径
            base_name = os.path.splitext(os.path.basename(self.file_path))[0]
            target_path = os.path.join(
                os.path.dirname(self.file_path),
                f"{base_name}.pdf"
            )
        
        self.log_message(f"开始导出 PDF...")
        self.log_message(f"源文件：{self.file_path}")
        self.log_message(f"目标文件：{target_path}")
        self.progress_bar.setValue(25)
        
        # 获取选项
        options = self.get_export_options()
        self.log_message(f"页面大小：{options.page_size}")
        self.log_message(f"质量：{options.quality}")
        self.progress_bar.setValue(50)
        
        # 导出
        self.log_message("正在导出...")
        success = self.exporter.export_docx_to_pdf(
            self.file_path,
            target_path,
            options.to_dict()
        )
        
        self.progress_bar.setValue(100)
        
        if success:
            self.log_message("✅ 导出成功!")
            QMessageBox.information(
                self,
                '成功',
                f'✅ PDF 导出成功!\n\n保存到：{target_path}'
            )
            self.accept()
        else:
            self.log_message("❌ 导出失败!")
            QMessageBox.critical(
                self,
                '错误',
                '❌ PDF 导出失败!\n\n请查看日志获取详细信息。'
            )


# 需要导入 os
import os
