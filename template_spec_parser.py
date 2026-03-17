import re
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ParsedRule:
    rule_name: str
    value: Any
    confidence: float
    source_text: str


@dataclass
class AnnotatedElement:
    element_type: str
    content: str
    annotation: str
    rules: Dict[str, Any]


class TemplateSpecParser:
    FONT_NAMES = {
        '宋体': '宋体',
        '黑体': '黑体',
        '楷体': '楷体',
        '仿宋': '仿宋',
        '仿宋_gb2312': '仿宋',
        'times new roman': 'Times New Roman',
        'times': 'Times New Roman',
        'arial': 'Arial',
    }
    
    CHINESE_SIZE_MAP = {
        '初号': 42, '小初': 36, '一号': 26, '小一': 24,
        '二号': 22, '小二': 18, '三号': 16, '小三': 15,
        '四号': 14, '小四': 12, '五号': 10.5, '小五': 9,
        '六号': 7.5, '小六': 6.5, '七号': 5.5, '八号': 5
    }
    
    ELEMENT_TYPE_MAP = {
        '标题': 'title',
        '论文标题': 'title',
        '文章标题': 'title',
        '正文': 'body',
        '正文内容': 'body',
        '一级标题': 'heading1',
        '章标题': 'heading1',
        '章': 'heading1',
        '二级标题': 'heading2',
        '节标题': 'heading2',
        '节': 'heading2',
        '三级标题': 'heading3',
        '四级标题': 'heading4',
        '摘要': 'abstract',
        '中文摘要': 'abstract',
        '关键词': 'keywords',
        '参考文献': 'reference',
        '致谢': 'acknowledgement',
        '图表标题': 'figure_caption',
        '表格标题': 'table_caption',
        '页眉': 'header',
        '页脚': 'footer',
        '页码': 'page_number',
    }
    
    def __init__(self):
        self.parsed_rules: Dict[str, ParsedRule] = {}
        self.raw_text: str = ""
        self.annotated_elements: List[AnnotatedElement] = []
    
    def parse(self, text: str) -> Dict[str, Any]:
        self.raw_text = text
        self.parsed_rules.clear()
        self.annotated_elements.clear()
        
        self._parse_annotated_template()
        
        self._parse_font_family()
        self._parse_font_size()
        self._parse_line_spacing()
        self._parse_margins()
        self._parse_title_settings()
        self._parse_heading_settings()
        self._parse_reference_format()
        self._parse_abstract_settings()
        
        return self._build_rules_dict()
    
    def _parse_annotated_template(self):
        annotation_patterns = [
            r'【([^】]+)】([^【]*)',
            r'\[([^\]]+)\]([^\[]*)',
            r'（([^）]+)）([^（]*)',
            r'\(([^)]+)\)([^()]*)',
        ]
        
        for pattern in annotation_patterns:
            matches = re.findall(pattern, self.raw_text)
            for annotation, content in matches:
                annotation = annotation.strip()
                content = content.strip()
                
                if not annotation or not content:
                    continue
                
                element_type = self._identify_element_type(annotation)
                if element_type:
                    rules = self._parse_annotation_rules(annotation, element_type)
                    
                    self.annotated_elements.append(AnnotatedElement(
                        element_type=element_type,
                        content=content,
                        annotation=annotation,
                        rules=rules
                    ))
                    
                    for rule_key, rule_value in rules.items():
                        if rule_key not in self.parsed_rules:
                            self.parsed_rules[rule_key] = ParsedRule(
                                rule_name=self._get_rule_name(rule_key),
                                value=rule_value,
                                confidence=0.95,
                                source_text=f'【{annotation}】'
                            )
    
    def _identify_element_type(self, annotation: str) -> Optional[str]:
        for keyword, element_type in self.ELEMENT_TYPE_MAP.items():
            if keyword in annotation:
                return element_type
        return None
    
    def _parse_annotation_rules(self, annotation: str, element_type: str) -> Dict[str, Any]:
        rules = {}
        
        for font_name, font_value in self.FONT_NAMES.items():
            if font_name in annotation:
                if element_type in ['title']:
                    rules['title_font'] = font_value
                elif element_type in ['heading1']:
                    rules['heading1_font'] = font_value
                elif element_type in ['heading2']:
                    rules['heading2_font'] = font_value
                elif element_type in ['heading3']:
                    rules['heading3_font'] = font_value
                elif element_type in ['abstract']:
                    rules['abstract_font'] = font_value
                elif element_type in ['body']:
                    rules['font_family'] = font_value
                break
        
        for size_name, size_value in self.CHINESE_SIZE_MAP.items():
            if size_name in annotation:
                if element_type in ['title']:
                    rules['title_size'] = size_value
                elif element_type in ['heading1']:
                    rules['heading1_size'] = size_value
                elif element_type in ['heading2']:
                    rules['heading2_size'] = size_value
                elif element_type in ['heading3']:
                    rules['heading3_size'] = size_value
                elif element_type in ['abstract']:
                    rules['abstract_size'] = size_value
                elif element_type in ['body']:
                    rules['font_size'] = size_value
                break
        
        pt_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:pt|磅)', annotation)
        if pt_match:
            size = float(pt_match.group(1))
            if element_type in ['title']:
                rules['title_size'] = size
            elif element_type in ['heading1']:
                rules['heading1_size'] = size
            elif element_type in ['body']:
                rules['font_size'] = size
        
        spacing_match = re.search(r'(\d+(?:\.\d+)?)\s*倍', annotation)
        if spacing_match:
            rules['line_spacing'] = float(spacing_match.group(1))
        
        if '居中' in annotation or '居中对齐' in annotation:
            rules['alignment'] = 'center'
        elif '左对齐' in annotation or '左齐' in annotation:
            rules['alignment'] = 'left'
        elif '右对齐' in annotation or '右齐' in annotation:
            rules['alignment'] = 'right'
        elif '两端对齐' in annotation or '分散对齐' in annotation:
            rules['alignment'] = 'justify'
        
        indent_match = re.search(r'首行缩进\s*(\d+)\s*(?:字符|字)?', annotation)
        if indent_match:
            rules['first_line_indent'] = int(indent_match.group(1))
        
        bold_match = re.search(r'加粗|粗体', annotation)
        if bold_match:
            rules['bold'] = True
        
        return rules
    
    def _get_rule_name(self, rule_key: str) -> str:
        name_map = {
            'font_family': '正文字体',
            'font_size': '正文字号',
            'line_spacing': '行距',
            'title_font': '标题字体',
            'title_size': '标题字号',
            'heading1_font': '一级标题字体',
            'heading1_size': '一级标题字号',
            'heading2_font': '二级标题字体',
            'heading2_size': '二级标题字号',
            'heading3_font': '三级标题字体',
            'heading3_size': '三级标题字号',
            'abstract_font': '摘要字体',
            'abstract_size': '摘要字号',
            'margin_top': '上边距',
            'margin_bottom': '下边距',
            'margin_left': '左边距',
            'margin_right': '右边距',
            'reference_format': '参考文献格式',
        }
        return name_map.get(rule_key, rule_key)
    
    def _parse_font_family(self):
        patterns = [
            r'正文[字体]*[：:]\s*["""]?([^，,。；;\s"""\n]+)',
            r'字体[：:]\s*["""]?([^，,。；;\s"""\n]+)',
            r'使用\s*["""]?([^，,。；;\s"""\n]+)["""]?\s*字体',
            r'采用\s*["""]?([^，,。；;\s"""\n]+)["""]?\s*体',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                font_name = match.group(1).strip()
                for key, value in self.FONT_NAMES.items():
                    if key.lower() in font_name.lower():
                        self.parsed_rules['font_family'] = ParsedRule(
                            rule_name='正文字体',
                            value=value,
                            confidence=0.9,
                            source_text=match.group(0)
                        )
                        return
    
    def _parse_font_size(self):
        patterns = [
            r'正文字号[：:]\s*(\S+)',
            r'字号[：:]\s*(\S+)',
            r'字体大小[：:]\s*(\S+)',
            r'小四|四号|五号|小三|三号|二号|小二|一号|小一',
            r'(\d+(?:\.\d+)?)\s*(?:pt|磅|点)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                size_text = match.group(1) if match.lastindex else match.group(0)
                size_text = size_text.strip()
                
                if size_text in self.CHINESE_SIZE_MAP:
                    self.parsed_rules['font_size'] = ParsedRule(
                        rule_name='正文字号',
                        value=self.CHINESE_SIZE_MAP[size_text],
                        confidence=0.95,
                        source_text=match.group(0)
                    )
                    return
                else:
                    try:
                        size = float(re.search(r'(\d+(?:\.\d+)?)', size_text).group(1))
                        if 5 <= size <= 72:
                            self.parsed_rules['font_size'] = ParsedRule(
                                rule_name='正文字号',
                                value=size,
                                confidence=0.8,
                                source_text=match.group(0)
                            )
                            return
                    except:
                        pass
    
    def _parse_line_spacing(self):
        patterns = [
            r'行距[：:]\s*(\d+(?:\.\d+)?)\s*(?:倍|倍行距)?',
            r'行间距[：:]\s*(\d+(?:\.\d+)?)\s*(?:倍)?',
            r'(\d+(?:\.\d+)?)\s*倍行距',
            r'固定值\s*(\d+)\s*磅',
            r'单倍行距',
            r'双倍行距',
        ]
        
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                if '单倍' in match.group(0):
                    self.parsed_rules['line_spacing'] = ParsedRule(
                        rule_name='行距',
                        value=1.0,
                        confidence=0.9,
                        source_text=match.group(0)
                    )
                    return
                elif '双倍' in match.group(0):
                    self.parsed_rules['line_spacing'] = ParsedRule(
                        rule_name='行距',
                        value=2.0,
                        confidence=0.9,
                        source_text=match.group(0)
                    )
                    return
                elif '固定值' in match.group(0):
                    pt = float(match.group(1))
                    self.parsed_rules['line_spacing'] = ParsedRule(
                        rule_name='行距',
                        value=pt / 12,
                        confidence=0.7,
                        source_text=match.group(0)
                    )
                    return
                else:
                    try:
                        spacing = float(match.group(1))
                        if 0.5 <= spacing <= 3.0:
                            self.parsed_rules['line_spacing'] = ParsedRule(
                                rule_name='行距',
                                value=spacing,
                                confidence=0.9,
                                source_text=match.group(0)
                            )
                            return
                    except:
                        pass
    
    def _parse_margins(self):
        margin_patterns = [
            (r'上[边]?距[：:]\s*(\d+(?:\.\d+)?)\s*(?:cm|厘米|mm|毫米)?', 'margin_top'),
            (r'下[边]?距[：:]\s*(\d+(?:\.\d+)?)\s*(?:cm|厘米|mm|毫米)?', 'margin_bottom'),
            (r'左[边]?距[：:]\s*(\d+(?:\.\d+)?)\s*(?:cm|厘米|mm|毫米)?', 'margin_left'),
            (r'右[边]?距[：:]\s*(\d+(?:\.\d+)?)\s*(?:cm|厘米|mm|毫米)?', 'margin_right'),
        ]
        
        for pattern, key in margin_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                if 'mm' in match.group(0).lower() or '毫米' in match.group(0):
                    value = value / 10
                self.parsed_rules[key] = ParsedRule(
                    rule_name=f'{"上" if "top" in key else "下" if "bottom" in key else "左" if "left" in key else "右"}边距',
                    value=value,
                    confidence=0.9,
                    source_text=match.group(0)
                )
        
        combined_pattern = r'页边距[：:]\s*上下左右\s*(\d+(?:\.\d+)?)\s*(?:cm|厘米)?'
        match = re.search(combined_pattern, self.raw_text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            for key in ['margin_top', 'margin_bottom', 'margin_left', 'margin_right']:
                if key not in self.parsed_rules:
                    self.parsed_rules[key] = ParsedRule(
                        rule_name='页边距',
                        value=value,
                        confidence=0.8,
                        source_text=match.group(0)
                    )
    
    def _parse_title_settings(self):
        patterns = [
            (r'论文标题[字体]*[：:]\s*["""]?([^，,。；;\s"""\n]+)', 'title_font'),
            (r'标题字体[：:]\s*["""]?([^，,。；;\s"""\n]+)', 'title_font'),
        ]
        
        for pattern, key in patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                font_name = match.group(1).strip()
                for k, v in self.FONT_NAMES.items():
                    if k.lower() in font_name.lower():
                        self.parsed_rules[key] = ParsedRule(
                            rule_name='标题字体',
                            value=v,
                            confidence=0.9,
                            source_text=match.group(0)
                        )
                        break
        
        size_patterns = [
            (r'论文标题字号[：:]\s*(\S+)', 'title_size'),
            (r'标题字号[：:]\s*(\S+)', 'title_size'),
        ]
        
        for pattern, key in size_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                size_text = match.group(1).strip()
                if size_text in self.CHINESE_SIZE_MAP:
                    self.parsed_rules[key] = ParsedRule(
                        rule_name='标题字号',
                        value=self.CHINESE_SIZE_MAP[size_text],
                        confidence=0.95,
                        source_text=match.group(0)
                    )
                else:
                    try:
                        size = float(re.search(r'(\d+(?:\.\d+)?)', size_text).group(1))
                        if 5 <= size <= 72:
                            self.parsed_rules[key] = ParsedRule(
                                rule_name='标题字号',
                                value=size,
                                confidence=0.8,
                                source_text=match.group(0)
                            )
                    except:
                        pass
    
    def _parse_heading_settings(self):
        heading_patterns = [
            (r'一级标题[字号]*[：:]\s*(\S+)', 'heading1_size'),
            (r'章标题[字号]*[：:]\s*(\S+)', 'heading1_size'),
            (r'二级标题[字号]*[：:]\s*(\S+)', 'heading2_size'),
            (r'节标题[字号]*[：:]\s*(\S+)', 'heading2_size'),
            (r'三级标题[字号]*[：:]\s*(\S+)', 'heading3_size'),
        ]
        
        for pattern, key in heading_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                size_text = match.group(1).strip()
                if size_text in self.CHINESE_SIZE_MAP:
                    self.parsed_rules[key] = ParsedRule(
                        rule_name=f'{key.replace("_size", "")}字号',
                        value=self.CHINESE_SIZE_MAP[size_text],
                        confidence=0.95,
                        source_text=match.group(0)
                    )
                else:
                    try:
                        size = float(re.search(r'(\d+(?:\.\d+)?)', size_text).group(1))
                        if 5 <= size <= 72:
                            self.parsed_rules[key] = ParsedRule(
                                rule_name=f'{key.replace("_size", "")}字号',
                                value=size,
                                confidence=0.8,
                                source_text=match.group(0)
                            )
                    except:
                        pass
        
        heading_font_patterns = [
            (r'一级标题[字体]*[：:]\s*["""]?([^，,。；;\s"""\n]+)', 'heading1_font'),
            (r'二级标题[字体]*[：:]\s*["""]?([^，,。；;\s"""\n]+)', 'heading2_font'),
            (r'三级标题[字体]*[：:]\s*["""]?([^，,。；;\s"""\n]+)', 'heading3_font'),
        ]
        
        for pattern, key in heading_font_patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                font_name = match.group(1).strip()
                for k, v in self.FONT_NAMES.items():
                    if k.lower() in font_name.lower():
                        self.parsed_rules[key] = ParsedRule(
                            rule_name=f'{key.replace("_font", "")}字体',
                            value=v,
                            confidence=0.9,
                            source_text=match.group(0)
                        )
                        break
    
    def _parse_reference_format(self):
        formats = ['GB/T 7714', 'IEEE', 'APA', 'MLA', 'Springer', '国标', '中国国家标准']
        
        for fmt in formats:
            if fmt.lower() in self.raw_text.lower():
                if fmt == '国标' or fmt == '中国国家标准':
                    fmt = 'GB/T 7714'
                self.parsed_rules['reference_format'] = ParsedRule(
                    rule_name='参考文献格式',
                    value=fmt,
                    confidence=0.9,
                    source_text=f'检测到: {fmt}'
                )
                return
    
    def _parse_abstract_settings(self):
        patterns = [
            (r'摘要[字体]*[：:]\s*["""]?([^，,。；;\s"""\n]+)', 'abstract_font'),
            (r'摘要字号[：:]\s*(\S+)', 'abstract_size'),
        ]
        
        for pattern, key in patterns:
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                value_text = match.group(1).strip()
                if 'font' in key:
                    for k, v in self.FONT_NAMES.items():
                        if k.lower() in value_text.lower():
                            self.parsed_rules[key] = ParsedRule(
                                rule_name='摘要字体',
                                value=v,
                                confidence=0.9,
                                source_text=match.group(0)
                            )
                            break
                else:
                    if value_text in self.CHINESE_SIZE_MAP:
                        self.parsed_rules[key] = ParsedRule(
                            rule_name='摘要字号',
                            value=self.CHINESE_SIZE_MAP[value_text],
                            confidence=0.95,
                            source_text=match.group(0)
                        )
    
    def _build_rules_dict(self) -> Dict[str, Any]:
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
            'heading1_size': 16,
            'heading2_size': 14,
            'heading3_size': 12,
            'reference_format': 'GB/T 7714',
        }
        
        for key, parsed_rule in self.parsed_rules.items():
            rules[key] = parsed_rule.value
        
        return rules
    
    def get_parse_summary(self) -> List[Tuple[str, Any, str, float]]:
        summary = []
        for key, rule in self.parsed_rules.items():
            summary.append((rule.rule_name, rule.value, rule.source_text, rule.confidence))
        return summary


def parse_template_spec(text: str) -> Tuple[Dict[str, Any], List[Tuple[str, Any, str, float]]]:
    parser = TemplateSpecParser()
    rules = parser.parse(text)
    summary = parser.get_parse_summary()
    return rules, summary
