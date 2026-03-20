"""
自动更新模块
Auto Updater for 论文排版优化器

功能：
- 检查 GitHub Release 最新版本
- 比较版本号
- 提示用户更新
- 下载更新包
"""

import requests
import json
import os
import sys
from datetime import datetime


class AutoUpdater:
    """自动更新器"""
    
    def __init__(self):
        self.current_version = "2.0.0"
        self.repo_owner = "taobaoaz"
        self.repo_name = "paper-formatter"
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        
    def get_current_version(self):
        """获取当前版本号"""
        return self.current_version
    
    def check_update(self):
        """
        检查是否有新版本
        
        返回：
        - dict: 包含更新信息
          - has_update: 是否有更新
          - latest_version: 最新版本
          - release_notes: 更新说明
          - download_url: 下载地址
        """
        try:
            # 获取最新版本信息
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            latest_version = data.get('tag_name', 'v0.0.0').lstrip('v')
            
            # 比较版本号
            if self._version_compare(latest_version, self.current_version) > 0:
                return {
                    'has_update': True,
                    'latest_version': latest_version,
                    'current_version': self.current_version,
                    'release_notes': data.get('body', ''),
                    'download_url': data.get('html_url', ''),
                    'assets': data.get('assets', [])
                }
            else:
                return {
                    'has_update': False,
                    'current_version': self.current_version,
                    'latest_version': latest_version
                }
                
        except Exception as e:
            return {
                'has_update': False,
                'error': str(e)
            }
    
    def _version_compare(self, v1, v2):
        """
        比较版本号
        
        返回：
        - 1: v1 > v2
        - 0: v1 = v2
        - -1: v1 < v2
        """
        def normalize(v):
            return [int(x) for x in v.split('.')]
        
        try:
            v1_parts = normalize(v1)
            v2_parts = normalize(v2)
            
            # 补齐位数
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1
            
            return 0
        except:
            return 0
    
    def download_update(self, download_url, save_path):
        """
        下载更新包
        
        参数：
        - download_url: 下载地址
        - save_path: 保存路径
        
        返回：
        - bool: 是否成功
        """
        try:
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # 显示进度
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r下载进度：{percent:.1f}%", end='')
            
            print("\n下载完成！")
            return True
            
        except Exception as e:
            print(f"\n下载失败：{e}")
            return False
    
    def get_download_asset(self, update_info, file_type='.exe'):
        """
        从更新信息中获取下载链接
        
        参数：
        - update_info: 更新信息
        - file_type: 文件类型
        
        返回：
        - str: 下载链接
        """
        assets = update_info.get('assets', [])
        for asset in assets:
            if asset.get('name', '').endswith(file_type):
                return asset.get('browser_download_url', '')
        
        return ''


class UpdateDialog:
    """更新提示对话框（GUI）"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.updater = AutoUpdater()
    
    def show_update_check(self):
        """显示更新检查对话框"""
        try:
            from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox
            from PyQt5.QtCore import Qt
            
            update_info = self.updater.check_update()
            
            if update_info.get('error'):
                QMessageBox.warning(self.parent, '检查更新失败', f'无法检查更新：{update_info["error"]}')
                return
            
            if not update_info.get('has_update'):
                QMessageBox.information(self.parent, '检查更新', 
                    f'当前已是最新版本！\n\n版本号：{update_info["current_version"]}')
                return
            
            # 显示更新对话框
            dialog = QDialog(self.parent)
            dialog.setWindowTitle('发现新版本')
            dialog.setMinimumSize(500, 400)
            
            layout = QVBoxLayout(dialog)
            
            # 版本信息
            title = QLabel(f'🎉 发现新版本 {update_info["latest_version"]}！')
            title.setStyleSheet('font-size: 16px; font-weight: bold; color: #2196F3;')
            layout.addWidget(title)
            
            current = QLabel(f'当前版本：{update_info["current_version"]}')
            layout.addWidget(current)
            
            # 更新说明
            notes_label = QLabel('更新内容：')
            notes_label.setStyleSheet('font-weight: bold; margin-top: 10px;')
            layout.addWidget(notes_label)
            
            notes = QTextEdit()
            notes.setReadOnly(True)
            notes.setPlainText(update_info.get('release_notes', '无更新说明'))
            notes.setMaximumHeight(200)
            layout.addWidget(notes)
            
            # 按钮
            btn_layout = QVBoxLayout()
            
            download_btn = QPushButton('⬇️ 立即下载更新')
            download_btn.setStyleSheet('background-color: #2196F3; color: white; padding: 10px; font-size: 14px;')
            download_btn.clicked.connect(lambda: self._download_update(update_info, dialog))
            btn_layout.addWidget(download_btn)
            
            later_btn = QPushButton('稍后再说')
            later_btn.clicked.connect(dialog.reject)
            btn_layout.addWidget(later_btn)
            
            layout.addLayout(btn_layout)
            
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self.parent, '错误', f'显示更新对话框失败：{e}')
    
    def _download_update(self, update_info, dialog):
        """下载更新"""
        try:
            from PyQt5.QtWidgets import QFileDialog, QMessageBox
            import webbrowser
            
            # 获取下载链接
            assets = update_info.get('assets', [])
            if not assets:
                # 没有附件，打开 Release 页面
                webbrowser.open(update_info.get('download_url', ''))
                dialog.accept()
                return
            
            # 选择保存位置
            default_name = f'论文排版优化器_{update_info["latest_version"]}.exe'
            save_path, _ = QFileDialog.getSaveFileName(
                dialog,
                '保存更新包',
                default_name,
                'EXE 文件 (*.exe)'
            )
            
            if save_path:
                # 下载文件
                download_url = self.updater.get_download_asset(update_info)
                if download_url:
                    QMessageBox.information(dialog, '下载更新', 
                        '将在浏览器中打开下载页面...\n\n'
                        '或者访问：' + update_info.get('download_url', ''))
                    webbrowser.open(download_url)
                    dialog.accept()
            
        except Exception as e:
            QMessageBox.critical(dialog, '错误', f'下载失败：{e}')


# 快捷函数
def check_for_updates(parent=None):
    """检查更新（带 GUI）"""
    dialog = UpdateDialog(parent)
    dialog.show_update_check()


def check_updates_cli():
    """检查更新（命令行）"""
    updater = AutoUpdater()
    update_info = updater.check_update()
    
    if update_info.get('error'):
        print(f'❌ 检查更新失败：{update_info["error"]}')
        return
    
    if update_info.get('has_update'):
        print(f'🎉 发现新版本 {update_info["latest_version"]}！')
        print(f'当前版本：{update_info["current_version"]}')
        print(f'\n更新内容：\n{update_info.get("release_notes", "")}')
        print(f'\n下载地址：{update_info.get("download_url", "")}')
    else:
        print(f'✅ 当前已是最新版本 (v{update_info["current_version"]})')


if __name__ == '__main__':
    # 命令行测试
    check_updates_cli()
