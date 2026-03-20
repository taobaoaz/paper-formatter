import json
import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import config


@dataclass
class TemplateRecognitionResult:
    template_id: str
    template_name: str
    template_type: str
    confidence: float
    rules: Dict[str, Any]
    description: str


class AIRecognizer:
    def __init__(self, api_url: str = None, api_key: str = None, model: str = None):
        self.api_url = api_url or config.AI_API_CONFIG.get('api_url', '')
        self.api_key = api_key or config.AI_API_CONFIG.get('api_key', '')
        self.model = model or config.AI_API_CONFIG.get('model', '')
        self.timeout = config.AI_API_CONFIG.get('timeout', 60)
    
    def recognize_template(self, document_info: Dict[str, Any]) -> TemplateRecognitionResult:
        if not self.api_url or not self.api_key:
            return self._fallback_recognition(document_info)
        
        prompt = self._build_recognition_prompt(document_info)
        
        try:
            response = self._call_api(prompt)
            return self._parse_response(response)
        except Exception as e:
            print(f"AI API 调用失败: {e}")
            return self._fallback_recognition(document_info)
    
    def _build_recognition_prompt(self, document_info: Dict[str, Any]) -> str:
        metadata = document_info.get('metadata', {})
        elements = document_info.get('elements', [])
        
        element_summary = []
        for elem in elements[:20]:
            element_summary.append({
                'type': elem.get('element_type', ''),
                'content': elem.get('content', '')[:100],
                'level': elem.get('level', 0)
            })
        
        prompt = f"""请分析以下论文文档信息，识别其对应的模板类型，并返回格式规范要求。

文档元数据:
- 标题: {metadata.get('title', '未知')}
- 作者: {metadata.get('author', '未知')}
- 关键词: {metadata.get('keywords', '未知')}

文档结构概览:
{json.dumps(element_summary, ensure_ascii=False, indent=2)}

请以JSON格式返回以下信息:
{{
    "template_id": "模板唯一标识符",
    "template_name": "模板名称",
    "template_type": "模板类型(中文期刊/国际期刊/学位论文/自定义)",
    "confidence": 0.95,
    "description": "模板描述",
    "rules": {{
        "font_family": "正文字体",
        "font_size": 正文字号,
        "line_spacing": 行距倍数,
        "margin_top": 上边距(cm),
        "margin_bottom": 下边距(cm),
        "margin_left": 左边距(cm),
        "margin_right": 右边距(cm),
        "title_font": "标题字体",
        "title_size": 标题字号,
        "heading1_font": "一级标题字体",
        "heading1_size": 一级标题字号,
        "heading2_font": "二级标题字体",
        "heading2_size": 二级标题字号,
        "heading3_font": "三级标题字体",
        "heading3_size": 三级标题字号,
        "abstract_font": "摘要字体",
        "abstract_size": 摘要字号,
        "reference_format": "参考文献格式(GB/T 7714/APA/MLA等)"
    }}
}}

只返回JSON，不要包含其他文字。"""
        
        return prompt
    
    def _call_api(self, prompt: str) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        data = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.3,
            'max_tokens': 2000
        }
        
        response = requests.post(
            self.api_url,
            headers=headers,
            json=data,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"API返回错误: {response.status_code} - {response.text}")
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _parse_response(self, response: str) -> TemplateRecognitionResult:
        json_match = None
        import re
        json_pattern = r'\{[\s\S]*\}'
        match = re.search(json_pattern, response)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
        else:
            data = json.loads(response)
        
        return TemplateRecognitionResult(
            template_id=data.get('template_id', 'unknown'),
            template_name=data.get('template_name', '未知模板'),
            template_type=data.get('template_type', '自定义'),
            confidence=data.get('confidence', 0.5),
            rules=data.get('rules', config.DEFAULT_TEMPLATE_RULES),
            description=data.get('description', '')
        )
    
    def _fallback_recognition(self, document_info: Dict[str, Any]) -> TemplateRecognitionResult:
        metadata = document_info.get('metadata', {})
        elements = document_info.get('elements', [])
        
        template_type = '自定义'
        template_name = '通用学术论文模板'
        rules = config.DEFAULT_TEMPLATE_RULES.copy()
        
        title = metadata.get('title', '')
        content_sample = ' '.join([e.get('content', '') for e in elements[:10]])
        
        if any(keyword in title + content_sample for keyword in ['学位论文', '毕业论文', '硕士', '博士']):
            template_type = '学位论文'
            template_name = '中国高校学位论文模板'
            rules.update({
                'font_family': '宋体',
                'font_size': 12,
                'line_spacing': 1.5,
                'margin_top': 2.5,
                'margin_bottom': 2.5,
                'margin_left': 2.5,
                'margin_right': 2.5,
                'title_font': '黑体',
                'title_size': 22,
                'reference_format': 'GB/T 7714'
            })
        elif any(keyword in title + content_sample for keyword in ['IEEE', 'ACM', 'Springer', 'Elsevier']):
            template_type = '国际期刊'
            template_name = '国际期刊模板'
            rules.update({
                'font_family': 'Times New Roman',
                'font_size': 10,
                'line_spacing': 1.0,
                'margin_top': 2.5,
                'margin_bottom': 2.5,
                'margin_left': 2.0,
                'margin_right': 2.0,
                'title_font': 'Times New Roman',
                'title_size': 14,
                'reference_format': 'IEEE'
            })
        elif any(keyword in content_sample for keyword in ['摘要', '关键词', '引言']):
            template_type = '中文期刊'
            template_name = '中文期刊模板'
            rules.update({
                'font_family': '宋体',
                'font_size': 10.5,
                'line_spacing': 1.25,
                'margin_top': 2.0,
                'margin_bottom': 2.0,
                'margin_left': 2.0,
                'margin_right': 2.0,
                'title_font': '黑体',
                'title_size': 18,
                'reference_format': 'GB/T 7714'
            })
        
        return TemplateRecognitionResult(
            template_id=template_type.lower().replace('/', '_'),
            template_name=template_name,
            template_type=template_type,
            confidence=0.7,
            rules=rules,
            description=f'基于文档内容自动识别的{template_type}模板'
        )
    
    def analyze_document_structure(self, document_info: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_url or not self.api_key:
            return self._basic_structure_analysis(document_info)
        
        prompt = f"""请分析以下论文文档的结构，识别可能存在的格式问题。

文档信息:
{json.dumps(document_info, ensure_ascii=False, indent=2, default=str)}

请以JSON格式返回结构分析结果:
{{
    "sections": ["章节列表"],
    "issues": [
        {{
            "type": "问题类型",
            "location": "位置描述",
            "description": "问题描述",
            "suggestion": "修改建议"
        }}
    ],
    "completeness_score": 0.85
}}

只返回JSON。"""
        
        try:
            response = self._call_api(prompt)
            return json.loads(response)
        except Exception as e:
            print(f"结构分析失败: {e}")
            return self._basic_structure_analysis(document_info)
    
    def _basic_structure_analysis(self, document_info: Dict[str, Any]) -> Dict[str, Any]:
        elements = document_info.get('elements', [])
        
        sections = []
        issues = []
        
        has_abstract = False
        has_keywords = False
        has_references = False
        has_introduction = False
        
        for elem in elements:
            elem_type = elem.get('element_type', '')
            content = elem.get('content', '')
            
            if elem_type == 'heading':
                sections.append(content)
            
            if elem_type == 'abstract':
                has_abstract = True
            elif elem_type == 'keywords':
                has_keywords = True
            elif elem_type == 'references':
                has_references = True
            elif '引言' in content or 'Introduction' in content.lower():
                has_introduction = True
        
        if not has_abstract:
            issues.append({
                'type': '缺失部分',
                'location': '文档开头',
                'description': '未检测到摘要部分',
                'suggestion': '添加中英文摘要'
            })
        
        if not has_keywords:
            issues.append({
                'type': '缺失部分',
                'location': '摘要后',
                'description': '未检测到关键词',
                'suggestion': '添加关键词'
            })
        
        if not has_references:
            issues.append({
                'type': '缺失部分',
                'location': '文档末尾',
                'description': '未检测到参考文献',
                'suggestion': '添加参考文献列表'
            })
        
        completeness = 1.0 - (len(issues) * 0.15)
        completeness = max(0.3, min(1.0, completeness))
        
        return {
            'sections': sections,
            'issues': issues,
            'completeness_score': completeness
        }
