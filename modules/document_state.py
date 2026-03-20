"""
文档状态快照模块
Document State Snapshot Module

功能：
- 文档状态快照（用于撤销/重做）
- 增量保存（只保存变化的部分）
- 状态比较和恢复

版本：v2.1.5
"""

import os
import json
import copy
import shutil
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class DocumentState:
    """文档状态数据类"""
    file_path: str  # 文件路径
    snapshot_path: str  # 快照文件路径
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    description: str = ""  # 快照描述
    state_type: str = "full"  # full(完整) 或 incremental(增量)
    file_size: int = 0  # 文件大小（字节）
    checksum: str = ""  # 文件校验和（可选）
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    
    @property
    def is_important(self) -> bool:
        """是否重要快照 (v2.1.8 新增)"""
        return self.metadata.get('is_important', False)
    
    def mark_as_important(self, reason: str = ""):
        """标记为重要快照 (v2.1.8 新增)"""
        self.metadata['is_important'] = True
        self.metadata['importance_reason'] = reason
        self.metadata['importance_marked_at'] = datetime.now().timestamp()
    
    def unmark_as_important(self):
        """取消重要标记 (v2.1.8 新增)"""
        self.metadata['is_important'] = False
        self.metadata.pop('importance_reason', None)
        self.metadata.pop('importance_marked_at', None)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'file_path': self.file_path,
            'snapshot_path': self.snapshot_path,
            'timestamp': self.timestamp,
            'description': self.description,
            'state_type': self.state_type,
            'file_size': self.file_size,
            'checksum': self.checksum,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentState':
        """从字典创建"""
        return cls(
            file_path=data['file_path'],
            snapshot_path=data['snapshot_path'],
            timestamp=data.get('timestamp', datetime.now().timestamp()),
            description=data.get('description', ''),
            state_type=data.get('state_type', 'full'),
            file_size=data.get('file_size', 0),
            checksum=data.get('checksum', ''),
            metadata=data.get('metadata', {})
        )
    
    def get_display_time(self) -> str:
        """获取显示时间"""
        dt = datetime.fromtimestamp(self.timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class Change:
    """变化数据类（用于增量保存）"""
    change_type: str  # format, style, content, structure
    location: str  # 位置描述（如 "第 3 段", "标题 1"）
    before: Any = None  # 变化前的值
    after: Any = None  # 变化后的值
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'change_type': self.change_type,
            'location': self.location,
            'before': self.before,
            'after': self.after,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Change':
        """从字典创建"""
        return cls(
            change_type=data['change_type'],
            location=data['location'],
            before=data.get('before'),
            after=data.get('after'),
            timestamp=data.get('timestamp', datetime.now().timestamp())
        )


@dataclass
class IncrementalState:
    """增量状态数据类"""
    base_state: DocumentState  # 基础状态
    changes: List[Change] = field(default_factory=list)  # 变化列表
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'base_state': self.base_state.to_dict(),
            'changes': [c.to_dict() for c in self.changes]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IncrementalState':
        """从字典创建"""
        base = DocumentState.from_dict(data['base_state'])
        changes = [Change.from_dict(c) for c in data.get('changes', [])]
        return cls(base_state=base, changes=changes)


class DocumentStateManager:
    """文档状态管理器"""
    
    def __init__(self, snapshot_dir: Optional[str] = None):
        """
        初始化文档状态管理器
        
        Args:
            snapshot_dir: 快照目录
        """
        self.snapshot_dir = snapshot_dir
        if not snapshot_dir:
            from pathlib import Path
            self.snapshot_dir = str(Path.home() / '.paper_formatter' / 'snapshots')
        
        os.makedirs(self.snapshot_dir, exist_ok=True)
        
        self.states: List[DocumentState] = []  # 状态历史
        self.max_states = 20  # 最多保存 20 个状态
    
    def create_snapshot(self, file_path: str, description: str = "", 
                       snapshot_type: str = "full", metadata: Dict[str, Any] = None) -> DocumentState:
        """
        创建文档快照
        
        Args:
            file_path: 文档文件路径
            description: 快照描述
            snapshot_type: 快照类型（full 或 incremental）
            metadata: 元数据（v2.1.8 新增）
        
        Returns:
            DocumentState 对象
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        # 生成快照文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        file_name = os.path.basename(file_path)
        snapshot_name = f"{os.path.splitext(file_name)[0]}_{timestamp}.docx"
        snapshot_path = os.path.join(self.snapshot_dir, snapshot_name)
        
        # 复制文件
        shutil.copy2(file_path, snapshot_path)
        
        # 计算文件大小
        file_size = os.path.getsize(snapshot_path)
        
        # 创建状态对象
        state = DocumentState(
            file_path=file_path,
            snapshot_path=snapshot_path,
            description=description,
            state_type=snapshot_type,
            file_size=file_size,
            metadata=metadata or {}
        )
        
        # 添加到历史
        self.states.append(state)
        
        # 如果超过最大数量，移除最旧的
        if len(self.states) > self.max_states:
            self._remove_oldest_state()
        
        # 保存索引
        self._save_index()
        
        return state
    
    def restore_snapshot(self, state: DocumentState, target_path: Optional[str] = None) -> bool:
        """
        恢复快照到指定路径
        
        Args:
            state: 快照状态对象
            target_path: 目标路径（可选，默认为原文件路径）
        
        Returns:
            bool: 是否成功
        """
        try:
            if not os.path.exists(state.snapshot_path):
                raise FileNotFoundError(f"快照文件不存在：{state.snapshot_path}")
            
            target = target_path or state.file_path
            
            # 恢复文件
            shutil.copy2(state.snapshot_path, target)
            
            return True
            
        except Exception as e:
            print(f"恢复快照失败：{e}")
            return False
    
    def delete_snapshot(self, state: DocumentState) -> bool:
        """
        删除快照
        
        Args:
            state: 快照状态对象
        
        Returns:
            bool: 是否成功
        """
        try:
            # 删除快照文件
            if os.path.exists(state.snapshot_path):
                os.remove(state.snapshot_path)
            
            # 从历史中移除
            if state in self.states:
                self.states.remove(state)
            
            # 保存索引
            self._save_index()
            
            return True
            
        except Exception as e:
            print(f"删除快照失败：{e}")
            return False
    
    def get_states(self, limit: int = 10) -> List[DocumentState]:
        """
        获取最近的状态历史
        
        Args:
            limit: 最多返回的数量
        
        Returns:
            状态列表（最近的在前）
        """
        return list(reversed(self.states[-limit:]))
    
    def clear_all(self):
        """清空所有快照"""
        for state in self.states:
            if os.path.exists(state.snapshot_path):
                os.remove(state.snapshot_path)
        
        self.states.clear()
        self._save_index()
    
    def _remove_oldest_state(self):
        """移除最旧的状态"""
        if self.states:
            oldest = self.states.pop(0)
            if os.path.exists(oldest.snapshot_path):
                os.remove(oldest.snapshot_path)
    
    def _save_index(self):
        """保存索引文件"""
        index_path = os.path.join(self.snapshot_dir, 'index.json')
        
        data = {
            'states': [s.to_dict() for s in self.states],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_index(self):
        """加载索引文件"""
        index_path = os.path.join(self.snapshot_dir, 'index.json')
        
        if not os.path.exists(index_path):
            return
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.states = [DocumentState.from_dict(s) for s in data.get('states', [])]
            
        except Exception as e:
            print(f"加载索引失败：{e}")
            self.states = []
    
    def get_state_by_index(self, index: int) -> Optional[DocumentState]:
        """
        根据索引获取状态
        
        Args:
            index: 索引（-1 表示最后一个）
        
        Returns:
            DocumentState 对象或 None
        """
        if not self.states:
            return None
        
        if index < 0:
            index = len(self.states) + index
        
        if 0 <= index < len(self.states):
            return self.states[index]
        
        return None
    
    def get_state_summary(self) -> str:
        """
        获取状态摘要
        
        Returns:
            str: 摘要文本
        """
        if not self.states:
            return "没有快照"
        
        lines = ["文档快照历史", "=" * 40]
        
        for i, state in enumerate(reversed(self.states[-10:])):
            lines.append(f"{i+1}. {state.get_display_time()} - {state.description or '无描述'}")
            lines.append(f"   文件：{os.path.basename(state.file_path)}")
            lines.append(f"   大小：{state.file_size / 1024:.1f} KB")
            lines.append(f"   类型：{state.state_type}")
            lines.append("")
        
        return "\n".join(lines)


class IncrementalSaver:
    """增量保存器"""
    
    def __init__(self):
        """初始化增量保存器"""
        self.changes: List[Change] = []
        self.base_state: Optional[DocumentState] = None
    
    def record_change(self, change_type: str, location: str, 
                     before: Any, after: Any, description: str = ""):
        """
        记录一个变化
        
        Args:
            change_type: 变化类型
            location: 位置
            before: 变化前
            after: 变化后
            description: 描述
        """
        change = Change(
            change_type=change_type,
            location=location,
            before=before,
            after=after
        )
        self.changes.append(change)
    
    def get_changes(self, limit: int = 100) -> List[Change]:
        """获取变化列表"""
        return self.changes[-limit:]
    
    def clear_changes(self):
        """清空变化记录"""
        self.changes.clear()
    
    def get_changes_summary(self) -> str:
        """
        获取变化摘要
        
        Returns:
            str: 摘要文本
        """
        if not self.changes:
            return "没有变化记录"
        
        lines = ["变化记录", "=" * 40]
        
        for i, change in enumerate(self.changes[-20:], 1):
            lines.append(f"{i}. [{change.change_type}] {change.location}")
            lines.append(f"   {change.before} → {change.after}")
            lines.append("")
        
        return "\n".join(lines)


# 快捷函数
def create_document_snapshot(file_path: str, description: str = "", 
                            snapshot_dir: Optional[str] = None) -> DocumentState:
    """创建文档快照的快捷函数"""
    manager = DocumentStateManager(snapshot_dir)
    return manager.create_snapshot(file_path, description)


def restore_document_snapshot(state: DocumentState, 
                             target_path: Optional[str] = None) -> bool:
    """恢复文档快照的快捷函数"""
    manager = DocumentStateManager()
    return manager.restore_snapshot(state, target_path)


if __name__ == '__main__':
    # 测试
    print("测试文档状态管理器...")
    
    manager = DocumentStateManager()
    print(f"快照目录：{manager.snapshot_dir}")
    
    # 测试创建快照（需要有测试文件）
    # state = manager.create_snapshot('/path/to/test.docx', '测试快照')
    # print(f"创建快照：{state}")
    
    # 测试获取历史
    print(manager.get_state_summary())
