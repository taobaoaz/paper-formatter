#!/usr/bin/env python3
"""
Paper Formatter - 基础测试
测试项目的基本结构和功能
"""

import unittest
import os
import sys
import json

class TestProjectStructure(unittest.TestCase):
    """测试项目结构"""
    
    def test_essential_files_exist(self):
        """测试必要文件是否存在"""
        essential_files = [
            'README.md',
            'CHANGELOG.md',
            'CONTRIBUTING.md',
            'LICENSE',
            '.gitignore',
            'launcher/requirements.txt'
        ]
        
        for file in essential_files:
            with self.subTest(file=file):
                self.assertTrue(os.path.exists(file), f"必要文件不存在: {file}")
    
    def test_directories_exist(self):
        """测试必要目录是否存在"""
        essential_dirs = [
            'core',
            'modules',
            'launcher',
            'templates',
            'releases',
            'tests',
            '.github/workflows'
        ]
        
        for directory in essential_dirs:
            with self.subTest(directory=directory):
                self.assertTrue(os.path.exists(directory), f"必要目录不存在: {directory}")

class TestDocumentation(unittest.TestCase):
    """测试文档"""
    
    def test_readme_content(self):
        """测试 README 内容"""
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('# Paper Formatter', content, "README.md 缺少标题")
            self.assertIn('## ✨ Features', content, "README.md 缺少功能列表")
            self.assertIn('## 🚀 Quick Start', content, "README.md 缺少快速开始")
    
    def test_changelog_format(self):
        """测试 CHANGELOG 格式"""
        with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('# Changelog', content, "CHANGELOG.md 缺少标题")
            self.assertIn('## [Unreleased]', content, "CHANGELOG.md 缺少 [Unreleased] 部分")
            self.assertIn('## [v2.2.3]', content, "CHANGELOG.md 缺少最新版本")
    
    def test_contributing_guidelines(self):
        """测试贡献指南"""
        with open('CONTRIBUTING.md', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('# Contributing to Paper Formatter', content, "CONTRIBUTING.md 缺少标题")
            self.assertIn('## 🎯 How to Contribute', content, "CONTRIBUTING.md 缺少贡献指南")

class TestGitHubWorkflows(unittest.TestCase):
    """测试 GitHub 工作流"""
    
    def test_workflow_files(self):
        """测试工作流文件"""
        workflow_files = [
            '.github/workflows/build-windows.yml',
            '.github/workflows/build-installer.yml'
        ]
        
        for file in workflow_files:
            with self.subTest(file=file):
                self.assertTrue(os.path.exists(file), f"GitHub 工作流文件不存在: {file}")
    
    def test_workflow_content(self):
        """测试工作流内容"""
        with open('.github/workflows/build-windows.yml', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('name: Build Windows EXE', content, "build-windows.yml 缺少名称")
            self.assertIn('on:', content, "build-windows.yml 缺少触发条件")
            self.assertIn('jobs:', content, "build-windows.yml 缺少任务定义")

class TestReleaseNotes(unittest.TestCase):
    """测试发布说明"""
    
    def test_release_notes_exist(self):
        """测试发布说明文件存在"""
        releases_dir = 'releases'
        self.assertTrue(os.path.exists(releases_dir), f"发布说明目录不存在: {releases_dir}")
        
        # 检查发布说明文件
        release_files = os.listdir(releases_dir)
        self.assertGreater(len(release_files), 0, "发布说明目录为空")
        
        # 检查至少有一个 RELEASE_NOTES 文件
        has_release_notes = any(f.startswith('RELEASE_NOTES_') for f in release_files)
        self.assertTrue(has_release_notes, "没有找到 RELEASE_NOTES 文件")

class TestRequirements(unittest.TestCase):
    """测试依赖文件"""
    
    def test_requirements_format(self):
        """测试 requirements.txt 格式"""
        with open('launcher/requirements.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0, "requirements.txt 为空")
            
            # 检查是否有有效的依赖
            valid_lines = [line for line in lines if line.strip() and not line.startswith('#')]
            self.assertGreater(len(valid_lines), 0, "requirements.txt 没有有效的依赖")

def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestProjectStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentation))
    suite.addTests(loader.loadTestsFromTestCase(TestGitHubWorkflows))
    suite.addTests(loader.loadTestsFromTestCase(TestReleaseNotes))
    suite.addTests(loader.loadTestsFromTestCase(TestRequirements))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出摘要
    print("\n" + "="*60)
    print("测试摘要:")
    print("="*60)
    print(f"总测试数: {result.testsRun}")
    print(f"通过: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            test_id = test.id().split('.')[-1]
            print(f"  ✗ {test_id}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            test_id = test.id().split('.')[-1]
            print(f"  ⚠ {test_id}")
    
    # 返回退出码
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    # 确保在项目根目录运行
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 运行测试
    sys.exit(run_tests())