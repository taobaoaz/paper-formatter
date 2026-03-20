"""
自动备份设置对话框
Auto Backup Settings Dialog

版本：v2.1.9
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QCheckBox, QSpinBox, QComboBox, QGroupBox, QMessageBox,
                             QFormLayout)
from PyQt5.QtCore import Qt
from auto_backup import BackupConfig


class AutoBackupSettingsDialog(QDialog):
    """自动备份设置对话框"""
    
    # 备份间隔选项（分钟）
    INTERVAL_OPTIONS = [5, 10, 15, 20, 30, 45, 60]
    
    def __init__(self, config: BackupConfig = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('⚙️ 自动备份设置')
        self.setMinimumSize(500, 400)
        
        self.config = config or BackupConfig()
        self.result_config = None  # 保存时返回的配置
        
        self.init_ui()
        self.load_config_to_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 启用开关
        enable_group = self.create_enable_group()
        layout.addWidget(enable_group)
        
        # 备份间隔
        interval_group = self.create_interval_group()
        layout.addWidget(interval_group)
        
        # 清理策略
        cleanup_group = self.create_cleanup_group()
        layout.addWidget(cleanup_group)
        
        # 通知设置
        notify_group = self.create_notify_group()
        layout.addWidget(notify_group)
        
        # 底部按钮
        button_layout = self.create_button_layout()
        layout.addLayout(button_layout)
    
    def create_enable_group(self):
        """创建启用开关组"""
        group = QGroupBox('🔌 自动备份开关')
        layout = QVBoxLayout(group)
        
        self.enable_checkbox = QCheckBox('启用自动备份')
        self.enable_checkbox.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.enable_checkbox.setToolTip('启用后，系统会定期自动创建文档快照')
        layout.addWidget(self.enable_checkbox)
        
        desc_label = QLabel(
            '💡 提示：启用自动备份可以防止意外丢失数据。\n'
            '系统会在后台定期创建文档快照，无需手动操作。'
        )
        desc_label.setStyleSheet('color: #666; font-size: 12px;')
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return group
    
    def create_interval_group(self):
        """创建备份间隔组"""
        group = QGroupBox('⏰ 备份间隔')
        layout = QFormLayout(group)
        
        # 间隔选择
        self.interval_combo = QComboBox()
        for minutes in self.INTERVAL_OPTIONS:
            if minutes < 60:
                text = f'{minutes} 分钟'
            else:
                text = f'{minutes // 60} 小时'
            self.interval_combo.addItem(text, minutes)
        
        self.interval_combo.setToolTip('选择自动备份的时间间隔')
        layout.addRow('备份间隔:', self.interval_combo)
        
        # 说明
        interval_desc = QLabel(
            '💡 建议设置：\n'
            '• 频繁编辑：5-10 分钟\n'
            '• 正常编辑：10-15 分钟\n'
            '• 偶尔编辑：30-60 分钟'
        )
        interval_desc.setStyleSheet('color: #666; font-size: 11px;')
        interval_desc.setWordWrap(True)
        layout.addRow(interval_desc)
        
        return group
    
    def create_cleanup_group(self):
        """创建清理策略组"""
        group = QGroupBox('🧹 智能清理策略')
        layout = QFormLayout(group)
        
        # 保留数量
        self.keep_count_spin = QSpinBox()
        self.keep_count_spin.setRange(5, 100)
        self.keep_count_spin.setValue(20)
        self.keep_count_spin.setToolTip('保留最近 N 个快照')
        layout.addRow('保留最近数量:', self.keep_count_spin)
        
        # 保留时间
        self.keep_hours_spin = QSpinBox()
        self.keep_hours_spin.setRange(1, 168)  # 1 小时到 7 天
        self.keep_hours_spin.setValue(24)
        self.keep_hours_spin.setToolTip('保留 N 小时内的快照')
        layout.addRow('保留时间 (小时):', self.keep_hours_spin)
        
        # 重要快照保护
        self.keep_important_checkbox = QCheckBox('保护重要快照（不被自动清理）')
        self.keep_important_checkbox.setChecked(True)
        self.keep_important_checkbox.setToolTip('标记为重要的快照永远不会被自动清理')
        layout.addRow(self.keep_important_checkbox)
        
        # 说明
        cleanup_desc = QLabel(
            '💡 清理规则：\n'
            '• 保留最近 N 个快照\n'
            '• 保留 N 小时内的快照\n'
            '• 重要快照永久保留\n'
            '• 满足任一条件即保留'
        )
        cleanup_desc.setStyleSheet('color: #666; font-size: 11px;')
        cleanup_desc.setWordWrap(True)
        layout.addRow(cleanup_desc)
        
        return group
    
    def create_notify_group(self):
        """创建通知设置组"""
        group = QGroupBox('🔔 通知设置')
        layout = QVBoxLayout(group)
        
        self.notify_checkbox = QCheckBox('备份完成后显示通知')
        self.notify_checkbox.setToolTip('每次自动备份完成后在状态栏显示提示')
        layout.addWidget(self.notify_checkbox)
        
        notify_desc = QLabel(
            '💡 通知只在状态栏显示，不会弹窗打扰。\n'
            '可以在状态栏查看备份状态和下次备份时间。'
        )
        notify_desc.setStyleSheet('color: #666; font-size: 11px;')
        notify_desc.setWordWrap(True)
        layout.addWidget(notify_desc)
        
        return group
    
    def create_button_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        layout.addStretch()
        
        # 重置
        reset_btn = QPushButton('🔄 重置为默认')
        reset_btn.clicked.connect(self.reset_to_default)
        layout.addWidget(reset_btn)
        
        # 取消
        cancel_btn = QPushButton('❌ 取消')
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        # 保存
        save_btn = QPushButton('💾 保存')
        save_btn.setStyleSheet('background-color: #4CAF50; color: white; padding: 8px 16px;')
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)
        
        return layout
    
    def load_config_to_ui(self):
        """加载配置到 UI"""
        # 启用状态
        self.enable_checkbox.setChecked(self.config.enabled)
        
        # 备份间隔
        index = self.interval_combo.findData(self.config.interval_minutes)
        if index >= 0:
            self.interval_combo.setCurrentIndex(index)
        
        # 清理策略
        self.keep_count_spin.setValue(self.config.keep_recent_count)
        self.keep_hours_spin.setValue(self.config.keep_hours)
        self.keep_important_checkbox.setChecked(self.config.keep_important)
        
        # 通知设置
        self.notify_checkbox.setChecked(self.config.notify_on_backup)
    
    def reset_to_default(self):
        """重置为默认配置"""
        reply = QMessageBox.question(
            self,
            '确认重置',
            '确定要重置为默认配置吗？\n\n所有自定义设置将会丢失。',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 创建默认配置
        default_config = BackupConfig()
        
        # 加载到 UI
        self.config = default_config
        self.load_config_to_ui()
        
        QMessageBox.information(
            self,
            '成功',
            '已重置为默认配置'
        )
    
    def get_config_from_ui(self) -> BackupConfig:
        """从 UI 获取配置"""
        config = BackupConfig()
        
        # 启用状态
        config.enabled = self.enable_checkbox.isChecked()
        
        # 备份间隔
        config.interval_minutes = self.interval_combo.currentData()
        
        # 清理策略
        config.keep_recent_count = self.keep_count_spin.value()
        config.keep_hours = self.keep_hours_spin.value()
        config.keep_important = self.keep_important_checkbox.isChecked()
        
        # 通知设置
        config.notify_on_backup = self.notify_checkbox.isChecked()
        
        return config
    
    def save_config(self):
        """保存配置"""
        # 获取 UI 配置
        self.result_config = self.get_config_from_ui()
        
        # 验证配置
        if self.result_config.enabled:
            reply = QMessageBox.question(
                self,
                '确认启用',
                f'确定要启用自动备份吗？\n\n'
                f'• 备份间隔：{self.result_config.interval_minutes} 分钟\n'
                f'• 保留数量：{self.result_config.keep_recent_count} 个\n'
                f'• 保留时间：{self.result_config.keep_hours} 小时\n\n'
                f'系统会在后台定期自动创建快照。',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply != QMessageBox.Yes:
                return
        
        # 保存成功
        QMessageBox.information(
            self,
            '成功',
            '✅ 自动备份配置已保存\n\n' +
            ('自动备份已启用' if self.result_config.enabled else '自动备份已禁用')
        )
        
        self.accept()
    
    def get_config(self) -> BackupConfig:
        """获取保存的配置"""
        return self.result_config
