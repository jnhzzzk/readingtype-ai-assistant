import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, List, Optional

from reading_type_database import ReadingTypeDatabase
from dictionary_manager import DictionaryManager
from semantic_parser import SemanticParser

# 加载环境变量
load_dotenv()

# 设置DeepSeek API密钥
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class ReadingTypeAgent:
    """ReadingType智能编码助手"""
    
    def __init__(self):
        self.conversation_history = []
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        
        # 初始化核心模块
        self.database = ReadingTypeDatabase()
        self.dictionary = DictionaryManager()
        self.parser = SemanticParser()
        
        # 可用工具
        self.available_tools = {
            "search_reading_type": self._search_reading_type,
            "generate_reading_type": self._generate_reading_type,
            "query_dictionary": self._query_dictionary,
            "view_codes_library": self._view_codes_library,
            "filter_codes": self._filter_codes,
            "add_to_library": self._add_to_library,
            "export_data": self._export_data,
            "get_statistics": self._get_statistics
        }
    
    def add_message(self, role: str, content):
        """添加消息到对话历史"""
        self.conversation_history.append({"role": role, "content": content})
    
    def _search_reading_type(self, args: Dict) -> str:
        """搜索ReadingType编码"""
        search_term = args.get("name", "").strip()
        
        if not search_term:
            return "❌ 请提供要搜索的量测名称"
        
        exact_matches, fuzzy_matches = self.database.search_codes(search_term)
        
        result = []
        
        if exact_matches:
            result.append("✅ 找到精确匹配:")
            for match in exact_matches:
                result.append(f"📊 名称: {match.get('name', 'N/A')}")
                result.append(f"🔢 ReadingTypeID: {match.get('reading_type_id', 'N/A')}")
                result.append(f"📝 说明: {match.get('description', 'N/A')}")
                result.append(f"🏷️ 类别: {match.get('category', 'N/A')}")
                result.append(f"⏰ 创建时间: {match.get('created_at', 'N/A')}")
                result.append("---")
        
        if fuzzy_matches and not exact_matches:
            result.append("🔍 找到相似的编码:")
            for i, (match, similarity) in enumerate(fuzzy_matches[:5], 1):
                result.append(f"{i}. {match.get('name', 'N/A')} (相似度: {similarity:.2f})")
                result.append(f"   ReadingTypeID: {match.get('reading_type_id', 'N/A')}")
                result.append(f"   说明: {match.get('description', 'N/A')}")
            result.append("\n❓ 以上是否有您需要的编码？如果没有，我可以为您生成新的编码。")
        
        if not exact_matches and not fuzzy_matches:
            result.append(f"❌ 未找到与'{search_term}'相关的编码")
            result.append("💡 我可以为您生成新的ReadingTypeID，请告诉我更多详细信息:")
            result.append("- 设备类型 (如: 电表、储能、气象)")
            result.append("- 测量内容 (如: 电压、电流、功率、能量)")
            result.append("- 特殊要求 (如: 相位、时间周期)")
        
        return "\n".join(result)
    
    def _generate_reading_type(self, args: Dict) -> str:
        """生成ReadingType编码"""
        description = args.get("description", "")
        field_values = args.get("field_values", {})
        
        if not description and not field_values:
            return "❌ 请提供量测描述或字段值"
        
        try:
            if field_values:
                # 直接使用提供的字段值
                reading_type_id = self.parser.build_reading_type_id(field_values)
                result = ["🤖 AI生成结果:", f"🔢 ReadingTypeID: {reading_type_id}"]
                
                # 显示字段详情
                result.append("\n📋 字段详情:")
                for i, field_name in enumerate(self.parser.field_names):
                    value = field_values.get(f"field_{i+1}", 0)
                    field_info = self.dictionary.get_field_description(field_name, str(value))
                    result.append(f"  {i+1:2d}. {field_name}: {value} ({field_info})")
            else:
                # 基于描述分析生成
                analysis = self.parser.analyze_measurement_description(description)
                reading_type_id = self.parser.build_reading_type_id(analysis)
                
                result = ["🤖 AI分析结果:", f"📝 输入描述: {description}"]
                
                # 显示识别要素
                info = self.parser.extract_measurement_info(description)
                if any(info.values()):
                    result.append("\n🔍 识别要素:")
                    for key, values in info.items():
                        if values:
                            chinese_key = {
                                'device_types': '设备类型',
                                'measurement_kinds': '测量类型',
                                'flow_directions': '流向',
                                'phases': '相位',
                                'time_periods': '时间周期',
                                'units': '单位',
                                'behaviors': '行为'
                            }.get(key, key)
                            result.append(f"  - {chinese_key}: {', '.join(values)}")
                
                # 显示字段映射
                result.append(f"\n💡 建议编码: {reading_type_id}")
                result.append("\n📋 字段映射:")
                for i, field_name in enumerate(self.parser.field_names):
                    value = analysis.get(f"field_{i+1}", 0)
                    if value != 0:  # 只显示非零字段
                        field_info = self.dictionary.get_field_description(field_name, str(value))
                        chinese_name = self.dictionary.get_field_chinese_name(field_name)
                        result.append(f"  {i+1:2d}. {chinese_name}({field_name}): {value} = {field_info}")
                
                # 验证字段组合
                is_valid, errors = self.parser.validate_field_combination(analysis)
                if not is_valid:
                    result.append("\n⚠️ 字段组合问题:")
                    for error in errors:
                        result.append(f"  - {error}")
                
                # 建议缺失字段
                suggestions = self.parser.suggest_missing_fields(analysis, description)
                if suggestions:
                    result.append("\n💭 完善建议:")
                    for suggestion in suggestions:
                        result.append(f"  - {suggestion}")
            
            result.append("\n✅ 是否采纳此编码？输入'是'确认，'否'取消，或提出修改建议。")
            return "\n".join(result)
            
        except Exception as e:
            return f"❌ 生成编码时发生错误: {str(e)}"
    
    def _query_dictionary(self, args: Dict) -> str:
        """查询字典信息"""
        field_name = args.get("field_name", "").strip()
        
        if not field_name:
            # 显示所有字段
            result = ["📚 ReadingType字段字典:"]
            fields = self.dictionary.get_all_fields()
            for i, (name, chinese_name) in enumerate(fields, 1):
                result.append(f"{i:2d}. {name} ({chinese_name})")
            result.append("\n💡 使用 '查询字典 [字段名]' 查看具体字段的可选值")
            return "\n".join(result)
        
        # 查询具体字段
        options = self.dictionary.get_field_options(field_name, limit=30)
        if options:
            result = [f"📖 字段 '{field_name}' 的可选值:"]
            chinese_name = self.dictionary.get_field_chinese_name(field_name)
            result.append(f"({chinese_name})")
            result.append("")
            
            for item in options:
                result.append(f"  {item['value']}: {item['display_name']}")
                if item.get('description') and len(str(item['description'])) < 100:
                    result.append(f"    {item['description']}")
            
            if len(self.dictionary.get_field_options(field_name, limit=1000)) > 30:
                result.append(f"\n... 显示前30个值，完整列表可导出查看")
            
            return "\n".join(result)
        else:
            return f"❌ 未找到字段 '{field_name}' 或该字段没有预定义值"
    
    def _view_codes_library(self, args: Dict) -> str:
        """查看编码库"""
        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 15))
        category = args.get("category", "")
        
        # 筛选数据
        if category:
            filtered_codes = self.database.filter_codes(category=category)
        else:
            filtered_codes = self.database.reading_type_codes
        
        total = len(filtered_codes)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_codes = filtered_codes[start_idx:end_idx]
        
        result = [f"📚 编码库 (第{page}页, 共{total}条记录)"]
        if category:
            result[0] += f" - 类别: {category}"
        
        result.append("=" * 60)
        
        for i, code in enumerate(page_codes, start_idx + 1):
            result.append(f"{i:3d}. {code.get('name', 'N/A')}")
            result.append(f"     📋 ID: {code.get('reading_type_id', 'N/A')}")
            result.append(f"     📝 说明: {code.get('description', 'N/A')[:50]}...")
            result.append(f"     🏷️ 类别: {code.get('category', 'N/A')} | 📅 {code.get('created_at', 'N/A')}")
            result.append("")
        
        # 分页信息
        total_pages = (total + per_page - 1) // per_page
        if total_pages > 1:
            result.append(f"📄 第{page}/{total_pages}页")
            if page < total_pages:
                result.append("💡 可以查看下一页或指定页码")
        
        return "\n".join(result)
    
    def _filter_codes(self, args: Dict) -> str:
        """筛选编码"""
        category = args.get("category", "")
        measurement_kind = args.get("measurement_kind", "")
        
        filtered_codes = self.database.filter_codes(category, measurement_kind)
        
        if not filtered_codes:
            return f"❌ 未找到符合条件的编码 (类别: {category}, 测量类型: {measurement_kind})"
        
        result = [f"🔍 筛选结果 (共{len(filtered_codes)}条):"]
        
        for i, code in enumerate(filtered_codes[:15], 1):  # 限制显示数量
            result.append(f"{i:2d}. {code.get('name', 'N/A')}")
            result.append(f"    📋 ID: {code.get('reading_type_id', 'N/A')}")
            result.append(f"    🏷️ 类别: {code.get('category', 'N/A')}")
        
        if len(filtered_codes) > 15:
            result.append(f"\n... 还有 {len(filtered_codes) - 15} 个结果，可使用查看编码库功能查看完整列表")
        
        return "\n".join(result)
    
    def _add_to_library(self, args: Dict) -> str:
        """添加编码到库中"""
        name = args.get("name", "")
        reading_type_id = args.get("reading_type_id", "")
        description = args.get("description", "")
        category = args.get("category", "用户生成")
        
        success, message = self.database.add_code(name, reading_type_id, description, category)
        
        if success:
            return f"✅ {message}"
        else:
            return f"❌ {message}"
    
    def _export_data(self, args: Dict) -> str:
        """导出数据"""
        format_type = args.get("format", "csv").lower()
        filter_category = args.get("category", "")
        
        success, result = self.database.export_data(format_type, filter_category)
        
        if success:
            return f"✅ 数据已导出到文件: {result}\n📊 共导出 {len(self.database.reading_type_codes)} 条记录"
        else:
            return f"❌ 导出失败: {result}"
    
    def _get_statistics(self, args: Dict) -> str:
        """获取统计信息"""
        stats = self.database.get_statistics()
        dict_stats = self.dictionary.get_statistics()
        
        result = ["📊 ReadingType编码库统计信息"]
        result.append("=" * 40)
        
        # 基本统计
        result.append(f"📚 总编码数量: {stats['total_codes']}")
        result.append(f"📖 字典字段数: {dict_stats['total_fields']}")
        result.append(f"🔧 自定义值数: {dict_stats['custom_values_count']}")
        
        # 按类别统计
        result.append("\n🏷️ 按类别分布:")
        for category, count in stats['category_stats'].items():
            percentage = (count / stats['total_codes']) * 100 if stats['total_codes'] > 0 else 0
            result.append(f"  • {category}: {count} ({percentage:.1f}%)")
        
        # 按来源统计
        result.append("\n📅 按来源分布:")
        for source, count in stats['source_stats'].items():
            percentage = (count / stats['total_codes']) * 100 if stats['total_codes'] > 0 else 0
            result.append(f"  • {source}: {count} ({percentage:.1f}%)")
        
        # 字典统计
        result.append("\n📖 字典详情:")
        for field_name, field_stat in dict_stats['field_stats'].items():
            result.append(f"  • {field_stat['chinese_name']}: {field_stat['total_values']}个值")
            if field_stat['custom_values'] > 0:
                result.append(f"    (含{field_stat['custom_values']}个自定义值)")
        
        return "\n".join(result)
    
    def handle_function_call(self, function_call: Dict) -> str:
        """处理函数调用"""
        function_name = function_call.get("name")
        function_args = {}
        
        if function_call.get("arguments"):
            try:
                function_args = json.loads(function_call.get("arguments", "{}"))
            except json.JSONDecodeError:
                pass
        
        if function_name in self.available_tools:
            function_response = self.available_tools[function_name](function_args)
            return function_response
        else:
            return f"错误: 未知的函数 '{function_name}'"
    
    def get_tools_definition(self) -> List[Dict]:
        """获取工具定义"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_reading_type",
                    "description": "在ReadingType编码库中搜索匹配的编码",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "要搜索的量测名称或关键词"
                            }
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_reading_type",
                    "description": "根据描述或字段值生成ReadingTypeID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "量测的详细描述"
                            },
                            "field_values": {
                                "type": "object",
                                "description": "具体的字段值字典"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "query_dictionary",
                    "description": "查询ReadingType字段字典信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "field_name": {
                                "type": "string",
                                "description": "要查询的字段名称，如commodity、measurementKind等"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "view_codes_library",
                    "description": "查看编码库内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "integer",
                                "description": "页码，默认为1"
                            },
                            "per_page": {
                                "type": "integer", 
                                "description": "每页显示数量，默认为15"
                            },
                            "category": {
                                "type": "string",
                                "description": "筛选的类别，如表计、储能、告警等"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "filter_codes",
                    "description": "筛选编码库",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "按类别筛选，如表计、储能、告警等"
                            },
                            "measurement_kind": {
                                "type": "string",
                                "description": "按测量类型筛选，如功率、电压、电流等"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_to_library",
                    "description": "添加新编码到库中",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "编码名称"
                            },
                            "reading_type_id": {
                                "type": "string",
                                "description": "ReadingTypeID编码，16个数字用'-'分隔"
                            },
                            "description": {
                                "type": "string",
                                "description": "编码说明"
                            },
                            "category": {
                                "type": "string",
                                "description": "编码类别"
                            }
                        },
                        "required": ["name", "reading_type_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "export_data",
                    "description": "导出编码库数据",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "format": {
                                "type": "string",
                                "description": "导出格式，支持csv和json"
                            },
                            "category": {
                                "type": "string",
                                "description": "筛选导出的类别"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_statistics",
                    "description": "获取编码库统计信息",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]
    
    def get_response(self, user_input: str, stream: bool = True) -> str:
        """获取AI的回复"""
        # 添加用户输入到对话历史
        self.add_message("user", user_input)
        
        try:
            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.conversation_history,
                tools=self.get_tools_definition(),
                tool_choice="auto",
                stream=False  # 工具调用时使用非流式
            )
            
            response_message = response.choices[0].message
            
            # 处理工具调用
            if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
                print("\n🤖 ReadingType助手正在处理...")
                
                # 添加完整的assistant响应到对话历史（包含tool_calls）
                assistant_message = {
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": []
                }
                
                # 构建assistant消息和执行工具调用
                tool_results = []
                for tool_call in response_message.tool_calls:
                    # 添加tool_call到assistant消息
                    assistant_message["tool_calls"].append({
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    })
                    
                    function_info = {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                    tool_result = self.handle_function_call(function_info)
                    print(f"🔧 工具使用: {tool_call.function.name}")
                    
                    # 收集工具调用结果
                    tool_results.append({
                        "role": "tool",
                        "content": tool_result,
                        "tool_call_id": tool_call.id
                    })
                
                # 先添加assistant消息到历史
                self.conversation_history.append(assistant_message)
                
                # 然后添加所有工具调用结果
                for tool_result in tool_results:
                    self.conversation_history.append(tool_result)
                
                # 再次调用API获取最终回复
                if stream:
                    print("\n🤖 ReadingType助手: ", end="", flush=True)
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
                    
                    print()  # 换行
                    ai_response = full_response
                else:
                    second_response = self.client.chat.completions.create(
                        model="deepseek-chat",
                        messages=self.conversation_history,
                        stream=False
                    )
                    ai_response = second_response.choices[0].message.content
                    print(f"\n🤖 ReadingType助手: {ai_response}")
                
                self.add_message("assistant", ai_response)
            else:
                # 没有工具调用，直接返回回复
                ai_response = response_message.content
                print(f"\n🤖 ReadingType助手: {ai_response}")
                self.add_message("assistant", ai_response)
            
            return ai_response
        
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(f"\n🤖 ReadingType助手: {error_msg}")
            return error_msg

    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = [] 