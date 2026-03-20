"""
文件备份模块
File Backup Module

功能：
- 格式化前自动备份原文件
- 支持手动备份
- 自动清理旧备份
"""

import os
import shutil
from datetime import datetime


class FileBackup:
    """文件备份管理器"""
    
    def __init__(self, backup_dir=None):
        """
        初始化备份管理器
        
        参数：
        - backup_dir: 备份目录，默认为原文件目录下的 backup 文件夹
        """
        self.backup_dir = backup_dir
    
    def backup_file(self, file_path, keep_original_path=True):
        """
        备份文件
        
        参数：
        - file_path: 原文件路径
        - keep_original_path: 是否保持原路径结构
        
        返回：
        - str: 备份文件路径，失败返回 None
        """
        try:
            if not os.path.exists(file_path):
                print(f"文件不存在：{file_path}")
                return None
            
            # 获取文件信息
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            file_base, file_ext = os.path.splitext(file_name)
            
            # 生成备份文件名（带时间戳）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_base}_backup_{timestamp}{file_ext}"
            
            # 确定备份目录
            if self.backup_dir:
                backup_path = os.path.join(self.backup_dir, backup_name)
                os.makedirs(self.backup_dir, exist_ok=True)
            elif keep_original_path:
                # 在原文件目录下创建 backup 文件夹
                backup_dir = os.path.join(file_dir, "backup")
                backup_path = os.path.join(backup_dir, backup_name)
                os.makedirs(backup_dir, exist_ok=True)
            else:
                backup_path = os.path.join(file_dir, backup_name)
            
            # 执行备份
            shutil.copy2(file_path, backup_path)
            
            print(f"✓ 文件已备份：{backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"✗ 备份失败：{e}")
            return None
    
    def restore_file(self, backup_path, original_path=None):
        """
        恢复文件
        
        参数：
        - backup_path: 备份文件路径
        - original_path: 恢复到的路径（可选，默认为备份文件名去掉 backup 标记）
        
        返回：
        - bool: 是否成功
        """
        try:
            if not os.path.exists(backup_path):
                print(f"备份文件不存在：{backup_path}")
                return False
            
            if original_path is None:
                # 从备份文件名推断原文件名
                backup_name = os.path.basename(backup_path)
                # 移除 _backup_YYYYMMDD_HHMMSS 部分
                import re
                original_name = re.sub(r'_backup_\d{8}_\d{6}', '', backup_name)
                original_path = os.path.join(os.path.dirname(backup_path), original_name)
            
            # 恢复文件
            shutil.copy2(backup_path, original_path)
            
            print(f"✓ 文件已恢复：{original_path}")
            return True
            
        except Exception as e:
            print(f"✗ 恢复失败：{e}")
            return False
    
    def list_backups(self, original_file_path):
        """
        列出某个文件的所有备份
        
        参数：
        - original_file_path: 原文件路径
        
        返回：
        - list: 备份文件列表（按时间排序）
        """
        try:
            file_dir = os.path.dirname(original_file_path)
            file_name = os.path.basename(original_file_path)
            file_base, file_ext = os.path.splitext(file_name)
            
            backup_dir = os.path.join(file_dir, "backup")
            
            if not os.path.exists(backup_dir):
                return []
            
            backups = []
            for f in os.listdir(backup_dir):
                if f.startswith(file_base) and f.endswith(file_ext) and '_backup_' in f:
                    backups.append(os.path.join(backup_dir, f))
            
            # 按时间排序（新的在前）
            backups.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            
            return backups
            
        except Exception as e:
            print(f"✗ 列出备份失败：{e}")
            return []
    
    def cleanup_old_backups(self, original_file_path, keep_count=3):
        """
        清理旧备份，只保留最近的几个
        
        参数：
        - original_file_path: 原文件路径
        - keep_count: 保留的备份数量
        
        返回：
        - int: 删除的备份数量
        """
        try:
            backups = self.list_backups(original_file_path)
            
            if len(backups) <= keep_count:
                return 0
            
            # 删除多余的备份
            deleted_count = 0
            for backup in backups[keep_count:]:
                os.remove(backup)
                deleted_count += 1
            
            print(f"✓ 已清理 {deleted_count} 个旧备份")
            return deleted_count
            
        except Exception as e:
            print(f"✗ 清理备份失败：{e}")
            return 0


# 快捷函数
def auto_backup(file_path, keep_count=3):
    """
    自动备份文件（带清理）
    
    参数：
    - file_path: 文件路径
    - keep_count: 保留的备份数量
    
    返回：
    - str: 备份文件路径，失败返回 None
    """
    backup = FileBackup()
    backup_path = backup.backup_file(file_path)
    
    if backup_path:
        backup.cleanup_old_backups(file_path, keep_count)
    
    return backup_path


if __name__ == '__main__':
    # 测试
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        backup_path = auto_backup(file_path)
        if backup_path:
            print(f"备份成功：{backup_path}")
        else:
            print("备份失败")
    else:
        print("用法：python file_backup.py <文件路径>")
