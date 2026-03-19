"""
撤销/重做管理器模块
版本：v2.1.4
功能：支持操作历史的撤销和重做
"""

import copy
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field, asdict


@dataclass
class UndoAction:
    """撤销动作数据类"""
    action_type: str  # 操作类型：format, template_apply, config_change, file_operation
    file_path: str  # 操作的文件路径
    description: str  # 用户友好的描述
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    before_state: Optional[Dict[str, Any]] = None  # 操作前状态
    after_state: Optional[Dict[str, Any]] = None  # 操作后状态
    undo_data: Optional[Dict[str, Any]] = None  # 撤销所需的完整数据（用于复杂操作）
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于序列化）"""
        return {
            'action_type': self.action_type,
            'file_path': self.file_path,
            'description': self.description,
            'timestamp': self.timestamp,
            'before_state': self.before_state,
            'after_state': self.after_state,
            'undo_data': self.undo_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UndoAction':
        """从字典创建"""
        return cls(
            action_type=data['action_type'],
            file_path=data['file_path'],
            description=data['description'],
            timestamp=data.get('timestamp', datetime.now().timestamp()),
            before_state=data.get('before_state'),
            after_state=data.get('after_state'),
            undo_data=data.get('undo_data')
        )
    
    def get_display_time(self) -> str:
        """获取显示时间"""
        dt = datetime.fromtimestamp(self.timestamp)
        return dt.strftime('%H:%M:%S')


class UndoManager:
    """撤销/重做管理器"""
    
    MAX_UNDO_STEPS = 50  # 最大撤销步数
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化撤销管理器
        
        Args:
            config_dir: 配置目录，用于保存撤销历史
        """
        self.undo_stack: List[UndoAction] = []  # 撤销栈
        self.redo_stack: List[UndoAction] = []  # 重做栈
        self.config_dir = config_dir
        self.enabled = True  # 是否启用撤销功能
        self.listeners: List[Callable] = []  # 状态变化监听器
        
        # 加载持久化的撤销历史
        if config_dir:
            self.load_history()
    
    def add_listener(self, callback: Callable):
        """添加状态变化监听器"""
        self.listeners.append(callback)
    
    def remove_listener(self, callback: Callable):
        """移除监听器"""
        if callback in self.listeners:
            self.listeners.remove(callback)
    
    def _notify_listeners(self):
        """通知所有监听器状态变化"""
        for callback in self.listeners:
            try:
                callback(self)
            except Exception as e:
                print(f"UndoManager listener error: {e}")
    
    def can_undo(self) -> bool:
        """是否可以撤销"""
        return len(self.undo_stack) > 0 and self.enabled
    
    def can_redo(self) -> bool:
        """是否可以重做"""
        return len(self.redo_stack) > 0 and self.enabled
    
    def get_undo_count(self) -> int:
        """获取撤销栈中的操作数量"""
        return len(self.undo_stack)
    
    def get_redo_count(self) -> int:
        """获取重做栈中的操作数量"""
        return len(self.redo_stack)
    
    def push(self, action: UndoAction):
        """
        压入一个新的操作到撤销栈
        
        Args:
            action: 撤销动作对象
        """
        if not self.enabled:
            return
        
        # 压入新操作前，清空重做栈（因为新操作使重做历史失效）
        self.redo_stack.clear()
        
        # 压入撤销栈
        self.undo_stack.append(action)
        
        # 如果超过最大步数，移除最旧的操作
        if len(self.undo_stack) > self.MAX_UNDO_STEPS:
            self.undo_stack.pop(0)
        
        # 通知监听器
        self._notify_listeners()
        
        # 自动保存历史
        if self.config_dir:
            self.save_history()
    
    def undo(self) -> Optional[UndoAction]:
        """
        执行撤销操作
        
        Returns:
            被撤销的动作，如果无法撤销则返回 None
        """
        if not self.can_undo():
            return None
        
        # 弹出栈顶操作
        action = self.undo_stack.pop()
        
        # 压入重做栈
        self.redo_stack.append(action)
        
        # 通知监听器
        self._notify_listeners()
        
        # 自动保存历史
        if self.config_dir:
            self.save_history()
        
        return action
    
    def redo(self) -> Optional[UndoAction]:
        """
        执行重做操作
        
        Returns:
            被重做的动作，如果无法重做则返回 None
        """
        if not self.can_redo():
            return None
        
        # 弹出栈顶操作
        action = self.redo_stack.pop()
        
        # 压入撤销栈
        self.undo_stack.append(action)
        
        # 通知监听器
        self._notify_listeners()
        
        # 自动保存历史
        if self.config_dir:
            self.save_history()
        
        return action
    
    def clear(self):
        """清空所有撤销/重做历史"""
        self.undo_stack.clear()
        self.redo_stack.clear()
        self._notify_listeners()
        if self.config_dir:
            self.save_history()
    
    def get_history(self, limit: int = 20) -> List[UndoAction]:
        """
        获取最近的操作历史
        
        Args:
            limit: 最多返回的操作数量
            
        Returns:
            操作历史列表（最近的在前）
        """
        return list(reversed(self.undo_stack[-limit:]))
    
    def save_history(self):
        """保存撤销历史到文件"""
        if not self.config_dir:
            return
        
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            history_file = os.path.join(self.config_dir, 'undo_history.json')
            
            data = {
                'undo_stack': [action.to_dict() for action in self.undo_stack],
                'redo_stack': [action.to_dict() for action in self.redo_stack],
                'saved_at': datetime.now().isoformat()
            }
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存撤销历史失败：{e}")
    
    def load_history(self):
        """从文件加载撤销历史"""
        if not self.config_dir:
            return
        
        try:
            history_file = os.path.join(self.config_dir, 'undo_history.json')
            
            if not os.path.exists(history_file):
                return
            
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.undo_stack = [UndoAction.from_dict(d) for d in data.get('undo_stack', [])]
            self.redo_stack = [UndoAction.from_dict(d) for d in data.get('redo_stack', [])]
            
            self._notify_listeners()
            
        except Exception as e:
            print(f"加载撤销历史失败：{e}")
            # 如果加载失败，清空历史
            self.clear()
    
    def create_format_action(self, file_path: str, before_format: Dict[str, Any], 
                            after_format: Dict[str, Any]) -> UndoAction:
        """
        创建格式化操作的撤销动作
        
        Args:
            file_path: 文件路径
            before_format: 格式化前的格式
            after_format: 格式化后的格式
            
        Returns:
            UndoAction 对象
        """
        return UndoAction(
            action_type='format',
            file_path=file_path,
            description='文档格式化',
            before_state=before_format,
            after_state=after_format,
            undo_data={
                'type': 'format',
                'before': before_format,
                'after': after_format
            }
        )
    
    def create_template_action(self, file_path: str, template_name: str,
                              before_rules: Dict[str, Any], after_rules: Dict[str, Any]) -> UndoAction:
        """
        创建模板应用操作的撤销动作
        
        Args:
            file_path: 文件路径
            template_name: 模板名称
            before_rules: 应用前的规则
            after_rules: 应用后的规则
            
        Returns:
            UndoAction 对象
        """
        return UndoAction(
            action_type='template_apply',
            file_path=file_path,
            description=f'应用模板：{template_name}',
            before_state=before_rules,
            after_state=after_rules,
            undo_data={
                'type': 'template_apply',
                'template_name': template_name,
                'before': before_rules,
                'after': after_rules
            }
        )
    
    def create_config_action(self, config_name: str, before_value: Any, 
                            after_value: Any) -> UndoAction:
        """
        创建配置修改操作的撤销动作
        
        Args:
            config_name: 配置项名称
            before_value: 修改前的值
            after_value: 修改后的值
            
        Returns:
            UndoAction 对象
        """
        return UndoAction(
            action_type='config_change',
            file_path='',
            description=f'修改配置：{config_name}',
            before_state={'key': config_name, 'value': before_value},
            after_state={'key': config_name, 'value': after_value},
            undo_data={
                'type': 'config_change',
                'key': config_name,
                'before': before_value,
                'after': after_value
            }
        )
    
    def create_file_operation_action(self, file_path: str, operation_type: str,
                                    description: str, undo_data: Dict[str, Any]) -> UndoAction:
        """
        创建文件操作（删除/移动等）的撤销动作
        
        Args:
            file_path: 文件路径
            operation_type: 操作类型（delete, move, rename）
            description: 操作描述
            undo_data: 撤销所需的完整数据
            
        Returns:
            UndoAction 对象
        """
        return UndoAction(
            action_type='file_operation',
            file_path=file_path,
            description=description,
            undo_data={
                'type': 'file_operation',
                'operation': operation_type,
                **undo_data
            }
        )


# 全局撤销管理器实例（可选）
_global_undo_manager: Optional[UndoManager] = None

def get_global_undo_manager(config_dir: Optional[str] = None) -> UndoManager:
    """获取全局撤销管理器实例"""
    global _global_undo_manager
    if _global_undo_manager is None:
        _global_undo_manager = UndoManager(config_dir)
    return _global_undo_manager
