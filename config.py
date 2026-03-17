import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
RULES_DIR = os.path.join(BASE_DIR, 'rules')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

AI_API_CONFIG = {
    'api_url': '',
    'api_key': '',
    'model': '',
    'timeout': 60
}

SUPPORTED_FORMATS = {
    'docx': 'Microsoft Word Document',
    'tex': 'LaTeX Document'
}

DEFAULT_TEMPLATE_RULES = {
    'paper_size': 'A4',
    'print_mode': '单面',
    
    'margin_top': 2.54,
    'margin_bottom': 2.54,
    'margin_left': 3.17,
    'margin_right': 3.17,
    'header_height': 1.5,
    'footer_height': 1.5,
    'binding': '左侧装订',
    
    'font_family': '宋体',
    'font_size': 12,
    'line_spacing': 1.5,
    'line_spacing_type': '多倍行距',
    'paragraph_spacing_before': 0,
    'paragraph_spacing_after': 0,
    'first_line_indent': 2,
    
    'title_font': '黑体',
    'title_size': 22,
    'title_bold': True,
    'title_alignment': '居中',
    
    'heading1_font': '黑体',
    'heading1_size': 16,
    'heading1_bold': True,
    'heading1_alignment': '居左',
    'heading1_numbering': '一、二、三、',
    
    'heading2_font': '黑体',
    'heading2_size': 14,
    'heading2_bold': True,
    'heading2_alignment': '居左',
    'heading2_numbering': '（一）（二）',
    
    'heading3_font': '黑体',
    'heading3_size': 12,
    'heading3_bold': True,
    'heading3_alignment': '居左',
    'heading3_numbering': '1. 2. 3.',
    
    'heading4_numbering': '（1）（2）',
    'heading5_numbering': '①②③',
    
    'abstract_title_font': '黑体',
    'abstract_title_size': 14,
    'abstract_font': '宋体',
    'abstract_size': 12,
    'abstract_line_spacing': 1.5,
    'abstract_word_limit': 300,
    
    'keywords_font': '宋体',
    'keywords_size': 12,
    'keywords_label_font': '黑体',
    'keywords_separator': '；',
    'keywords_count_min': 3,
    'keywords_count_max': 5,
    
    'abstract_en_font': 'Times New Roman',
    'abstract_en_size': 12,
    'keywords_en_font': 'Times New Roman',
    'keywords_en_size': 12,
    
    'figure_caption_font': '宋体',
    'figure_caption_size': 10.5,
    'figure_caption_position': '图下',
    'figure_numbering': '图1-1',
    
    'table_caption_font': '宋体',
    'table_caption_size': 10.5,
    'table_caption_position': '表上',
    'table_numbering': '表1-1',
    'table_style': '三线表',
    'table_content_font': '宋体',
    'table_content_size': 10.5,
    
    'formula_indent': 2,
    'formula_numbering': '(1-1)',
    'formula_number_position': '行右',
    
    'reference_title_font': '黑体',
    'reference_title_size': 14,
    'reference_font': '宋体',
    'reference_size': 10.5,
    'reference_format': 'GB/T 7714',
    'reference_numbering': '[1]',
    'reference_min_count': 10,
    'reference_foreign_min': 2,
    
    'page_number_font': '宋体',
    'page_number_size': 10.5,
    'page_number_position': '页脚居中',
    'page_number_front_style': '罗马数字',
    'page_number_body_style': '阿拉伯数字',
    
    'header_font': '宋体',
    'header_size': 10.5,
    'header_content': '论文题目',
    
    'conclusion_title_font': '黑体',
    'conclusion_title_size': 14,
    'conclusion_font': '宋体',
    'conclusion_size': 12,
    
    'acknowledgement_title_font': '黑体',
    'acknowledgement_title_size': 14,
    'acknowledgement_font': '宋体',
    'acknowledgement_size': 12,
    
    'appendix_title_font': '黑体',
    'appendix_title_size': 14,
    'appendix_font': '宋体',
    'appendix_size': 12,
    
    'cover_required_fields': ['论文题目', '作者姓名', '学号', '专业', '指导教师', '完成日期'],
    'binding_order': ['封面', '摘要', '目录', '正文', '参考文献', '致谢', '附录'],
    
    'word_count_min': 8000,
    'word_count_requirement': '正文不少于8000字'
}

for dir_path in [TEMPLATES_DIR, RULES_DIR, OUTPUT_DIR]:
    os.makedirs(dir_path, exist_ok=True)
