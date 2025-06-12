"""
ReadingTypeID Agent集成测试
测试完整的工作流程和组件间协作
"""

import pytest
import os
import pandas as pd
import time
import threading
from unittest.mock import patch, MagicMock


class TestReadingTypeIDAgentIntegration:
    """ReadingTypeID Agent集成测试类"""

    @pytest.fixture
    def agent_class(self):
        """完整Agent类夹具 - 待实现"""
        # 这里将导入实际的完整Agent类
        # from reading_type_agent import ReadingTypeIDAgent
        # return ReadingTypeIDAgent
        return MagicMock  # 临时mock，实际开发时替换

    @pytest.fixture
    def full_agent(self, agent_class, sample_csv_file, sample_dictionary_xml_file):
        """完整配置的Agent实例"""
        agent = agent_class(
            csv_file=sample_csv_file,
            xml_file=sample_dictionary_xml_file
        )
        return agent

    @pytest.mark.integration
    def test_end_to_end_search_workflow(self, full_agent):
        """测试端到端搜索工作流"""
        # 1. 用户输入查询
        user_query = "有功电能"
        
        # 2. Agent处理查询
        result = full_agent.handle_chat_message(user_query)
        
        # 3. 验证返回结果
        assert result is not None
        assert result["type"] == "search_result"
        assert len(result["matches"]) > 0
        
        # 4. 验证操作被记录
        history = full_agent.get_operation_history()
        assert len(history) > 0
        assert history[-1]["operation"] == "search"

    @pytest.mark.integration
    def test_end_to_end_generation_workflow(self, full_agent):
        """测试端到端生成工作流"""
        # 1. 用户请求生成新编码
        user_input = "三相15分钟平均有功功率"
        
        # 2. Agent解析并生成
        result = full_agent.handle_chat_message(f"为{user_input}生成编码")
        
        # 3. 验证生成结果
        assert result is not None
        assert result["type"] == "generation_suggestion"
        assert "reading_type_id" in result
        assert "fields" in result
        
        # 4. 用户确认添加
        confirm_result = full_agent.confirm_generation(result["generation_id"])
        assert confirm_result is True
        
        # 5. 验证编码已添加到数据库
        search_result = full_agent.search_reading_type(user_input)
        assert len(search_result["matches"]) > 0

    @pytest.mark.integration
    def test_dictionary_extension_workflow(self, full_agent):
        """测试字典扩展工作流"""
        # 1. 检查原始字典状态
        original_commodity_values = full_agent.query_dictionary("commodity")
        original_count = len(original_commodity_values)
        
        # 2. 扩展字典
        extension_data = {
            "field_name": "commodity",
            "value": "10",
            "name": "风能",
            "description": "风能相关量测"
        }
        
        extend_result = full_agent.extend_dictionary(extension_data)
        assert extend_result is True
        
        # 3. 验证字典已扩展
        updated_commodity_values = full_agent.query_dictionary("commodity")
        assert len(updated_commodity_values) == original_count + 1
        assert "10" in updated_commodity_values
        
        # 4. 使用新字典值生成编码
        result = full_agent.generate_reading_type("风能功率测量")
        assert result["fields"]["commodity"] == 10

    @pytest.mark.integration
    def test_export_import_workflow(self, full_agent, temp_dir):
        """测试导出导入工作流"""
        # 1. 导出当前数据
        export_file = os.path.join(temp_dir, "export_test.csv")
        export_result = full_agent.export_data(export_file)
        assert export_result is True
        assert os.path.exists(export_file)
        
        # 2. 验证导出的数据格式
        exported_df = pd.read_csv(export_file, encoding='utf-8-sig')
        assert len(exported_df) > 0
        assert "reading_type_id" in exported_df.columns
        
        # 3. 添加新数据
        new_data = {
            "name": "导出测试",
            "description": "用于测试导出导入的数据",
            "reading_type_id": "0.0.0.1.1.1.0.0.1.0.0.0.0.0.0.0",
            "category": "测试"
        }
        full_agent.add_reading_type(new_data)
        
        # 4. 再次导出，验证新数据包含在内
        export_file2 = os.path.join(temp_dir, "export_test2.csv")
        full_agent.export_data(export_file2)
        
        exported_df2 = pd.read_csv(export_file2, encoding='utf-8-sig')
        assert len(exported_df2) > len(exported_df)

    @pytest.mark.integration
    @pytest.mark.ai
    def test_ai_fallback_workflow(self, full_agent):
        """测试AI服务失败时的后备机制"""
        # 1. 模拟AI服务不可用
        with patch.object(full_agent.semantic_parser, 'call_ai_api', side_effect=Exception("AI Service Down")):
            
            # 2. 尝试生成编码
            result = full_agent.generate_reading_type("有功功率")
            
            # 3. 验证后备机制生效
            assert result is not None
            assert "reading_type_id" in result
            assert result.get("fallback_used", False) is True 