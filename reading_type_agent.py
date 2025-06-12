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

# 加载环境变量
load_dotenv()

# 设置DeepSeek API密钥
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class ReadingTypeAgent:
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
        
        # 加载数据
        self.reading_type_codes = self.load_reading_type_codes()
        self.field_dictionaries = self.load_field_dictionaries()
        
        # ReadingType字段定义
        self.field_names = [
            "macroPeriod", "aggregate", "measurePeriod", "accumulationBehaviour",
            "flowDirection", "commodity", "measurementKind", "harmonic",
            "argumentNumerator", "TOU", "cpp", "tier", "phase", "multiplier", "uom", "currency"
        ]
        
        # 设置可用工具
        self.available_tools = {
            "search_reading_type": self.search_reading_type,
            "generate_reading_type": self.generate_reading_type,
            "query_dictionary": self.query_dictionary,
            "export_data": self.export_data,
            "view_codes_library": self.view_codes_library,
            "filter_codes": self.filter_codes,
            "add_to_library": self.add_to_library
        }
    
    def load_reading_type_codes(self):
        """加载ReadingType编码库"""
        try:
            df = pd.read_csv(self.codes_file)
            return df.to_dict('records')
        except FileNotFoundError:
            print(f"警告: 编码库文件 {self.codes_file} 未找到")
            return []
    
    def load_field_dictionaries(self):
        """加载字段字典"""
        try:
            df = pd.read_csv(self.dictionaries_file)
            # 按字段名分组
            dictionaries = {}
            for _, row in df.iterrows():
                field_name = row['field_name'].strip()
                if field_name not in dictionaries:
                    dictionaries[field_name] = []
                dictionaries[field_name].append({
                    'value': row['field_value'],
                    'display_name': row['display_name'],
                    'description': row['description'],
                    'is_custom': row.get('is_custom', False)
                })
            return dictionaries
        except FileNotFoundError:
            print(f"警告: 字典文件 {self.dictionaries_file} 未找到")
            return {}
    
    def add_message(self, role, content):
        """添加消息到对话历史"""
        self.conversation_history.append({"role": role, "content": content})
    
    def search_reading_type(self, args):
        """在编码库中搜索ReadingTypeID"""
        search_term = args.get("name", "").strip()
        
        if not search_term:
            return "❌ 请提供要搜索的量测名称"
        
        # 精确匹配
        exact_matches = []
        fuzzy_matches = []
        
        for code in self.reading_type_codes:
            name = code.get('name', '')
            description = code.get('description', '')
            
            # 精确匹配
            if search_term.lower() == name.lower():
                exact_matches.append(code)
            # 模糊匹配
            elif (search_term.lower() in name.lower() or 
                  search_term.lower() in description.lower() or
                  self.similarity(search_term, name) > 0.6):
                fuzzy_matches.append((code, self.similarity(search_term, name)))
        
        # 构建返回结果
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
            # 按相似度排序
            fuzzy_matches.sort(key=lambda x: x[1], reverse=True)
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
        
        # 记录操作历史
        self.log_operation(search_term, "search", "\n".join(result))
        
        return "\n".join(result)
    
    def generate_reading_type(self, args):
        """根据解析的字段生成ReadingTypeID"""
        # 获取用户描述
        description = args.get("description", "")
        field_values = args.get("field_values", {})
        
        if not description and not field_values:
            return "❌ 请提供量测描述或字段值"
        
        try:
            # 如果有字段值，直接生成
            if field_values:
                reading_type_id = self.build_reading_type_id(field_values)
                result = []
                result.append("🤖 AI生成结果:")
                result.append(f"🔢 ReadingTypeID: {reading_type_id}")
                result.append("\n📋 字段详情:")
                
                for i, field_name in enumerate(self.field_names):
                    value = field_values.get(f"field_{i+1}", 0)
                    field_info = self.get_field_description(field_name, value)
                    result.append(f"  {field_name}: {value} ({field_info})")
                
                result.append("\n✅ 是否采纳此编码？输入'是'确认，'否'取消，或提出修改建议。")
                return "\n".join(result)
            
            # 基于描述进行AI分析生成
            analysis = self.analyze_measurement_description(description)
            if analysis:
                reading_type_id = self.build_reading_type_id(analysis)
                
                result = []
                result.append("🤖 AI分析结果:")
                result.append(f"📝 输入描述: {description}")
                result.append("\n📋 识别要素:")
                
                # 显示分析结果
                for field_name, value in analysis.items():
                    if value != 0:  # 只显示非零字段
                        field_info = self.get_field_description(field_name.replace('field_', ''), value)
                        result.append(f"  - {field_name}: {value} ({field_info})")
                
                result.append(f"\n💡 建议编码: {reading_type_id}")
                result.append("\n✅ 是否采纳此编码？输入'是'确认，'否'取消，或提出修改建议。")
                
                # 记录操作历史
                self.log_operation(description, "generate", "\n".join(result))
                
                return "\n".join(result)
            else:
                return "❌ 无法解析描述，请提供更详细的信息或使用标准术语"
                
        except Exception as e:
            return f"❌ 生成编码时发生错误: {str(e)}"
    
    def analyze_measurement_description(self, description):
        """分析量测描述并推断字段值"""
        # 这里实现基于关键词的简单映射
        analysis = {f"field_{i+1}": 0 for i in range(16)}
        
        desc_lower = description.lower()
        
        # commodity (商品类型) - field_6
        if any(word in desc_lower for word in ['电', '电力', '电能', '电压', '电流', '功率']):
            analysis['field_6'] = 1  # 电力
        elif any(word in desc_lower for word in ['气', '天然气', '燃气']):
            analysis['field_6'] = 7  # 天然气
        elif any(word in desc_lower for word in ['水']):
            analysis['field_6'] = 4  # 水
        elif any(word in desc_lower for word in ['热', '蒸汽']):
            analysis['field_6'] = 6  # 热能
        
        # measurementKind (测量类型) - field_7
        if any(word in desc_lower for word in ['电压', '电位']):
            analysis['field_7'] = 54  # 电压
        elif any(word in desc_lower for word in ['电流']):
            analysis['field_7'] = 4   # 电流
        elif any(word in desc_lower for word in ['功率']):
            if '有功' in desc_lower:
                analysis['field_7'] = 37  # 有功功率
            elif '无功' in desc_lower:
                analysis['field_7'] = 53  # 无功功率
            elif '视在' in desc_lower:
                analysis['field_7'] = 15  # 视在功率
            else:
                analysis['field_7'] = 37  # 默认有功功率
        elif any(word in desc_lower for word in ['能量', '电能']):
            analysis['field_7'] = 12  # 能量
        elif any(word in desc_lower for word in ['频率']):
            analysis['field_7'] = 46  # 频率
        elif any(word in desc_lower for word in ['温度']):
            analysis['field_7'] = 139 # 温度
        elif any(word in desc_lower for word in ['状态', '告警', '报警']):
            analysis['field_7'] = 118 # 状态
        
        # flowDirection (流向) - field_5
        if any(word in desc_lower for word in ['正向', '充电', '进']):
            analysis['field_5'] = 1   # 正向
        elif any(word in desc_lower for word in ['反向', '放电', '出']):
            analysis['field_5'] = 19  # 反向
        elif any(word in desc_lower for word in ['净', '双向']):
            analysis['field_5'] = 4   # 净值
        
        # accumulationBehaviour (累积行为) - field_4
        if any(word in desc_lower for word in ['累积', '累计', '总']):
            analysis['field_4'] = 3   # 累积
        elif any(word in desc_lower for word in ['瞬时', '当前', '实时']):
            analysis['field_4'] = 6   # 瞬时
        elif any(word in desc_lower for word in ['间隔', '区间']):
            analysis['field_4'] = 4   # 间隔
        elif any(word in desc_lower for word in ['最大', '峰值']):
            analysis['field_4'] = 6   # 瞬时 (用于需量等)
        
        # measurePeriod (测量周期) - field_3
        if any(word in desc_lower for word in ['15分钟', '15min']):
            analysis['field_3'] = 2   # 15分钟
        elif any(word in desc_lower for word in ['5分钟', '5min']):
            analysis['field_3'] = 6   # 5分钟
        elif any(word in desc_lower for word in ['1小时', '小时']):
            analysis['field_3'] = 15  # 1小时
        elif any(word in desc_lower for word in ['日', '天']):
            analysis['field_3'] = 11  # 日
        elif any(word in desc_lower for word in ['月']):
            analysis['field_3'] = 13  # 月
        
        # phase (相位) - field_13
        if 'a相' in desc_lower or '甲相' in desc_lower:
            analysis['field_13'] = 128  # A相
        elif 'b相' in desc_lower or '乙相' in desc_lower:
            analysis['field_13'] = 64   # B相
        elif 'c相' in desc_lower or '丙相' in desc_lower:
            analysis['field_13'] = 32   # C相
        elif '三相' in desc_lower:
            analysis['field_13'] = 224  # 三相合计
        
        # multiplier (乘数) - field_14
        if any(word in desc_lower for word in ['k', 'kw', 'kwh', '千']):
            analysis['field_14'] = 3    # kilo (×10³)
        elif any(word in desc_lower for word in ['m', 'mw', 'mwh', '兆']):
            analysis['field_14'] = 6    # mega (×10⁶)
        
        # uom (单位) - field_15
        if any(word in desc_lower for word in ['wh', '瓦时', '电能']):
            analysis['field_15'] = 72   # Wh
        elif any(word in desc_lower for word in ['w', '瓦', '功率']):
            analysis['field_15'] = 38   # W
        elif any(word in desc_lower for word in ['v', '伏', '电压']):
            analysis['field_15'] = 29   # V
        elif any(word in desc_lower for word in ['a', '安', '电流']):
            analysis['field_15'] = 5    # A
        elif any(word in desc_lower for word in ['hz', '赫兹', '频率']):
            analysis['field_15'] = 23   # Hz
        elif any(word in desc_lower for word in ['°c', '摄氏度', '温度']):
            analysis['field_15'] = 109  # 摄氏度
        
        return analysis
    
    def get_field_description(self, field_name, value):
        """获取字段值的描述"""
        if field_name in self.field_dictionaries:
            for item in self.field_dictionaries[field_name]:
                if str(item['value']) == str(value):
                    return item['display_name']
        return f"值: {value}"
    
    def build_reading_type_id(self, field_values):
        """构建ReadingTypeID字符串"""
        values = []
        for i in range(16):
            field_key = f"field_{i+1}"
            values.append(str(field_values.get(field_key, 0)))
        return "-".join(values)
    
    def query_dictionary(self, args):
        """查询字典信息"""
        field_name = args.get("field_name", "").strip()
        
        if not field_name:
            # 显示所有字段
            result = ["📚 ReadingType字段字典:"]
            for i, name in enumerate(self.field_names, 1):
                chinese_name = self.get_chinese_field_name(name)
                result.append(f"{i:2d}. {name} ({chinese_name})")
            result.append("\n💡 使用 '查询字典 [字段名]' 查看具体字段的可选值")
            return "\n".join(result)
        
        # 查询具体字段
        if field_name in self.field_dictionaries:
            result = [f"📖 字段 '{field_name}' 的可选值:"]
            items = self.field_dictionaries[field_name]
            
            # 按值排序
            sorted_items = sorted(items, key=lambda x: float(str(x['value']).replace('–', '-')))
            
            for item in sorted_items[:20]:  # 限制显示数量
                result.append(f"  {item['value']}: {item['display_name']}")
                if item.get('description'):
                    result.append(f"    {item['description']}")
            
            if len(items) > 20:
                result.append(f"\n... 还有 {len(items) - 20} 个值，使用具体数值查询详情")
            
            return "\n".join(result)
        else:
            return f"❌ 未找到字段 '{field_name}'"
    
    def get_chinese_field_name(self, field_name):
        """获取字段的中文名称"""
        chinese_names = {
            "macroPeriod": "宏周期",
            "aggregate": "聚合类型", 
            "measurePeriod": "测量周期",
            "accumulationBehaviour": "累积行为",
            "flowDirection": "流向",
            "commodity": "商品类型",
            "measurementKind": "测量类型",
            "harmonic": "谐波",
            "argumentNumerator": "参数分子",
            "TOU": "时段",
            "cpp": "关键峰值期",
            "tier": "阶梯",
            "phase": "相位",
            "multiplier": "乘数",
            "uom": "单位",
            "currency": "货币"
        }
        return chinese_names.get(field_name, field_name)
    
    def view_codes_library(self, args):
        """查看编码库"""
        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 20))
        category = args.get("category", "")
        
        # 筛选数据
        filtered_codes = self.reading_type_codes
        if category:
            filtered_codes = [code for code in filtered_codes if code.get('category', '').lower() == category.lower()]
        
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
            result.append(f"     类别: {code.get('category', 'N/A')} | 来源: {code.get('source', 'N/A')}")
            result.append("")
        
        # 分页信息
        total_pages = (total + per_page - 1) // per_page
        if total_pages > 1:
            result.append(f"📄 第{page}/{total_pages}页")
            if page < total_pages:
                result.append("💡 输入 '下一页' 查看更多")
        
        return "\n".join(result)
    
    def filter_codes(self, args):
        """筛选编码"""
        category = args.get("category", "")
        measurement_kind = args.get("measurement_kind", "")
        
        filtered_codes = self.reading_type_codes
        
        # 按类别筛选
        if category:
            filtered_codes = [code for code in filtered_codes if category.lower() in code.get('category', '').lower()]
        
        # 按测量类型筛选
        if measurement_kind:
            filtered_codes = [code for code in filtered_codes if measurement_kind.lower() in code.get('name', '').lower()]
        
        if not filtered_codes:
            return f"❌ 未找到符合条件的编码 (类别: {category}, 测量类型: {measurement_kind})"
        
        result = [f"🔍 筛选结果 (共{len(filtered_codes)}条):"]
        
        for code in filtered_codes[:10]:  # 限制显示数量
            result.append(f"• {code.get('name', 'N/A')}")
            result.append(f"  ID: {code.get('reading_type_id', 'N/A')}")
            result.append(f"  类别: {code.get('category', 'N/A')}")
        
        if len(filtered_codes) > 10:
            result.append(f"\n... 还有 {len(filtered_codes) - 10} 个结果")
        
        return "\n".join(result)
    
    def add_to_library(self, args):
        """添加编码到库中"""
        name = args.get("name", "")
        reading_type_id = args.get("reading_type_id", "")
        description = args.get("description", "")
        category = args.get("category", "用户生成")
        
        if not name or not reading_type_id:
            return "❌ 请提供编码名称和ReadingTypeID"
        
        # 验证编码格式
        if not self.validate_reading_type_id(reading_type_id):
            return "❌ ReadingTypeID格式不正确，应为16个数字用'-'分隔"
        
        # 检查是否已存在
        for code in self.reading_type_codes:
            if (code.get('name', '').lower() == name.lower() or 
                code.get('reading_type_id', '') == reading_type_id):
                return f"❌ 编码已存在: {code.get('name', 'N/A')} ({code.get('reading_type_id', 'N/A')})"
        
        # 添加新编码
        new_code = {
            'id': len(self.reading_type_codes) + 1,
            'name': name,
            'description': description,
            'reading_type_id': reading_type_id,
            'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'source': '用户生成',
            'category': category
        }
        
        # 解析字段值
        fields = reading_type_id.split('-')
        for i, field_value in enumerate(fields):
            new_code[f'field_{i+1}'] = field_value
        
        self.reading_type_codes.append(new_code)
        
        # 保存到文件
        self.save_reading_type_codes()
        
        # 记录操作历史
        self.log_operation(f"添加编码: {name}", "add", f"成功添加编码 {reading_type_id}")
        
        return f"✅ 成功添加编码到库中:\n📊 名称: {name}\n🔢 ID: {reading_type_id}\n📝 说明: {description}"
    
    def validate_reading_type_id(self, reading_type_id):
        """验证ReadingTypeID格式"""
        parts = reading_type_id.split('-')
        if len(parts) != 16:
            return False
        
        for part in parts:
            try:
                float(part)  # 允许小数和负数
            except ValueError:
                return False
        
        return True
    
    def save_reading_type_codes(self):
        """保存编码库到文件"""
        try:
            df = pd.DataFrame(self.reading_type_codes)
            df.to_csv(self.codes_file, index=False)
        except Exception as e:
            print(f"保存编码库失败: {e}")
    
    def export_data(self, args):
        """导出数据"""
        format_type = args.get("format", "csv").lower()
        filter_category = args.get("category", "")
        
        # 筛选数据
        export_data = self.reading_type_codes
        if filter_category:
            export_data = [code for code in export_data if code.get('category', '').lower() == filter_category.lower()]
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reading_type_export_{timestamp}.{format_type}"
        
        try:
            if format_type == "csv":
                df = pd.DataFrame(export_data)
                df.to_csv(filename, index=False)
            elif format_type == "json":
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
            else:
                return "❌ 不支持的导出格式，支持: csv, json"
            
            return f"✅ 数据已导出到文件: {filename}\n📊 共导出 {len(export_data)} 条记录"
        
        except Exception as e:
            return f"❌ 导出失败: {str(e)}"
    
    def similarity(self, a, b):
        """计算字符串相似度"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def log_operation(self, input_text, operation_type, result, user_action="pending"):
        """记录操作历史"""
        try:
            history_entry = {
                'id': '',  # 由CSV文件行数决定
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'input_text': input_text,
                'operation_type': operation_type,
                'result': result[:200] + "..." if len(result) > 200 else result,  # 限制长度
                'user_action': user_action
            }
            
            # 追加到历史文件
            file_exists = os.path.isfile(self.history_file)
            with open(self.history_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=history_entry.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(history_entry)
        
        except Exception as e:
            print(f"记录历史失败: {e}")
    
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
            self.add_message(
                "function",
                {
                    "name": function_name,
                    "content": function_response
                }
            )
            
            return function_response
        else:
            return f"错误: 未知的函数 '{function_name}'"
    
    def get_response(self, user_input, stream=True):
        """获取AI的回复"""
        # 添加用户输入到对话历史
        self.add_message("user", user_input)
        
        try:
            # 创建可用工具的描述
            tools = [
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
                                    "description": "要查询的字段名称"
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
                                    "description": "每页显示数量，默认为20"
                                },
                                "category": {
                                    "type": "string",
                                    "description": "筛选的类别"
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
                                    "description": "按类别筛选"
                                },
                                "measurement_kind": {
                                    "type": "string",
                                    "description": "按测量类型筛选"
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
                                    "description": "ReadingTypeID编码"
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
                                    "description": "导出格式 (csv/json)"
                                },
                                "category": {
                                    "type": "string",
                                    "description": "筛选导出的类别"
                                }
                            }
                        }
                    }
                }
            ]
            
            # 调用DeepSeek API，非流式方式，因为需要检查是否有工具调用
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.conversation_history,
                tools=tools,
                tool_choice="auto",
                stream=False  # 工具调用时使用非流式
            )
            
            response_message = response.choices[0].message
            
            # 处理工具调用
            if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
                print("\n🤖 ReadingType助手正在处理...")
                
                # 添加助手的响应到对话历史
                self.add_message("assistant", response_message)
                
                # 处理每个工具调用
                for tool_call in response_message.tool_calls:
                    function_info = {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                    tool_result = self.handle_function_call(function_info)
                    print(f"🔧 工具使用: {tool_call.function.name}")
                
                # 再次调用API获取最终回复，这次使用流式输出
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
                if stream:
                    # 由于已经获取了非流式响应，直接打印
                    ai_response = response_message.content
                    print(f"\n🤖 ReadingType助手: {ai_response}")
                else:
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


def main():
    print("🚀 ReadingTypeID智能编码助手")
    print("=" * 50)
    print("💡 我可以帮您:")
    print("   • 搜索现有的ReadingType编码")
    print("   • 生成新的ReadingTypeID")
    print("   • 查询字段字典信息")
    print("   • 管理编码库")
    print("   • 导出数据")
    print("\n📝 支持自然语言对话，输入'退出'结束对话")
    print("🔍 示例: '有功电能' / '生成储能充电功率编码' / '查看编码库'")
    print("=" * 50)
    
    # 创建AI助手实例
    agent = ReadingTypeAgent()
    
    # 设置系统消息
    agent.add_message("system", """你是一个专业的ReadingTypeID编码助手，基于IEC61968-9-2024标准。你的任务是：

1. 理解用户的量测需求，搜索现有编码或生成新编码
2. 提供准确的ReadingType编码信息和解释
3. 管理和维护编码库
4. 导出和分析编码数据

核心原则：
- 准确理解用户意图，提供精确的编码信息
- 对于模糊的需求，主动询问细节
- 解释编码的含义和标准依据
- 保持友好和专业的对话风格
- 使用emoji增强可读性

当用户提及具体的量测名称时，优先搜索现有编码。
当用户要求生成新编码时，分析描述并映射到正确的字段值。
当用户询问字典信息时，提供清晰的字段说明。""")
    
    # 对话循环
    while True:
        user_input = input("\n💬 您: ")
        
        if user_input.lower() in ["退出", "exit", "quit", "再见"]:
            print("👋 再见！感谢使用ReadingTypeID编码助手!")
            break
        
        if user_input.strip() == "":
            continue
        
        # 获取AI回复（内部已处理输出）
        agent.get_response(user_input)


if __name__ == "__main__":
    main() 