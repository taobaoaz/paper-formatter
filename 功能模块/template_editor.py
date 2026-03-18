"""
模板编辑模块
Template Editor Module

功能：
- 创建新模板
- 编辑模板
- 删除模板
- 导入/导出模板
- 模板预览
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Any


class TemplateEditor:
    """模板编辑器"""
    
    # 模板存储目录
    TEMPLATE_DIR = os.path.join(os.path.expanduser('~'), '.paper_formatter', 'templates')
    
    def __init__(self, template_dir=None):
        """
        初始化模板编辑器
        
        参数：
        - template_dir: 模板目录
        """
        self.template_dir = template_dir or self.TEMPLATE_DIR
        os.makedirs(self.template_dir, exist_ok=True)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """
        列出所有模板
        
        返回：
        - list: 模板信息列表
        """
        templates = []
        
        if not os.path.exists(self.template_dir):
            return templates
        
        for filename in os.listdir(self.template_dir):
            if filename.endswith('.json'):
                template_path = os.path.join(self.template_dir, filename)
                template_info = self.get_template_info(template_path)
                if template_info:
                    templates.append(template_info)
        
        # 按创建时间排序
        templates.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return templates
    
    def get_template_info(self, template_path) -> Dict[str, Any]:
        """
        获取模板信息
        
        参数：
        - template_path: 模板文件路径
        
        返回：
        - dict: 模板信息
        """
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            return {
                'id': template_data.get('id', ''),
                'name': template_data.get('name', '未命名模板'),
                'description': template_data.get('description', ''),
                'school': template_data.get('school', ''),
                'type': template_data.get('type', 'general'),
                'created_at': template_data.get('created_at', ''),
                'updated_at': template_data.get('updated_at', ''),
                'path': template_path,
            }
        except:
            return {}
    
    def create_template(self, name: str, description: str = '', school: str = '', 
                       template_type: str = 'general') -> str:
        """
        创建新模板
        
        参数：
        - name: 模板名称
        - description: 模板描述
        - school: 适用学校
        - template_type: 模板类型（thesis/paper/general）
        
        返回：
        - str: 模板 ID，失败返回 None
        """
        try:
            # 生成模板 ID
            template_id = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # 创建模板数据
            template_data = {
                'id': template_id,
                'name': name,
                'description': description,
                'school': school,
                'type': template_type,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'format_config': {
                    'font': {
                        'chinese_font': '宋体',
                        'english_font': 'Times New Roman',
                        'font_size_pt': 12,
                        'line_spacing': 1.5,
                    },
                    'paragraph': {
                        'first_line_indent': 2,
                        'before_spacing': 0,
                        'after_spacing': 0,
                        'line_spacing_type': 'multi',
                        'line_spacing_value': 1.5,
                    },
                    'page': {
                        'paper_size': 'A4',
                        'margin_top_cm': 2.54,
                        'margin_bottom_cm': 2.54,
                        'margin_left_cm': 3.17,
                        'margin_right_cm': 3.17,
                    },
                    'heading': {
                        'level_1': {
                            'font_size_pt': 16,
                            'bold': True,
                            'numbering': '第 1 章',
                        },
                        'level_2': {
                            'font_size_pt': 14,
                            'bold': True,
                            'numbering': '1.1',
                        },
                        'level_3': {
                            'font_size_pt': 12,
                            'bold': False,
                            'numbering': '1.1.1',
                        },
                    },
                },
                'cover_config': {
                    'enabled': True,
                    'fields': [],
                },
            }
            
            # 保存模板
            template_path = os.path.join(self.template_dir, f'{template_id}.json')
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            
            print(f'✓ 模板已创建：{name}')
            return template_id
            
        except Exception as e:
            print(f'✗ 创建模板失败：{e}')
            return None
    
    def load_template(self, template_id: str) -> Dict[str, Any]:
        """
        加载模板
        
        参数：
        - template_id: 模板 ID
        
        返回：
        - dict: 模板数据
        """
        try:
            template_path = os.path.join(self.template_dir, f'{template_id}.json')
            
            if not os.path.exists(template_path):
                print(f'✗ 模板不存在：{template_id}')
                return None
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            return template_data
            
        except Exception as e:
            print(f'✗ 加载模板失败：{e}')
            return None
    
    def save_template(self, template_id: str, template_data: Dict[str, Any]) -> bool:
        """
        保存模板
        
        参数：
        - template_id: 模板 ID
        - template_data: 模板数据
        
        返回：
        - bool: 是否成功
        """
        try:
            template_path = os.path.join(self.template_dir, f'{template_id}.json')
            
            # 更新时间
            template_data['updated_at'] = datetime.now().isoformat()
            
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            
            print(f'✓ 模板已保存：{template_data.get("name", "")}')
            return True
            
        except Exception as e:
            print(f'✗ 保存模板失败：{e}')
            return False
    
    def delete_template(self, template_id: str) -> bool:
        """
        删除模板
        
        参数：
        - template_id: 模板 ID
        
        返回：
        - bool: 是否成功
        """
        try:
            template_path = os.path.join(self.template_dir, f'{template_id}.json')
            
            if not os.path.exists(template_path):
                print(f'✗ 模板不存在：{template_id}')
                return False
            
            os.remove(template_path)
            print(f'✓ 模板已删除：{template_id}')
            return True
            
        except Exception as e:
            print(f'✗ 删除模板失败：{e}')
            return False
    
    def export_template(self, template_id: str, export_path: str) -> bool:
        """
        导出模板
        
        参数：
        - template_id: 模板 ID
        - export_path: 导出路径
        
        返回：
        - bool: 是否成功
        """
        try:
            template_path = os.path.join(self.template_dir, f'{template_id}.json')
            
            if not os.path.exists(template_path):
                return False
            
            shutil.copy2(template_path, export_path)
            print(f'✓ 模板已导出：{export_path}')
            return True
            
        except Exception as e:
            print(f'✗ 导出模板失败：{e}')
            return False
    
    def import_template(self, import_path: str) -> str:
        """
        导入模板
        
        参数：
        - import_path: 导入路径
        
        返回：
        - str: 模板 ID，失败返回 None
        """
        try:
            if not os.path.exists(import_path):
                print(f'✗ 文件不存在：{import_path}')
                return None
            
            # 读取导入文件
            with open(import_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            # 生成新 ID
            template_id = datetime.now().strftime('%Y%m%d%H%M%S')
            template_data['id'] = template_id
            template_data['updated_at'] = datetime.now().isoformat()
            
            # 保存
            template_path = os.path.join(self.template_dir, f'{template_id}.json')
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            
            print(f'✓ 模板已导入：{template_data.get("name", "")}')
            return template_id
            
        except Exception as e:
            print(f'✗ 导入模板失败：{e}')
            return None
    
    def duplicate_template(self, template_id: str, new_name: str) -> str:
        """
        复制模板
        
        参数：
        - template_id: 原模板 ID
        - new_name: 新模板名称
        
        返回：
        - str: 新模板 ID
        """
        try:
            # 加载原模板
            template_data = self.load_template(template_id)
            
            if not template_data:
                return None
            
            # 修改名称
            template_data['name'] = new_name
            
            # 创建新模板
            new_id = self.create_template(
                name=new_name,
                description=template_data.get('description', ''),
                school=template_data.get('school', ''),
                template_type=template_data.get('type', 'general')
            )
            
            # 保存完整数据
            if new_id:
                self.save_template(new_id, template_data)
            
            return new_id
            
        except Exception as e:
            print(f'✗ 复制模板失败：{e}')
            return None
    
    def get_template_count(self) -> int:
        """
        获取模板数量
        
        返回：
        - int: 模板数量
        """
        return len(self.list_templates())


# 快捷函数
def create_editor(template_dir=None):
    """创建模板编辑器"""
    return TemplateEditor(template_dir)


if __name__ == '__main__':
    # 测试
    editor = TemplateEditor()
    
    print(f'当前模板数：{editor.get_template_count()}')
    
    # 列出模板
    templates = editor.list_templates()
    for t in templates:
        print(f"- {t['name']} ({t['school']})")
