"""
字体下载器模块
Font Downloader Module

功能：
- 在线字体搜索
- 字体包下载
- 自动安装字体
- 字体预览

版本：v2.2.2
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime


@dataclass
class FontInfo:
    """字体信息数据类"""
    name: str  # 字体名称
    family: str  # 字体系列
    style: str = "Regular"  # 字体风格
    url: str = ""  # 下载链接
    size: str = ""  # 文件大小
    license: str = "Unknown"  # 许可证
    category: str = "sans-serif"  # 字体分类
    is_chinese: bool = False  # 是否中文字体
    download_count: int = 0  # 下载次数
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'family': self.family,
            'style': self.style,
            'url': self.url,
            'size': self.size,
            'license': self.license,
            'category': self.category,
            'is_chinese': self.is_chinese,
            'download_count': self.download_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FontInfo':
        """从字典创建"""
        return cls(
            name=data.get('name', ''),
            family=data.get('family', ''),
            style=data.get('style', 'Regular'),
            url=data.get('url', ''),
            size=data.get('size', ''),
            license=data.get('license', 'Unknown'),
            category=data.get('category', 'sans-serif'),
            is_chinese=data.get('is_chinese', False),
            download_count=data.get('download_count', 0)
        )


class FontDownloader:
    """字体下载器"""
    
    # 字体源列表
    FONT_SOURCES = [
        {
            'name': 'Google Fonts',
            'api_url': 'https://www.googleapis.com/webfonts/v1/webfonts',
            'web_url': 'https://fonts.google.com',
            'requires_key': True
        },
        {
            'name': 'Font Squirrel',
            'web_url': 'https://www.fontsquirrel.com',
            'requires_key': False
        },
        {
            'name': 'DaFont',
            'web_url': 'https://www.dafont.com',
            'requires_key': False
        }
    ]
    
    # 中文字体列表（预定义）
    CHINESE_FONTS = [
        {
            'name': '思源黑体',
            'family': 'Source Han Sans',
            'url': 'https://github.com/adobe-fonts/source-han-sans',
            'category': 'sans-serif',
            'is_chinese': True
        },
        {
            'name': '思源宋体',
            'family': 'Source Han Serif',
            'url': 'https://github.com/adobe-fonts/source-han-serif',
            'category': 'serif',
            'is_chinese': True
        },
        {
            'name': '站酷高端黑',
            'family': 'ZCOOL GaoDuan Hei',
            'url': 'https://github.com/zcool/zcool-fonts',
            'category': 'sans-serif',
            'is_chinese': True
        },
        {
            'name': '文泉驿正黑',
            'family': 'WenQuanYi Zen Hei',
            'url': 'https://github.com/zven21/wqy-zenhei',
            'category': 'sans-serif',
            'is_chinese': True
        }
    ]
    
    def __init__(self, font_dir: str = None):
        """
        初始化字体下载器
        
        Args:
            font_dir: 字体保存目录
        """
        self.font_dir = font_dir
        if not font_dir:
            self.font_dir = str(Path.home() / '.paper_formatter' / 'fonts')
        
        os.makedirs(self.font_dir, exist_ok=True)
        
        self.api_keys = {}
        self._load_api_keys()
    
    def _load_api_keys(self):
        """加载 API 密钥"""
        key_file = os.path.join(self.font_dir, 'api_keys.json')
        if os.path.exists(key_file):
            try:
                with open(key_file, 'r', encoding='utf-8') as f:
                    self.api_keys = json.load(f)
            except Exception as e:
                print(f"加载 API 密钥失败：{e}")
    
    def save_api_keys(self):
        """保存 API 密钥"""
        key_file = os.path.join(self.font_dir, 'api_keys.json')
        try:
            with open(key_file, 'w', encoding='utf-8') as f:
                json.dump(self.api_keys, f, indent=2)
        except Exception as e:
            print(f"保存 API 密钥失败：{e}")
    
    def set_api_key(self, source: str, key: str):
        """设置 API 密钥"""
        self.api_keys[source] = key
        self.save_api_keys()
    
    def search_fonts(self, query: str = "", category: str = None,
                    is_chinese: bool = False) -> List[FontInfo]:
        """
        搜索字体
        
        Args:
            query: 搜索关键词
            category: 字体分类
            is_chinese: 是否中文字体
            
        Returns:
            字体信息列表
        """
        fonts = []
        
        # 如果是中文字体，返回预定义列表
        if is_chinese:
            for font_data in self.CHINESE_FONTS:
                if not query or query.lower() in font_data['name'].lower():
                    fonts.append(FontInfo(
                        name=font_data['name'],
                        family=font_data['family'],
                        url=font_data['url'],
                        category=font_data['category'],
                        is_chinese=True
                    ))
            return fonts
        
        # 搜索 Google Fonts
        try:
            google_fonts = self._search_google_fonts(query, category)
            fonts.extend(google_fonts)
        except Exception as e:
            print(f"搜索 Google Fonts 失败：{e}")
        
        return fonts
    
    def _search_google_fonts(self, query: str = "", category: str = None) -> List[FontInfo]:
        """搜索 Google Fonts"""
        fonts = []
        
        api_key = self.api_keys.get('google', '')
        if not api_key:
            # 没有 API 密钥时返回空列表
            return fonts
        
        try:
            url = 'https://www.googleapis.com/webfonts/v1/webfonts'
            params = {
                'key': api_key,
                'sort': 'popularity'
            }
            
            if query:
                params['query'] = query
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            items = data.get('items', [])
            
            for item in items:
                # 过滤分类
                if category and item.get('category') != category:
                    continue
                
                font = FontInfo(
                    name=item.get('family', ''),
                    family=item.get('family', ''),
                    category=item.get('category', 'sans-serif'),
                    url=item.get('files', {}).get('regular', ''),
                    is_chinese=False
                )
                fonts.append(font)
            
        except requests.exceptions.RequestException as e:
            print(f"Google Fonts API 请求失败：{e}")
        
        return fonts
    
    def download_font(self, font: FontInfo, save_path: str = None) -> str:
        """
        下载字体
        
        Args:
            font: 字体信息
            save_path: 保存路径
            
        Returns:
            保存的文件路径
        """
        if not font.url:
            raise ValueError("字体 URL 为空")
        
        if not save_path:
            # 自动生成保存路径
            filename = f"{font.family.replace(' ', '_')}.ttf"
            save_path = os.path.join(self.font_dir, filename)
        
        try:
            print(f"正在下载字体：{font.name}")
            response = requests.get(font.url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            
            # 写入文件
            with open(save_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # 显示进度
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r  下载进度：{percent:.1f}%", end='')
            
            print(f"\n✅ 字体下载完成：{save_path}")
            return save_path
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 字体下载失败：{e}")
            raise
    
    def install_font(self, font_path: str) -> bool:
        """
        安装字体
        
        Args:
            font_path: 字体文件路径
            
        Returns:
            是否成功
        """
        if not os.path.exists(font_path):
            print(f"❌ 字体文件不存在：{font_path}")
            return False
        
        try:
            # 不同平台的安装方式
            if sys.platform == 'win32':
                return self._install_font_windows(font_path)
            elif sys.platform == 'darwin':
                return self._install_font_macos(font_path)
            else:
                return self._install_font_linux(font_path)
                
        except Exception as e:
            print(f"❌ 字体安装失败：{e}")
            return False
    
    def _install_font_windows(self, font_path: str) -> bool:
        """Windows 安装字体"""
        try:
            import shutil
            import winreg
            
            # Windows 字体目录
            fonts_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
            
            # 复制字体文件
            font_name = os.path.basename(font_path)
            dest_path = os.path.join(fonts_dir, font_name)
            shutil.copy2(font_path, dest_path)
            
            # 注册字体
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows NT\CurrentVersion\Fonts',
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, font_name, 0, winreg.REG_SZ, font_name)
            winreg.CloseKey(key)
            
            print(f"✅ 字体已安装到 Windows: {font_name}")
            return True
            
        except Exception as e:
            print(f"❌ Windows 字体安装失败：{e}")
            return False
    
    def _install_font_macos(self, font_path: str) -> bool:
        """macOS 安装字体"""
        try:
            import shutil
            
            # macOS 用户字体目录
            fonts_dir = os.path.expanduser('~/Library/Fonts')
            
            # 复制字体文件
            font_name = os.path.basename(font_path)
            dest_path = os.path.join(fonts_dir, font_name)
            shutil.copy2(font_path, dest_path)
            
            print(f"✅ 字体已安装到 macOS: {font_name}")
            return True
            
        except Exception as e:
            print(f"❌ macOS 字体安装失败：{e}")
            return False
    
    def _install_font_linux(self, font_path: str) -> bool:
        """Linux 安装字体"""
        try:
            import shutil
            
            # Linux 用户字体目录
            fonts_dir = os.path.expanduser('~/.local/share/fonts')
            os.makedirs(fonts_dir, exist_ok=True)
            
            # 复制字体文件
            font_name = os.path.basename(font_path)
            dest_path = os.path.join(fonts_dir, font_name)
            shutil.copy2(font_path, dest_path)
            
            # 更新字体缓存
            os.system('fc-cache -fv')
            
            print(f"✅ 字体已安装到 Linux: {font_name}")
            return True
            
        except Exception as e:
            print(f"❌ Linux 字体安装失败：{e}")
            return False
    
    def get_installed_fonts(self) -> List[Dict[str, Any]]:
        """获取已安装的字体列表"""
        fonts = []
        
        # 扫描字体目录
        if os.path.exists(self.font_dir):
            for filename in os.listdir(self.font_dir):
                if filename.lower().endswith(('.ttf', '.otf', '.ttc')):
                    font_path = os.path.join(self.font_dir, filename)
                    font_info = self._get_font_info(font_path)
                    if font_info:
                        fonts.append(font_info)
        
        return fonts
    
    def _get_font_info(self, font_path: str) -> Optional[Dict[str, Any]]:
        """获取字体文件信息"""
        try:
            # 尝试使用 fonttools 读取字体信息
            from fontTools.ttLib import TTFont
            
            font = TTFont(font_path)
            name_table = font['name']
            
            info = {
                'path': font_path,
                'filename': os.path.basename(font_path),
                'name': '',
                'family': '',
                'style': ''
            }
            
            # 读取字体名称
            for record in name_table.names:
                if record.nameID == 1:  # Font Family
                    info['family'] = record.toUnicode()
                elif record.nameID == 2:  # Font Subfamily
                    info['style'] = record.toUnicode()
                elif record.nameID == 4:  # Full Name
                    info['name'] = record.toUnicode()
            
            font.close()
            return info
            
        except Exception as e:
            # 如果无法读取，返回基本信息
            return {
                'path': font_path,
                'filename': os.path.basename(font_path),
                'name': os.path.splitext(os.path.basename(font_path))[0],
                'family': '',
                'style': ''
            }
    
    def uninstall_font(self, font_path: str) -> bool:
        """卸载字体"""
        try:
            if os.path.exists(font_path):
                os.remove(font_path)
                print(f"✅ 字体已卸载：{font_path}")
                return True
            else:
                print(f"❌ 字体文件不存在：{font_path}")
                return False
        except Exception as e:
            print(f"❌ 字体卸载失败：{e}")
            return False
