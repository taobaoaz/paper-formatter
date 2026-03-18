import os
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from docx import Document
from docx.shared import Pt, Cm, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH


@dataclass
class ExtractedFormat:
    element_type: str
    content_sample: str
    font_name: str
    font_size: float
    bold: bool
    italic: bool
    alignment: str
    line_spacing: float
    first_line_indent: float
    confidence: float


class WordFormatExtractor:
    ELEMENT_KEYWORDS = {
        'title': ['毕业论文', '论文题目', '论文标题', '题目', '标题', '论文题目：', '文章标题'],
        'title_en': ['title', 'thesis', 'dissertation'],
        'author': ['作者', '姓名', '学号', '学生姓名'],
        'affiliation': ['单位', '学院', '学校', '专业', '系'],
        'abstract': ['摘要', '中文摘要', '内容摘要', '摘 要'],
        'abstract_en': ['abstract', '摘要'],
        'keywords': ['关键词', '关键字', '关键词：'],
        'heading1': ['第一章', '第二章', '第三章', '第1章', '一、', '二、', '三、', '1 ', '2 ', '3 '],
        'heading2': ['1.1', '2.1', '第一节', '第二节', '（一）', '（二）', '1.1 ', '2.1 '],
        'heading3': ['1.1.1', '2.1.1', '1.1.1 ', '2.1.1 '],
        'body': ['本人', '本文', '研究', '分析', '方法', '结果', '结论', '本论文'],
        'reference': ['参考文献', '参考文献：', 'references'],
        'acknowledgement': ['致谢', '谢辞', '后记', '感谢'],
    }
    
    ALIGNMENT_MAP = {
        WD_ALIGN_PARAGRAPH.LEFT: 'left',
        WD_ALIGN_PARAGRAPH.CENTER: 'center',
        WD_ALIGN_PARAGRAPH.RIGHT: 'right',
        WD_ALIGN_PARAGRAPH.JUSTIFY: 'justify',
        WD_ALIGN_PARAGRAPH.DISTRIBUTE: 'distribute',
    }
    
    def __init__(self):
        self.extracted_formats: List[ExtractedFormat] = []
        self.page_settings: Dict[str, float] = {}
    
    def extract_from_docx(self, file_path: str) -> Tuple[Dict[str, Any], List[ExtractedFormat]]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        doc = Document(file_path)
        self.extracted_formats.clear()
        
        self._extract_page_settings(doc)
        
        for para in doc.paragraphs:
            if not para.text.strip():
                continue
            
            format_info = self._extract_paragraph_format(para)
            if format_info:
                self.extracted_formats.append(format_info)
        
        return self._build_rules(), self.extracted_formats
    
    def _extract_page_settings(self, doc: Document):
        if doc.sections:
            section = doc.sections[0]
            self.page_settings = {
                'margin_top': round(section.top_margin.cm, 2),
                'margin_bottom': round(section.bottom_margin.cm, 2),
                'margin_left': round(section.left_margin.cm, 2),
                'margin_right': round(section.right_margin.cm, 2),
            }
    
    def _extract_paragraph_format(self, para) -> Optional[ExtractedFormat]:
        text = para.text.strip()
        if not text:
            return None
        
        element_type = self._identify_element_type(text)
        
        font_name = None
        font_size = None
        bold = False
        italic = False
        
        for run in para.runs:
            if run.font.name:
                font_name = run.font.name
            if run.font.size:
                font_size = run.font.size.pt
            if run.bold:
                bold = True
            if run.italic:
                italic = True
            if font_name and font_size:
                break
        
        if not font_size:
            if para.style and para.style.font and para.style.font.size:
                font_size = para.style.font.size.pt
        
        alignment = self.ALIGNMENT_MAP.get(para.alignment, 'left')
        
        line_spacing = 1.5
        pf = para.paragraph_format
        if pf.line_spacing:
            if pf.line_spacing_rule:
                from docx.enum.text import WD_LINE_SPACING
                if pf.line_spacing_rule == WD_LINE_SPACING.SINGLE:
                    line_spacing = 1.0
                elif pf.line_spacing_rule == WD_LINE_SPACING.DOUBLE:
                    line_spacing = 2.0
                elif pf.line_spacing_rule == WD_LINE_SPACING.ONE_POINT_FIVE:
                    line_spacing = 1.5
                else:
                    line_spacing = round(pf.line_spacing, 2)
            else:
                line_spacing = round(pf.line_spacing, 2)
        
        first_line_indent = 0
        if pf.first_line_indent:
            first_line_indent = round(pf.first_line_indent.cm, 2)
        
        confidence = self._calculate_confidence(element_type, text)
        
        return ExtractedFormat(
            element_type=element_type,
            content_sample=text[:50] + '...' if len(text) > 50 else text,
            font_name=font_name or '宋体',
            font_size=font_size or 12,
            bold=bold,
            italic=italic,
            alignment=alignment,
            line_spacing=line_spacing,
            first_line_indent=first_line_indent,
            confidence=confidence
        )
    
    def _identify_element_type(self, text: str) -> str:
        text_lower = text.lower().strip()
        
        for element_type, keywords in self.ELEMENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return element_type
        
        if len(text) < 30 and not text.endswith('。'):
            if any(c.isdigit() for c in text[:5]):
                return 'heading'
            return 'title_candidate'
        
        return 'body'
    
    def _calculate_confidence(self, element_type: str, text: str) -> float:
        if element_type in ['title', 'heading1', 'heading2', 'heading3', 'abstract', 'reference', 'acknowledgement']:
            return 0.95
        elif element_type in ['author', 'affiliation', 'keywords']:
            return 0.9
        elif element_type == 'body':
            return 0.7
        elif element_type == 'title_candidate':
            return 0.6
        return 0.5
    
    def _build_rules(self) -> Dict[str, Any]:
        rules = {
            'font_family': '宋体',
            'font_size': 12,
            'line_spacing': 1.5,
            'margin_top': 2.54,
            'margin_bottom': 2.54,
            'margin_left': 3.17,
            'margin_right': 3.17,
            'title_font': '黑体',
            'title_size': 22,
            'heading1_font': '黑体',
            'heading1_size': 16,
            'heading2_font': '黑体',
            'heading2_size': 14,
            'heading3_font': '黑体',
            'heading3_size': 12,
            'abstract_font': '宋体',
            'abstract_size': 12,
            'reference_format': 'GB/T 7714',
        }
        
        if self.page_settings:
            rules.update(self.page_settings)
        
        type_to_rule = {
            'title': ('title_font', 'title_size'),
            'heading1': ('heading1_font', 'heading1_size'),
            'heading2': ('heading2_font', 'heading2_size'),
            'heading3': ('heading3_font', 'heading3_size'),
            'abstract': ('abstract_font', 'abstract_size'),
            'body': ('font_family', 'font_size'),
        }
        
        for fmt in self.extracted_formats:
            if fmt.element_type in type_to_rule:
                font_key, size_key = type_to_rule[fmt.element_type]
                if fmt.font_name:
                    rules[font_key] = fmt.font_name
                if fmt.font_size:
                    rules[size_key] = fmt.font_size
                
                if fmt.element_type == 'body' and fmt.line_spacing:
                    rules['line_spacing'] = fmt.line_spacing
        
        return rules
    
    def get_format_summary(self) -> List[Tuple[str, str, str, float, float, str]]:
        summary = []
        for fmt in self.extracted_formats:
            summary.append((
                fmt.element_type,
                fmt.content_sample,
                fmt.font_name,
                fmt.font_size,
                fmt.line_spacing,
                f'{fmt.confidence:.0%}'
            ))
        return summary


def extract_format_from_docx(file_path: str) -> Tuple[Dict[str, Any], List[ExtractedFormat]]:
    extractor = WordFormatExtractor()
    return extractor.extract_from_docx(file_path)
