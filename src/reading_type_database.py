import os
import csv
import datetime
import pandas as pd
from difflib import SequenceMatcher
from typing import List, Dict, Optional, Tuple

class ReadingTypeDatabase:
    """ReadingType编码数据库管理类"""
    
    def __init__(self, codes_file="reading_type_codes.csv", 
                 dictionaries_file="field_dictionaries.csv",
                 history_file="operation_history.csv"):
        self.codes_file = codes_file
        self.dictionaries_file = dictionaries_file
        self.history_file = history_file
        
        # ReadingType字段定义
        self.field_names = [
            "macroPeriod", "aggregate", "measurePeriod", "accumulationBehaviour",
            "flowDirection", "commodity", "measurementKind", "harmonic",
            "argumentNumerator", "TOU", "cpp", "tier", "phase", "multiplier", "uom", "currency"
        ]
        
        # 加载数据
        self.reading_type_codes = self.load_reading_type_codes()
        self.field_dictionaries = self.load_field_dictionaries()
    
    def load_reading_type_codes(self) -> List[Dict]:
        """加载ReadingType编码库"""
        try:
            if not os.path.exists(self.codes_file):
                print(f"警告: 编码库文件 {self.codes_file} 未找到")
                return []
            
            df = pd.read_csv(self.codes_file)
            return df.to_dict('records')
        except Exception as e:
            print(f"加载编码库失败: {e}")
            return []
    
    def load_field_dictionaries(self) -> Dict:
        """加载字段字典"""
        try:
            if not os.path.exists(self.dictionaries_file):
                print(f"警告: 字典文件 {self.dictionaries_file} 未找到")
                return {}
                
            df = pd.read_csv(self.dictionaries_file)
            # 按字段名分组
            dictionaries = {}
            for _, row in df.iterrows():
                field_name = str(row['field_name']).strip()
                if field_name not in dictionaries:
                    dictionaries[field_name] = []
                dictionaries[field_name].append({
                    'value': row['field_value'],
                    'display_name': row['display_name'],
                    'description': row['description'],
                    'is_custom': row.get('is_custom', False)
                })
            return dictionaries
        except Exception as e:
            print(f"加载字典失败: {e}")
            return {}
    
    def search_codes(self, search_term: str, fuzzy_threshold: float = 0.6) -> Tuple[List[Dict], List[Tuple[Dict, float]]]:
        """搜索ReadingType编码
        
        Args:
            search_term: 搜索关键词
            fuzzy_threshold: 模糊匹配阈值
            
        Returns:
            (精确匹配列表, 模糊匹配列表)
        """
        if not search_term.strip():
            return [], []
        
        exact_matches = []
        fuzzy_matches = []
        
        for code in self.reading_type_codes:
            name = str(code.get('name', ''))
            description = str(code.get('description', ''))
            
            # 精确匹配
            if search_term.lower() == name.lower():
                exact_matches.append(code)
            # 模糊匹配
            elif (search_term.lower() in name.lower() or 
                  search_term.lower() in description.lower() or
                  self.similarity(search_term, name) > fuzzy_threshold):
                similarity_score = self.similarity(search_term, name)
                fuzzy_matches.append((code, similarity_score))
        
        # 按相似度排序模糊匹配结果
        fuzzy_matches.sort(key=lambda x: x[1], reverse=True)
        
        return exact_matches, fuzzy_matches
    
    def filter_codes(self, category: str = "", measurement_kind: str = "") -> List[Dict]:
        """筛选编码
        
        Args:
            category: 按类别筛选
            measurement_kind: 按测量类型筛选
            
        Returns:
            筛选后的编码列表
        """
        filtered_codes = self.reading_type_codes.copy()
        
        # 按类别筛选
        if category:
            filtered_codes = [
                code for code in filtered_codes 
                if category.lower() in str(code.get('category', '')).lower()
            ]
        
        # 按测量类型筛选
        if measurement_kind:
            filtered_codes = [
                code for code in filtered_codes 
                if measurement_kind.lower() in str(code.get('name', '')).lower()
            ]
        
        return filtered_codes
    
    def get_field_description(self, field_name: str, value: str) -> str:
        """获取字段值的描述"""
        if field_name in self.field_dictionaries:
            for item in self.field_dictionaries[field_name]:
                if str(item['value']) == str(value):
                    return item['display_name']
        return f"值: {value}"
    
    def get_field_options(self, field_name: str) -> List[Dict]:
        """获取字段的所有可选值"""
        if field_name in self.field_dictionaries:
            return sorted(
                self.field_dictionaries[field_name],
                key=lambda x: float(str(x['value']).replace('–', '-'))
            )
        return []
    
    def validate_reading_type_id(self, reading_type_id: str) -> bool:
        """验证ReadingTypeID格式"""
        if not reading_type_id:
            return False
            
        parts = reading_type_id.split('-')
        if len(parts) != 16:
            return False
        
        for part in parts:
            try:
                float(part)  # 允许小数和负数
            except ValueError:
                return False
        
        return True
    
    def add_code(self, name: str, reading_type_id: str, 
                 description: str = "", category: str = "用户生成") -> Tuple[bool, str]:
        """添加新编码到库中
        
        Args:
            name: 编码名称
            reading_type_id: ReadingTypeID编码
            description: 编码说明
            category: 编码类别
            
        Returns:
            (是否成功, 结果消息)
        """
        if not name or not reading_type_id:
            return False, "请提供编码名称和ReadingTypeID"
        
        # 验证编码格式
        if not self.validate_reading_type_id(reading_type_id):
            return False, "ReadingTypeID格式不正确，应为16个数字用'-'分隔"
        
        # 检查是否已存在
        for code in self.reading_type_codes:
            if (str(code.get('name', '')).lower() == name.lower() or 
                str(code.get('reading_type_id', '')) == reading_type_id):
                return False, f"编码已存在: {code.get('name', 'N/A')} ({code.get('reading_type_id', 'N/A')})"
        
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
        success = self.save_reading_type_codes()
        if success:
            self.log_operation(f"添加编码: {name}", "add", f"成功添加编码 {reading_type_id}")
            return True, f"成功添加编码: {name} ({reading_type_id})"
        else:
            return False, "保存编码失败"
    
    def save_reading_type_codes(self) -> bool:
        """保存编码库到文件"""
        try:
            df = pd.DataFrame(self.reading_type_codes)
            df.to_csv(self.codes_file, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"保存编码库失败: {e}")
            return False
    
    def export_data(self, format_type: str = "csv", filter_category: str = "") -> Tuple[bool, str]:
        """导出数据
        
        Args:
            format_type: 导出格式 (csv/json)
            filter_category: 筛选的类别
            
        Returns:
            (是否成功, 结果消息或文件名)
        """
        # 筛选数据
        export_data = self.reading_type_codes
        if filter_category:
            export_data = [
                code for code in export_data 
                if str(code.get('category', '')).lower() == filter_category.lower()
            ]
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reading_type_export_{timestamp}.{format_type}"
        
        try:
            if format_type == "csv":
                df = pd.DataFrame(export_data)
                df.to_csv(filename, index=False, encoding='utf-8')
            elif format_type == "json":
                import json
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
            else:
                return False, "不支持的导出格式，支持: csv, json"
            
            return True, filename
        
        except Exception as e:
            return False, f"导出失败: {str(e)}"
    
    def get_statistics(self) -> Dict:
        """获取数据库统计信息"""
        total_codes = len(self.reading_type_codes)
        
        # 按类别统计
        category_stats = {}
        for code in self.reading_type_codes:
            category = code.get('category', '未知')
            category_stats[category] = category_stats.get(category, 0) + 1
        
        # 按来源统计
        source_stats = {}
        for code in self.reading_type_codes:
            source = code.get('source', '未知')
            source_stats[source] = source_stats.get(source, 0) + 1
        
        return {
            'total_codes': total_codes,
            'category_stats': category_stats,
            'source_stats': source_stats,
            'field_count': len(self.field_names),
            'dictionary_fields': len(self.field_dictionaries)
        }
    
    def similarity(self, a: str, b: str) -> float:
        """计算字符串相似度"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def log_operation(self, input_text: str, operation_type: str, 
                     result: str, user_action: str = "pending") -> None:
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
    
    def get_chinese_field_name(self, field_name: str) -> str:
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