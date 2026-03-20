"""
字体管理对话框
Font Manager Dialog

版本：v2.2.2
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QListWidget, QListWidgetItem, QGroupBox, QLineEdit,
                             QComboBox, QCheckBox, QProgressBar, QTextEdit,
                             QMessageBox, QFileDialog, QSplitter, QWidget,
                             QFormLayout, QTabWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from font_downloader import FontDownloader, FontInfo
import os


class FontSearchThread(QThread):
    """字体搜索线程"""
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, downloader: FontDownloader, query: str, is_chinese: bool):
        super().__init__()
        self.downloader = downloader
        self.query = query
        self.is_chinese = is_chinese
    
    def run(self):
        try:
            fonts = self.downloader.search_fonts(
                query=self.query,
                is_chinese=self.is_chinese
            )
            self.finished.emit(fonts)
        except Exception as e:
            self.error.emit(str(e))


class FontDownloadThread(QThread):
    """字体下载线程"""
    progress = pyqtSignal(int, str)  # 进度百分比，消息
    finished = pyqtSignal(str)  # 保存路径
    error = pyqtSignal(str)
    
    def __init__(self, downloader: FontDownloader, font: FontInfo):
        super().__init__()
        self.downloader = downloader
        self.font = font
    
    def run(self):
        try:
            self.progress.emit(0, f"开始下载 {self.font.name}...")
            path = self.downloader.download_font(self.font)
            self.progress.emit(100, "下载完成")
            self.finished.emit(path)
        except Exception as e:
            self.error.emit(str(e))


class FontManagerDialog(QDialog):
    """字体管理对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('🔤 字体管理')
        self.setMinimumSize(900, 600)
        
        self.downloader = FontDownloader()
        self.search_thread = None
        self.download_thread = None
        
        self.init_ui()
        self.load_installed_fonts()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建标签页
        self.tabs = QTabWidget()
        
        # 已安装字体页
        installed_tab = self.create_installed_tab()
        self.tabs.addTab(installed_tab, '📦 已安装字体')
        
        # 搜索下载页
        search_tab = self.create_search_tab()
        self.tabs.addTab(search_tab, '🔍 搜索下载')
        
        # API 设置页
        api_tab = self.create_api_tab()
        self.tabs.addTab(api_tab, '🔑 API 设置')
        
        layout.addWidget(self.tabs)
        
        # 底部按钮
        button_layout = self.create_button_layout()
        layout.addLayout(button_layout)
    
    def create_installed_tab(self):
        """创建已安装字体标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 字体列表
        list_group = self.create_font_list_group()
        layout.addWidget(list_group)
        
        # 字体操作
        action_group = self.create_font_actions_group()
        layout.addWidget(action_group)
        
        return widget
    
    def create_font_list_group(self):
        """创建字体列表组"""
        group = QGroupBox('已安装字体')
        layout = QVBoxLayout(group)
        
        # 字体列表
        self.font_list = QListWidget()
        self.font_list.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.font_list)
        
        return group
    
    def create_font_actions_group(self):
        """创建字体操作组"""
        group = QGroupBox('字体操作')
        layout = QHBoxLayout(group)
        
        # 导入字体
        import_btn = QPushButton('📥 导入字体')
        import_btn.clicked.connect(self.import_fonts)
        layout.addWidget(import_btn)
        
        # 导出字体
        export_btn = QPushButton('📤 导出字体')
        export_btn.clicked.connect(self.export_fonts)
        layout.addWidget(export_btn)
        
        # 卸载字体
        uninstall_btn = QPushButton('🗑️ 卸载选中')
        uninstall_btn.clicked.connect(self.uninstall_fonts)
        layout.addWidget(uninstall_btn)
        
        layout.addStretch()
        
        return group
    
    def create_search_tab(self):
        """创建搜索下载标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 搜索栏
        search_group = self.create_search_group()
        layout.addWidget(search_group)
        
        # 搜索结果
        result_group = self.create_result_group()
        layout.addWidget(result_group)
        
        # 下载进度
        progress_group = self.create_progress_group()
        layout.addWidget(progress_group)
        
        return widget
    
    def create_search_group(self):
        """创建搜索栏组"""
        group = QGroupBox('字体搜索')
        layout = QHBoxLayout(group)
        
        # 搜索框
        layout.addWidget(QLabel('搜索:'))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('输入字体名称...')
        self.search_input.returnPressed.connect(self.search_fonts)
        layout.addWidget(self.search_input)
        
        # 中文字体复选框
        self.chinese_checkbox = QCheckBox('只搜索中文字体')
        self.chinese_checkbox.setChecked(True)
        layout.addWidget(self.chinese_checkbox)
        
        # 搜索按钮
        search_btn = QPushButton('🔍 搜索')
        search_btn.clicked.connect(self.search_fonts)
        layout.addWidget(search_btn)
        
        return group
    
    def create_result_group(self):
        """创建搜索结果组"""
        group = QGroupBox('搜索结果')
        layout = QVBoxLayout(group)
        
        # 结果列表
        self.result_list = QListWidget()
        layout.addWidget(self.result_list)
        
        # 下载按钮
        download_btn = QPushButton('⬇️ 下载选中')
        download_btn.setStyleSheet('background-color: #4CAF50; color: white; padding: 8px 16px;')
        download_btn.clicked.connect(self.download_selected)
        layout.addWidget(download_btn)
        
        return group
    
    def create_progress_group(self):
        """创建下载进度组"""
        group = QGroupBox('下载进度')
        layout = QVBoxLayout(group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # 状态文本
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(80)
        self.status_text.setStyleSheet('background-color: #f5f5f5; font-family: monospace;')
        layout.addWidget(self.status_text)
        
        return group
    
    def create_api_tab(self):
        """创建 API 设置标签页"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Google Fonts API
        layout.addWidget(QLabel('📌 Google Fonts API 设置'))
        
        google_key_label = QLabel('API Key:')
        self.google_key_input = QLineEdit()
        self.google_key_input.setPlaceholderText('输入 Google Fonts API 密钥')
        self.google_key_input.setText(self.downloader.api_keys.get('google', ''))
        layout.addRow(google_key_label, self.google_key_input)
        
        # 说明
        help_text = QLabel(
            '💡 获取 API 密钥：\n'
            '1. 访问 https://developers.google.com/fonts/docs/developer_api\n'
            '2. 创建项目并获取 API 密钥\n'
            '3. 将密钥粘贴到上方输入框\n'
            '4. 点击"保存"按钮'
        )
        help_text.setStyleSheet('color: #666; font-size: 11px;')
        help_text.setWordWrap(True)
        layout.addRow(help_text)
        
        # 保存按钮
        save_btn = QPushButton('💾 保存设置')
        save_btn.clicked.connect(self.save_api_settings)
        layout.addRow(save_btn)
        
        return widget
    
    def create_button_layout(self):
        """创建底部按钮布局"""
        layout = QHBoxLayout()
        layout.addStretch()
        
        # 关闭
        close_btn = QPushButton('❌ 关闭')
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)
        
        return layout
    
    def load_installed_fonts(self):
        """加载已安装字体"""
        self.font_list.clear()
        
        fonts = self.downloader.get_installed_fonts()
        for font in fonts:
            item_text = font.get('name', font.get('filename', 'Unknown'))
            item = QListWidgetItem(f"📦 {item_text}")
            item.setData(Qt.UserRole, font)
            self.font_list.addItem(item)
        
        self.statusBar().showMessage(f'已加载 {len(fonts)} 个字体', 3000)
    
    def import_fonts(self):
        """导入字体"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            '选择字体文件',
            '',
            '字体文件 (*.ttf *.otf *.ttc);;所有文件 (*)'
        )
        
        if files:
            count = 0
            for file in files:
                if self.downloader.install_font(file):
                    count += 1
            
            QMessageBox.information(
                self,
                '导入完成',
                f'✅ 成功导入 {count}/{len(files)} 个字体'
            )
            
            # 刷新列表
            self.load_installed_fonts()
    
    def export_fonts(self):
        """导出字体"""
        selected_items = self.font_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '警告', '请先选择要导出的字体')
            return
        
        # 选择保存目录
        save_dir = QFileDialog.getExistingDirectory(
            self,
            '选择保存目录'
        )
        
        if save_dir:
            count = 0
            import shutil
            
            for item in selected_items:
                font = item.data(Qt.UserRole)
                if font and 'path' in font:
                    try:
                        dest = os.path.join(save_dir, font['filename'])
                        shutil.copy2(font['path'], dest)
                        count += 1
                    except Exception as e:
                        print(f"导出失败：{e}")
            
            QMessageBox.information(
                self,
                '导出完成',
                f'✅ 成功导出 {count}/{len(selected_items)} 个字体'
            )
    
    def uninstall_fonts(self):
        """卸载字体"""
        selected_items = self.font_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '警告', '请先选择要卸载的字体')
            return
        
        reply = QMessageBox.question(
            self,
            '确认卸载',
            f'确定要卸载选中的 {len(selected_items)} 个字体吗？\n\n此操作不可恢复！',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        count = 0
        for item in selected_items:
            font = item.data(Qt.UserRole)
            if font and 'path' in font:
                if self.downloader.uninstall_font(font['path']):
                    count += 1
        
        QMessageBox.information(
            self,
            '卸载完成',
            f'✅ 成功卸载 {count}/{len(selected_items)} 个字体'
        )
        
        # 刷新列表
        self.load_installed_fonts()
    
    def search_fonts(self):
        """搜索字体"""
        query = self.search_input.text()
        is_chinese = self.chinese_checkbox.isChecked()
        
        self.status_text.append(f'🔍 搜索：{query} (中文字体：{"是" if is_chinese else "否"})')
        self.result_list.clear()
        self.progress_bar.setValue(0)
        
        # 使用线程搜索
        self.search_thread = FontSearchThread(self.downloader, query, is_chinese)
        self.search_thread.finished.connect(self.on_search_finished)
        self.search_thread.error.connect(self.on_search_error)
        self.search_thread.start()
    
    def on_search_finished(self, fonts):
        """搜索完成"""
        self.result_list.clear()
        
        for font in fonts:
            item_text = f"{font.name} ({font.family})"
            if font.is_chinese:
                item_text = f"🀄 {item_text}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, font)
            self.result_list.addItem(item)
        
        self.status_text.append(f'✅ 找到 {len(fonts)} 个字体')
        self.statusBar().showMessage(f'搜索完成，找到 {len(fonts)} 个字体', 3000)
    
    def on_search_error(self, error):
        """搜索错误"""
        self.status_text.append(f'❌ 搜索失败：{error}')
        QMessageBox.warning(self, '警告', f'搜索失败：{error}')
    
    def download_selected(self):
        """下载选中的字体"""
        selected_items = self.result_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '警告', '请先选择要下载的字体')
            return
        
        # 下载第一个选中的字体
        font = selected_items[0].data(Qt.UserRole)
        
        self.status_text.append(f'⬇️ 开始下载：{font.name}')
        self.progress_bar.setValue(0)
        
        # 使用线程下载
        self.download_thread = FontDownloadThread(self.downloader, font)
        self.download_thread.progress.connect(self.on_download_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.error.connect(self.on_download_error)
        self.download_thread.start()
    
    def on_download_progress(self, percent, message):
        """下载进度更新"""
        self.progress_bar.setValue(percent)
        self.status_text.append(message)
    
    def on_download_finished(self, path):
        """下载完成"""
        self.status_text.append(f'✅ 下载完成：{path}')
        self.statusBar().showMessage('字体下载完成', 3000)
        
        # 询问是否安装
        reply = QMessageBox.question(
            self,
            '安装字体',
            '是否立即安装此字体？',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.downloader.install_font(path):
                QMessageBox.information(self, '成功', '字体安装成功')
                self.load_installed_fonts()
            else:
                QMessageBox.warning(self, '警告', '字体安装失败')
    
    def on_download_error(self, error):
        """下载错误"""
        self.status_text.append(f'❌ 下载失败：{error}')
        QMessageBox.warning(self, '警告', f'下载失败：{error}')
    
    def save_api_settings(self):
        """保存 API 设置"""
        google_key = self.google_key_input.text()
        
        if google_key:
            self.downloader.set_api_key('google', google_key)
            QMessageBox.information(self, '成功', 'API 设置已保存')
        else:
            QMessageBox.warning(self, '警告', '请输入有效的 API 密钥')
