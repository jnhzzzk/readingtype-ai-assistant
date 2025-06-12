from typing import Dict, List, Optional, Tuple
import csv
import datetime

class DictionaryManager:
    """ReadingType字典管理类"""
    
    def __init__(self, dictionaries_file="field_dictionaries.csv"):
        self.dictionaries_file = dictionaries_file
        self.field_dictionaries = self.load_dictionaries()
        
        # 字段中文名映射
        self.chinese_field_names = {
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
    
    def load_dictionaries(self) -> Dict[str, List[Dict]]:
        """加载字典数据"""
        try:
            import pandas as pd
            df = pd.read_csv(self.dictionaries_file)
            
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
    
    def get_field_description(self, field_name: str, value: str) -> str:
        """获取字段值的描述"""
        if field_name in self.field_dictionaries:
            for item in self.field_dictionaries[field_name]:
                if str(item['value']) == str(value):
                    return item['display_name']
        return f"值: {value}"
    
    def get_field_options(self, field_name: str, limit: int = 50) -> List[Dict]:
        """获取字段的所有可选值
        
        Args:
            field_name: 字段名
            limit: 返回结果数量限制
            
        Returns:
            字段值列表
        """
        if field_name not in self.field_dictionaries:
            return []
        
        try:
            # 按数值排序
            sorted_items = sorted(
                self.field_dictionaries[field_name],
                key=lambda x: float(str(x['value']).replace('–', '-'))
            )
            return sorted_items[:limit]
        except:
            # 如果排序失败，按原顺序返回
            return self.field_dictionaries[field_name][:limit]
    
    def search_field_values(self, field_name: str, search_term: str) -> List[Dict]:
        """在字段值中搜索
        
        Args:
            field_name: 字段名
            search_term: 搜索关键词
            
        Returns:
            匹配的字段值列表
        """
        if field_name not in self.field_dictionaries:
            return []
        
        results = []
        search_lower = search_term.lower()
        
        for item in self.field_dictionaries[field_name]:
            display_name = str(item['display_name']).lower()
            description = str(item.get('description', '')).lower()
            
            if (search_lower in display_name or 
                search_lower in description or
                str(item['value']) == search_term):
                results.append(item)
        
        return results
    
    def add_custom_value(self, field_name: str, value: str, 
                        display_name: str, description: str = "") -> Tuple[bool, str]:
        """添加自定义字段值
        
        Args:
            field_name: 字段名
            value: 字段值
            display_name: 显示名称
            description: 描述
            
        Returns:
            (是否成功, 结果消息)
        """
        if field_name not in self.field_dictionaries:
            return False, f"字段 '{field_name}' 不存在"
        
        # 检查值是否已存在
        for item in self.field_dictionaries[field_name]:
            if str(item['value']) == str(value):
                return False, f"值 '{value}' 已存在于字段 '{field_name}' 中"
        
        # 添加新值
        new_item = {
            'value': value,
            'display_name': display_name,
            'description': description,
            'is_custom': True
        }
        
        self.field_dictionaries[field_name].append(new_item)
        
        # 保存到文件
        success = self.save_dictionaries()
        if success:
            return True, f"成功添加自定义值: {field_name}.{value} = {display_name}"
        else:
            return False, "保存字典失败"
    
    def save_dictionaries(self) -> bool:
        """保存字典到文件"""
        try:
            import pandas as pd
            
            # 将字典数据转换为DataFrame格式
            rows = []
            for field_name, items in self.field_dictionaries.items():
                chinese_name = self.chinese_field_names.get(field_name, field_name)
                for item in items:
                    rows.append({
                        'field_name': field_name,
                        'field_chinese_name': chinese_name,
                        'field_value': item['value'],
                        'display_name': item['display_name'],
                        'description': item.get('description', ''),
                        'is_custom': item.get('is_custom', False)
                    })
            
            df = pd.DataFrame(rows)
            df.to_csv(self.dictionaries_file, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"保存字典失败: {e}")
            return False
    
    def get_all_fields(self) -> List[Tuple[str, str]]:
        """获取所有字段名和中文名
        
        Returns:
            (英文名, 中文名) 列表
        """
        return [(name, self.chinese_field_names.get(name, name)) 
                for name in self.chinese_field_names.keys()]
    
    def validate_field_value(self, field_name: str, value: str) -> bool:
        """验证字段值是否有效
        
        Args:
            field_name: 字段名
            value: 字段值
            
        Returns:
            是否有效
        """
        if field_name not in self.field_dictionaries:
            return False
        
        for item in self.field_dictionaries[field_name]:
            if str(item['value']) == str(value):
                return True
        
        return False
    
    def get_statistics(self) -> Dict:
        """获取字典统计信息"""
        stats = {
            'total_fields': len(self.field_dictionaries),
            'field_stats': {},
            'custom_values_count': 0
        }
        
        for field_name, items in self.field_dictionaries.items():
            total_values = len(items)
            custom_values = sum(1 for item in items if item.get('is_custom', False))
            standard_values = total_values - custom_values
            
            stats['field_stats'][field_name] = {
                'total_values': total_values,
                'standard_values': standard_values,
                'custom_values': custom_values,
                'chinese_name': self.chinese_field_names.get(field_name, field_name)
            }
            
            stats['custom_values_count'] += custom_values
        
        return stats
    
    def export_dictionary(self, field_name: str = "", format_type: str = "csv") -> Tuple[bool, str]:
        """导出字典数据
        
        Args:
            field_name: 特定字段名，为空则导出全部
            format_type: 导出格式 (csv/json)
            
        Returns:
            (是否成功, 文件名或错误消息)
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if field_name:
                # 导出特定字段
                if field_name not in self.field_dictionaries:
                    return False, f"字段 '{field_name}' 不存在"
                
                filename = f"dictionary_{field_name}_{timestamp}.{format_type}"
                export_data = self.field_dictionaries[field_name]
            else:
                # 导出全部字典
                filename = f"dictionary_all_{timestamp}.{format_type}"
                export_data = self.field_dictionaries
            
            if format_type == "csv":
                import pandas as pd
                
                if field_name:
                    # 单个字段
                    rows = []
                    for item in export_data:
                        rows.append({
                            'field_name': field_name,
                            'value': item['value'],
                            'display_name': item['display_name'],
                            'description': item.get('description', ''),
                            'is_custom': item.get('is_custom', False)
                        })
                    df = pd.DataFrame(rows)
                else:
                    # 全部字段
                    rows = []
                    for fname, items in export_data.items():
                        for item in items:
                            rows.append({
                                'field_name': fname,
                                'field_chinese_name': self.chinese_field_names.get(fname, fname),
                                'value': item['value'],
                                'display_name': item['display_name'],
                                'description': item.get('description', ''),
                                'is_custom': item.get('is_custom', False)
                            })
                    df = pd.DataFrame(rows)
                
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
    
    def get_field_chinese_name(self, field_name: str) -> str:
        """获取字段的中文名称"""
        return self.chinese_field_names.get(field_name, field_name) 