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
    
    def backup_config(self, backup_dir=None):
        """
        备份当前配置
        
        参数：
        - backup_dir: 备份目录（可选）
        
        返回：
        - str: 备份文件路径，失败返回 None
        """
        try:
            from datetime import datetime
            
            if not backup_dir:
                from pathlib import Path
                backup_dir = Path.home() / '.paper_formatter' / 'backups'
                backup_dir.mkdir(exist_ok=True)
            elif not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f'format_config_{timestamp}.json')
            
            if self.save_config(backup_path):
                print(f'✓ 配置已备份：{backup_path}')
                return backup_path
            else:
                return None
                
        except Exception as e:
            print(f'✗ 备份配置失败：{e}')
            return None
    
    def auto_fix_config(self):
        """
        自动修复配置问题
        
        返回：
        - tuple: (修复数量，修复报告)
        """
        fixes = []
        
        # 自动修复字体
        font = self.config.get('font', {})
        if not font.get('chinese_font'):
            self.config['font']['chinese_font'] = '宋体'
            fixes.append('设置默认中文字体：宋体')
        
        if not font.get('english_font'):
            self.config['font']['english_font'] = 'Times New Roman'
            fixes.append('设置默认英文字体：Times New Roman')
        
        # 自动修复字号
        font_size_pt = font.get('font_size_pt', 0)
        if font_size_pt <= 0:
            self.config['font']['font_size_pt'] = 12
            fixes.append('设置默认字号：12pt')
        elif font_size_pt > 72:
            self.config['font']['font_size_pt'] = 72
            fixes.append('修正字号为最大值：72pt')
        
        # 自动修复行距
        line_spacing = font.get('line_spacing', 0)
        if line_spacing <= 0:
            self.config['font']['line_spacing'] = 1.5
            fixes.append('设置默认行距：1.5 倍')
        elif line_spacing > 3.0:
            self.config['font']['line_spacing'] = 3.0
            fixes.append('修正行距为最大值：3.0 倍')
        
        # 自动修复页边距
        page = self.config.get('page', {})
        if page.get('margin_left_cm', 0) <= 0:
            self.config['page']['margin_left_cm'] = 3.17
            fixes.append('设置默认左边距：3.17cm')
        if page.get('margin_right_cm', 0) <= 0:
            self.config['page']['margin_right_cm'] = 3.17
            fixes.append('设置默认右边距：3.17cm')
        if page.get('margin_top_cm', 0) <= 0:
            self.config['page']['margin_top_cm'] = 2.54
            fixes.append('设置默认上边距：2.54cm')
        if page.get('margin_bottom_cm', 0) <= 0:
            self.config['page']['margin_bottom_cm'] = 2.54
            fixes.append('设置默认下边距：2.54cm')
        
        # 自动修复纸张尺寸
        width = page.get('width_cm', 0)
        height = page.get('height_cm', 0)
        if width <= 0 or height <= 0:
            self.config['page']['width_cm'] = 21
            self.config['page']['height_cm'] = 29.7
            fixes.append('设置默认纸张尺寸：A4 (21x29.7cm)')
        elif width > 50:
            self.config['page']['width_cm'] = 50
            fixes.append('修正纸张宽度为最大值：50cm')
        elif height > 100:
            self.config['page']['height_cm'] = 100
            fixes.append('修正纸张高度为最大值：100cm')
        
        report = f'自动修复完成，共修复 {len(fixes)} 个问题:\n' + '\n'.join([f'  ✓ {f}' for f in fixes]) if fixes else '无需修复'
        
        return len(fixes), report
    
    def compare_configs(self, other_config):
        """
        比较两个配置的差异
        
        参数：
        - other_config: 另一个配置对象或配置字典
        
        返回：
        - dict: 差异字典 {section: {key: (old_value, new_value)}}
        """
        if isinstance(other_config, FormatConfig):
            other = other_config.config
        else:
            other = other_config
        
        differences = {}
        
        for section in set(list(self.config.keys()) + list(other.keys())):
            section_diff = {}
            self_section = self.config.get(section, {})
            other_section = other.get(section, {})
            
            all_keys = set(list(self_section.keys()) + list(other_section.keys()))
            
            for key in all_keys:
                self_value = self_section.get(key)
                other_value = other_section.get(key)
                
                if self_value != other_value:
                    section_diff[key] = (self_value, other_value)
            
            if section_diff:
                differences[section] = section_diff
        
        return differences
    
    def get_config_diff_report(self, other_config):
        """
        获取配置差异报告
        
        参数：
        - other_config: 另一个配置对象
        
        返回：
        - str: 差异报告文本
        """
        differences = self.compare_configs(other_config)
        
        if not differences:
            return '两个配置完全相同'
        
        report = ['配置差异报告', '=' * 40]
        
        for section, section_diff in differences.items():
            report.append(f'\n[{section}]')
            for key, (old_val, new_val) in section_diff.items():
                report.append(f'  {key}: {old_val} → {new_val}')
        
        return '\n'.join(report)
    
    def validate_config(self, strict=False):
        """
        验证配置
        
        参数：
        - strict: 是否严格模式（严格模式下警告也算错误）
        
        返回：
        - tuple: (是否有效，错误列表，警告列表)
        """
        errors = []
        warnings = []
        
        # 验证字体配置
        font = self.config.get('font', {})
        if not font.get('chinese_font'):
            errors.append('中文字体不能为空')
        elif font.get('chinese_font') not in self._get_valid_chinese_fonts():
            warnings.append(f"中文字体 '{font.get('chinese_font')}' 可能不可用")
        
        if not font.get('english_font'):
            errors.append('英文字体不能为空')
        elif font.get('english_font') not in self._get_valid_english_fonts():
            warnings.append(f"英文字体 '{font.get('english_font')}' 可能不可用")
        
        # 验证字号
        font_size_pt = font.get('font_size_pt', 0)
        if font_size_pt <= 0 or font_size_pt > 72:
            errors.append(f"字号必须在 0-72pt 之间，当前为 {font_size_pt}pt")
        
        # 验证行距
        line_spacing = font.get('line_spacing', 0)
        if line_spacing <= 0 or line_spacing > 3.0:
            errors.append(f"行距必须在 0-3.0 之间，当前为 {line_spacing}")
        
        # 验证页面配置
        page = self.config.get('page', {})
        if page.get('margin_left_cm', 0) <= 0:
            errors.append('左边距必须大于 0')
        if page.get('margin_right_cm', 0) <= 0:
            errors.append('右边距必须大于 0')
        if page.get('margin_top_cm', 0) <= 0:
            errors.append('上边距必须大于 0')
        if page.get('margin_bottom_cm', 0) <= 0:
            errors.append('下边距必须大于 0')
        
        # 验证纸张尺寸
        width = page.get('width_cm', 0)
        height = page.get('height_cm', 0)
        if width <= 0 or height <= 0:
            errors.append('纸张尺寸必须大于 0')
        elif width > 50 or height > 100:
            warnings.append('纸张尺寸异常，请确认是否正确')
        
        # 验证段落配置
        paragraph = self.config.get('paragraph', {})
        first_line_indent = paragraph.get('first_line_indent', 0)
        if first_line_indent < 0 or first_line_indent > 10:
            warnings.append(f"首行缩进 {first_line_indent} 字符可能不合理")
        
        # 验证标题配置
        heading = self.config.get('heading', {})
        for level in ['level_1', 'level_2', 'level_3']:
            if level in heading:
                h = heading[level]
                h_size = h.get('font_size_pt', 0)
                if h_size <= 0 or h_size > 72:
                    errors.append(f"{level} 字号必须在 0-72pt 之间")
        
        # 严格模式下，警告也算错误
        if strict:
            errors.extend(warnings)
            warnings = []
        
        return len(errors) == 0, errors, warnings
    
    def _get_valid_chinese_fonts(self):
        """获取有效的中文字体列表"""
        return ['宋体', '黑体', '楷体', '仿宋', '微软雅黑', '思源宋体', '思源黑体', 
                '华文宋体', '华文黑体', '方正宋体', '方正黑体', '隶书']
    
    def _get_valid_english_fonts(self):
        """获取有效的英文字体列表"""
        return ['Times New Roman', 'Arial', 'Calibri', 'Cambria', 'Georgia', 
                'Verdana', 'Helvetica', 'Garamond', 'Courier New']
    
    def get_validation_report(self):
        """
        获取配置验证报告
        
        返回：
        - str: 验证报告文本
        """
        is_valid, errors, warnings = self.validate_config()
        
        report = []
        report.append('配置验证报告')
        report.append('=' * 40)
        
        if is_valid and not warnings:
            report.append('✅ 配置验证通过，无问题')
        elif is_valid:
            report.append(f'⚠️ 配置验证通过，但有 {len(warnings)} 个警告')
            for w in warnings:
                report.append(f'  - {w}')
        else:
            report.append(f'❌ 配置验证失败：{len(errors)} 个错误，{len(warnings)} 个警告')
            for e in errors:
                report.append(f'  ✗ {e}')
            for w in warnings:
                report.append(f'  ⚠ {w}')
        
        return '\n'.join(report)
    
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
