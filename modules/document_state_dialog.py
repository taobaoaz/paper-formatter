"""
文档状态快照管理对话框
Document State Snapshot Dialog

版本：v2.1.6
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
                             QMessageBox, QFileDialog, QHeaderView, QLineEdit,
                             QCheckBox, QComboBox)
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from datetime import datetime
from document_state import DocumentStateManager


class DocumentStateDialog(QDialog):
    """文档状态快照管理对话框"""
    
    def __init__(self, file_path=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('📸 文档快照管理')
        self.setMinimumSize(800, 600)
        
        self.file_path = file_path
        self.state_manager = DocumentStateManager()
        self.selected_state = None
        
        self.init_ui()
        self.load_snapshots()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 顶部工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 搜索和过滤
        filter_bar = self.create_filter_bar()
        layout.addWidget(filter_bar)
        
        # 快照列表
        list_group = self.create_snapshot_list()
        layout.addWidget(list_group)
        
        # 预览面板
        preview_group = self.create_preview_panel()
        layout.addWidget(preview_group)
        
        # 底部按钮
        button_layout = self.create_button_layout()
        layout.addLayout(button_layout)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QGroupBox('🛠️ 操作')
        layout = QHBoxLayout(toolbar)
        
        # 创建快照
        create_btn = QPushButton('➕ 创建快照')
        create_btn.setStyleSheet('background-color: #4CAF50; color: white; padding: 8px 16px;')
        create_btn.clicked.connect(self.create_snapshot)
        layout.addWidget(create_btn)
        
        # 刷新
        refresh_btn = QPushButton('🔄 刷新')
        refresh_btn.clicked.connect(self.load_snapshots)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
        
        # 关闭
        close_btn = QPushButton('❌ 关闭')
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)
        
        return toolbar
    
    def create_filter_bar(self):
        """创建过滤栏"""
        group = QGroupBox('🔍 搜索和过滤')
        layout = QHBoxLayout(group)
        
        # 搜索框
        layout.addWidget(QLabel('搜索:'))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('输入描述或文件名...')
        self.search_input.textChanged.connect(self.filter_snapshots)
        layout.addWidget(self.search_input)
        
        # 快照类型过滤
        layout.addWidget(QLabel('类型:'))
        self.type_filter = QComboBox()
        self.type_filter.addItem('全部', 'all')
        self.type_filter.addItem('完整快照', 'full')
        self.type_filter.addItem('增量快照', 'incremental')
        self.type_filter.currentIndexChanged.connect(self.filter_snapshots)
        layout.addWidget(self.type_filter)
        
        # 显示数量
        self.count_label = QLabel('共 0 个快照')
        self.count_label.setStyleSheet('color: #666; font-weight: bold;')
        layout.addWidget(self.count_label)
        
        return group
    
    def create_snapshot_list(self):
        """创建快照列表"""
        group = QGroupBox('📋 快照列表')
        layout = QVBoxLayout(group)
        
        self.snapshot_table = QTableWidget()
        self.snapshot_table.setColumnCount(5)
        self.snapshot_table.setHorizontalHeaderLabels([
            '时间', '文件名', '描述', '类型', '大小'
        ])
        
        # 设置列宽
        header = self.snapshot_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        # 选择行为
        self.snapshot_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.snapshot_table.setSelectionMode(QTableWidget.SingleSelection)
        self.snapshot_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.snapshot_table.itemSelectionChanged.connect(self.on_selection_changed)
        
        layout.addWidget(self.snapshot_table)
        
        return group
    
    def create_preview_panel(self):
        """创建预览面板"""
        group = QGroupBox('📊 快照详情')
        layout = QVBoxLayout(group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(150)
        self.preview_text.setStyleSheet('background-color: #f5f5f5; font-family: monospace;')
        layout.addWidget(self.preview_text)
        
        return group
    
    def create_button_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        layout.addStretch()
        
        # 恢复快照
        self.restore_btn = QPushButton('↩️ 恢复到此快照')
        self.restore_btn.setStyleSheet('background-color: #2196F3; color: white; padding: 8px 16px;')
        self.restore_btn.clicked.connect(self.restore_snapshot)
        self.restore_btn.setEnabled(False)
        layout.addWidget(self.restore_btn)
        
        # 删除快照
        self.delete_btn = QPushButton('🗑️ 删除快照')
        self.delete_btn.setStyleSheet('background-color: #f44336; color: white; padding: 8px 16px;')
        self.delete_btn.clicked.connect(self.delete_snapshot)
        self.delete_btn.setEnabled(False)
        layout.addWidget(self.delete_btn)
        
        return layout
    
    def load_snapshots(self):
        """加载快照列表"""
        self.snapshot_table.setRowCount(0)
        
        # 获取所有快照
        states = self.state_manager.get_states(limit=100)
        
        # 应用过滤
        filtered_states = self.apply_filters(states)
        
        # 填充表格
        for state in filtered_states:
            row = self.snapshot_table.rowCount()
            self.snapshot_table.insertRow(row)
            
            # 时间
            time_item = QTableWidgetItem(state.get_display_time())
            time_item.setData(Qt.UserRole, state)
            self.snapshot_table.setItem(row, 0, time_item)
            
            # 文件名
            import os
            filename = os.path.basename(state.file_path)
            self.snapshot_table.setItem(row, 1, QTableWidgetItem(filename))
            
            # 描述
            desc = state.description or '(无描述)'
            self.snapshot_table.setItem(row, 2, QTableWidgetItem(desc))
            
            # 类型
            type_text = '完整' if state.state_type == 'full' else '增量'
            self.snapshot_table.setItem(row, 3, QTableWidgetItem(type_text))
            
            # 大小
            size_kb = state.file_size / 1024
            size_text = f'{size_kb:.1f} KB' if size_kb < 1024 else f'{size_kb/1024:.1f} MB'
            self.snapshot_table.setItem(row, 4, QTableWidgetItem(size_text))
        
        # 更新计数
        self.count_label.setText(f'共 {len(filtered_states)} 个快照')
        
        # 清空选择
        self.selected_state = None
        self.update_button_state()
        self.preview_text.clear()
    
    def apply_filters(self, states):
        """应用过滤条件"""
        filtered = states
        
        # 搜索过滤
        search_text = self.search_input.text().lower()
        if search_text:
            filtered = [
                s for s in filtered
                if search_text in s.file_path.lower()
                or search_text in s.description.lower()
            ]
        
        # 类型过滤
        type_filter = self.type_filter.currentData()
        if type_filter != 'all':
            filtered = [s for s in filtered if s.state_type == type_filter]
        
        return filtered
    
    def filter_snapshots(self):
        """过滤快照"""
        self.load_snapshots()
    
    def on_selection_changed(self):
        """选择变化时的处理"""
        selected_rows = self.snapshot_table.selectedItems()
        if not selected_rows:
            self.selected_state = None
            self.update_button_state()
            self.preview_text.clear()
            return
        
        # 获取选中的状态
        row = selected_rows[0].row()
        self.selected_state = self.snapshot_table.item(row, 0).data(Qt.UserRole)
        
        # 更新按钮状态
        self.update_button_state()
        
        # 显示详情
        self.show_preview()
    
    def update_button_state(self):
        """更新按钮状态"""
        has_selection = self.selected_state is not None
        self.restore_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    
    def show_preview(self):
        """显示快照详情"""
        if not self.selected_state:
            return
        
        state = self.selected_state
        preview = f"""
📸 快照详情
━━━━━━━━━━━━━━━━━━━━━━━━

📁 文件路径：{state.file_path}
📝 描述：{state.description or '(无描述)'}
⏰ 创建时间：{state.get_display_time()}
📊 类型：{'完整快照' if state.state_type == 'full' else '增量快照'}
💾 大小：{state.file_size / 1024:.1f} KB
🔐 校验和：{state.checksum or '未计算'}

元数据:
{self.format_metadata(state.metadata)}
"""
        self.preview_text.setPlainText(preview)
    
    def format_metadata(self, metadata):
        """格式化元数据"""
        if not metadata:
            return '  (无)'
        
        lines = []
        for key, value in metadata.items():
            lines.append(f'  {key}: {value}')
        return '\n'.join(lines)
    
    def create_snapshot(self):
        """创建快照"""
        # 如果没有指定文件路径，让用户选择
        if not self.file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                '选择文档',
                '',
                'Word 文档 (*.docx);;所有文件 (*)'
            )
            if not file_path:
                return
        else:
            file_path = self.file_path
        
        # 输入描述
        from PyQt5.QtWidgets import QInputDialog
        description, ok = QInputDialog.getText(
            self,
            '创建快照',
            '请输入快照描述（可选）:',
            text=f'创建于 {datetime.now().strftime("%H:%M")}'
        )
        
        if not ok:
            return
        
        try:
            # 创建快照
            state = self.state_manager.create_snapshot(
                file_path=file_path,
                description=description or ''
            )
            
            QMessageBox.information(
                self,
                '成功',
                f'✅ 快照创建成功!\n\n文件：{state.file_path}\n时间：{state.get_display_time()}\n大小：{state.file_size / 1024:.1f} KB'
            )
            
            # 刷新列表
            self.load_snapshots()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 创建快照失败:\n{str(e)}'
            )
    
    def restore_snapshot(self):
        """恢复快照"""
        if not self.selected_state:
            return
        
        # 确认对话框
        reply = QMessageBox.question(
            self,
            '确认恢复',
            f'⚠️ 确定要恢复到此快照吗？\n\n时间：{self.selected_state.get_display_time()}\n描述：{self.selected_state.description or "(无)"}\n\n⚠️ 当前文档的未保存修改将会丢失!',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        try:
            # 恢复快照
            success = self.state_manager.restore_snapshot(self.selected_state)
            
            if success:
                QMessageBox.information(
                    self,
                    '成功',
                    f'✅ 快照恢复成功!\n\n已恢复到：{self.selected_state.get_display_time()}'
                )
                
                # 通知父窗口刷新
                if self.parent():
                    # 触发刷新事件（如果需要）
                    pass
                    
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    '警告',
                    '⚠️ 恢复失败，快照文件可能已损坏或丢失'
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 恢复失败:\n{str(e)}'
            )
    
    def delete_snapshot(self):
        """删除快照"""
        if not self.selected_state:
            return
        
        # 确认对话框
        reply = QMessageBox.question(
            self,
            '确认删除',
            f'⚠️ 确定要删除此快照吗？\n\n时间：{self.selected_state.get_display_time()}\n描述：{self.selected_state.description or "(无)"}\n\n此操作不可恢复!',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        try:
            # 删除快照
            self.state_manager.delete_snapshot(self.selected_state)
            
            QMessageBox.information(
                self,
                '成功',
                '✅ 快照已删除'
            )
            
            # 刷新列表
            self.load_snapshots()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 删除失败:\n{str(e)}'
            )
