"""
批量 PDF 导出对话框
Batch PDF Export Dialog

版本：v2.2.1
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QGroupBox, QFileDialog, QListWidget, QListWidgetItem,
                             QProgressBar, QTextEdit, QComboBox, QCheckBox,
                             QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt
from pdf_exporter import PDFExporter, PDFExportOptions
import os


class BatchPDFExportDialog(QDialog):
    """批量 PDF 导出对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('📄 批量导出 PDF')
        self.setMinimumSize(700, 500)
        
        self.exporter = PDFExporter()
        self.files = []
        self.export_options = PDFExportOptions()
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 文件列表
        file_group = self.create_file_list_group()
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
    
    def create_file_list_group(self):
        """创建文件列表组"""
        group = QGroupBox('📁 文件列表')
        layout = QVBoxLayout(group)
        
        # 文件列表
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.file_list.setDragDropMode(QListWidget.DragDrop)
        layout.addWidget(self.file_list)
        
        # 文件操作按钮
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton('➕ 添加文件')
        add_btn.clicked.connect(self.add_files)
        btn_layout.addWidget(add_btn)
        
        remove_btn = QPushButton('➖ 移除选中')
        remove_btn.clicked.connect(self.remove_selected)
        btn_layout.addWidget(remove_btn)
        
        clear_btn = QPushButton('🗑️ 清空列表')
        clear_btn.clicked.connect(self.clear_list)
        btn_layout.addWidget(clear_btn)
        
        btn_layout.addStretch()
        
        self.count_label = QLabel('共 0 个文件')
        self.count_label.setStyleSheet('color: #666; font-weight: bold;')
        btn_layout.addWidget(self.count_label)
        
        layout.addLayout(btn_layout)
        
        return group
    
    def create_options_group(self):
        """创建导出选项组"""
        group = QGroupBox('⚙️ 导出选项')
        layout = QHBoxLayout(group)
        
        # 页面大小
        layout.addWidget(QLabel('页面大小:'))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(['A4', 'A3', 'B5', 'Letter', 'Legal'])
        self.page_size_combo.setCurrentText('A4')
        layout.addWidget(self.page_size_combo)
        
        # 导出质量
        layout.addWidget(QLabel('质量:'))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(['标准质量', '高质量', '最小文件'])
        self.quality_combo.setCurrentText('标准质量')
        layout.addWidget(self.quality_combo)
        
        # 压缩
        self.compress_checkbox = QCheckBox('压缩')
        self.compress_checkbox.setChecked(True)
        layout.addWidget(self.compress_checkbox)
        
        # 嵌入字体
        self.embed_fonts_checkbox = QCheckBox('嵌入字体')
        self.embed_fonts_checkbox.setChecked(True)
        layout.addWidget(self.embed_fonts_checkbox)
        
        layout.addStretch()
        
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
        self.status_text.setMaximumHeight(120)
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
        export_btn = QPushButton('💾 开始导出')
        export_btn.setStyleSheet('background-color: #4CAF50; color: white; padding: 8px 16px;')
        export_btn.clicked.connect(self.batch_export)
        layout.addWidget(export_btn)
        
        return layout
    
    def add_files(self):
        """添加文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            '选择 Word 文档',
            '',
            'Word 文档 (*.docx)'
        )
        
        if files:
            for file in files:
                if file not in self.files:
                    self.files.append(file)
                    item = QListWidgetItem(os.path.basename(file))
                    item.setToolTip(file)
                    self.file_list.addItem(item)
            
            self.update_count()
            self.log_message(f'添加了 {len(files)} 个文件')
    
    def remove_selected(self):
        """移除选中文件"""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '警告', '请先选择要移除的文件')
            return
        
        for item in selected_items:
            row = self.file_list.row(item)
            if 0 <= row < len(self.files):
                self.files.pop(row)
            self.file_list.takeItem(row)
        
        self.update_count()
        self.log_message(f'移除了 {len(selected_items)} 个文件')
    
    def clear_list(self):
        """清空列表"""
        reply = QMessageBox.question(
            self,
            '确认清空',
            '确定要清空文件列表吗？',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.file_list.clear()
            self.files = []
            self.update_count()
            self.log_message('已清空文件列表')
    
    def update_count(self):
        """更新文件计数"""
        self.count_label.setText(f'共 {len(self.files)} 个文件')
    
    def log_message(self, message: str):
        """记录日志消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.status_text.append(f'[{timestamp}] {message}')
    
    def get_export_options(self) -> PDFExportOptions:
        """获取导出选项"""
        options = PDFExportOptions()
        options.page_size = self.page_size_combo.currentText()
        
        quality_map = {
            '标准质量': 'standard',
            '高质量': 'high',
            '最小文件': 'minimum'
        }
        options.quality = quality_map.get(self.quality_combo.currentText(), 'standard')
        
        options.compress = self.compress_checkbox.isChecked()
        options.embed_fonts = self.embed_fonts_checkbox.isChecked()
        
        return options
    
    def batch_export(self):
        """批量导出"""
        if not self.files:
            QMessageBox.warning(self, '警告', '请先添加要导出的文件')
            return
        
        # 选择输出目录
        output_dir = QFileDialog.getExistingDirectory(
            self,
            '选择 PDF 保存目录'
        )
        
        if not output_dir:
            return
        
        self.log_message(f'开始批量导出...')
        self.log_message(f'文件数量：{len(self.files)}')
        self.log_message(f'保存目录：{output_dir}')
        
        # 获取选项
        options = self.get_export_options()
        self.log_message(f'页面大小：{options.page_size}')
        self.log_message(f'质量：{options.quality}')
        
        # 更新进度条
        self.progress_bar.setMaximum(len(self.files))
        self.progress_bar.setValue(0)
        
        # 导出统计
        success_count = 0
        failed_count = 0
        
        # 开始导出
        for i, docx_path in enumerate(self.files):
            try:
                # 生成 PDF 文件名
                base_name = os.path.splitext(os.path.basename(docx_path))[0]
                pdf_path = os.path.join(output_dir, f'{base_name}.pdf')
                
                self.log_message(f'[{i+1}/{len(self.files)}] 导出：{os.path.basename(docx_path)}')
                
                # 导出 PDF
                success = self.exporter.export_docx_to_pdf(docx_path, pdf_path, options.to_dict())
                
                if success:
                    success_count += 1
                    self.log_message(f'  ✅ 成功：{pdf_path}')
                else:
                    failed_count += 1
                    self.log_message(f'  ❌ 失败')
                
                # 更新进度条
                self.progress_bar.setValue(i + 1)
                
            except Exception as e:
                failed_count += 1
                self.log_message(f'  ❌ 错误：{str(e)}')
                self.progress_bar.setValue(i + 1)
        
        # 导出完成
        self.log_message('=' * 50)
        self.log_message(f'批量导出完成！')
        self.log_message(f'成功：{success_count} 个')
        self.log_message(f'失败：{failed_count} 个')
        
        # 显示结果
        QMessageBox.information(
            self,
            '批量导出完成',
            f'✅ 批量导出完成！\n\n'
            f'成功：{success_count} 个\n'
            f'失败：{failed_count} 个\n\n'
            f'保存目录：{output_dir}'
        )
        
        self.accept()
