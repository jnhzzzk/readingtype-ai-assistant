"""
字典管理模块单元测试
"""

import pytest
import xml.etree.ElementTree as ET
import os
from unittest.mock import patch, MagicMock


class TestDictionaryManager:
    """字典管理器测试类"""

    @pytest.fixture
    def dictionary_class(self):
        """字典管理类夹具 - 待实现"""
        # 这里将导入实际的字典管理类
        # from reading_type_agent.dictionary import DictionaryManager
        # return DictionaryManager
        return MagicMock  # 临时mock，实际开发时替换

    @pytest.fixture
    def dict_manager(self, dictionary_class, sample_dictionary_xml_file):
        """字典管理器实例夹具"""
        return dictionary_class(xml_file=sample_dictionary_xml_file)

    @pytest.mark.unit
    @pytest.mark.database
    def test_load_xml_dictionary(self, sample_dictionary_xml_file, dictionary_class):
        """测试加载XML字典文件"""
        manager = dictionary_class(xml_file=sample_dictionary_xml_file)
        # 应该成功加载字典
        assert manager is not None

    @pytest.mark.unit
    @pytest.mark.database
    def test_load_invalid_xml(self, temp_dir, dictionary_class):
        """测试加载无效XML文件"""
        invalid_xml_path = os.path.join(temp_dir, 'invalid.xml')
        with open(invalid_xml_path, 'w') as f:
            f.write("invalid xml content")
        
        # 应该抛出异常
        with pytest.raises(ET.ParseError):
            dictionary_class(xml_file=invalid_xml_path)

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_field_values(self, dict_manager):
        """测试获取字段的所有值"""
        values = dict_manager.get_field_values("measurementKind")
        # 应该返回测量类型的所有值
        assert isinstance(values, dict)
        assert len(values) > 0

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_field_description(self, dict_manager):
        """测试获取字段值的描述"""
        description = dict_manager.get_field_description("measurementKind", "12")
        # 应该返回对应的描述
        assert description == "功率"

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_nonexistent_field(self, dict_manager):
        """测试获取不存在的字段"""
        values = dict_manager.get_field_values("nonexistent_field")
        # 应该返回空字典或None
        assert values is None or len(values) == 0

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_by_description(self, dict_manager):
        """测试根据描述搜索字段值"""
        results = dict_manager.search_by_description("功率")
        # 应该返回包含"功率"的字段和值
        assert isinstance(results, list)
        assert len(results) > 0

    @pytest.mark.unit
    @pytest.mark.database
    def test_add_custom_field_value(self, dict_manager):
        """测试添加自定义字段值"""
        result = dict_manager.add_custom_value(
            field_name="commodity",
            value="10",
            name="风能",
            description="风能相关量测"
        )
        # 应该成功添加自定义值
        assert result is True

    @pytest.mark.unit
    @pytest.mark.database
    def test_add_duplicate_field_value(self, dict_manager):
        """测试添加重复的字段值"""
        # 应该抛出异常或返回错误
        with pytest.raises(ValueError):
            dict_manager.add_custom_value(
                field_name="commodity",
                value="1",  # 已存在的值
                name="重复",
                description="重复的值"
            )

    @pytest.mark.unit
    @pytest.mark.database
    def test_remove_custom_field_value(self, dict_manager):
        """测试删除自定义字段值"""
        # 首先添加一个自定义值
        dict_manager.add_custom_value(
            field_name="commodity",
            value="99",
            name="测试值",
            description="用于测试删除的值"
        )
        
        # 然后删除它
        result = dict_manager.remove_custom_value("commodity", "99")
        assert result is True

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_all_fields(self, dict_manager):
        """测试获取所有字段"""
        fields = dict_manager.get_all_fields()
        # 应该返回所有字段的列表
        assert isinstance(fields, list)
        assert len(fields) > 0
        assert "measurementKind" in fields

    @pytest.mark.unit
    @pytest.mark.database
    def test_validate_field_value(self, dict_manager):
        """测试验证字段值的有效性"""
        # 测试有效值
        assert dict_manager.validate_field_value("measurementKind", "12") is True
        
        # 测试无效值
        assert dict_manager.validate_field_value("measurementKind", "999") is False

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_field_chinese_name(self, dict_manager):
        """测试获取字段的中文名称"""
        chinese_name = dict_manager.get_field_chinese_name("measurementKind")
        assert chinese_name == "测量类型"

    @pytest.mark.unit
    @pytest.mark.database
    def test_export_to_csv(self, dict_manager, temp_dir):
        """测试导出字典到CSV格式"""
        csv_file = os.path.join(temp_dir, "exported_dict.csv")
        result = dict_manager.export_to_csv(csv_file)
        
        assert result is True
        assert os.path.exists(csv_file)

    @pytest.mark.unit
    @pytest.mark.database
    def test_save_xml(self, dict_manager, temp_dir):
        """测试保存字典到XML文件"""
        output_xml = os.path.join(temp_dir, "output_dict.xml")
        result = dict_manager.save_xml(output_xml)
        
        assert result is True
        assert os.path.exists(output_xml)

    @pytest.mark.unit
    @pytest.mark.database
    def test_backup_and_restore_dictionary(self, dict_manager, temp_dir):
        """测试字典备份和恢复"""
        backup_file = os.path.join(temp_dir, "dict_backup.xml")
        
        # 创建备份
        backup_result = dict_manager.backup(backup_file)
        assert backup_result is True
        
        # 恢复备份
        restore_result = dict_manager.restore(backup_file)
        assert restore_result is True

    @pytest.mark.unit
    @pytest.mark.database
    def test_get_statistics(self, dict_manager):
        """测试获取字典统计信息"""
        stats = dict_manager.get_statistics()
        
        assert isinstance(stats, dict)
        assert 'total_fields' in stats
        assert 'total_values' in stats
        assert 'custom_values' in stats

    @pytest.mark.unit
    @pytest.mark.database
    def test_merge_dictionaries(self, dict_manager, temp_dir):
        """测试合并多个字典文件"""
        # 创建另一个字典文件
        other_xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<ReadingTypeDictionaries version="IEC61968-9-2024">
  <Field name="newField" chinese_name="新字段">
    <Item value="1" name="新值" description="新的测试值" is_custom="true"/>
  </Field>
</ReadingTypeDictionaries>'''
        
        other_xml_path = os.path.join(temp_dir, 'other_dict.xml')
        with open(other_xml_path, 'w', encoding='utf-8') as f:
            f.write(other_xml_content)
        
        # 合并字典
        result = dict_manager.merge_from_file(other_xml_path)
        assert result is True

    @pytest.mark.unit
    @pytest.mark.database
    def test_search_fuzzy_match(self, dict_manager):
        """测试模糊匹配搜索"""
        results = dict_manager.fuzzy_search("功")
        # 应该返回包含"功"字的所有相关字段值
        assert isinstance(results, list)
        assert len(results) > 0 