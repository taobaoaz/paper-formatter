"""
配置快照管理对话框
Configuration Snapshot Dialog

版本：v2.1.6
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QListWidget, QListWidgetItem, QTextEdit, QGroupBox,
                             QMessageBox, QFileDialog, QLineEdit, QCheckBox,
                             QComboBox, QInputDialog, QSplitter, QTableWidget,
                             QTableWidgetItem, QHeaderView, QTreeWidget)
from PyQt5.QtCore import Qt
from datetime import datetime
from config_snapshot import ConfigSnapshotManager


class ConfigSnapshotDialog(QDialog):
    """配置快照管理对话框"""
    
    def __init__(self, config=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('⚙️ 配置快照管理')
        self.setMinimumSize(850, 650)
        
        self.current_config = config
        self.snapshot_manager = ConfigSnapshotManager()
        self.selected_snapshot = None
        
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
        
        # 主内容区（分割器）
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：快照列表
        left_panel = self.create_snapshot_list()
        splitter.addWidget(left_panel)
        
        # 右侧：详情面板
        right_panel = self.create_detail_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([350, 500])
        
        layout.addWidget(splitter)
        
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
        
        # 从当前配置创建
        if self.current_config:
            create_current_btn = QPushButton('📋 从当前配置创建')
            create_current_btn.setStyleSheet('background-color: #2196F3; color: white; padding: 8px 16px;')
            create_current_btn.clicked.connect(self.create_from_current)
            layout.addWidget(create_current_btn)
        
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
        self.search_input.setPlaceholderText('输入名称、描述或标签...')
        self.search_input.textChanged.connect(self.filter_snapshots)
        layout.addWidget(self.search_input, stretch=2)
        
        # 标签过滤
        layout.addWidget(QLabel('标签:'))
        self.tag_filter = QComboBox()
        self.tag_filter.setEditable(True)
        self.tag_filter.setPlaceholderText('选择或输入标签')
        self.tag_filter.currentTextChanged.connect(self.filter_snapshots)
        self.load_tag_filter()
        layout.addWidget(self.tag_filter)
        
        # 显示数量
        self.count_label = QLabel('共 0 个快照')
        self.count_label.setStyleSheet('color: #666; font-weight: bold;')
        layout.addWidget(self.count_label)
        
        return group
    
    def create_snapshot_list(self):
        """创建快照列表"""
        group = QGroupBox('📋 快照列表')
        layout = QVBoxLayout(group)
        
        self.snapshot_list = QListWidget()
        self.snapshot_list.setSelectionMode(QListWidget.SingleSelection)
        self.snapshot_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.snapshot_list.itemDoubleClicked.connect(self.restore_snapshot)
        layout.addWidget(self.snapshot_list)
        
        return group
    
    def create_detail_panel(self):
        """创建详情面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 详情
        detail_group = self.create_detail_group()
        layout.addWidget(detail_group)
        
        # 配置预览
        preview_group = self.create_preview_group()
        layout.addWidget(preview_group)
        
        return panel
    
    def create_detail_group(self):
        """创建详情组"""
        group = QGroupBox('📊 快照详情')
        layout = QVBoxLayout(group)
        
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMaximumHeight(200)
        self.detail_text.setStyleSheet('background-color: #f5f5f5; font-family: monospace;')
        layout.addWidget(self.detail_text)
        
        return group
    
    def create_preview_group(self):
        """创建配置预览组"""
        group = QGroupBox('⚙️ 配置预览')
        layout = QVBoxLayout(group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet('background-color: #fafafa; font-family: Consolas, monospace; font-size: 11px;')
        layout.addWidget(self.preview_text)
        
        return group
    
    def create_button_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        
        # 导入
        import_btn = QPushButton('📥 导入配置')
        import_btn.clicked.connect(self.import_snapshot)
        layout.addWidget(import_btn)
        
        # 导出
        self.export_btn = QPushButton('📤 导出配置')
        self.export_btn.clicked.connect(self.export_snapshot)
        self.export_btn.setEnabled(False)
        layout.addWidget(self.export_btn)
        
        layout.addStretch()
        
        # 恢复
        self.restore_btn = QPushButton('↩️ 恢复此配置')
        self.restore_btn.setStyleSheet('background-color: #2196F3; color: white; padding: 8px 16px;')
        self.restore_btn.clicked.connect(self.restore_snapshot)
        self.restore_btn.setEnabled(False)
        layout.addWidget(self.restore_btn)
        
        # 比较
        self.compare_btn = QPushButton('📊 比较差异')
        self.compare_btn.clicked.connect(self.compare_snapshots)
        self.compare_btn.setEnabled(False)
        layout.addWidget(self.compare_btn)
        
        # 删除
        self.delete_btn = QPushButton('🗑️ 删除快照')
        self.delete_btn.setStyleSheet('background-color: #f44336; color: white; padding: 8px 16px;')
        self.delete_btn.clicked.connect(self.delete_snapshot)
        self.delete_btn.setEnabled(False)
        layout.addWidget(self.delete_btn)
        
        return layout
    
    def load_tag_filter(self):
        """加载标签过滤器"""
        self.tag_filter.clear()
        self.tag_filter.addItem('全部标签', '')
        
        # 收集所有标签
        all_tags = set()
        snapshots = self.snapshot_manager.list_snapshots()
        for snapshot in snapshots:
            all_tags.update(snapshot.tags)
        
        # 添加标签
        for tag in sorted(all_tags):
            self.tag_filter.addItem(f'🏷️ {tag}', tag)
    
    def load_snapshots(self):
        """加载快照列表"""
        self.snapshot_list.clear()
        
        # 获取所有快照
        snapshots = self.snapshot_manager.list_snapshots()
        
        # 应用过滤
        filtered = self.apply_filters(snapshots)
        
        # 填充列表
        for snapshot in filtered:
            item_text = f"📋 {snapshot.name}"
            if snapshot.description:
                item_text += f" - {snapshot.description}"
            if snapshot.tags:
                item_text += f" [{', '.join(snapshot.tags)}]"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, snapshot)
            item.setToolTip(f"创建时间：{snapshot.get_display_time()}\n标签：{snapshot.get_tags_str()}")
            self.snapshot_list.addItem(item)
        
        # 更新计数
        self.count_label.setText(f'共 {len(filtered)} 个快照')
        
        # 清空选择
        self.selected_snapshot = None
        self.update_button_state()
        self.detail_text.clear()
        self.preview_text.clear()
    
    def apply_filters(self, snapshots):
        """应用过滤条件"""
        filtered = snapshots
        
        # 搜索过滤
        search_text = self.search_input.text().lower()
        if search_text:
            filtered = [
                s for s in filtered
                if search_text in s.name.lower()
                or search_text in (s.description or '').lower()
                or any(search_text in tag.lower() for tag in s.tags)
            ]
        
        # 标签过滤
        tag = self.tag_filter.currentData()
        if tag:
            filtered = [s for s in filtered if tag in s.tags]
        
        return filtered
    
    def filter_snapshots(self):
        """过滤快照"""
        self.load_snapshots()
    
    def on_selection_changed(self):
        """选择变化时的处理"""
        selected_items = self.snapshot_list.selectedItems()
        if not selected_items:
            self.selected_snapshot = None
            self.update_button_state()
            self.detail_text.clear()
            self.preview_text.clear()
            return
        
        # 获取选中的快照
        self.selected_snapshot = selected_items[0].data(Qt.UserRole)
        
        # 更新按钮状态
        self.update_button_state()
        
        # 显示详情
        self.show_detail()
        self.show_preview()
    
    def update_button_state(self):
        """更新按钮状态"""
        has_selection = self.selected_snapshot is not None
        self.export_btn.setEnabled(has_selection)
        self.restore_btn.setEnabled(has_selection)
        self.compare_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    
    def show_detail(self):
        """显示详情"""
        if not self.selected_snapshot:
            return
        
        snapshot = self.selected_snapshot
        detail = f"""
📋 配置快照详情
━━━━━━━━━━━━━━━━━━━━━━━━

📝 名称：{snapshot.name}
📄 描述：{snapshot.description or '(无描述)'}
⏰ 创建时间：{snapshot.get_display_time()}
🏷️ 标签：{snapshot.get_tags_str()}
🔖 版本：{snapshot.version}
📊 配置项：{len(snapshot.config)} 个

配置结构:
{self.format_config_structure(snapshot.config)}
"""
        self.detail_text.setPlainText(detail)
    
    def format_config_structure(self, config, indent=0):
        """格式化配置结构"""
        lines = []
        prefix = '  ' * indent
        
        for key, value in sorted(config.items()):
            if isinstance(value, dict):
                lines.append(f'{prefix}📁 {key}:')
                lines.extend(self.format_config_structure(value, indent + 1).split('\n'))
            else:
                lines.append(f'{prefix}• {key}: {value}')
        
        return '\n'.join(lines)
    
    def show_preview(self):
        """显示配置预览"""
        if not self.selected_snapshot:
            return
        
        import json
        preview = json.dumps(self.selected_snapshot.config, indent=2, ensure_ascii=False)
        self.preview_text.setPlainText(preview)
    
    def create_snapshot(self):
        """创建快照"""
        # 输入名称
        name, ok = QInputDialog.getText(
            self,
            '创建配置快照',
            '请输入快照名称:',
            text='我的配置'
        )
        
        if not ok or not name:
            return
        
        # 输入描述
        description, ok = QInputDialog.getText(
            self,
            '创建配置快照',
            '请输入描述（可选）:',
        )
        
        if not ok:
            return
        
        # 输入标签
        tags_text, ok = QInputDialog.getText(
            self,
            '创建配置快照',
            '请输入标签（用逗号分隔，可选）:',
            text='个人，常用'
        )
        
        if not ok:
            return
        
        tags = [t.strip() for t in tags_text.split(',') if t.strip()] if tags_text else []
        
        # 创建空配置或从示例创建
        config = self.get_sample_config()
        
        try:
            snapshot = self.snapshot_manager.create_snapshot(
                name=name,
                config=config,
                description=description or '',
                tags=tags
            )
            
            QMessageBox.information(
                self,
                '成功',
                f'✅ 配置快照创建成功!\n\n名称：{snapshot.name}\n时间：{snapshot.get_display_time()}'
            )
            
            # 刷新列表
            self.load_tag_filter()
            self.load_snapshots()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 创建失败:\n{str(e)}'
            )
    
    def create_from_current(self):
        """从当前配置创建"""
        if not self.current_config:
            QMessageBox.warning(self, '警告', '当前没有可用的配置')
            return
        
        # 输入名称
        name, ok = QInputDialog.getText(
            self,
            '创建配置快照',
            '请输入快照名称:',
            text='当前配置'
        )
        
        if not ok or not name:
            return
        
        # 输入描述
        description, ok = QInputDialog.getText(
            self,
            '创建配置快照',
            '请输入描述（可选）:',
        )
        
        if not ok:
            return
        
        # 输入标签
        tags_text, ok = QInputDialog.getText(
            self,
            '创建配置快照',
            '请输入标签（用逗号分隔，可选）:',
            text='当前，活动'
        )
        
        if not ok:
            return
        
        tags = [t.strip() for t in tags_text.split(',') if t.strip()] if tags_text else []
        
        try:
            snapshot = self.snapshot_manager.create_snapshot(
                name=name,
                config=self.current_config,
                description=description or '',
                tags=tags
            )
            
            QMessageBox.information(
                self,
                '成功',
                f'✅ 配置快照创建成功!\n\n名称：{snapshot.name}\n配置项：{len(snapshot.config)} 个'
            )
            
            # 刷新列表
            self.load_tag_filter()
            self.load_snapshots()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 创建失败:\n{str(e)}'
            )
    
    def get_sample_config(self):
        """获取示例配置"""
        return {
            'font': {
                'chinese_font': '宋体',
                'english_font': 'Times New Roman',
                'font_size': 10.5
            },
            'page': {
                'paper_size': 'A4',
                'margin_top': 2.54,
                'margin_bottom': 2.54,
                'margin_left': 3.17,
                'margin_right': 3.17
            },
            'paragraph': {
                'line_spacing': 1.5,
                'space_before': 0,
                'space_after': 0
            }
        }
    
    def restore_snapshot(self):
        """恢复快照"""
        if not self.selected_snapshot:
            return
        
        # 确认对话框
        reply = QMessageBox.question(
            self,
            '确认恢复',
            f'⚠️ 确定要恢复此配置吗？\n\n名称：{self.selected_snapshot.name}\n创建时间：{self.selected_snapshot.get_display_time()}\n\n当前配置将会被替换!',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        try:
            # 恢复配置
            config = self.snapshot_manager.restore_snapshot(self.selected_snapshot.name)
            
            QMessageBox.information(
                self,
                '成功',
                f'✅ 配置恢复成功!\n\n已恢复：{self.selected_snapshot.name}\n配置项：{len(config)} 个'
            )
            
            # 通知父窗口
            if self.parent() and hasattr(self.parent(), 'load_config'):
                self.parent().load_config(config)
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 恢复失败:\n{str(e)}'
            )
    
    def compare_snapshots(self):
        """比较快照"""
        if not self.selected_snapshot:
            return
        
        # 选择另一个快照进行比较
        snapshots = self.snapshot_manager.list_snapshots()
        if len(snapshots) < 2:
            QMessageBox.warning(self, '警告', '至少需要两个快照才能进行比较')
            return
        
        # 创建选择对话框
        from PyQt5.QtWidgets import QInputDialog
        names = [s.name for s in snapshots if s.name != self.selected_snapshot.name]
        
        other_name, ok = QInputDialog.getItem(
            self,
            '选择比较对象',
            '选择要比较的另一个快照:',
            names,
            0,
            False
        )
        
        if not ok or not other_name:
            return
        
        try:
            other_snapshot = self.snapshot_manager.get_snapshot(other_name)
            diff = self.snapshot_manager.compare_snapshots(self.selected_snapshot.name, other_name)
            
            # 显示差异
            diff_text = self.format_diff(diff)
            
            QMessageBox.information(
                self,
                '比较结果',
                diff_text
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 比较失败:\n{str(e)}'
            )
    
    def format_diff(self, diff):
        """格式化差异"""
        if not diff:
            return '✅ 两个配置完全相同'
        
        lines = ['📊 配置差异比较:\n']
        
        for section, changes in diff.items():
            lines.append(f'\n📁 [{section}]')
            for key, (before, after) in changes.items():
                lines.append(f'  {key}: {before} → {after}')
        
        return '\n'.join(lines)
    
    def export_snapshot(self):
        """导出快照"""
        if not self.selected_snapshot:
            return
        
        # 选择保存位置
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '导出配置',
            f'{self.selected_snapshot.name}.json',
            'JSON 文件 (*.json);;所有文件 (*)'
        )
        
        if not file_path:
            return
        
        try:
            self.snapshot_manager.export_snapshot(self.selected_snapshot.name, file_path)
            
            QMessageBox.information(
                self,
                '成功',
                f'✅ 配置导出成功!\n\n保存到：{file_path}'
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 导出失败:\n{str(e)}'
            )
    
    def import_snapshot(self):
        """导入快照"""
        # 选择文件
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '导入配置',
            '',
            'JSON 文件 (*.json);;所有文件 (*)'
        )
        
        if not file_path:
            return
        
        try:
            snapshot = self.snapshot_manager.import_snapshot(file_path)
            
            QMessageBox.information(
                self,
                '成功',
                f'✅ 配置导入成功!\n\n名称：{snapshot.name}\n配置项：{len(snapshot.config)} 个'
            )
            
            # 刷新列表
            self.load_tag_filter()
            self.load_snapshots()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 导入失败:\n{str(e)}'
            )
    
    def delete_snapshot(self):
        """删除快照"""
        if not self.selected_snapshot:
            return
        
        # 确认对话框
        reply = QMessageBox.question(
            self,
            '确认删除',
            f'⚠️ 确定要删除此配置快照吗？\n\n名称：{self.selected_snapshot.name}\n创建时间：{self.selected_snapshot.get_display_time()}\n\n此操作不可恢复!',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        try:
            self.snapshot_manager.delete_snapshot(self.selected_snapshot.name)
            
            QMessageBox.information(
                self,
                '成功',
                '✅ 配置快照已删除'
            )
            
            # 刷新列表
            self.load_tag_filter()
            self.load_snapshots()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                '错误',
                f'❌ 删除失败:\n{str(e)}'
            )


# 需要导入 QWidget
from PyQt5.QtWidgets import QWidget
