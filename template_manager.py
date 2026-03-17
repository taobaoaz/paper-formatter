import os
import json
import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
import config


@dataclass
class TemplateRule:
    name: str
    value: Any
    description: str = ""
    unit: str = ""


@dataclass
class Template:
    template_id: str
    template_name: str
    template_type: str
    description: str
    rules: Dict[str, Any]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Template':
        return cls(
            template_id=data.get('template_id', ''),
            template_name=data.get('template_name', ''),
            template_type=data.get('template_type', '自定义'),
            description=data.get('description', ''),
            rules=data.get('rules', {}),
            created_at=data.get('created_at', datetime.now().isoformat()),
            updated_at=data.get('updated_at', datetime.now().isoformat())
        )


class TemplateManager:
    def __init__(self, templates_dir: str = None):
        self.templates_dir = templates_dir or config.TEMPLATES_DIR
        self.templates: Dict[str, Template] = {}
        self._ensure_dir()
        self._load_builtin_templates()
        self._load_custom_templates()
    
    def _ensure_dir(self):
        os.makedirs(self.templates_dir, exist_ok=True)
    
    def _load_builtin_templates(self):
        builtin_templates = [
            {
                'template_id': 'cn_journal_standard',
                'template_name': '中文期刊标准模板',
                'template_type': '中文期刊',
                'description': '适用于中国知网、万方等中文学术期刊',
                'rules': {
                    'font_family': '宋体',
                    'font_size': 10.5,
                    'line_spacing': 1.25,
                    'margin_top': 2.0,
                    'margin_bottom': 2.0,
                    'margin_left': 2.0,
                    'margin_right': 2.0,
                    'title_font': '黑体',
                    'title_size': 18,
                    'title_bold': True,
                    'heading1_font': '黑体',
                    'heading1_size': 14,
                    'heading1_bold': True,
                    'heading2_font': '黑体',
                    'heading2_size': 12,
                    'heading2_bold': True,
                    'heading3_font': '黑体',
                    'heading3_size': 10.5,
                    'heading3_bold': True,
                    'abstract_font': '楷体',
                    'abstract_size': 9,
                    'keywords_font': '楷体',
                    'keywords_size': 9,
                    'reference_format': 'GB/T 7714',
                    'reference_font': '宋体',
                    'reference_size': 9
                }
            },
            {
                'template_id': 'cn_thesis_master',
                'template_name': '中国高校硕士学位论文模板',
                'template_type': '学位论文',
                'description': '适用于中国高校硕士学位论文',
                'rules': {
                    'font_family': '宋体',
                    'font_size': 12,
                    'line_spacing': 1.5,
                    'margin_top': 2.5,
                    'margin_bottom': 2.5,
                    'margin_left': 2.5,
                    'margin_right': 2.5,
                    'title_font': '黑体',
                    'title_size': 22,
                    'title_bold': True,
                    'heading1_font': '黑体',
                    'heading1_size': 16,
                    'heading1_bold': True,
                    'heading2_font': '黑体',
                    'heading2_size': 14,
                    'heading2_bold': True,
                    'heading3_font': '黑体',
                    'heading3_size': 12,
                    'heading3_bold': True,
                    'abstract_font': '宋体',
                    'abstract_size': 12,
                    'keywords_font': '宋体',
                    'keywords_size': 12,
                    'reference_format': 'GB/T 7714',
                    'reference_font': '宋体',
                    'reference_size': 10.5
                }
            },
            {
                'template_id': 'cn_thesis_doctor',
                'template_name': '中国高校博士学位论文模板',
                'template_type': '学位论文',
                'description': '适用于中国高校博士学位论文',
                'rules': {
                    'font_family': '宋体',
                    'font_size': 12,
                    'line_spacing': 1.5,
                    'margin_top': 3.0,
                    'margin_bottom': 3.0,
                    'margin_left': 2.5,
                    'margin_right': 2.5,
                    'title_font': '黑体',
                    'title_size': 26,
                    'title_bold': True,
                    'heading1_font': '黑体',
                    'heading1_size': 18,
                    'heading1_bold': True,
                    'heading2_font': '黑体',
                    'heading2_size': 16,
                    'heading2_bold': True,
                    'heading3_font': '黑体',
                    'heading3_size': 14,
                    'heading3_bold': True,
                    'abstract_font': '宋体',
                    'abstract_size': 12,
                    'keywords_font': '宋体',
                    'keywords_size': 12,
                    'reference_format': 'GB/T 7714',
                    'reference_font': '宋体',
                    'reference_size': 10.5
                }
            },
            {
                'template_id': 'ieee_journal',
                'template_name': 'IEEE期刊模板',
                'template_type': '国际期刊',
                'description': '适用于IEEE期刊投稿',
                'rules': {
                    'font_family': 'Times New Roman',
                    'font_size': 10,
                    'line_spacing': 1.0,
                    'margin_top': 1.9,
                    'margin_bottom': 2.54,
                    'margin_left': 1.78,
                    'margin_right': 1.78,
                    'title_font': 'Times New Roman',
                    'title_size': 24,
                    'title_bold': True,
                    'heading1_font': 'Times New Roman',
                    'heading1_size': 10,
                    'heading1_bold': True,
                    'heading2_font': 'Times New Roman',
                    'heading2_size': 10,
                    'heading2_bold': True,
                    'heading2_italic': True,
                    'heading3_font': 'Times New Roman',
                    'heading3_size': 10,
                    'heading3_italic': True,
                    'abstract_font': 'Times New Roman',
                    'abstract_size': 9,
                    'abstract_italic': True,
                    'keywords_font': 'Times New Roman',
                    'keywords_size': 9,
                    'reference_format': 'IEEE',
                    'reference_font': 'Times New Roman',
                    'reference_size': 9
                }
            },
            {
                'template_id': 'springer_journal',
                'template_name': 'Springer期刊模板',
                'template_type': '国际期刊',
                'description': '适用于Springer期刊投稿',
                'rules': {
                    'font_family': 'Times New Roman',
                    'font_size': 10,
                    'line_spacing': 1.2,
                    'margin_top': 2.5,
                    'margin_bottom': 2.5,
                    'margin_left': 2.0,
                    'margin_right': 2.0,
                    'title_font': 'Times New Roman',
                    'title_size': 16,
                    'title_bold': True,
                    'heading1_font': 'Times New Roman',
                    'heading1_size': 12,
                    'heading1_bold': True,
                    'heading2_font': 'Times New Roman',
                    'heading2_size': 11,
                    'heading2_bold': True,
                    'heading3_font': 'Times New Roman',
                    'heading3_size': 10,
                    'heading3_bold': True,
                    'abstract_font': 'Times New Roman',
                    'abstract_size': 9,
                    'keywords_font': 'Times New Roman',
                    'keywords_size': 9,
                    'reference_format': 'Springer',
                    'reference_font': 'Times New Roman',
                    'reference_size': 9
                }
            }
        ]
        
        for template_data in builtin_templates:
            template = Template.from_dict(template_data)
            self.templates[template.template_id] = template
    
    def _load_custom_templates(self):
        for filename in os.listdir(self.templates_dir):
            if filename.endswith(('.json', '.yaml', '.yml')):
                filepath = os.path.join(self.templates_dir, filename)
                try:
                    template = self._load_template_file(filepath)
                    if template:
                        self.templates[template.template_id] = template
                except Exception as e:
                    print(f"加载模板文件失败 {filename}: {e}")
    
    def _load_template_file(self, filepath: str) -> Optional[Template]:
        with open(filepath, 'r', encoding='utf-8') as f:
            if filepath.endswith('.json'):
                data = json.load(f)
            else:
                data = yaml.safe_load(f)
        
        return Template.from_dict(data)
    
    def get_template(self, template_id: str) -> Optional[Template]:
        return self.templates.get(template_id)
    
    def get_all_templates(self) -> List[Template]:
        return list(self.templates.values())
    
    def get_templates_by_type(self, template_type: str) -> List[Template]:
        return [t for t in self.templates.values() if t.template_type == template_type]
    
    def add_template(self, template: Template) -> bool:
        try:
            self.templates[template.template_id] = template
            self._save_template(template)
            return True
        except Exception as e:
            print(f"添加模板失败: {e}")
            return False
    
    def update_template(self, template_id: str, rules: Dict[str, Any]) -> bool:
        template = self.templates.get(template_id)
        if not template:
            return False
        
        template.rules.update(rules)
        template.updated_at = datetime.now().isoformat()
        self._save_template(template)
        return True
    
    def delete_template(self, template_id: str) -> bool:
        if template_id not in self.templates:
            return False
        
        template = self.templates[template_id]
        
        builtin_ids = ['cn_journal_standard', 'cn_thesis_master', 'cn_thesis_doctor', 
                       'ieee_journal', 'springer_journal']
        if template_id in builtin_ids:
            return False
        
        del self.templates[template_id]
        
        for ext in ['.json', '.yaml']:
            filepath = os.path.join(self.templates_dir, f"{template_id}{ext}")
            if os.path.exists(filepath):
                os.remove(filepath)
        
        return True
    
    def _save_template(self, template: Template):
        filepath = os.path.join(self.templates_dir, f"{template.template_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template.to_dict(), f, ensure_ascii=False, indent=2)
    
    def create_custom_template(self, name: str, base_template_id: str = None, 
                                custom_rules: Dict[str, Any] = None) -> Template:
        import uuid
        
        template_id = f"custom_{uuid.uuid4().hex[:8]}"
        
        if base_template_id and base_template_id in self.templates:
            base_rules = self.templates[base_template_id].rules.copy()
        else:
            base_rules = config.DEFAULT_TEMPLATE_RULES.copy()
        
        if custom_rules:
            base_rules.update(custom_rules)
        
        template = Template(
            template_id=template_id,
            template_name=name,
            template_type='自定义',
            description=f'用户自定义模板 - {name}',
            rules=base_rules
        )
        
        self.add_template(template)
        return template
    
    def export_template(self, template_id: str, export_path: str) -> bool:
        template = self.templates.get(template_id)
        if not template:
            return False
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(template.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"导出模板失败: {e}")
            return False
    
    def import_template(self, filepath: str) -> Optional[Template]:
        try:
            template = self._load_template_file(filepath)
            if template:
                template.template_id = f"imported_{template.template_id}"
                self.add_template(template)
                return template
            return None
        except Exception as e:
            print(f"导入模板失败: {e}")
            return None
