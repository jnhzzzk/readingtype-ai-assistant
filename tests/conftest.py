"""
全局测试夹具和配置
"""

import pytest
import pandas as pd
import tempfile
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List


@pytest.fixture
def temp_dir():
    """临时目录夹具"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_reading_type_data():
    """示例ReadingType数据"""
    return [
        {
            'id': 1,
            'name': '有功电能',
            'description': 'A相有功电能',
            'reading_type_id': '0.0.2.12.61.1.7.58.128.0.0.0.0.0.0.0',
            'field_1': 0, 'field_2': 0, 'field_3': 2, 'field_4': 12,
            'field_5': 61, 'field_6': 1, 'field_7': 7, 'field_8': 58,
            'field_9': 128, 'field_10': 0, 'field_11': 0, 'field_12': 0,
            'field_13': 0, 'field_14': 0, 'field_15': 0, 'field_16': 0,
            'created_at': '2024-01-15 10:30:00',
            'source': 'test',
            'category': '表计'
        },
        {
            'id': 2,
            'name': '无功功率',
            'description': '三相无功功率',
            'reading_type_id': '0.0.0.12.63.1.0.0.896.0.0.0.0.0.0.0',
            'field_1': 0, 'field_2': 0, 'field_3': 0, 'field_4': 12,
            'field_5': 63, 'field_6': 1, 'field_7': 0, 'field_8': 0,
            'field_9': 896, 'field_10': 0, 'field_11': 0, 'field_12': 0,
            'field_13': 0, 'field_14': 0, 'field_15': 0, 'field_16': 0,
            'created_at': '2024-01-15 10:31:00',
            'source': 'test',
            'category': '表计'
        }
    ]


@pytest.fixture
def sample_csv_file(temp_dir, sample_reading_type_data):
    """示例CSV文件"""
    csv_path = os.path.join(temp_dir, 'test_reading_types.csv')
    df = pd.DataFrame(sample_reading_type_data)
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    return csv_path


@pytest.fixture
def sample_dictionary_xml():
    """示例字典XML数据"""
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<ReadingTypeDictionaries version="IEC61968-9-2024" created="2024-01-15 10:30:00">
  <Field name="macroPeriod" chinese_name="宏周期">
    <Item value="0" name="none" description="不适用" is_custom="false"/>
    <Item value="8" name="billingPeriod" description="计费周期" is_custom="false"/>
  </Field>
  <Field name="commodity" chinese_name="商品类型">
    <Item value="1" name="电力" description="电力相关量测" is_custom="false"/>
    <Item value="2" name="天然气" description="天然气相关量测" is_custom="false"/>
  </Field>
  <Field name="measurementKind" chinese_name="测量类型">
    <Item value="12" name="power" description="功率" is_custom="false"/>
    <Item value="7" name="voltage" description="电压" is_custom="false"/>
    <Item value="5" name="current" description="电流" is_custom="false"/>
  </Field>
</ReadingTypeDictionaries>'''
    return xml_content


@pytest.fixture
def sample_dictionary_xml_file(temp_dir, sample_dictionary_xml):
    """示例字典XML文件"""
    xml_path = os.path.join(temp_dir, 'test_dictionaries.xml')
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(sample_dictionary_xml)
    return xml_path


@pytest.fixture
def mock_ai_responses():
    """模拟AI响应数据"""
    return {
        "有功功率": {
            "commodity": 1,
            "measurementKind": 12,
            "uom": 61,
            "phase": 896,
            "description": "三相有功功率"
        },
        "A相电压": {
            "commodity": 1,
            "measurementKind": 7,
            "uom": 29,
            "phase": 128,
            "description": "A相电压有效值"
        }
    }


@pytest.fixture
def operation_history_data():
    """操作历史示例数据"""
    return [
        {
            'id': 1,
            'operation': 'search',
            'query': '有功电能',
            'result': 'found',
            'details': 'Found 1 match',
            'timestamp': '2024-01-15 10:30:00',
            'user': 'test_user'
        },
        {
            'id': 2,
            'operation': 'generate',
            'query': '无功功率',
            'result': 'created',
            'details': 'Generated new ReadingType: 0.0.0.12.63.1.0.0.896.0.0.0.0.0.0.0',
            'timestamp': '2024-01-15 10:31:00',
            'user': 'test_user'
        }
    ] 