"""
批量处理对话框
Batch Processor Dialog
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QListWidget, QListWidgetItem, QFileDialog, QProgressBar,
                             QTextEdit, QMessageBox, QGroupBox, QCheckBox, QLineEdit)
from PyQt5.QtCore import Qt
from batch_processor import BatchProcessor, BatchReport
from file_backup import FileBackup


class BatchProcessorDialog(QDialog):
    """批量处理对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('批量处理')
        self.setMinimumSize(700, 600)
        
        self.files = []
        self.processor = BatchProcessor()
        self.backup = FileBackup()
        
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 文件列表
        file_group = QGroupBox('文件列表')
        file_layout = QVBoxLayout(file_group)
        
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        file_layout.addWidget(self.file_list)
        
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
        file_layout.addLayout(btn_layout)
        
        layout.addWidget(file_group)
        
        # 选项
        option_group = QGroupBox('选项')
        option_layout = QHBoxLayout(option_group)
        
        self.backup_check = QCheckBox('格式化前自动备份')
        self.backup_check.setChecked(True)
        option_layout.addWidget(self.backup_check)
        
        option_layout.addStretch()
        
        layout.addWidget(option_group)
        
        # 进度条
        progress_group = QGroupBox('处理进度')
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel('就绪')
        self.progress_label.setStyleSheet('color: #666;')
        progress_layout.addWidget(self.progress_label)
        
        layout.addWidget(progress_group)
        
        # 日志
        log_group = QGroupBox('处理日志')
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.start_btn = QPushButton('🚀 开始处理')
        self.start_btn.setStyleSheet('background-color: #667eea; color: white; padding: 10px 30px; font-size: 14px; font-weight: bold;')
        self.start_btn.clicked.connect(self.start_processing)
        button_layout.addWidget(self.start_btn)
        
        self.cancel_btn = QPushButton('❌ 取消')
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_processing)
        button_layout.addWidget(self.cancel_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def connect_signals(self):
        """连接信号"""
        self.processor.progress.connect(self.on_progress)
        self.processor.file_completed.connect(self.on_file_completed)
        self.processor.batch_completed.connect(self.on_batch_completed)
        self.processor.error.connect(self.on_error)
    
    def add_files(self):
        """添加文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            '选择文件',
            '',
            'Word 文件 (*.docx);;所有文件 (*)'
        )
        
        for file in files:
            if file not in self.files:
                self.files.append(file)
                item = QListWidgetItem(file)
                item.setToolTip(file)
                self.file_list.addItem(item)
        
        self.log(f'添加了 {len(files)} 个文件')
    
    def remove_selected(self):
        """移除选中"""
        selected_items = self.file_list.selectedItems()
        for item in selected_items:
            row = self.file_list.row(item)
            if 0 <= row < len(self.files):
                self.files.pop(row)
            self.file_list.takeItem(row)
        
        self.log(f'移除了 {len(selected_items)} 个文件')
    
    def clear_list(self):
        """清空列表"""
        self.file_list.clear()
        self.files = []
        self.log('已清空列表')
    
    def start_processing(self):
        """开始处理"""
        if not self.files:
            QMessageBox.warning(self, '警告', '请先添加文件')
            return
        
        # 禁用按钮
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        
        # 重置进度
        self.progress_bar.setValue(0)
        self.log_text.clear()
        
        self.log(f'开始处理 {len(self.files)} 个文件...')
        
        # 这里调用实际的处理函数
        # 为了演示，我们使用一个简单的复制函数
        def dummy_process(file_path, output_path):
            import shutil
            shutil.copy2(file_path, output_path)
            return True
        
        # 启动处理线程
        import threading
        thread = threading.Thread(target=self.process_files, args=(dummy_process,))
        thread.daemon = True
        thread.start()
    
    def process_files(self, process_func):
        """处理文件（在后台线程）"""
        total = len(self.files)
        success = 0
        fail = 0
        
        for i, file_path in enumerate(self.files):
            if self.processor.cancelled:
                break
            
            file_name = file_path.split('/')[-1]
            
            # 更新进度（使用 Qt 的信号槽）
            from PyQt5.QtCore import QMetaObject, Qt
            QMetaObject.invokeMethod(
                self.progress_bar,
                'setValue',
                Qt.QueuedConnection,
                ('i', int((i + 1) / total * 100))
            )
            
            QMetaObject.invokeMethod(
                self.progress_label,
                'setText',
                Qt.QueuedConnection,
                ('s', f'处理中：{file_name}')
            )
            
            try:
                # 备份
                if self.backup_check.isChecked():
                    backup_path = self.backup.backup_file(file_path)
                    if backup_path:
                        QMetaObject.invokeMethod(
                            self,
                            'log',
                            Qt.QueuedConnection,
                            ('s', f'✓ 已备份：{file_name}')
                        )
                
                # 处理
                output_path = file_path  # 这里应该根据实际需求修改
                success_flag = process_func(file_path, output_path)
                
                if success_flag:
                    success += 1
                    QMetaObject.invokeMethod(
                        self,
                        'log',
                        Qt.QueuedConnection,
                        ('s', f'✓ 成功：{file_name}')
                    )
                else:
                    fail += 1
                    QMetaObject.invokeMethod(
                        self,
                        'log',
                        Qt.QueuedConnection,
                        ('s', f'✗ 失败：{file_name}')
                    )
                    
            except Exception as e:
                fail += 1
                QMetaObject.invokeMethod(
                    self,
                    'log',
                    Qt.QueuedConnection,
                    ('s', f'✗ 错误：{file_name} - {str(e)}')
                )
        
        # 完成
        QMetaObject.invokeMethod(
            self,
            'on_processing_done',
            Qt.QueuedConnection,
            ('i', success),
            ('i', fail)
        )
    
    def on_processing_done(self, success, fail):
        """处理完成"""
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        
        self.log(f'\n处理完成！成功：{success}, 失败：{fail}')
        QMessageBox.information(
            self,
            '完成',
            f'批量处理完成！\n成功：{success}\n失败：{fail}'
        )
    
    def cancel_processing(self):
        """取消处理"""
        self.processor.cancel()
        self.log('正在取消...')
    
    def log(self, message):
        """添加日志"""
        self.log_text.append(message)
        # 滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_progress(self, current, total, file_name):
        """进度更新"""
        self.progress_bar.setValue(int(current / total * 100))
        self.progress_label.setText(f'处理中：{file_name}')
    
    def on_file_completed(self, file_name, success, message):
        """文件处理完成"""
        status = '✓' if success else '✗'
        self.log(f'{status} {file_name}: {message}')
    
    def on_batch_completed(self, success, fail):
        """批量处理完成"""
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.log(f'\n批量处理完成！成功：{success}, 失败：{fail}')
    
    def on_error(self, error_msg):
        """错误"""
        self.log(f'错误：{error_msg}')
