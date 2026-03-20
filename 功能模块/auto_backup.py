"""
自动备份管理器模块
Auto Backup Manager Module

功能：
- 定期自动备份
- 智能清理策略
- 快照重要性标记

版本：v2.1.8
"""

import os
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from pathlib import Path

from document_state import DocumentStateManager, DocumentState


@dataclass
class BackupConfig:
    """备份配置数据类"""
    enabled: bool = True  # 是否启用自动备份
    interval_minutes: int = 10  # 备份间隔（分钟）
    keep_recent_count: int = 20  # 保留最近 N 个快照
    keep_hours: int = 24  # 保留 N 小时内的快照
    keep_important: bool = True  # 保留重要快照
    notify_on_backup: bool = False  # 备份后通知
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'enabled': self.enabled,
            'interval_minutes': self.interval_minutes,
            'keep_recent_count': self.keep_recent_count,
            'keep_hours': self.keep_hours,
            'keep_important': self.keep_important,
            'notify_on_backup': self.notify_on_backup
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupConfig':
        """从字典创建"""
        return cls(
            enabled=data.get('enabled', True),
            interval_minutes=data.get('interval_minutes', 10),
            keep_recent_count=data.get('keep_recent_count', 20),
            keep_hours=data.get('keep_hours', 24),
            keep_important=data.get('keep_important', True),
            notify_on_backup=data.get('notify_on_backup', False)
        )


class SmartCleanupPolicy:
    """智能清理策略"""
    
    def __init__(self, config: BackupConfig = None):
        """
        初始化清理策略
        
        Args:
            config: 备份配置
        """
        self.config = config or BackupConfig()
    
    def get_snapshots_to_delete(self, states: List[DocumentState]) -> List[DocumentState]:
        """
        获取需要删除的快照列表
        
        Args:
            states: 所有快照状态列表
            
        Returns:
            需要删除的快照列表
        """
        if not states:
            return []
        
        now = time.time()
        to_keep_paths = set()  # 使用路径作为唯一标识
        
        # 1. 保留重要快照
        if self.config.keep_important:
            important_states = [s for s in states if s.metadata.get('is_important', False)]
            to_keep_paths.update([s.snapshot_path for s in important_states])
            print(f"智能清理：保留 {len(important_states)} 个重要快照")
        
        # 2. 保留最近 N 个
        sorted_states = sorted(states, key=lambda s: s.timestamp, reverse=True)
        recent_states = sorted_states[:self.config.keep_recent_count]
        to_keep_paths.update([s.snapshot_path for s in recent_states])
        print(f"智能清理：保留最近 {self.config.keep_recent_count} 个快照")
        
        # 3. 保留 N 小时内的快照
        keep_seconds = self.config.keep_hours * 3600
        recent_24h = [s for s in states if now - s.timestamp < keep_seconds]
        to_keep_paths.update([s.snapshot_path for s in recent_24h])
        print(f"智能清理：保留 {self.config.keep_hours} 小时内的快照 ({len(recent_24h)} 个)")
        
        # 计算需要删除的快照
        to_delete = [s for s in states if s.snapshot_path not in to_keep_paths]
        
        print(f"智能清理：总计 {len(states)} 个快照，保留 {len(to_keep_paths)} 个，删除 {len(to_delete)} 个")
        
        return to_delete
    
    def cleanup(self, manager: DocumentStateManager) -> Dict[str, Any]:
        """
        执行清理操作
        
        Args:
            manager: 文档状态管理器
            
        Returns:
            清理结果统计
        """
        states = manager.get_states(limit=100)
        to_delete = self.get_snapshots_to_delete(states)
        
        deleted_count = 0
        for state in to_delete:
            try:
                manager.delete_snapshot(state)
                deleted_count += 1
            except Exception as e:
                print(f"删除快照失败：{state.snapshot_path} - {e}")
        
        return {
            'total_states': len(states),
            'deleted_count': deleted_count,
            'remaining_count': len(states) - deleted_count
        }


class AutoBackupManager:
    """自动备份管理器"""
    
    def __init__(self, state_manager: DocumentStateManager, config: BackupConfig = None):
        """
        初始化自动备份管理器
        
        Args:
            state_manager: 文档状态管理器
            config: 备份配置
        """
        self.state_manager = state_manager
        self.config = config or BackupConfig()
        self.last_backup_time = None
        self.backup_listeners: List[Callable] = []
        
        # 加载上次备份时间
        self._load_last_backup_time()
    
    def add_listener(self, callback: Callable):
        """添加备份事件监听器"""
        self.backup_listeners.append(callback)
    
    def remove_listener(self, callback: Callable):
        """移除监听器"""
        if callback in self.backup_listeners:
            self.backup_listeners.remove(callback)
    
    def _notify_listeners(self, event_type: str, data: Dict[str, Any] = None):
        """通知监听器"""
        for callback in self.backup_listeners:
            try:
                callback(event_type, data)
            except Exception as e:
                print(f"AutoBackupManager listener error: {e}")
    
    def _load_last_backup_time(self):
        """加载上次备份时间"""
        try:
            index_file = os.path.join(self.state_manager.snapshot_dir, 'auto_backup.json')
            if os.path.exists(index_file):
                with open(index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.last_backup_time = data.get('last_backup_time')
        except Exception as e:
            print(f"加载上次备份时间失败：{e}")
    
    def _save_last_backup_time(self):
        """保存上次备份时间"""
        try:
            index_file = os.path.join(self.state_manager.snapshot_dir, 'auto_backup.json')
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'last_backup_time': self.last_backup_time
                }, f, indent=2)
        except Exception as e:
            print(f"保存上次备份时间失败：{e}")
    
    def should_backup(self, file_path: str = None) -> bool:
        """
        检查是否应该备份
        
        Args:
            file_path: 文件路径（可选，用于检查文件是否有新快照）
            
        Returns:
            是否应该备份
        """
        if not self.config.enabled:
            return False
        
        now = time.time()
        
        # 如果从未备份过，应该备份
        if self.last_backup_time is None:
            return True
        
        # 检查是否超过间隔时间
        elapsed = now - self.last_backup_time
        interval_seconds = self.config.interval_minutes * 60
        
        if elapsed >= interval_seconds:
            return True
        
        return False
    
    def create_backup(self, file_path: str, description: str = "") -> Optional[DocumentState]:
        """
        创建备份
        
        Args:
            file_path: 文件路径
            description: 备份描述
            
        Returns:
            创建的快照状态，失败返回 None
        """
        if not self.config.enabled:
            print("自动备份已禁用")
            return None
        
        if not os.path.exists(file_path):
            print(f"文件不存在：{file_path}")
            return None
        
        try:
            # 生成描述
            if not description:
                description = f'自动备份 - {datetime.now().strftime("%Y-%m-%d %H:%M")}'
            
            # 创建快照
            snapshot = self.state_manager.create_snapshot(
                file_path=file_path,
                description=description,
                metadata={'auto_backup': True}
            )
            
            # 更新上次备份时间
            self.last_backup_time = time.time()
            self._save_last_backup_time()
            
            # 通知监听器
            self._notify_listeners('backup_created', {
                'snapshot': snapshot,
                'file_path': file_path
            })
            
            print(f"自动备份完成：{snapshot.snapshot_path}")
            
            return snapshot
            
        except Exception as e:
            print(f"自动备份失败：{e}")
            self._notify_listeners('backup_failed', {
                'file_path': file_path,
                'error': str(e)
            })
            return None
    
    def check_and_backup(self, file_path: str = None) -> Optional[DocumentState]:
        """
        检查并执行备份
        
        Args:
            file_path: 文件路径
            
        Returns:
            创建的快照状态，未备份返回 None
        """
        if self.should_backup(file_path):
            return self.create_backup(file_path)
        return None
    
    def cleanup(self) -> Dict[str, Any]:
        """
        执行智能清理
        
        Returns:
            清理结果统计
        """
        policy = SmartCleanupPolicy(self.config)
        result = policy.cleanup(self.state_manager)
        
        if result['deleted_count'] > 0:
            self._notify_listeners('cleanup_completed', result)
        
        return result
    
    def get_backup_status(self) -> Dict[str, Any]:
        """
        获取备份状态
        
        Returns:
            备份状态信息
        """
        now = time.time()
        
        status = {
            'enabled': self.config.enabled,
            'interval_minutes': self.config.interval_minutes,
            'last_backup_time': self.last_backup_time,
            'next_backup_in_seconds': None,
            'next_backup_in_minutes': None
        }
        
        if self.last_backup_time:
            elapsed = now - self.last_backup_time
            interval_seconds = self.config.interval_minutes * 60
            remaining = interval_seconds - elapsed
            
            if remaining > 0:
                status['next_backup_in_seconds'] = int(remaining)
                status['next_backup_in_minutes'] = int(remaining / 60)
            else:
                status['next_backup_in_seconds'] = 0
                status['next_backup_in_minutes'] = 0
        
        return status
    
    def save_config(self, config_path: str = None):
        """保存配置"""
        if not config_path:
            config_path = os.path.join(self.state_manager.snapshot_dir, 'backup_config.json')
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config.to_dict(), f, indent=2)
            print(f"备份配置已保存：{config_path}")
        except Exception as e:
            print(f"保存备份配置失败：{e}")
    
    def load_config(self, config_path: str = None):
        """加载配置"""
        if not config_path:
            config_path = os.path.join(self.state_manager.snapshot_dir, 'backup_config.json')
        
        if not os.path.exists(config_path):
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.config = BackupConfig.from_dict(data)
            print(f"备份配置已加载：{config_path}")
        except Exception as e:
            print(f"加载备份配置失败：{e}")
