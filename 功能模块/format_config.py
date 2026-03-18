"""
格式化配置模块
Format Configuration Module

功能：
- 字体配置
- 段落配置
- 页面配置
- 目录配置
- 配置保存/加载
"""

import json
import os
from typing import Dict, Any


class FormatConfig:
    """格式化配置管理器"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        'font': {
            'chinese_font': '宋体',
            'english_font': 'Times New Roman',
            'font_size': '小四',
            'font_size_pt': 12,
            'line_spacing': 1.5,
        },
        'paragraph': {
            'first_line_indent': 2,  # 字符数
            'before_spacing': 0,  # 磅
            'after_spacing': 0,  # 磅
            'line_spacing_type': 'multi',  # single, multi, exactly
            'line_spacing_value': 1.5,
        },
        'page': {
            'paper_size': 'A4',
            'width_cm': 21,
            'height_cm': 29.7,
            'margin_top_cm': 2.54,
            'margin_bottom_cm': 2.54,
            'margin_left_cm': 3.17,
            'margin_right_cm': 3.17,
        },
        'heading': {
            'level_1': {
                'font_size': '三号',
                'font_size_pt': 16,
                'bold': True,
                'numbering': '第 1 章',
            },
            'level_2': {
                'font_size': '四号',
                'font_size_pt': 14,
                'bold': True,
                'numbering': '1.1',
            },
            'level_3': {
                'font_size': '小四',
                'font_size_pt': 12,
                'bold': False,
                'numbering': '1.1.1',
            },
        },
        'toc': {
            'enabled': True,
            'max_level': 3,
            'title': '目录',
        },
        'reference': {
            'style': 'GB/T 7714',
            'title': '参考文献',
        }
    }
    
    def __init__(self, config_path=None):
        """
        初始化配置管理器
        
        参数：
        - config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        
        # 如果配置文件存在，加载配置
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
    
    def get_config(self, section=None, key=None):
        """
        获取配置
        
        参数：
        - section: 配置节（如 'font', 'paragraph'）
        - key: 配置键（如 'chinese_font'）
        
        返回：
        - 配置值
        """
        if section is None:
            return self.config
        
        if section not in self.config:
            return None
        
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key)
    
    def set_config(self, section, key, value):
        """
        设置配置
        
        参数：
        - section: 配置节
        - key: 配置键
        - value: 配置值
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
    
    def update_config(self, section, updates):
        """
        批量更新配置
        
        参数：
        - section: 配置节
        - updates: 更新字典
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section].update(updates)
    
    def save_config(self, path=None):
        """
        保存配置到文件
        
        参数：
        - path: 保存路径（可选）
        
        返回：
        - bool: 是否成功
        """
        try:
            save_path = path or self.config_path
            
            if not save_path:
                # 默认保存到用户目录
                from pathlib import Path
                config_dir = Path.home() / '.paper_formatter'
                config_dir.mkdir(exist_ok=True)
                save_path = str(config_dir / 'format_config.json')
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            print(f'✓ 配置已保存：{save_path}')
            return True
            
        except Exception as e:
            print(f'✗ 保存配置失败：{e}')
            return False
    
    def load_config(self, path=None):
        """
        从文件加载配置
        
        参数：
        - path: 加载路径（可选）
        
        返回：
        - bool: 是否成功
        """
        try:
            load_path = path or self.config_path
            
            if not load_path or not os.path.exists(load_path):
                return False
            
            with open(load_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            
            # 合并配置
            self._merge_config(loaded_config)
            
            print(f'✓ 配置已加载：{load_path}')
            return True
            
        except Exception as e:
            print(f'✗ 加载配置失败：{e}')
            return False
    
    def _merge_config(self, new_config):
        """
        合并配置
        
        参数：
        - new_config: 新配置
        """
        for section, values in new_config.items():
            if section not in self.config:
                self.config[section] = values
            elif isinstance(values, dict):
                self.config[section].update(values)
            else:
                self.config[section] = values
    
    def reset_to_default(self):
        """重置为默认配置"""
        self.config = self.DEFAULT_CONFIG.copy()
        print('✓ 已重置为默认配置')
    
    def export_config(self, path):
        """
        导出配置
        
        参数：
        - path: 导出路径
        """
        return self.save_config(path)
    
    def import_config(self, path):
        """
        导入配置
        
        参数：
        - path: 导入路径
        
        返回：
        - bool: 是否成功
        """
        return self.load_config(path)
    
    def validate_config(self):
        """
        验证配置
        
        返回：
        - tuple: (是否有效，错误列表)
        """
        errors = []
        
        # 验证字体配置
        font = self.config.get('font', {})
        if not font.get('chinese_font'):
            errors.append('中文字体不能为空')
        if not font.get('english_font'):
            errors.append('英文字体不能为空')
        
        # 验证页面配置
        page = self.config.get('page', {})
        if page.get('margin_left_cm', 0) <= 0:
            errors.append('左边距必须大于 0')
        if page.get('margin_right_cm', 0) <= 0:
            errors.append('右边距必须大于 0')
        
        return len(errors) == 0, errors
    
    def get_config_summary(self):
        """
        获取配置摘要
        
        返回：
        - str: 配置摘要文本
        """
        summary = []
        summary.append('格式化配置摘要')
        summary.append('=' * 40)
        
        font = self.config.get('font', {})
        summary.append(f"字体：{font.get('chinese_font', 'N/A')} / {font.get('english_font', 'N/A')}")
        summary.append(f"字号：{font.get('font_size', 'N/A')} ({font.get('font_size_pt', 'N/A')}pt)")
        
        paragraph = self.config.get('paragraph', {})
        summary.append(f"行距：{paragraph.get('line_spacing_value', 'N/A')} 倍")
        summary.append(f"首行缩进：{paragraph.get('first_line_indent', 'N/A')} 字符")
        
        page = self.config.get('page', {})
        summary.append(f"纸张：{page.get('paper_size', 'N/A')} ({page.get('width_cm', 'N/A')}x{page.get('height_cm', 'N/A')}cm)")
        
        return '\n'.join(summary)


# 快捷函数
def get_default_config():
    """获取默认配置"""
    return FormatConfig.DEFAULT_CONFIG.copy()


def create_config(config_path=None):
    """创建配置管理器"""
    return FormatConfig(config_path)


if __name__ == '__main__':
    # 测试
    config = FormatConfig()
    print(config.get_config_summary())
    
    # 测试保存
    config.save_config('test_config.json')
    
    # 测试加载
    config2 = FormatConfig('test_config.json')
    print(config2.get_config_summary())
