"""
配置快照模块
Configuration Snapshot Module

功能：
- 配置快照管理
- 快照命名和描述
- 快照标签分类
- 一键恢复

版本：v2.1.5
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConfigSnapshot:
    """配置快照数据类"""
    name: str  # 快照名称
    config: Dict[str, Any]  # 配置内容
    description: str = ""  # 描述
    tags: List[str] = field(default_factory=list)  # 标签
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    version: str = "1.0"  # 快照版本
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'config': self.config,
            'description': self.description,
            'tags': self.tags,
            'created_at': self.created_at,
            'version': self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConfigSnapshot':
        """从字典创建"""
        return cls(
            name=data['name'],
            config=data['config'],
            description=data.get('description', ''),
            tags=data.get('tags', []),
            created_at=data.get('created_at', datetime.now().timestamp()),
            version=data.get('version', '1.0')
        )
    
    def get_display_time(self) -> str:
        """获取显示时间"""
        dt = datetime.fromtimestamp(self.created_at)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_tags_str(self) -> str:
        """获取标签字符串"""
        return ', '.join(self.tags) if self.tags else '无标签'


class ConfigSnapshotManager:
    """配置快照管理器"""
    
    def __init__(self, snapshot_dir: Optional[str] = None):
        """
        初始化配置快照管理器
        
        Args:
            snapshot_dir: 快照目录
        """
        self.snapshot_dir = snapshot_dir
        if not snapshot_dir:
            self.snapshot_dir = str(Path.home() / '.paper_formatter' / 'config_snapshots')
        
        os.makedirs(self.snapshot_dir, exist_ok=True)
        
        self.snapshots: List[ConfigSnapshot] = []
        self._load_index()
    
    def create_snapshot(self, name: str, config: Dict[str, Any], 
                       description: str = "", tags: List[str] = None) -> ConfigSnapshot:
        """
        创建配置快照
        
        Args:
            name: 快照名称
            config: 配置字典
            description: 描述
            tags: 标签列表
        
        Returns:
            ConfigSnapshot 对象
        """
        # 检查名称是否重复
        if any(s.name == name for s in self.snapshots):
            raise ValueError(f"快照名称 '{name}' 已存在")
        
        snapshot = ConfigSnapshot(
            name=name,
            config=config,
            description=description,
            tags=tags or []
        )
        
        # 保存快照文件
        self._save_snapshot(snapshot)
        
        # 添加到列表
        self.snapshots.append(snapshot)
        
        # 保存索引
        self._save_index()
        
        return snapshot
    
    def get_snapshot(self, name: str) -> Optional[ConfigSnapshot]:
        """
        根据名称获取快照
        
        Args:
            name: 快照名称
        
        Returns:
            ConfigSnapshot 对象或 None
        """
        for snapshot in self.snapshots:
            if snapshot.name == name:
                return snapshot
        return None
    
    def restore_snapshot(self, name: str) -> Optional[Dict[str, Any]]:
        """
        恢复快照配置
        
        Args:
            name: 快照名称
        
        Returns:
            配置字典，如果快照不存在则返回 None
        """
        snapshot = self.get_snapshot(name)
        if snapshot:
            return snapshot.config
        return None
    
    def delete_snapshot(self, name: str) -> bool:
        """
        删除快照
        
        Args:
            name: 快照名称
        
        Returns:
            bool: 是否成功
        """
        snapshot = self.get_snapshot(name)
        if not snapshot:
            return False
        
        # 删除快照文件
        snapshot_file = os.path.join(self.snapshot_dir, f"{name}.json")
        if os.path.exists(snapshot_file):
            os.remove(snapshot_file)
        
        # 从列表中移除
        self.snapshots = [s for s in self.snapshots if s.name != name]
        
        # 保存索引
        self._save_index()
        
        return True
    
    def list_snapshots(self, tag_filter: Optional[str] = None) -> List[ConfigSnapshot]:
        """
        列出所有快照
        
        Args:
            tag_filter: 标签过滤（可选）
        
        Returns:
            快照列表
        """
        if tag_filter:
            return [s for s in self.snapshots if tag_filter in s.tags]
        return self.snapshots
    
    def search_snapshots(self, keyword: str) -> List[ConfigSnapshot]:
        """
        搜索快照
        
        Args:
            keyword: 关键词
        
        Returns:
            匹配的快照列表
        """
        results = []
        for snapshot in self.snapshots:
            if (keyword.lower() in snapshot.name.lower() or
                keyword.lower() in snapshot.description.lower() or
                any(keyword.lower() in tag.lower() for tag in snapshot.tags)):
                results.append(snapshot)
        return results
    
    def update_snapshot(self, name: str, config: Optional[Dict[str, Any]] = None,
                       description: Optional[str] = None, 
                       tags: Optional[List[str]] = None) -> bool:
        """
        更新快照
        
        Args:
            name: 快照名称
            config: 新配置（可选）
            description: 新描述（可选）
            tags: 新标签（可选）
        
        Returns:
            bool: 是否成功
        """
        snapshot = self.get_snapshot(name)
        if not snapshot:
            return False
        
        # 删除旧快照
        self.delete_snapshot(name)
        
        # 创建新快照
        new_config = config if config is not None else snapshot.config
        new_desc = description if description is not None else snapshot.description
        new_tags = tags if tags is not None else snapshot.tags
        
        self.create_snapshot(name, new_config, new_desc, new_tags)
        
        return True
    
    def export_snapshot(self, name: str, export_path: str) -> bool:
        """
        导出快照到文件
        
        Args:
            name: 快照名称
            export_path: 导出路径
        
        Returns:
            bool: 是否成功
        """
        snapshot = self.get_snapshot(name)
        if not snapshot:
            return False
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(snapshot.to_dict(), f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"导出快照失败：{e}")
            return False
    
    def import_snapshot(self, import_path: str) -> Optional[ConfigSnapshot]:
        """
        从文件导入快照
        
        Args:
            import_path: 导入路径
        
        Returns:
            ConfigSnapshot 对象或 None
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            snapshot = ConfigSnapshot.from_dict(data)
            
            # 如果名称已存在，添加时间戳
            if any(s.name == snapshot.name for s in self.snapshots):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                snapshot.name = f"{snapshot.name}_{timestamp}"
            
            # 保存快照
            self._save_snapshot(snapshot)
            self.snapshots.append(snapshot)
            self._save_index()
            
            return snapshot
            
        except Exception as e:
            print(f"导入快照失败：{e}")
            return None
    
    def get_snapshot_summary(self) -> str:
        """
        获取快照摘要
        
        Returns:
            str: 摘要文本
        """
        if not self.snapshots:
            return "没有配置快照"
        
        lines = ["配置快照列表", "=" * 60]
        
        for i, snapshot in enumerate(self.snapshots, 1):
            lines.append(f"\n{i}. {snapshot.name}")
            lines.append(f"   描述：{snapshot.description or '无描述'}")
            lines.append(f"   时间：{snapshot.get_display_time()}")
            lines.append(f"   标签：{snapshot.get_tags_str()}")
            lines.append(f"   配置项：{len(snapshot.config)} 个")
        
        lines.append(f"\n总计：{len(self.snapshots)} 个快照")
        
        return "\n".join(lines)
    
    def compare_snapshots(self, name1: str, name2: str) -> Optional[Dict[str, Any]]:
        """
        比较两个快照的差异
        
        Args:
            name1: 快照 1 名称
            name2: 快照 2 名称
        
        Returns:
            差异字典或 None
        """
        snap1 = self.get_snapshot(name1)
        snap2 = self.get_snapshot(name2)
        
        if not snap1 or not snap2:
            return None
        
        differences = {}
        
        all_sections = set(list(snap1.config.keys()) + list(snap2.config.keys()))
        
        for section in all_sections:
            config1 = snap1.config.get(section, {})
            config2 = snap2.config.get(section, {})
            
            if isinstance(config1, dict) and isinstance(config2, dict):
                all_keys = set(list(config1.keys()) + list(config2.keys()))
                
                section_diff = {}
                for key in all_keys:
                    val1 = config1.get(key)
                    val2 = config2.get(key)
                    
                    if val1 != val2:
                        section_diff[key] = {
                            'snapshot_1': val1,
                            'snapshot_2': val2
                        }
                
                if section_diff:
                    differences[section] = section_diff
            elif config1 != config2:
                differences[section] = {
                    'snapshot_1': config1,
                    'snapshot_2': config2
                }
        
        return differences
    
    def _save_snapshot(self, snapshot: ConfigSnapshot):
        """保存快照文件"""
        snapshot_file = os.path.join(self.snapshot_dir, f"{snapshot.name}.json")
        
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(snapshot.to_dict(), f, ensure_ascii=False, indent=2)
    
    def _load_index(self):
        """加载索引文件"""
        index_path = os.path.join(self.snapshot_dir, 'index.json')
        
        if not os.path.exists(index_path):
            # 尝试从现有文件重建索引
            self._rebuild_index()
            return
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.snapshots = [ConfigSnapshot.from_dict(s) for s in data.get('snapshots', [])]
            
        except Exception as e:
            print(f"加载索引失败：{e}")
            self._rebuild_index()
    
    def _rebuild_index(self):
        """从快照文件重建索引"""
        self.snapshots = []
        
        for file_name in os.listdir(self.snapshot_dir):
            if file_name.endswith('.json') and file_name != 'index.json':
                file_path = os.path.join(self.snapshot_dir, file_name)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    snapshot = ConfigSnapshot.from_dict(data)
                    self.snapshots.append(snapshot)
                    
                except Exception as e:
                    print(f"加载快照文件失败 {file_name}: {e}")
        
        self._save_index()
    
    def _save_index(self):
        """保存索引文件"""
        index_path = os.path.join(self.snapshot_dir, 'index.json')
        
        data = {
            'snapshots': [s.to_dict() for s in self.snapshots],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# 快捷函数
def create_config_snapshot(name: str, config: Dict[str, Any], 
                          description: str = "", tags: List[str] = None) -> ConfigSnapshot:
    """创建配置快照的快捷函数"""
    manager = ConfigSnapshotManager()
    return manager.create_snapshot(name, config, description, tags)


def restore_config_snapshot(name: str) -> Optional[Dict[str, Any]]:
    """恢复配置快照的快捷函数"""
    manager = ConfigSnapshotManager()
    return manager.restore_snapshot(name)


if __name__ == '__main__':
    # 测试
    print("测试配置快照管理器...")
    
    manager = ConfigSnapshotManager()
    print(f"快照目录：{manager.snapshot_dir}")
    
    # 测试创建快照
    test_config = {
        'font': {'chinese_font': '宋体', 'english_font': 'Times New Roman'},
        'page': {'paper_size': 'A4'}
    }
    
    snapshot = manager.create_snapshot(
        name='测试快照',
        config=test_config,
        description='这是一个测试快照',
        tags=['测试', '示例']
    )
    
    print(f"创建快照：{snapshot.name}")
    
    # 测试获取摘要
    print(manager.get_snapshot_summary())
    
    # 测试恢复
    restored = manager.restore_snapshot('测试快照')
    print(f"恢复配置：{restored}")
