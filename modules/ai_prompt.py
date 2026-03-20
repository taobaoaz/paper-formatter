import json
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import config


AI_PROMPT_TEMPLATE = """# 任务说明
你是论文格式规范解析专家。请分析提供的论文模板文件/说明，提取所有格式要求并转换为标准JSON格式。

# 待分析的模板内容
{template_content}

# 输出格式要求
请严格按照以下JSON格式输出，不要包含任何其他文字：

```json
{{
  "template_name": "模板名称",
  "template_type": "模板类型（中文期刊/国际期刊/学位论文/自定义）",
  "description": "模板简要描述",
  "rules": {{
    "paper_size": "A4",
    "print_mode": "单面/双面",
    
    "margin_top": 2.5,
    "margin_bottom": 2.5,
    "margin_left": 3.0,
    "margin_right": 2.5,
    "header_height": 1.5,
    "footer_height": 1.5,
    "binding": "左侧装订",
    
    "font_family": "宋体",
    "font_size": 12,
    "line_spacing": 1.5,
    "line_spacing_type": "多倍行距",
    "paragraph_spacing_before": 0,
    "paragraph_spacing_after": 0,
    "first_line_indent": 2,
    
    "title_font": "黑体",
    "title_size": 22,
    "title_bold": true,
    "title_alignment": "居中",
    
    "heading1_font": "黑体",
    "heading1_size": 16,
    "heading1_bold": true,
    "heading1_alignment": "居左",
    "heading1_numbering": "一、二、三、",
    
    "heading2_font": "黑体",
    "heading2_size": 14,
    "heading2_bold": true,
    "heading2_alignment": "居左",
    "heading2_numbering": "（一）（二）",
    
    "heading3_font": "黑体",
    "heading3_size": 12,
    "heading3_bold": true,
    "heading3_alignment": "居左",
    "heading3_numbering": "1. 2. 3.",
    
    "heading4_numbering": "（1）（2）",
    "heading5_numbering": "①②③",
    
    "abstract_title_font": "黑体",
    "abstract_title_size": 14,
    "abstract_font": "宋体",
    "abstract_size": 12,
    "abstract_line_spacing": 1.5,
    "abstract_word_limit": 300,
    
    "keywords_font": "宋体",
    "keywords_size": 12,
    "keywords_label_font": "黑体",
    "keywords_separator": "；",
    "keywords_count_min": 3,
    "keywords_count_max": 5,
    
    "abstract_en_font": "Times New Roman",
    "abstract_en_size": 12,
    "keywords_en_font": "Times New Roman",
    "keywords_en_size": 12,
    
    "figure_caption_font": "宋体",
    "figure_caption_size": 10.5,
    "figure_caption_position": "图下",
    "figure_numbering": "图1-1",
    
    "table_caption_font": "宋体",
    "table_caption_size": 10.5,
    "table_caption_position": "表上",
    "table_numbering": "表1-1",
    "table_style": "三线表",
    "table_content_font": "宋体",
    "table_content_size": 10.5,
    
    "formula_indent": 2,
    "formula_numbering": "(1-1)",
    "formula_number_position": "行右",
    
    "reference_title_font": "黑体",
    "reference_title_size": 14,
    "reference_font": "宋体",
    "reference_size": 10.5,
    "reference_format": "GB/T 7714",
    "reference_numbering": "[1]",
    "reference_min_count": 10,
    "reference_foreign_min": 2,
    
    "page_number_font": "宋体",
    "page_number_size": 10.5,
    "page_number_position": "页脚居中",
    "page_number_front_style": "罗马数字",
    "page_number_body_style": "阿拉伯数字",
    
    "header_font": "宋体",
    "header_size": 10.5,
    "header_content": "论文题目",
    
    "conclusion_title_font": "黑体",
    "conclusion_title_size": 14,
    "conclusion_font": "宋体",
    "conclusion_size": 12,
    
    "acknowledgement_title_font": "黑体",
    "acknowledgement_title_size": 14,
    "acknowledgement_font": "宋体",
    "acknowledgement_size": 12,
    
    "appendix_title_font": "黑体",
    "appendix_title_size": 14,
    "appendix_font": "宋体",
    "appendix_size": 12,
    
    "cover_required_fields": ["论文题目", "作者姓名", "学号", "专业", "指导教师", "完成日期"],
    "binding_order": ["封面", "独创性声明", "摘要", "目录", "正文", "参考文献", "致谢", "附录"],
    
    "word_count_min": 8000,
    "word_count_requirement": "正文不少于8000字"
  }}
}}
```

# 字号对照表
| 中文字号 | 磅值(pt) |
|---------|---------|
| 八号 | 5 |
| 七号 | 5.5 |
| 小六 | 6.5 |
| 六号 | 7.5 |
| 小五 | 9 |
| 五号 | 10.5 |
| 小四 | 12 |
| 四号 | 14 |
| 小三 | 15 |
| 三号 | 16 |
| 小二 | 18 |
| 二号 | 22 |
| 小一 | 24 |
| 一号 | 26 |
| 小初 | 36 |
| 初号 | 42 |

# 提取规则
1. 所有数值字段必须是数字类型（如 font_size: 12，不是 "12pt"）
2. 布尔值使用 true 或 false
3. 字体名称保留原文（宋体、黑体、Times New Roman等）
4. 如果某项未明确规定，根据模板类型推断合理默认值
5. 页边距单位统一为厘米(cm)
6. 行距：固定值直接填磅数（如22），倍数填数值（如1.5）
7. 首行缩进填字符数（通常为2）
8. 编号格式示例："一、二、三、"、"（一）（二）"、"1. 2. 3."、"（1）（2）"、"①②③"

# 注意事项
- 仔细阅读文档中的每一个格式要求
- 对于表格、图片等元素，注意标题位置和编号格式
- 参考文献格式要明确是哪种标准
- 页码格式注意区分前置部分和正文部分
- 封面必填字段和装订顺序要按文档要求列出
"""


AI_PROMPT_FOR_DOCX = """# 任务说明
你是论文格式规范解析专家。请分析以下从Word模板文档中提取的内容和格式信息，识别所有格式要求并转换为标准JSON格式。

# 模板文档内容
{template_content}

# 分析要点
1. 根据内容识别文档结构（标题、摘要、正文、参考文献等）
2. 根据格式标注识别字体、字号、行距等要求
3. 如果是示例文档，从示例中提取格式规范
4. 注意文档中的注释和说明文字

# 输出格式
请输出标准JSON格式，包含以下字段：
- template_name: 模板名称
- template_type: 模板类型
- description: 描述
- rules: 格式规则（参考完整模板）

{rules_template}
"""


QUICK_PROMPT = """请分析这个论文模板，提取格式要求返回JSON。

必填字段：
- template_name: 模板名称
- font_family/font_size/line_spacing: 正文格式
- margin_top/bottom/left/right: 页边距(cm)
- title_font/size/bold: 标题格式
- heading1/2/3_font/size/bold: 各级标题
- abstract_font/size: 摘要格式
- reference_format/font/size: 参考文献

字号转换：小四=12pt，四号=14pt，三号=16pt，二号=22pt

只返回JSON，格式：
{"template_name":"名称","template_type":"类型","rules":{...}}
"""


@dataclass
class ParsedTemplateData:
    template_name: str
    template_type: str
    description: str
    rules: Dict[str, Any]
    raw_json: str
    is_valid: bool = True
    error_message: str = ""


def generate_ai_prompt(template_content: str, is_docx: bool = False) -> str:
    if is_docx:
        return AI_PROMPT_FOR_DOCX.format(
            template_content=template_content,
            rules_template=get_rules_template()
        )
    return AI_PROMPT_TEMPLATE.format(template_content=template_content)


def get_rules_template() -> str:
    return """
rules字段示例：
{
  "font_family": "宋体",
  "font_size": 12,
  "line_spacing": 1.5,
  "margin_top": 2.5,
  "margin_bottom": 2.5,
  "margin_left": 3.0,
  "margin_right": 2.5,
  "title_font": "黑体",
  "title_size": 22,
  "heading1_font": "黑体",
  "heading1_size": 16,
  "heading2_font": "黑体",
  "heading2_size": 14,
  "heading3_font": "黑体",
  "heading3_size": 12,
  "abstract_font": "宋体",
  "abstract_size": 12,
  "reference_format": "GB/T 7714",
  "reference_font": "宋体",
  "reference_size": 10.5
}
"""


def get_quick_prompt() -> str:
    return QUICK_PROMPT


def parse_ai_response(response_text: str) -> ParsedTemplateData:
    try:
        json_str = extract_json_from_response(response_text)
        
        if not json_str:
            return ParsedTemplateData(
                template_name="",
                template_type="",
                description="",
                rules={},
                raw_json=response_text,
                is_valid=False,
                error_message="无法从响应中提取JSON数据"
            )
        
        data = json.loads(json_str)
        
        if 'rules' in data:
            template_name = data.get('template_name', '未命名模板')
            template_type = data.get('template_type', '自定义')
            description = data.get('description', '')
            rules = data.get('rules', {})
        elif 'font_family' in data or 'font_size' in data or 'margin_top' in data:
            template_name = '未命名模板'
            template_type = '自定义'
            description = '从AI识别结果创建'
            rules = data
        else:
            template_name = data.get('template_name', '未命名模板')
            template_type = data.get('template_type', '自定义')
            description = data.get('description', '')
            rules = data
        
        rules = normalize_rules(rules)
        
        return ParsedTemplateData(
            template_name=template_name,
            template_type=template_type,
            description=description,
            rules=rules,
            raw_json=json_str,
            is_valid=True
        )
        
    except json.JSONDecodeError as e:
        return ParsedTemplateData(
            template_name="",
            template_type="",
            description="",
            rules={},
            raw_json=response_text,
            is_valid=False,
            error_message=f"JSON解析错误: {str(e)}"
        )
    except Exception as e:
        return ParsedTemplateData(
            template_name="",
            template_type="",
            description="",
            rules={},
            raw_json=response_text,
            is_valid=False,
            error_message=f"解析错误: {str(e)}"
        )


def extract_json_from_response(response_text: str) -> Optional[str]:
    code_block_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    code_matches = re.findall(code_block_pattern, response_text)
    
    if code_matches:
        for match in code_matches:
            try:
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue
    
    json_pattern = r'\{[\s\S]*\}'
    matches = re.findall(json_pattern, response_text)
    
    if matches:
        for match in matches:
            try:
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue
    
    if re.search(r'"\w+"\s*:\s*[\d"\[\]]', response_text):
        lines = response_text.strip().split('\n')
        cleaned_lines = []
        for i, line in enumerate(lines):
            cleaned = line.strip()
            if cleaned and not cleaned.startswith('//') and not cleaned.startswith('#'):
                if cleaned.endswith('"') or re.search(r'[\]\d]$', cleaned):
                    if not cleaned.endswith(',') and not cleaned.endswith('}') and not cleaned.endswith('{'):
                        cleaned = cleaned + ','
                cleaned_lines.append(cleaned)
        
        if cleaned_lines:
            cleaned_text = '\n'.join(cleaned_lines)
            if cleaned_lines[-1].endswith(','):
                cleaned_text = cleaned_text[:-1]
            wrapped = '{\n' + cleaned_text + '\n}'
            try:
                json.loads(wrapped)
                return wrapped
            except json.JSONDecodeError:
                pass
    
    return None


def normalize_rules(rules: Dict[str, Any]) -> Dict[str, Any]:
    normalized = config.DEFAULT_TEMPLATE_RULES.copy()
    
    for key, value in rules.items():
        if value is not None:
            normalized[key] = value
    
    FONT_SIZE_MAP = {
        '小五': 9, '五号': 10.5, '小四': 12, '四号': 14,
        '小三': 15, '三号': 16, '小二': 18, '二号': 22,
        '小一': 24, '一号': 26, '小初': 36, '初号': 42,
        '六号': 7.5, '小六': 6.5, '七号': 5.5, '八号': 5
    }
    
    for key in normalized:
        if 'size' in key or 'font_size' in key:
            value = normalized[key]
            if isinstance(value, str):
                if value in FONT_SIZE_MAP:
                    normalized[key] = FONT_SIZE_MAP[value]
                else:
                    try:
                        normalized[key] = float(value.replace('pt', '').replace('磅', '').strip())
                    except (ValueError, AttributeError):
                        pass
    
    numeric_fields = [
        'font_size', 'line_spacing', 'margin_top', 'margin_bottom',
        'margin_left', 'margin_right', 'title_size', 'heading1_size',
        'heading2_size', 'heading3_size', 'abstract_size', 'keywords_size',
        'reference_size', 'figure_caption_size', 'table_caption_size',
        'table_content_size', 'page_number_size', 'header_size',
        'first_line_indent', 'header_height', 'footer_height',
        'abstract_word_limit', 'keywords_count_min', 'keywords_count_max',
        'reference_min_count', 'reference_foreign_min', 'word_count_min',
        'conclusion_title_size', 'conclusion_size',
        'acknowledgement_title_size', 'acknowledgement_size',
        'appendix_title_size', 'appendix_size', 'formula_indent'
    ]
    
    for field in numeric_fields:
        if field in normalized and normalized[field] is not None:
            try:
                if isinstance(normalized[field], str):
                    cleaned = normalized[field].replace('cm', '').replace('pt', '').replace('磅', '').replace('字符', '').strip()
                    normalized[field] = float(cleaned)
            except (ValueError, AttributeError):
                pass
    
    boolean_fields = [
        'title_bold', 'heading1_bold', 'heading2_bold', 'heading3_bold',
        'align_to_grid'
    ]
    
    for field in boolean_fields:
        if field in normalized and isinstance(normalized[field], str):
            normalized[field] = normalized[field].lower() in ('true', 'yes', '是', '1', '加粗')
    
    return normalized


def validate_template_data(data: ParsedTemplateData) -> tuple:
    if not data.is_valid:
        return False, data.error_message
    
    if not data.template_name:
        return False, "模板名称不能为空"
    
    if not data.rules:
        return False, "模板规则不能为空"
    
    return True, "验证通过"


def get_quick_prompt_for_template_file() -> str:
    return QUICK_PROMPT


def get_simple_prompt() -> str:
    return QUICK_PROMPT
