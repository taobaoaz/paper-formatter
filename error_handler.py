from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass


class ErrorCode(Enum):
    SUCCESS = 0
    
    FILE_NOT_FOUND = 1001
    FILE_READ_ERROR = 1002
    FILE_WRITE_ERROR = 1003
    FILE_FORMAT_UNSUPPORTED = 1004
    FILE_ENCODING_ERROR = 1005
    FILE_CORRUPTED = 1006
    
    PYTHON_NOT_INSTALLED = 2001
    PYTHON_VERSION_ERROR = 2002
    DEPENDENCY_MISSING = 2003
    DEPENDENCY_INSTALL_FAILED = 2004
    
    PARSE_ERROR = 3001
    PARSE_DOCX_ERROR = 3002
    PARSE_TEX_ERROR = 3003
    PARSE_ENCODING_ERROR = 3004
    
    TEMPLATE_NOT_FOUND = 4001
    TEMPLATE_INVALID = 4002
    TEMPLATE_RULE_MISSING = 4003
    TEMPLATE_TYPE_UNSUPPORTED = 4004
    
    FORMAT_ERROR = 5001
    FORMAT_FONT_ERROR = 5002
    FORMAT_MARGIN_ERROR = 5003
    FORMAT_HEADING_ERROR = 5004
    FORMAT_REFERENCE_ERROR = 5005
    FORMAT_TABLE_ERROR = 5006
    FORMAT_FIGURE_ERROR = 5007
    
    AI_API_ERROR = 6001
    AI_API_TIMEOUT = 6002
    AI_API_KEY_INVALID = 6003
    AI_RESPONSE_INVALID = 6004
    AI_PARSE_ERROR = 6005
    
    GENERATION_ERROR = 7001
    GENERATION_FIELD_MISSING = 7002
    GENERATION_CONTENT_EMPTY = 7003
    
    UNKNOWN_ERROR = 9999


ERROR_MESSAGES = {
    ErrorCode.SUCCESS: "操作成功",
    
    ErrorCode.FILE_NOT_FOUND: "文件不存在",
    ErrorCode.FILE_READ_ERROR: "文件读取失败",
    ErrorCode.FILE_WRITE_ERROR: "文件写入失败",
    ErrorCode.FILE_FORMAT_UNSUPPORTED: "不支持的文件格式",
    ErrorCode.FILE_ENCODING_ERROR: "文件编码错误",
    ErrorCode.FILE_CORRUPTED: "文件已损坏",
    
    ErrorCode.PYTHON_NOT_INSTALLED: "Python 未安装",
    ErrorCode.PYTHON_VERSION_ERROR: "Python 版本不兼容",
    ErrorCode.DEPENDENCY_MISSING: "依赖包缺失",
    ErrorCode.DEPENDENCY_INSTALL_FAILED: "依赖包安装失败",
    
    ErrorCode.PARSE_ERROR: "文档解析失败",
    ErrorCode.PARSE_DOCX_ERROR: "Word文档解析失败",
    ErrorCode.PARSE_TEX_ERROR: "LaTeX文档解析失败",
    ErrorCode.PARSE_ENCODING_ERROR: "文档编码解析失败",
    
    ErrorCode.TEMPLATE_NOT_FOUND: "模板不存在",
    ErrorCode.TEMPLATE_INVALID: "模板无效",
    ErrorCode.TEMPLATE_RULE_MISSING: "模板规则缺失",
    ErrorCode.TEMPLATE_TYPE_UNSUPPORTED: "不支持的模板类型",
    
    ErrorCode.FORMAT_ERROR: "格式化失败",
    ErrorCode.FORMAT_FONT_ERROR: "字体格式设置失败",
    ErrorCode.FORMAT_MARGIN_ERROR: "页边距设置失败",
    ErrorCode.FORMAT_HEADING_ERROR: "标题格式设置失败",
    ErrorCode.FORMAT_REFERENCE_ERROR: "参考文献格式设置失败",
    ErrorCode.FORMAT_TABLE_ERROR: "表格格式设置失败",
    ErrorCode.FORMAT_FIGURE_ERROR: "图片格式设置失败",
    
    ErrorCode.AI_API_ERROR: "AI API 调用失败",
    ErrorCode.AI_API_TIMEOUT: "AI API 请求超时",
    ErrorCode.AI_API_KEY_INVALID: "AI API 密钥无效",
    ErrorCode.AI_RESPONSE_INVALID: "AI 返回数据无效",
    ErrorCode.AI_PARSE_ERROR: "AI 数据解析失败",
    
    ErrorCode.GENERATION_ERROR: "文档生成失败",
    ErrorCode.GENERATION_FIELD_MISSING: "必填字段缺失",
    ErrorCode.GENERATION_CONTENT_EMPTY: "内容为空",
    
    ErrorCode.UNKNOWN_ERROR: "未知错误",
}


@dataclass
class AppError:
    code: ErrorCode
    message: str
    detail: Optional[str] = None
    suggestion: Optional[str] = None
    
    def __str__(self) -> str:
        result = f"[错误码 {self.code.value}] {self.message}"
        if self.detail:
            result += f"\n详情: {self.detail}"
        if self.suggestion:
            result += f"\n建议: {self.suggestion}"
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': self.code.value,
            'message': self.message,
            'detail': self.detail,
            'suggestion': self.suggestion
        }


class ErrorHandler:
    def __init__(self):
        self.errors: list = []
    
    def add_error(self, code: ErrorCode, detail: str = None, suggestion: str = None) -> AppError:
        error = AppError(
            code=code,
            message=ERROR_MESSAGES.get(code, "未知错误"),
            detail=detail,
            suggestion=suggestion
        )
        self.errors.append(error)
        return error
    
    def has_errors(self) -> bool:
        return len(self.errors) > 0
    
    def get_errors(self) -> list:
        return self.errors
    
    def get_last_error(self) -> Optional[AppError]:
        return self.errors[-1] if self.errors else None
    
    def clear_errors(self):
        self.errors.clear()
    
    def get_error_summary(self) -> str:
        if not self.errors:
            return "无错误"
        
        summary = f"共 {len(self.errors)} 个错误:\n"
        for i, error in enumerate(self.errors, 1):
            summary += f"{i}. {error.message}"
            if error.detail:
                summary += f" - {error.detail}"
            summary += "\n"
        return summary


def create_error(code: ErrorCode, detail: str = None, suggestion: str = None) -> AppError:
    return AppError(
        code=code,
        message=ERROR_MESSAGES.get(code, "未知错误"),
        detail=detail,
        suggestion=suggestion
    )


def get_error_message(code: ErrorCode) -> str:
    return ERROR_MESSAGES.get(code, "未知错误")


SUGGESTIONS = {
    ErrorCode.FILE_NOT_FOUND: "请检查文件路径是否正确",
    ErrorCode.FILE_READ_ERROR: "请确保文件未被其他程序占用，且有读取权限",
    ErrorCode.FILE_WRITE_ERROR: "请确保有写入权限，且磁盘空间充足",
    ErrorCode.FILE_FORMAT_UNSUPPORTED: "支持的格式: .docx, .tex",
    ErrorCode.FILE_ENCODING_ERROR: "尝试使用其他编码打开文件",
    
    ErrorCode.PYTHON_NOT_INSTALLED: "请运行 '启动.bat' 自动安装 Python",
    ErrorCode.DEPENDENCY_MISSING: "请运行 '启动.bat' 自动安装依赖",
    
    ErrorCode.PARSE_ERROR: "请确保文档格式正确，未损坏",
    ErrorCode.PARSE_DOCX_ERROR: "请使用 Microsoft Word 打开并另存为 .docx 格式",
    
    ErrorCode.TEMPLATE_NOT_FOUND: "请在模板设定中创建或导入模板",
    ErrorCode.TEMPLATE_INVALID: "请检查模板配置是否完整",
    
    ErrorCode.FORMAT_ERROR: "请检查文档内容和模板设置",
    
    ErrorCode.AI_API_ERROR: "请检查网络连接和 API 配置",
    ErrorCode.AI_API_TIMEOUT: "请稍后重试或检查网络连接",
    ErrorCode.AI_API_KEY_INVALID: "请在设置中配置正确的 API 密钥",
    ErrorCode.AI_RESPONSE_INVALID: "请重新生成或手动调整",
    
    ErrorCode.GENERATION_FIELD_MISSING: "请填写所有必填字段",
    ErrorCode.GENERATION_CONTENT_EMPTY: "请输入论文内容",
}


def get_suggestion(code: ErrorCode) -> str:
    return SUGGESTIONS.get(code, "请参考帮助文档或联系技术支持")
