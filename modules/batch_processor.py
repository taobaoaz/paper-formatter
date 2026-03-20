"""
批量处理模块
Batch Processing Module

功能：
- 批量格式化多个文档
- 支持进度显示
- 支持取消操作
- 生成处理报告
"""

import os
import threading
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal


class BatchProcessor(QObject):
    """批量处理器"""
    
    # 信号
    progress = pyqtSignal(int, int, str)  # 当前，总数，文件名
    file_completed = pyqtSignal(str, bool, str)  # 文件名，成功，消息
    batch_completed = pyqtSignal(int, int)  # 成功数，失败数
    error = pyqtSignal(str)  # 错误信息
    
    def __init__(self):
        super().__init__()
        self.cancelled = False
        self.processing = False
    
    def process_files(self, file_list, process_func, output_dir=None):
        """
        批量处理文件
        
        参数：
        - file_list: 文件路径列表
        - process_func: 处理函数 (file_path, output_path) -> bool
        - output_dir: 输出目录（可选）
        """
        self.cancelled = False
        self.processing = True
        
        total = len(file_list)
        success_count = 0
        fail_count = 0
        
        for index, file_path in enumerate(file_list):
            # 检查是否取消
            if self.cancelled:
                print("用户取消处理")
                break
            
            file_name = os.path.basename(file_path)
            
            # 发送进度信号
            self.progress.emit(index + 1, total, file_name)
            
            # 确定输出路径
            if output_dir:
                output_path = os.path.join(output_dir, os.path.basename(file_path))
            else:
                output_path = file_path
            
            try:
                # 执行处理
                success = process_func(file_path, output_path)
                
                if success:
                    success_count += 1
                    self.file_completed.emit(file_name, True, "处理成功")
                else:
                    fail_count += 1
                    self.file_completed.emit(file_name, False, "处理失败")
                    
            except Exception as e:
                fail_count += 1
                error_msg = f"{file_name}: {str(e)}"
                self.file_completed.emit(file_name, False, error_msg)
                self.error.emit(error_msg)
        
        self.processing = False
        
        # 发送完成信号
        self.batch_completed.emit(success_count, fail_count)
        
        return success_count, fail_count
    
    def cancel(self):
        """取消处理"""
        if self.processing:
            self.cancelled = True
            print("正在取消...")
        else:
            print("没有正在进行的处理")
    
    def is_processing(self):
        """是否正在处理"""
        return self.processing


class BatchReport:
    """批量处理报告"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def add_result(self, file_name, success, message=""):
        """添加处理结果"""
        self.results.append({
            'file': file_name,
            'success': success,
            'message': message,
            'time': datetime.now().strftime("%H:%M:%S")
        })
    
    def generate_report(self, output_path=None):
        """
        生成报告
        
        参数：
        - output_path: 输出路径（可选）
        
        返回：
        - str: 报告内容
        """
        success_count = sum(1 for r in self.results if r['success'])
        fail_count = len(self.results) - success_count
        
        report = []
        report.append("=" * 60)
        report.append("批量处理报告")
        report.append("=" * 60)
        report.append(f"处理时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"总文件数：{len(self.results)}")
        report.append(f"成功：{success_count}")
        report.append(f"失败：{fail_count}")
        report.append("=" * 60)
        report.append("")
        report.append("详细结果：")
        report.append("-" * 60)
        
        for result in self.results:
            status = "✓" if result['success'] else "✗"
            report.append(f"[{status}] {result['file']} - {result['message']} ({result['time']})")
        
        report.append("-" * 60)
        
        report_text = "\n".join(report)
        
        # 保存到文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"报告已保存：{output_path}")
        
        return report_text


# 快捷函数
def batch_process_files(file_list, process_func, output_dir=None, show_progress=True):
    """
    批量处理文件（简单版本）
    
    参数：
    - file_list: 文件列表
    - process_func: 处理函数
    - output_dir: 输出目录
    - show_progress: 显示进度
    
    返回：
    - tuple: (成功数，失败数)
    """
    total = len(file_list)
    success = 0
    fail = 0
    
    for i, file_path in enumerate(file_list):
        file_name = os.path.basename(file_path)
        
        if show_progress:
            print(f"[{i+1}/{total}] 处理：{file_name}")
        
        try:
            if output_dir:
                output_path = os.path.join(output_dir, os.path.basename(file_path))
            else:
                output_path = file_path
            
            if process_func(file_path, output_path):
                success += 1
                if show_progress:
                    print(f"  ✓ 成功")
            else:
                fail += 1
                if show_progress:
                    print(f"  ✗ 失败")
                    
        except Exception as e:
            fail += 1
            if show_progress:
                print(f"  ✗ 错误：{e}")
    
    return success, fail


if __name__ == '__main__':
    # 测试
    print("批量处理模块测试")
    print("此模块需要在 GUI 中使用")
