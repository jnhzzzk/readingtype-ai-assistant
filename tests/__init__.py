"""
ReadingTypeID Agent 测试套件
基于TDD开发模式的完整测试用例
"""

import os
import sys
import pytest

# 添加项目根目录到路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# 测试配置
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TEST_FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

# 确保测试目录存在
os.makedirs(TEST_DATA_DIR, exist_ok=True)
os.makedirs(TEST_FIXTURES_DIR, exist_ok=True) 