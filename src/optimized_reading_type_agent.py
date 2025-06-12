import os
import json
import csv
import datetime
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import re
from typing import Dict, List, Optional, Tuple

from .enhanced_semantic_parser import EnhancedSemanticParser
from .enhanced_dictionary_manager import EnhancedDictionaryManager

# 加载环境变量
load_dotenv()

# 设置DeepSeek API密钥
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class OptimizedReadingTypeAgent:
    """优化版ReadingType智能编码助手"""
    
    def __init__(self):
        self.conversation_history = []
        
        # 使用OpenAI客户端，配置DeepSeek基础URL
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        
        # 数据文件路径
        self.codes_file = "reading_type_codes.csv"
        self.dictionaries_file = "field_dictionaries.csv"
        self.history_file = "operation_history.csv"
        
        # 初始化增强组件
        self.dictionary_manager = EnhancedDictionaryManager(self.dictionaries_file)
        self.semantic_parser = EnhancedSemanticParser(self.dictionary_manager)
        
        # 加载编码库
        self.reading_type_codes = self.load_reading_type_codes()
        
        # ReadingType字段定义
        self.field_names = [
            "macroPeriod", "aggregate", "measurePeriod", "accumulationBehaviour",
            "flowDirection", "commodity", "measurementKind", "harmonic",
            "argumentNumerator", "TOU", "cpp", "tier", "phase", "multiplier", "uom", "currency"
        ]
        
        # 设置可用工具
        self.available_tools = {
            "search_reading_type": self.search_reading_type,
            "generate_reading_type_enhanced": self.generate_reading_type_enhanced,
            "query_dictionary_enhanced": self.query_dictionary_enhanced,
            "smart_dictionary_search": self.smart_dictionary_search,
            "validate_reading_type": self.validate_reading_type,
            "export_data": self.export_data,
            "view_codes_library": self.view_codes_library,
            "get_analysis_report": self.get_analysis_report
        }
        
        # 用户反馈学习
        self.feedback_data = []
    
    def load_reading_type_codes(self):
        """加载ReadingType编码库"""
        try:
            df = pd.read_csv(self.codes_file)
            return df.to_dict('records')
        except FileNotFoundError:
            print(f"警告: 编码库文件 {self.codes_file} 未找到")
            return []
    
    def add_message(self, role, content):
        """添加消息到对话历史"""
        self.conversation_history.append({"role": role, "content": content})
    
    def search_reading_type(self, args):
        """增强版编码搜索"""
        search_term = args.get("name", "").strip()
        
        if not search_term:
            return "❌ 请提供要搜索的量测名称"
        
        # 使用增强的搜索逻辑
        exact_matches = []
        fuzzy_matches = []
        
        # 预处理搜索词
        processed_term = self.semantic_parser._preprocess_text(search_term)
        
        for code in self.reading_type_codes:
            name = code.get('name', '')
            description = code.get('description', '')
            
            # 精确匹配
            if search_term.lower() == name.lower():
                exact_matches.append(code)
            else:
                # 增强的模糊匹配
                score = self._calculate_search_score(processed_term, name, description)
                if score > 0.4:  # 提高阈值
                    fuzzy_matches.append((code, score))
        
        # 构建返回结果
        result = []
        
        if exact_matches:
            result.append("✅ 找到精确匹配:")
            for match in exact_matches:
                result.append(f"📊 名称: {match.get('name', 'N/A')}")
                result.append(f"🔢 ReadingTypeID: {match.get('reading_type_id', 'N/A')}")
                result.append(f"📝 说明: {match.get('description', 'N/A')}")
                result.append(f"🏷️ 类别: {match.get('category', 'N/A')}")
                result.append("---")
        
        if fuzzy_matches and not exact_matches:
            # 按相似度排序
            fuzzy_matches.sort(key=lambda x: x[1], reverse=True)
            result.append("🔍 找到相似的编码:")
            for i, (match, similarity) in enumerate(fuzzy_matches[:5], 1):
                result.append(f"{i}. {match.get('name', 'N/A')} (相似度: {similarity:.1%})")
                result.append(f"   ReadingTypeID: {match.get('reading_type_id', 'N/A')}")
                result.append(f"   说明: {match.get('description', 'N/A')[:80]}...")
        
        if not exact_matches and not fuzzy_matches:
            result.append(f"❌ 未找到与'{search_term}'相关的编码")
            result.append("💡 我可以为您生成新的ReadingTypeID")
            # 自动分析并提供建议
            analysis, confidence = self.semantic_parser.analyze_description_enhanced(search_term)
            if confidence > 0.3:
                result.append("🤖 基于描述的初步分析:")
                result.append(f"   置信度: {confidence:.1%}")
                result.append("   建议使用 '生成编码' 功能获取详细结果")
        
        # 记录操作历史
        self.log_operation(search_term, "search", "\n".join(result))
        
        return "\n".join(result)
    
    def _calculate_search_score(self, search_term: str, name: str, description: str) -> float:
        """计算搜索相关性分数"""
        scores = []
        
        name_lower = name.lower()
        desc_lower = description.lower()
        
        # 1. 直接包含匹配
        if search_term in name_lower:
            scores.append(0.8)
        if search_term in desc_lower:
            scores.append(0.6)
        
        # 2. 关键词匹配
        search_words = search_term.split()
        name_words = name_lower.split()
        desc_words = desc_lower.split()
        
        for word in search_words:
            if len(word) >= 2:
                if word in name_words:
                    scores.append(0.7)
                if word in desc_words:
                    scores.append(0.5)
        
        # 3. 序列匹配
        name_similarity = SequenceMatcher(None, search_term, name_lower).ratio()
        if name_similarity > 0.5:
            scores.append(name_similarity * 0.6)
        
        desc_similarity = SequenceMatcher(None, search_term, desc_lower).ratio()
        if desc_similarity > 0.3:
            scores.append(desc_similarity * 0.4)
        
        return max(scores) if scores else 0.0
    
    def generate_reading_type_enhanced(self, args):
        """增强版ReadingType生成"""
        description = args.get("description", "")
        field_values = args.get("field_values", {})
        
        if not description and not field_values:
            return "❌ 请提供量测描述或字段值"
        
        try:
            if field_values:
                # 直接使用提供的字段值
                analysis = field_values
                confidence = 0.9  # 用户直接提供的值给高置信度
            else:
                # 使用增强的语义分析
                analysis, confidence = self.semantic_parser.analyze_description_enhanced(description)
            
            # 验证字段组合
            field_dict = {}
            for i, field_name in enumerate(self.field_names):
                field_key = f"field_{i+1}"
                if field_key in analysis:
                    field_dict[field_name] = str(analysis[field_key])
            
            is_valid, warnings = self.dictionary_manager.validate_field_combination(field_dict)
            
            # 构建ReadingTypeID
            reading_type_id = self.semantic_parser.build_reading_type_id(analysis)
            
            result = []
            result.append("🤖 增强版AI分析结果:")
            result.append(f"🔢 生成的ReadingTypeID: {reading_type_id}")
            result.append(f"🎯 分析置信度: {confidence:.1%}")
            result.append("")
            
            # 显示字段详情
            result.append("📋 字段解析详情:")
            for i, field_name in enumerate(self.field_names):
                field_key = f"field_{i+1}"
                value = analysis.get(field_key, 0)
                if value != 0:
                    chinese_name = self.dictionary_manager.chinese_field_names.get(field_name, field_name)
                    field_desc = self.dictionary_manager.get_field_description(field_name, str(value))
                    result.append(f"  {chinese_name}: {value} ({field_desc})")
            
            # 显示验证警告
            if warnings:
                result.append("")
                result.append("⚠️ 字段组合建议:")
                for warning in warnings:
                    result.append(f"  • {warning}")
            
            # 显示改进建议
            suggestions = self.semantic_parser.suggest_alternatives(analysis, confidence)
            if suggestions:
                result.append("")
                result.extend(suggestions)
            
            result.append("")
            result.append("✅ 是否采纳此编码？输入'是'确认，'否'取消，或提出修改建议。")
            
            # 记录操作历史
            self.log_operation(description, "generate_enhanced", "\n".join(result))
            
            return "\n".join(result)
            
        except Exception as e:
            return f"❌ 生成编码时发生错误: {str(e)}"
    
    def query_dictionary_enhanced(self, args):
        """增强版字典查询"""
        field_name = args.get("field_name", "").strip()
        search_term = args.get("search_term", "").strip()
        
        if not field_name and not search_term:
            # 显示所有字段概览
            result = ["📚 ReadingType字段字典 (增强版):"]
            stats = self.dictionary_manager.get_field_usage_statistics()
            
            for i, (name, chinese_name) in enumerate(self.dictionary_manager.chinese_field_names.items(), 1):
                field_stats = stats.get(name, {})
                total = field_stats.get('total_values', 0)
                result.append(f"{i:2d}. {name} ({chinese_name}) - {total}个值")
            
            result.append("\n💡 使用方式:")
            result.append("   • '查询字典 [字段名]' - 查看字段所有值")
            result.append("   • '智能搜索 [关键词]' - 跨字段智能搜索")
            return "\n".join(result)
        
        if field_name and not search_term:
            # 查询特定字段
            if field_name not in self.dictionary_manager.field_dictionaries:
                # 尝试字段名建议
                suggestions = self.dictionary_manager.get_field_suggestions(field_name)
                if suggestions:
                    result = [f"❌ 字段 '{field_name}' 不存在，您是否要查询:"]
                    for eng_name, chi_name in suggestions:
                        result.append(f"   • {eng_name} ({chi_name})")
                    return "\n".join(result)
                else:
                    return f"❌ 未找到字段 '{field_name}'"
            
            # 获取字段详细信息
            items = self.dictionary_manager.get_field_options(field_name, limit=30)
            chinese_name = self.dictionary_manager.chinese_field_names.get(field_name, field_name)
            
            result = [f"📖 字段 '{field_name}' ({chinese_name}) 详情:"]
            result.append(f"📊 总计 {len(self.dictionary_manager.field_dictionaries[field_name])} 个值")
            result.append("")
            
            for item in items:
                marker = "🔧" if item.get('is_custom', False) else "📌"
                result.append(f"{marker} {item['value']}: {item['display_name']}")
                if item.get('description'):
                    # 截断长描述
                    desc = str(item['description'])[:80]
                    if len(str(item['description'])) > 80:
                        desc += "..."
                    result.append(f"    📝 {desc}")
            
            if len(self.dictionary_manager.field_dictionaries[field_name]) > 30:
                remaining = len(self.dictionary_manager.field_dictionaries[field_name]) - 30
                result.append(f"\n... 还有 {remaining} 个值，使用搜索功能查找特定值")
            
            return "\n".join(result)
        
        # 如果有搜索词，使用智能搜索
        return self.smart_dictionary_search({"search_term": search_term, "field_name": field_name})
    
    def smart_dictionary_search(self, args):
        """智能字典搜索"""
        search_term = args.get("search_term", "").strip()
        field_name = args.get("field_name", "").strip()
        
        if not search_term:
            return "❌ 请提供搜索关键词"
        
        # 使用增强的搜索功能
        results = self.dictionary_manager.smart_search(
            search_term=search_term,
            field_name=field_name,
            max_results=15,
            threshold=0.3
        )
        
        if not results:
            return f"❌ 未找到与 '{search_term}' 相关的字典项"
        
        result = [f"🔍 智能搜索结果 (关键词: '{search_term}'):"]
        if field_name:
            result[0] += f" 限定字段: {field_name}"
        result.append("")
        
        # 按相似度分组显示
        high_relevance = [r for r in results if r[2] >= 0.8]
        medium_relevance = [r for r in results if 0.5 <= r[2] < 0.8]
        low_relevance = [r for r in results if r[2] < 0.5]
        
        if high_relevance:
            result.append("🎯 高相关度匹配:")
            for fname, item, score in high_relevance:
                chinese_name = self.dictionary_manager.chinese_field_names.get(fname, fname)
                result.append(f"  📌 {fname}({chinese_name}).{item['value']}: {item['display_name']}")
                result.append(f"      相似度: {score:.1%}")
        
        if medium_relevance:
            result.append("\n🔸 中等相关度匹配:")
            for fname, item, score in medium_relevance[:5]:  # 限制显示数量
                chinese_name = self.dictionary_manager.chinese_field_names.get(fname, fname)
                result.append(f"  📋 {fname}({chinese_name}).{item['value']}: {item['display_name']}")
        
        if low_relevance:
            result.append(f"\n🔹 其他可能相关的结果: {len(low_relevance)} 个")
        
        return "\n".join(result)
    
    def validate_reading_type(self, args):
        """验证ReadingType编码"""
        reading_type_id = args.get("reading_type_id", "").strip()
        
        if not reading_type_id:
            return "❌ 请提供ReadingTypeID"
        
        try:
            # 解析ReadingTypeID
            field_values = self.semantic_parser.parse_reading_type_id(reading_type_id)
            
            # 转换为字段名格式
            field_dict = {}
            for i, field_name in enumerate(self.field_names):
                field_key = f"field_{i+1}"
                if field_key in field_values:
                    field_dict[field_name] = str(field_values[field_key])
            
            # 验证字段组合
            is_valid, warnings = self.dictionary_manager.validate_field_combination(field_dict)
            
            result = []
            result.append("🔍 ReadingType编码验证结果:")
            result.append(f"🔢 编码: {reading_type_id}")
            result.append(f"✅ 基本格式: {'有效' if len(reading_type_id.split('-')) == 16 else '无效'}")
            result.append("")
            
            # 显示字段解析
            result.append("📋 字段解析:")
            for field_name, value in field_dict.items():
                if value != '0':
                    chinese_name = self.dictionary_manager.chinese_field_names.get(field_name, field_name)
                    field_desc = self.dictionary_manager.get_field_description(field_name, value)
                    
                    # 获取上下文信息
                    context = self.dictionary_manager.get_value_context(field_name, value)
                    status = "✅" if context else "⚠️"
                    
                    result.append(f"  {status} {chinese_name}: {value} ({field_desc})")
            
            # 显示验证警告
            if warnings:
                result.append("")
                result.append("⚠️ 字段组合建议:")
                for warning in warnings:
                    result.append(f"  • {warning}")
            else:
                result.append("\n✅ 字段组合验证通过")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"❌ 验证时发生错误: {str(e)}"
    
    def get_analysis_report(self, args):
        """获取详细分析报告"""
        description = args.get("description", "")
        
        if not description:
            return "❌ 请提供要分析的描述"
        
        try:
            # 进行增强分析
            analysis, confidence = self.semantic_parser.analyze_description_enhanced(description)
            
            # 生成完整报告
            report = self.semantic_parser.export_analysis_report(description, analysis, confidence)
            
            return report
            
        except Exception as e:
            return f"❌ 生成报告时发生错误: {str(e)}"
    
    def view_codes_library(self, args):
        """查看编码库（保持兼容性）"""
        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 20))
        category = args.get("category", "")
        
        # 筛选数据
        filtered_codes = self.reading_type_codes
        if category:
            filtered_codes = [code for code in filtered_codes 
                            if code.get('category', '').lower() == category.lower()]
        
        total = len(filtered_codes)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_codes = filtered_codes[start_idx:end_idx]
        
        result = [f"📚 编码库 (第{page}页, 共{total}条记录)"]
        if category:
            result[0] += f" - 类别: {category}"
        
        result.append("=" * 50)
        
        for i, code in enumerate(page_codes, start_idx + 1):
            result.append(f"{i:3d}. {code.get('name', 'N/A')}")
            result.append(f"     ID: {code.get('reading_type_id', 'N/A')}")
            result.append(f"     描述: {code.get('description', 'N/A')[:60]}...")
            result.append("")
        
        # 分页信息
        total_pages = (total + per_page - 1) // per_page
        if total_pages > 1:
            result.append(f"📄 第 {page}/{total_pages} 页")
            if page < total_pages:
                result.append("💡 使用 '查看编码库 页码=N' 查看其他页面")
        
        return "\n".join(result)
    
    def export_data(self, args):
        """导出数据（保持兼容性）"""
        data_type = args.get("type", "codes")
        
        if data_type == "dictionary":
            field_name = args.get("field_name", "")
            return self.dictionary_manager.export_enhanced_report(field_name)
        else:
            # 导出编码库
            result = []
            result.append("📊 ReadingType编码库导出报告")
            result.append("=" * 50)
            result.append(f"📅 导出时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            result.append(f"📈 总编码数量: {len(self.reading_type_codes)}")
            result.append("")
            
            # 按类别统计
            categories = {}
            for code in self.reading_type_codes:
                cat = code.get('category', '未分类')
                categories[cat] = categories.get(cat, 0) + 1
            
            result.append("📋 分类统计:")
            for cat, count in sorted(categories.items()):
                result.append(f"  {cat}: {count} 个")
            
            return "\n".join(result)
    
    def log_operation(self, input_text, operation_type, result, user_action="pending"):
        """记录操作历史"""
        try:
            log_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'input': input_text,
                'operation': operation_type,
                'result_length': len(result),
                'user_action': user_action
            }
            
            # 简单的CSV记录
            with open(self.history_file, 'a', newline='', encoding='utf-8') as f:
                if f.tell() == 0:  # 文件为空，写入标题
                    f.write('timestamp,input,operation,result_length,user_action\n')
                f.write(f"{log_entry['timestamp']},{log_entry['input']},{log_entry['operation']},{log_entry['result_length']},{log_entry['user_action']}\n")
        except Exception as e:
            print(f"记录历史失败: {e}")
    
    def add_user_feedback(self, description: str, generated_code: str, 
                         user_rating: int, correct_code: str = ""):
        """添加用户反馈以改进系统"""
        feedback = {
            'timestamp': datetime.datetime.now().isoformat(),
            'description': description,
            'generated_code': generated_code,
            'user_rating': user_rating,  # 1-5 分
            'correct_code': correct_code
        }
        self.feedback_data.append(feedback)
        
        # 如果评分较低，可以用于改进关键词映射
        if user_rating <= 2 and correct_code:
            self._learn_from_feedback(description, correct_code)
    
    def _learn_from_feedback(self, description: str, correct_code: str):
        """从用户反馈中学习（简单的规则更新）"""
        try:
            # 解析正确的编码
            correct_analysis = self.semantic_parser.parse_reading_type_id(correct_code)
            
            # 分析描述中的关键词
            keywords = self.semantic_parser._preprocess_text(description).split()
            
            # 这里可以实现更复杂的学习逻辑
            # 例如更新关键词映射权重等
            print(f"学习反馈: {description} -> {correct_code}")
            
        except Exception as e:
            print(f"学习反馈失败: {e}")
    
    # 保持与原版本的兼容性
    def handle_function_call(self, function_call):
        """处理函数调用"""
        function_name = function_call.get("name")
        function_args = {}
        
        if function_call.get("arguments"):
            try:
                function_args = json.loads(function_call.get("arguments", "{}"))
            except:
                pass
        
        if function_name in self.available_tools:
            function_response = self.available_tools[function_name](function_args)
            
            # 添加函数结果到对话历史
            self.add_message("function", {
                "name": function_name,
                "content": function_response
            })
            
            return function_response
        else:
            return f"错误: 未知的函数 '{function_name}'"
    
    def get_response(self, user_input, stream=True):
        """获取AI回复（保持与原版本兼容）"""
        # 添加用户输入到对话历史
        self.add_message("user", user_input)
        
        try:
            # 工具描述（更新版本）
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "search_reading_type",
                        "description": "搜索现有的ReadingType编码",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "要搜索的量测名称"}
                            },
                            "required": ["name"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "generate_reading_type_enhanced",
                        "description": "使用增强AI算法生成ReadingType编码",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "description": {"type": "string", "description": "量测描述"},
                                "field_values": {"type": "object", "description": "指定的字段值"}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "smart_dictionary_search",
                        "description": "智能字典搜索功能",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "search_term": {"type": "string", "description": "搜索关键词"},
                                "field_name": {"type": "string", "description": "限定字段名(可选)"}
                            },
                            "required": ["search_term"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "validate_reading_type",
                        "description": "验证ReadingType编码的有效性",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "reading_type_id": {"type": "string", "description": "要验证的ReadingTypeID"}
                            },
                            "required": ["reading_type_id"]
                        }
                    }
                }
            ]
            
            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.conversation_history,
                tools=tools,
                tool_choice="auto",
                stream=False
            )
            
            response_message = response.choices[0].message
            
            # 处理工具调用
            if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
                self.add_message("assistant", response_message)
                
                # 处理每个工具调用
                for tool_call in response_message.tool_calls:
                    function_info = {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                    tool_result = self.handle_function_call(function_info)
                    print(f"🔧 使用工具: {tool_call.function.name}")
                
                # 再次调用API获取最终回复
                if stream:
                    print("\n🤖 AI助手: ", end="", flush=True)
                    second_response = self.client.chat.completions.create(
                        model="deepseek-chat",
                        messages=self.conversation_history,
                        stream=True
                    )
                    
                    full_response = ""
                    for chunk in second_response:
                        if chunk.choices and len(chunk.choices) > 0:
                            content = chunk.choices[0].delta.content
                            if content:
                                print(content, end="", flush=True)
                                full_response += content
                    
                    print()
                    ai_response = full_response
                else:
                    second_response = self.client.chat.completions.create(
                        model="deepseek-chat",
                        messages=self.conversation_history,
                        stream=False
                    )
                    ai_response = second_response.choices[0].message.content
                    print(f"\n🤖 AI助手: {ai_response}")
                
                self.add_message("assistant", ai_response)
            else:
                # 没有工具调用，直接返回回复
                ai_response = response_message.content
                print(f"\n🤖 AI助手: {ai_response}")
                self.add_message("assistant", ai_response)
            
            return ai_response
            
        except Exception as e:
            error_msg = f"❌ 获取回复时发生错误: {str(e)}"
            print(error_msg)
            return error_msg
    
    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = [] 