"""
ReadingTypeID Agent主类单元测试
"""

import pytest
from unittest.mock import patch, MagicMock


class TestReadingTypeIDAgent:
    """ReadingTypeID Agent测试类"""

    @pytest.fixture
    def agent_class(self):
        """Agent类夹具 - 待实现"""
        # 这里将导入实际的Agent类
        # from reading_type_agent import ReadingTypeIDAgent
        # return ReadingTypeIDAgent
        return MagicMock  # 临时mock，实际开发时替换

    @pytest.fixture
    def agent(self, agent_class):
        """Agent实例夹具"""
        return agent_class()

    @pytest.mark.unit
    def test_agent_initialization(self, agent_class):
        """测试Agent初始化"""
        agent = agent_class()
        assert agent is not None
        # 验证各个组件是否正确初始化
        assert hasattr(agent, 'database')
        assert hasattr(agent, 'dictionary')
        assert hasattr(agent, 'semantic_parser')

    @pytest.mark.unit
    def test_search_exact_match(self, agent):
        """测试精确匹配搜索"""
        query = "有功电能"
        result = agent.search_reading_type(query)
        
        assert result is not None
        assert "matches" in result
        assert "exact_match" in result

    @pytest.mark.unit
    def test_search_partial_match(self, agent):
        """测试部分匹配搜索"""
        query = "功率"
        result = agent.search_reading_type(query)
        
        assert result is not None
        assert "matches" in result
        assert len(result["matches"]) > 0

    @pytest.mark.unit
    def test_search_no_match(self, agent):
        """测试无匹配搜索"""
        query = "不存在的测量项"
        result = agent.search_reading_type(query)
        
        assert result is not None
        assert len(result["matches"]) == 0

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_new_reading_type(self, agent):
        """测试生成新的ReadingType"""
        user_input = "B相无功功率"
        result = agent.generate_reading_type(user_input)
        
        assert result is not None
        assert "reading_type_id" in result
        assert "fields" in result
        assert "confidence" in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_complex_reading_type(self, agent):
        """测试生成复杂ReadingType"""
        user_input = "三相15分钟最大有功功率"
        result = agent.generate_reading_type(user_input)
        
        assert result is not None
        assert result["fields"]["phase"] == 896  # 三相
        assert result["fields"]["measurePeriod"] == 2  # 15分钟
        assert result["fields"]["aggregate"] == 8  # 最大值

    @pytest.mark.unit
    def test_validate_reading_type_id(self, agent):
        """测试ReadingTypeID验证"""
        valid_id = "0.0.2.12.61.1.7.58.128.0.0.0.0.0.0.0"
        invalid_id = "invalid.format"
        
        assert agent.validate_reading_type_id(valid_id) is True
        assert agent.validate_reading_type_id(invalid_id) is False

    @pytest.mark.unit
    def test_add_reading_type(self, agent):
        """测试添加ReadingType"""
        reading_type_data = {
            "name": "测试电流",
            "description": "测试用电流量测",
            "reading_type_id": "0.0.0.5.5.1.0.0.128.0.0.0.0.0.0.0",
            "category": "表计"
        }
        
        result = agent.add_reading_type(reading_type_data)
        assert result is True

    @pytest.mark.unit
    def test_export_data(self, agent, temp_dir):
        """测试数据导出"""
        import os
        output_file = os.path.join(temp_dir, "exported_data.csv")
        
        result = agent.export_data(output_file)
        assert result is True
        assert os.path.exists(output_file)

    @pytest.mark.unit
    def test_export_with_filters(self, agent, temp_dir):
        """测试带筛选条件的数据导出"""
        import os
        output_file = os.path.join(temp_dir, "filtered_export.csv")
        filters = {"category": "表计"}
        
        result = agent.export_data(output_file, filters=filters)
        assert result is True

    @pytest.mark.unit
    def test_get_statistics(self, agent):
        """测试获取统计信息"""
        stats = agent.get_statistics()
        
        assert isinstance(stats, dict)
        assert "total_reading_types" in stats
        assert "categories" in stats
        assert "dictionary_stats" in stats

    @pytest.mark.unit
    def test_query_dictionary(self, agent):
        """测试字典查询"""
        field_name = "measurementKind"
        result = agent.query_dictionary(field_name)
        
        assert result is not None
        assert isinstance(result, dict)
        assert len(result) > 0

    @pytest.mark.unit
    def test_extend_dictionary(self, agent):
        """测试字典扩展"""
        extension_data = {
            "field_name": "commodity",
            "value": "10",
            "name": "风能",
            "description": "风能相关量测"
        }
        
        result = agent.extend_dictionary(extension_data)
        assert result is True

    @pytest.mark.unit
    def test_handle_chat_message(self, agent):
        """测试聊天消息处理"""
        # 测试搜索请求
        search_message = "查找有功功率的编码"
        result = agent.handle_chat_message(search_message)
        
        assert result is not None
        assert "type" in result
        assert result["type"] in ["search_result", "generation_suggestion", "error"]

    @pytest.mark.unit
    def test_handle_generation_request(self, agent):
        """测试生成请求处理"""
        generation_message = "为三相有功功率生成编码"
        result = agent.handle_chat_message(generation_message)
        
        assert result is not None
        assert result["type"] == "generation_suggestion"

    @pytest.mark.unit
    def test_handle_help_request(self, agent):
        """测试帮助请求处理"""
        help_message = "帮助"
        result = agent.handle_chat_message(help_message)
        
        assert result is not None
        assert result["type"] == "help"
        assert "content" in result

    @pytest.mark.unit
    def test_error_handling(self, agent):
        """测试错误处理"""
        # 模拟数据库错误
        with patch.object(agent, 'database', side_effect=Exception("Database Error")):
            result = agent.search_reading_type("测试查询")
            
            assert result is not None
            assert "error" in result

    @pytest.mark.unit
    def test_operation_history_logging(self, agent):
        """测试操作历史记录"""
        query = "有功功率"
        
        # 执行搜索操作
        agent.search_reading_type(query)
        
        # 检查历史记录
        history = agent.get_operation_history()
        assert len(history) > 0
        assert history[-1]["operation"] == "search"
        assert history[-1]["query"] == query

    @pytest.mark.unit
    def test_confidence_thresholds(self, agent):
        """测试置信度阈值处理"""
        # 低置信度的解析结果应该要求用户确认
        with patch.object(agent.semantic_parser, 'parse', return_value={"confidence": 0.3}):
            result = agent.generate_reading_type("模糊的输入")
            
            assert result["requires_confirmation"] is True

    @pytest.mark.unit
    def test_batch_operations(self, agent):
        """测试批量操作"""
        queries = ["有功功率", "无功功率", "A相电压"]
        results = agent.batch_search(queries)
        
        assert isinstance(results, list)
        assert len(results) == len(queries)

    @pytest.mark.unit
    def test_context_management(self, agent):
        """测试上下文管理"""
        # 设置上下文
        agent.set_context("domain", "电力")
        
        # 验证上下文影响解析结果
        result = agent.generate_reading_type("功率")
        assert result["fields"]["commodity"] == 1  # 电力

    @pytest.mark.unit
    def test_backup_and_restore(self, agent, temp_dir):
        """测试备份和恢复功能"""
        import os
        backup_dir = temp_dir
        
        # 创建备份
        backup_result = agent.create_backup(backup_dir)
        assert backup_result is True
        
        # 验证备份文件存在
        assert os.path.exists(os.path.join(backup_dir, "reading_types_backup.csv"))
        assert os.path.exists(os.path.join(backup_dir, "dictionaries_backup.xml"))

    @pytest.mark.unit
    def test_data_validation(self, agent):
        """测试数据验证"""
        # 测试有效数据
        valid_data = {
            "name": "有效测量",
            "reading_type_id": "0.0.0.12.61.1.0.0.128.0.0.0.0.0.0.0",
            "category": "表计"
        }
        assert agent.validate_reading_type_data(valid_data) is True
        
        # 测试无效数据
        invalid_data = {
            "name": "",  # 空名称
            "reading_type_id": "invalid.format",
            "category": "未知类别"
        }
        assert agent.validate_reading_type_data(invalid_data) is False

    @pytest.mark.unit
    def test_performance_monitoring(self, agent):
        """测试性能监控"""
        # 执行一些操作
        agent.search_reading_type("测试查询")
        agent.generate_reading_type("测试生成")
        
        # 获取性能统计
        perf_stats = agent.get_performance_stats()
        
        assert isinstance(perf_stats, dict)
        assert "search_avg_time" in perf_stats
        assert "generation_avg_time" in perf_stats 