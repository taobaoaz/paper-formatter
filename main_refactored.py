"""
论文排版优化器 - 主程序重构版
Paper Formatter - Refactored Main Program

集成封面声明页配置器和模板页面选择器
优化 UI 结构和代码组织
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QGroupBox,
    QFileDialog, QMessageBox, QProgressBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QSplitter, QFrame, QScrollArea,
    QDialog, QDialogButtonBox, QFormLayout, QSpinBox, QDoubleSpinBox,
    QCheckBox, QListWidget, QListWidgetItem, QStatusBar, QAction,
    QToolBar, QMenu, QMenuBar, QStackedWidget, QSizePolicy, QRadioButton,
    QButtonGroup
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer, QSettings
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QDesktopServices
from PyQt5.QtCore import QUrl
from typing import Dict, Any, Optional, List
import json
from datetime import datetime
import traceback

# 可选依赖
PYWINSTYLES_AVAILABLE = False
try:
    import pywinstyles
    PYWINSTYLES_AVAILABLE = True
except ImportError:
    pass

FLUENT_WIDGETS_AVAILABLE = False
try:
    from qfluentwidgets import (
        setTheme, Theme, setThemeColor, FluentWindow,
        PushButton, CardWidget, PrimaryPushButton,
        ComboBox, LineEdit, TextEdit, SpinBox, DoubleSpinBox,
        CheckBox, ListWidget, TableWidget, TabWidget, ScrollArea,
        TitleLabel, SubtitleLabel, BodyLabel, CaptionLabel
    )
    FLUENT_WIDGETS_AVAILABLE = True
except ImportError:
    pass

# 导入项目模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parsers import DocumentParserFactory, ParsedDocument
from ai_recognizer import AIRecognizer, TemplateRecognitionResult
from template_manager import TemplateManager, Template
from formatter import DocumentFormatter, OptimizationResult
from ai_prompt import generate_ai_prompt, parse_ai_response, ParsedTemplateData, get_quick_prompt_for_template_file
from document_generator import DocumentGenerator, get_fields_by_group, get_all_fields, DEFAULT_FIELDS, SECTION_TEMPLATES
from reference_formatter import ReferenceManager, ReferenceParser, ReferenceFormatter, ReferenceFormat
from error_handler import ErrorHandler, ErrorCode, create_error, get_error_message
from template_spec_parser import parse_template_spec
from word_format_extractor import extract_format_from_docx, WordFormatExtractor

# 新增：封面和声明页配置
from cover_declaration_config import CoverDeclarationConfigDialog, CoverDeclarationManager
from template_page_selector import TemplatePageSelectorDialog, TemplatePageManager

import config


# ============================================================================
# 工作线程类
# ============================================================================

class WorkerThread(QThread):
    """通用工作线程"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, task_func, *args, **kwargs):
        super().__init__()
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            result = self.task_func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


# ============================================================================
# 主窗口类
# ============================================================================

class PaperFormatterMainWindow(QMainWindow):
    """论文排版优化器主窗口"""
    
    def __init__(self):
        super().__init__()
        self.template_manager = TemplateManager()
        self.formatter = DocumentFormatter()
        self.current_template = None
        self.cover_config = None
        self.worker_thread = None
        
        self.init_ui()
        self.apply_modern_style()
        self.load_settings()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('论文排版优化器 v2.0 - 开发小助手')
        self.setMinimumSize(1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 1. 顶部工具栏
        self.create_toolbar()
        
        # 2. 主标签页
        self.main_tabs = QTabWidget()
        self.main_tabs.setTabPosition(QTabWidget.North)
        self.main_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # 创建各个标签页
        self.home_tab = self.create_home_tab()
        self.template_tab = self.create_template_tab()
        self.format_tab = self.create_format_tab()
        self.reference_tab = self.create_reference_tab()
        self.settings_tab = self.create_settings_tab()
        
        # 添加到标签页
        self.main_tabs.addTab(self.home_tab, '🏠 首页')
        self.main_tabs.addTab(self.template_tab, '📋 模板管理')
        self.main_tabs.addTab(self.format_tab, '📄 文档格式化')
        self.main_tabs.addTab(self.reference_tab, '📚 参考文献')
        self.main_tabs.addTab(self.settings_tab, '⚙️ 设置')
        
        main_layout.addWidget(self.main_tabs)
        
        # 3. 状态栏
        self.statusBar().showMessage('就绪')
        self.statusBar().setSizeGripEnabled(True)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar('主工具栏')
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # 文件操作
        new_action = QAction('📄 新建', self)
        new_action.triggered.connect(self.on_new_document)
        toolbar.addAction(new_action)
        
        open_action = QAction('📂 打开', self)
        open_action.triggered.connect(self.on_open_document)
        toolbar.addAction(open_action)
        
        save_action = QAction('💾 保存', self)
        save_action.triggered.connect(self.on_save_document)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # 工具
        cover_action = QAction('📘 封面配置', self)
        cover_action.triggered.connect(self.on_cover_declaration_config)
        toolbar.addAction(cover_action)
        
        template_action = QAction('📐 模板上传', self)
        template_action.triggered.connect(self.on_template_upload)
        toolbar.addAction(template_action)
        
        toolbar.addSeparator()
        
        # 帮助
        help_action = QAction('❓ 帮助', self)
        help_action.triggered.connect(self.on_help)
        toolbar.addAction(help_action)
        
        about_action = QAction('ℹ️ 关于', self)
        about_action.triggered.connect(self.on_about)
        toolbar.addAction(about_action)
    
    def create_home_tab(self) -> QWidget:
        """创建首页标签"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # 欢迎区域
        welcome_group = QGroupBox('🎓 欢迎使用论文排版优化器')
        welcome_layout = QVBoxLayout(welcome_group)
        
        welcome_label = QLabel(
            '论文排版优化器是一款专业的学术论文格式化工具。\n'
            '支持期刊论文、学位论文等多种模板类型，\n'
            '自动识别格式要求，一键完成排版。'
        )
        welcome_label.setStyleSheet('font-size: 14px; padding: 10px;')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_label)
        
        quick_start_layout = QHBoxLayout()
        
        # 快速开始按钮
        quick_start_btn = PrimaryPushButton('🚀 快速开始')
        quick_start_btn.setMinimumSize(200, 60)
        quick_start_btn.clicked.connect(lambda: self.main_tabs.setCurrentIndex(2))
        quick_start_layout.addWidget(quick_start_btn)
        
        # 上传模板按钮
        upload_template_btn = PrimaryPushButton('📤 上传模板')
        upload_template_btn.setMinimumSize(200, 60)
        upload_template_btn.clicked.connect(lambda: self.main_tabs.setCurrentIndex(1))
        quick_start_layout.addWidget(upload_template_btn)
        
        # 封面配置按钮
        cover_config_btn = PrimaryPushButton('📘 封面配置')
        cover_config_btn.setMinimumSize(200, 60)
        cover_config_btn.clicked.connect(self.on_cover_declaration_config)
        quick_start_layout.addWidget(cover_config_btn)
        
        welcome_layout.addLayout(quick_start_layout)
        layout.addWidget(welcome_group)
        
        # 功能卡片
        features_group = QGroupBox('✨ 主要功能')
        features_layout = QGridLayout(features_group)
        
        features = [
            ('📋 模板管理', '支持多种论文模板，自定义创建'),
            ('🤖 AI 识别', '自动识别格式要求'),
            ('📄 文档格式化', '一键完成排版'),
            ('📘 封面声明', '可视化配置封面和声明页'),
            ('📚 参考文献', '支持 GB/T、APA、MLA 等格式'),
            ('🚀 批量处理', '一次处理多个文档'),
        ]
        
        for i, (title, desc) in enumerate(features):
            card = QFrame()
            card.setStyleSheet('''
                QFrame {
                    background-color: #f5f5f5;
                    border-radius: 8px;
                    padding: 15px;
                }
                QFrame:hover {
                    background-color: #e3f2fd;
                }
            ''')
            card_layout = QVBoxLayout(card)
            
            title_label = QLabel(title)
            title_label.setStyleSheet('font-size: 16px; font-weight: bold;')
            card_layout.addWidget(title_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet('font-size: 12px; color: #666;')
            card_layout.addWidget(desc_label)
            
            row = i // 3
            col = i % 3
            features_layout.addWidget(card, row, col)
        
        layout.addWidget(features_group)
        
        # 最近使用
        recent_group = QGroupBox('📂 最近使用')
        recent_layout = QVBoxLayout(recent_group)
        
        self.recent_list = QListWidget()
        self.recent_list.setMaximumHeight(150)
        recent_layout.addWidget(self.recent_list)
        
        layout.addWidget(recent_group)
        
        return widget
    
    def create_template_tab(self) -> QWidget:
        """创建模板管理标签"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 模板列表
        template_group = QGroupBox('📋 模板列表')
        template_layout = QVBoxLayout(template_group)
        
        self.template_table = QTableWidget()
        self.template_table.setColumnCount(5)
        self.template_table.setHorizontalHeaderLabels(['名称', '类型', '描述', '创建时间', '操作'])
        self.template_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.template_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.template_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.template_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.template_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        template_layout.addWidget(self.template_table)
        
        # 模板操作按钮
        btn_layout = QHBoxLayout()
        
        add_template_btn = QPushButton('➕ 新建模板')
        add_template_btn.clicked.connect(self.on_add_template)
        btn_layout.addWidget(add_template_btn)
        
        import_template_btn = QPushButton('📥 导入模板')
        import_template_btn.clicked.connect(self.on_import_template)
        btn_layout.addWidget(import_template_btn)
        
        export_template_btn = QPushButton('📤 导出模板')
        export_template_btn.clicked.connect(self.on_export_template)
        btn_layout.addWidget(export_template_btn)
        
        btn_layout.addStretch()
        template_layout.addLayout(btn_layout)
        
        layout.addWidget(template_group)
        
        return widget
    
    def create_format_tab(self) -> QWidget:
        """创建文档格式化标签"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 文件选择
        file_group = QGroupBox('📂 文件选择')
        file_layout = QFormLayout(file_group)
        
        input_layout = QHBoxLayout()
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setPlaceholderText('选择输入文件...')
        input_layout.addWidget(self.input_path_edit)
        
        browse_input_btn = QPushButton('浏览...')
        browse_input_btn.clicked.connect(self.browse_input_file)
        input_layout.addWidget(browse_input_btn)
        
        file_layout.addRow('输入文件:', input_layout)
        
        output_layout = QHBoxLayout()
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText('选择输出路径...')
        output_layout.addWidget(self.output_path_edit)
        
        browse_output_btn = QPushButton('浏览...')
        browse_output_btn.clicked.connect(self.browse_output_file)
        output_layout.addWidget(browse_output_btn)
        
        file_layout.addRow('输出文件:', output_layout)
        
        layout.addWidget(file_group)
        
        # 模板选择
        template_group = QGroupBox('📋 选择模板')
        template_layout = QVBoxLayout(template_group)
        
        self.format_template_combo = QComboBox()
        self.format_template_combo.addItem('请选择模板...')
        template_layout.addWidget(self.format_template_combo)
        
        layout.addWidget(template_group)
        
        # 封面和声明页选项
        cover_group = QGroupBox('📘 封面和声明页')
        cover_layout = QVBoxLayout(cover_group)
        
        self.use_cover_check = QCheckBox('添加封面和声明页')
        self.use_cover_check.stateChanged.connect(self.toggle_cover_options)
        cover_layout.addWidget(self.use_cover_check)
        
        self.cover_config_label = QLabel('未配置封面信息')
        self.cover_config_label.setStyleSheet('color: gray; font-size: 12px;')
        cover_layout.addWidget(self.cover_config_label)
        
        config_cover_btn = QPushButton('⚙️ 配置封面和声明页')
        config_cover_btn.clicked.connect(self.on_cover_declaration_config)
        cover_layout.addWidget(config_cover_btn)
        
        layout.addWidget(cover_group)
        
        # 进度条
        progress_group = QGroupBox('⏳ 进度')
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel('就绪')
        self.progress_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.progress_label)
        
        layout.addWidget(progress_group)
        
        # 开始按钮
        start_btn = PrimaryPushButton('🚀 开始格式化')
        start_btn.setMinimumHeight(50)
        start_btn.clicked.connect(self.start_formatting)
        layout.addWidget(start_btn)
        
        return widget
    
    def create_reference_tab(self) -> QWidget:
        """创建参考文献标签"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        ref_group = QGroupBox('📚 参考文献格式化')
        ref_layout = QVBoxLayout(ref_group)
        
        ref_format_layout = QFormLayout()
        
        self.ref_format_combo = QComboBox()
        self.ref_format_combo.addItems(['GB/T 7714', 'APA', 'MLA', 'IEEE', 'Springer'])
        ref_format_layout.addRow('引用格式:', self.ref_format_combo)
        
        self.ref_input_edit = QTextEdit()
        self.ref_input_edit.setPlaceholderText('粘贴参考文献列表...')
        self.ref_input_edit.setMaximumHeight(200)
        ref_format_layout.addRow('参考文献:', self.ref_input_edit)
        
        ref_layout.addLayout(ref_format_layout)
        
        format_ref_btn = PrimaryPushButton('格式化参考文献')
        format_ref_btn.clicked.connect(self.format_references)
        ref_layout.addWidget(format_ref_btn)
        
        self.ref_output_edit = QTextEdit()
        self.ref_output_edit.setReadOnly(True)
        self.ref_output_edit.setPlaceholderText('格式化结果将显示在这里...')
        self.ref_output_edit.setMaximumHeight(200)
        ref_layout.addWidget(QLabel('格式化结果:'))
        ref_layout.addWidget(self.ref_output_edit)
        
        layout.addWidget(ref_group)
        
        return widget
    
    def create_settings_tab(self) -> QWidget:
        """创建设置标签"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 外观设置
        appearance_group = QGroupBox('🎨 外观')
        appearance_layout = QFormLayout(appearance_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['浅色', '深色', '自动'])
        appearance_layout.addRow('主题:', self.theme_combo)
        
        layout.addWidget(appearance_group)
        
        # 保存设置
        save_group = QGroupBox('💾 保存')
        save_layout = QVBoxLayout(save_group)
        
        save_settings_btn = QPushButton('保存设置')
        save_settings_btn.clicked.connect(self.save_settings)
        save_layout.addWidget(save_settings_btn)
        
        reset_settings_btn = QPushButton('重置设置')
        reset_settings_btn.clicked.connect(self.reset_settings)
        save_layout.addWidget(reset_settings_btn)
        
        layout.addWidget(save_group)
        
        layout.addStretch()
        
        return widget
    
    def apply_modern_style(self):
        """应用现代化样式"""
        if PYWINSTYLES_AVAILABLE:
            try:
                pywinstyles.apply_style(self, "aero")
            except Exception:
                pass
        
        # 自定义样式表
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #1976d2;
            }
            
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
            }
            
            QPushButton:hover {
                background-color: #1565c0;
            }
            
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            
            QPushButton:disabled {
                background-color: #bdbdbd;
            }
            
            PrimaryPushButton, QPushButton#primary {
                background-color: #4caf50;
            }
            
            PrimaryPushButton:hover, QPushButton#primary:hover {
                background-color: #43a047;
            }
            
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #e0e0e0;
                border: 1px solid #ddd;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
            }
            
            QTabBar::tab:hover {
                background-color: #f5f5f5;
            }
            
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            
            QTableWidget::item {
                padding: 8px;
            }
            
            QTableWidget::item:selected {
                background-color: #1976d2;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #ddd;
                font-weight: bold;
            }
            
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 8px;
                text-align: center;
                background-color: #f5f5f5;
            }
            
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 7px;
            }
            
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #1976d2;
            }
            
            QCheckBox {
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #ddd;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                background-color: #1976d2;
            }
            
            QScrollBar:vertical {
                background-color: #f5f5f5;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #bdbdbd;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #9e9e9e;
            }
        ''')
    
    # ========================================================================
    # 事件处理方法
    # ========================================================================
    
    def on_new_document(self):
        """新建文档"""
        QMessageBox.information(self, '提示', '新建文档功能开发中...')
    
    def on_open_document(self):
        """打开文档"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '打开文档',
            '',
            'Word 文档 (*.docx);;所有文件 (*)'
        )
        
        if file_path:
            self.input_path_edit.setText(file_path)
            self.statusBar().showMessage(f'已打开：{file_path}')
    
    def on_save_document(self):
        """保存文档"""
        QMessageBox.information(self, '提示', '保存功能开发中...')
    
    def on_cover_declaration_config(self):
        """打开封面和声明页配置"""
        dialog = CoverDeclarationConfigDialog(self.cover_config, self)
        
        if dialog.exec_() == QDialog.Accepted:
            self.cover_config = dialog.get_config()
            
            # 更新界面显示
            if self.cover_config:
                if self.cover_config.get('template', {}).get('enabled'):
                    template_path = self.cover_config['template']['template_path']
                    filename = os.path.basename(template_path)
                    self.cover_config_label.setText(
                        f'✓ 使用模板：{filename}\n'
                        f'封面：第 {self.cover_config["template"]["page_selection"]["cover_page_index"] + 1} 页 | '
                        f'声明：第 {self.cover_config["template"]["page_selection"]["declaration_page_index"] + 1} 页'
                    )
                else:
                    school = self.cover_config.get('cover', {}).get('school_name', '未设置')
                    self.cover_config_label.setText(f'✓ 学校：{school} | 类型：{self.cover_config.get("cover", {}).get("thesis_type", "未设置")}')
                
                self.cover_config_label.setStyleSheet('color: green; font-size: 12px;')
                self.use_cover_check.setChecked(True)
            
            self.statusBar().showMessage('封面配置已更新')
    
    def on_template_upload(self):
        """上传模板"""
        QMessageBox.information(self, '提示', '模板上传功能开发中...')
    
    def on_add_template(self):
        """添加模板"""
        QMessageBox.information(self, '提示', '添加模板功能开发中...')
    
    def on_import_template(self):
        """导入模板"""
        QMessageBox.information(self, '提示', '导入模板功能开发中...')
    
    def on_export_template(self):
        """导出模板"""
        QMessageBox.information(self, '提示', '导出模板功能开发中...')
    
    def on_help(self):
        """帮助"""
        help_path = os.path.join(os.path.dirname(__file__), '用户使用手册.md')
        if os.path.exists(help_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(help_path))
        else:
            QMessageBox.information(self, '帮助', '请使用论文排版优化器查看帮助文档')
    
    def on_about(self):
        """关于"""
        QMessageBox.about(
            self,
            '关于论文排版优化器',
            '<h2>论文排版优化器 v2.0</h2>'
            '<p>专业的学术论文格式化工具</p>'
            '<p>开发小助手 · 严谨专业版</p>'
            '<p>© 2024 All Rights Reserved</p>'
        )
    
    def browse_input_file(self):
        """浏览输入文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '选择输入文件',
            '',
            'Word 文档 (*.docx);;所有文件 (*)'
        )
        
        if file_path:
            self.input_path_edit.setText(file_path)
    
    def browse_output_file(self):
        """浏览输出文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '选择输出文件',
            '',
            'Word 文档 (*.docx)'
        )
        
        if file_path:
            self.output_path_edit.setText(file_path)
    
    def toggle_cover_options(self, state):
        """切换封面选项"""
        # 可以在这里添加更多逻辑
        pass
    
    def start_formatting(self):
        """开始格式化"""
        input_path = self.input_path_edit.text()
        output_path = self.output_path_edit.text()
        
        if not input_path:
            QMessageBox.warning(self, '警告', '请选择输入文件')
            return
        
        if not output_path:
            QMessageBox.warning(self, '警告', '请选择输出路径')
            return
        
        # 禁用按钮
        self.progress_bar.setValue(0)
        self.progress_label.setText('正在格式化...')
        
        # 创建工作线程
        self.worker_thread = WorkerThread(
            self.format_document_task,
            input_path,
            output_path
        )
        
        self.worker_thread.progress.connect(self.on_format_progress)
        self.worker_thread.finished.connect(self.on_format_finished)
        self.worker_thread.error.connect(self.on_format_error)
        
        self.worker_thread.start()
    
    def format_document_task(self, input_path, output_path):
        """格式化文档任务"""
        try:
            # 1. 加载文档
            from docx import Document
            doc = Document(input_path)
            
            # 2. 应用模板
            if self.current_template:
                formatter = DocumentFormatter()
                formatter.apply_template(doc, self.current_template)
            
            # 3. 添加封面和声明页
            if self.use_cover_check.isChecked() and self.cover_config:
                if self.cover_config.get('template', {}).get('enabled'):
                    # 使用模板页面
                    template_manager = TemplatePageManager()
                    template_path = self.cover_config['template']['template_path']
                    page_selection = self.cover_config['template']['page_selection']
                    
                    pages = template_manager.extract_pages(
                        template_path,
                        page_selection['cover_page_index'],
                        page_selection['declaration_page_index']
                    )
                    
                    template_manager.merge_with_thesis(
                        input_path,
                        pages['cover_path'],
                        pages['declaration_path'],
                        output_path
                    )
                else:
                    # 使用简单配置
                    cover_manager = CoverDeclarationManager(self.cover_config)
                    cover_manager.apply_cover_and_declaration(doc, self.cover_config)
            
            # 4. 保存文档
            if not self.cover_config or not self.cover_config.get('template', {}).get('enabled'):
                doc.save(output_path)
            
            return {'success': True, 'output_path': output_path}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def on_format_progress(self, message):
        """格式化进度更新"""
        self.progress_label.setText(message)
    
    def on_format_finished(self, result):
        """格式化完成"""
        if result.get('success'):
            self.progress_bar.setValue(100)
            self.progress_label.setText('格式化完成！')
            QMessageBox.information(
                self,
                '成功',
                f'文档格式化完成！\n\n输出文件：{result["output_path"]}'
            )
        else:
            self.progress_label.setText('格式化失败')
            QMessageBox.critical(self, '错误', f'格式化失败：{result.get("error", "未知错误")}')
    
    def on_format_error(self, error_message):
        """格式化错误"""
        self.progress_label.setText('发生错误')
        QMessageBox.critical(self, '错误', f'格式化过程中发生错误：{error_message}')
    
    def format_references(self):
        """格式化参考文献"""
        input_text = self.ref_input_edit.toPlainText()
        format_type = self.ref_format_combo.currentText()
        
        if not input_text.strip():
            QMessageBox.warning(self, '警告', '请输入参考文献')
            return
        
        try:
            parser = ReferenceParser()
            formatter = ReferenceFormatter()
            
            refs = parser.parse(input_text)
            formatted = formatter.format_list(refs, format_type)
            
            self.ref_output_edit.setPlainText('\n\n'.join(formatted))
            QMessageBox.information(self, '成功', '参考文献格式化完成！')
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'格式化失败：{str(e)}')
    
    def load_settings(self):
        """加载设置"""
        settings = QSettings('PaperFormatter', 'Settings')
        theme = settings.value('theme', 'light')
        # 加载其他设置
    
    def save_settings(self):
        """保存设置"""
        settings = QSettings('PaperFormatter', 'Settings')
        settings.setValue('theme', self.theme_combo.currentText())
        QMessageBox.information(self, '成功', '设置已保存')
    
    def reset_settings(self):
        """重置设置"""
        settings = QSettings('PaperFormatter', 'Settings')
        settings.clear()
        QMessageBox.information(self, '成功', '设置已重置')
    
    def closeEvent(self, event):
        """关闭事件"""
        reply = QMessageBox.question(
            self,
            '确认退出',
            '确定要退出吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# ============================================================================
# 程序入口
# ============================================================================

def main():
    """程序入口"""
    app = QApplication(sys.argv)
    app.setApplicationName('论文排版优化器')
    app.setOrganizationName('PaperFormatter')
    
    # 设置应用样式
    if FLUENT_WIDGETS_AVAILABLE:
        setTheme(Theme.AUTO)
    
    # 创建主窗口
    window = PaperFormatterMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
