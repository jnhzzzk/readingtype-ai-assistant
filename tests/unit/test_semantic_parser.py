"""
AI语义解析模块单元测试
"""

import pytest
from unittest.mock import patch, MagicMock


class TestSemanticParser:
    """语义解析器测试类"""

    @pytest.fixture
    def parser_class(self):
        """语义解析器类夹具 - 待实现"""
        # 这里将导入实际的语义解析器类
        # from reading_type_agent.semantic_parser import SemanticParser
        # return SemanticParser
        return MagicMock  # 临时mock，实际开发时替换

    @pytest.fixture
    def semantic_parser(self, parser_class):
        """语义解析器实例夹具"""
        return parser_class()

    @pytest.mark.unit
    @pytest.mark.ai
    def test_parse_simple_power_measurement(self, semantic_parser):
        """测试解析简单功率测量"""
        user_input = "有功功率"
        result = semantic_parser.parse(user_input)
        
        # 期望的解析结果
        expected = {
            "commodity": 1,  # 电力
            "measurementKind": 12,  # 功率
            "uom": 61,  # W
            "confidence": 0.9
        }
        
        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.unit
    @pytest.mark.ai
    def test_parse_phase_specific_measurement(self, semantic_parser):
        """测试解析特定相位测量"""
        user_input = "A相电压"
        result = semantic_parser.parse(user_input)
        
        # 期望包含相位信息
        expected_fields = ["commodity", "measurementKind", "phase"]
        assert result is not None
        for field in expected_fields:
            assert field in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_parse_time_period_measurement(self, semantic_parser):
        """测试解析包含时间周期的测量"""
        user_input = "15分钟有功电能"
        result = semantic_parser.parse(user_input)
        
        # 期望包含时间周期信息
        assert result is not None
        assert "measurePeriod" in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_parse_aggregation_measurement(self, semantic_parser):
        """测试解析包含聚合方式的测量"""
        user_input = "最大有功功率"
        result = semantic_parser.parse(user_input)
        
        # 期望包含聚合方式信息
        assert result is not None
        assert "aggregate" in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_parse_complex_measurement(self, semantic_parser):
        """测试解析复杂测量描述"""
        user_input = "三相15分钟平均有功功率"
        result = semantic_parser.parse(user_input)
        
        # 期望包含多个字段
        expected_fields = ["commodity", "measurementKind", "phase", "measurePeriod", "aggregate"]
        assert result is not None
        for field in expected_fields:
            assert field in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_parse_ambiguous_input(self, semantic_parser):
        """测试解析模糊输入"""
        user_input = "电能"  # 可能是有功电能或无功电能
        result = semantic_parser.parse(user_input)
        
        # 应该返回多个可能的解析结果或要求用户澄清
        assert result is not None
        assert "alternatives" in result or "clarification_needed" in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_parse_invalid_input(self, semantic_parser):
        """测试解析无效输入"""
        user_input = "不相关的内容"
        result = semantic_parser.parse(user_input)
        
        # 应该返回错误或空结果
        assert result is None or "error" in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_extract_keywords(self, semantic_parser):
        """测试关键词提取"""
        user_input = "三相有功功率测量"
        keywords = semantic_parser.extract_keywords(user_input)
        
        expected_keywords = ["三相", "有功", "功率", "测量"]
        assert isinstance(keywords, list)
        assert len(keywords) > 0

    @pytest.mark.unit
    @pytest.mark.ai
    def test_map_keywords_to_fields(self, semantic_parser):
        """测试关键词到字段的映射"""
        keywords = ["有功", "功率", "A相"]
        field_mapping = semantic_parser.map_keywords_to_fields(keywords)
        
        assert isinstance(field_mapping, dict)
        assert "measurementKind" in field_mapping
        assert "phase" in field_mapping

    @pytest.mark.unit
    @pytest.mark.ai
    def test_validate_field_combination(self, semantic_parser):
        """测试字段组合验证"""
        valid_combination = {
            "commodity": 1,
            "measurementKind": 12,
            "uom": 61
        }
        
        invalid_combination = {
            "commodity": 1,
            "measurementKind": 12,
            "uom": 999  # 无效的单位
        }
        
        assert semantic_parser.validate_field_combination(valid_combination) is True
        assert semantic_parser.validate_field_combination(invalid_combination) is False

    @pytest.mark.unit
    @pytest.mark.ai
    def test_generate_reading_type_id(self, semantic_parser):
        """测试ReadingTypeID生成"""
        fields = {
            "macroPeriod": 0,
            "aggregate": 0,
            "measurePeriod": 2,
            "commodity": 1,
            "measurementKind": 12,
            "uom": 61,
            "phase": 128
        }
        
        reading_type_id = semantic_parser.generate_reading_type_id(fields)
        
        assert isinstance(reading_type_id, str)
        assert reading_type_id.count('.') == 15  # 16个字段，15个点分隔符

    @pytest.mark.unit
    @pytest.mark.ai
    def test_confidence_calculation(self, semantic_parser):
        """测试置信度计算"""
        high_confidence_input = "有功功率"  # 明确的输入
        low_confidence_input = "功率"  # 模糊的输入
        
        high_result = semantic_parser.parse(high_confidence_input)
        low_result = semantic_parser.parse(low_confidence_input)
        
        assert high_result["confidence"] > low_result["confidence"]

    @pytest.mark.unit
    @pytest.mark.ai
    @patch('reading_type_agent.semantic_parser.requests.post')
    def test_ai_api_call(self, mock_post, semantic_parser):
        """测试AI API调用"""
        # 模拟AI API响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"commodity": 1, "measurementKind": 12}'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = semantic_parser.call_ai_api("有功功率")
        
        assert result is not None
        assert "commodity" in result

    @pytest.mark.unit
    @pytest.mark.ai
    def test_fallback_parsing(self, semantic_parser):
        """测试后备解析机制"""
        # 当AI API不可用时的后备解析
        with patch.object(semantic_parser, 'call_ai_api', side_effect=Exception("API Error")):
            result = semantic_parser.parse("有功功率")
            
            # 应该使用规则解析作为后备
            assert result is not None

    @pytest.mark.unit
    @pytest.mark.ai
    def test_parse_batch_inputs(self, semantic_parser):
        """测试批量解析"""
        inputs = ["有功功率", "无功功率", "A相电压"]
        results = semantic_parser.parse_batch(inputs)
        
        assert isinstance(results, list)
        assert len(results) == len(inputs)
        assert all(result is not None for result in results)

    @pytest.mark.unit
    @pytest.mark.ai
    def test_learning_from_feedback(self, semantic_parser):
        """测试从用户反馈中学习"""
        user_input = "功率"
        initial_result = semantic_parser.parse(user_input)
        
        # 用户反馈正确的解析应该是有功功率
        feedback = {
            "input": user_input,
            "correct_result": {"commodity": 1, "measurementKind": 12, "uom": 61},
            "user_choice": "有功功率"
        }
        
        semantic_parser.learn_from_feedback(feedback)
        
        # 再次解析相同输入，应该有更高的置信度
        new_result = semantic_parser.parse(user_input)
        assert new_result["confidence"] >= initial_result["confidence"]

    @pytest.mark.unit
    @pytest.mark.ai
    def test_context_awareness(self, semantic_parser):
        """测试上下文感知"""
        # 设置上下文：用户之前查询过电力相关的测量
        semantic_parser.set_context("domain", "电力")
        
        # 模糊输入在电力上下文中应该偏向电力相关解释
        result = semantic_parser.parse("功率")
        
        assert result["commodity"] == 1  # 电力商品类型 