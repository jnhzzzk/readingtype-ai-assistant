import re
from typing import Dict, List, Optional, Tuple

class SemanticParser:
    """语义解析器，用于解析用户描述并生成ReadingType字段值"""
    
    def __init__(self):
        # ReadingType字段定义
        self.field_names = [
            "macroPeriod", "aggregate", "measurePeriod", "accumulationBehaviour",
            "flowDirection", "commodity", "measurementKind", "harmonic",
            "argumentNumerator", "TOU", "cpp", "tier", "phase", "multiplier", "uom", "currency"
        ]
        
        # 关键词映射规则
        self.keyword_mappings = self._init_keyword_mappings()
    
    def _init_keyword_mappings(self) -> Dict:
        """初始化关键词映射规则"""
        return {
            # commodity (商品类型) - field_6
            'commodity': {
                'keywords': {
                    1: ['电', '电力', '电能', '电压', '电流', '功率'],  # 电力
                    4: ['水'],  # 水
                    6: ['热', '蒸汽', '热能'],  # 热能
                    7: ['气', '天然气', '燃气'],  # 天然气
                    41: ['储能', '电池', 'PCS'],  # 储能相关
                    40: ['气象', '环境', '天气'],  # 气象
                    3: ['通信', '网络', '信号'],  # 通信
                    2: ['微网', '电网'],  # 微网
                },
                'default': 1  # 默认电力
            },
            
            # measurementKind (测量类型) - field_7
            'measurementKind': {
                'keywords': {
                    54: ['电压', '电位', 'voltage', 'v'],  # 电压
                    4: ['电流', 'current', 'a'],  # 电流
                    37: ['有功功率', '有功', 'active power'],  # 有功功率
                    53: ['无功功率', '无功', 'reactive power'],  # 无功功率
                    15: ['视在功率', '视在', 'apparent power'],  # 视在功率
                    12: ['能量', '电能', 'energy', 'wh'],  # 能量
                    46: ['频率', 'frequency', 'hz'],  # 频率
                    139: ['温度', 'temperature'],  # 温度
                    118: ['状态', '告警', '报警', 'status', 'alarm'],  # 状态
                    183: ['充电状态', 'charging status'],  # 充电状态
                    119: ['容量', 'capacity', 'soc'],  # 容量/SOC
                    158: ['单相电压', '相电压'],  # 单相电压
                    904: ['远方', '就地'],  # 远方/就地
                    11: ['并网', '离网'],  # 并网状态
                    38: ['功率因数', 'power factor'],  # 功率因数
                    121: ['控制系数'],  # 控制系数
                },
                'default': 0
            },
            
            # flowDirection (流向) - field_5
            'flowDirection': {
                'keywords': {
                    1: ['正向', '充电', '进', '输入', 'forward', 'charge'],  # 正向
                    19: ['反向', '放电', '出', '输出', 'reverse', 'discharge'],  # 反向
                    4: ['净', '双向', '净值', 'net'],  # 净值
                    20: ['充放电', 'pcs'],  # PCS充放电
                },
                'default': 0
            },
            
            # accumulationBehaviour (累积行为) - field_4
            'accumulationBehaviour': {
                'keywords': {
                    3: ['累积', '累计', '总', 'cumulative', 'total'],  # 累积
                    6: ['瞬时', '当前', '实时', 'instantaneous', 'current'],  # 瞬时
                    4: ['间隔', '区间', 'interval'],  # 间隔
                    1: ['容量', '总量', 'bulk'],  # 容量
                    10: ['计划', 'plan'],  # 计划
                },
                'default': 6  # 默认瞬时
            },
            
            # measurePeriod (测量周期) - field_3
            'measurePeriod': {
                'keywords': {
                    2: ['15分钟', '15min', 'fifteen minute'],  # 15分钟
                    6: ['5分钟', '5min', 'five minute'],  # 5分钟
                    15: ['1小时', '小时', 'hour'],  # 1小时
                    11: ['日', '天', 'daily'],  # 日
                    13: ['月', 'monthly'],  # 月
                    24: ['周', '星期', 'weekly'],  # 周
                    0: ['瞬时', '实时'],  # 瞬时 (无周期)
                },
                'default': 0
            },
            
            # phase (相位) - field_13
            'phase': {
                'keywords': {
                    128: ['a相', '甲相', 'phase a'],  # A相
                    64: ['b相', '乙相', 'phase b'],  # B相
                    32: ['c相', '丙相', 'phase c'],  # C相
                    224: ['三相', '总', 'three phase', 'total'],  # 三相合计
                    132: ['ab相', 'a-b相', 'line ab'],  # AB线
                    66: ['bc相', 'b-c相', 'line bc'],  # BC线
                    40: ['ca相', 'c-a相', 'line ca'],  # CA线
                    225: ['平均', 'average'],  # 平均
                },
                'default': 0
            },
            
            # multiplier (乘数) - field_14
            'multiplier': {
                'keywords': {
                    3: ['k', 'kw', 'kwh', '千', 'kilo'],  # kilo (×10³)
                    6: ['m', 'mw', 'mwh', '兆', 'mega'],  # mega (×10⁶)
                    0: ['基本', '基础'],  # 基本单位
                },
                'default': 0
            },
            
            # uom (单位) - field_15
            'uom': {
                'keywords': {
                    72: ['wh', '瓦时', '电能'],  # Wh
                    38: ['w', '瓦', '功率'],  # W
                    29: ['v', '伏', '电压'],  # V
                    5: ['a', '安', '电流'],  # A
                    23: ['hz', '赫兹', '频率'],  # Hz
                    109: ['°c', '摄氏度', '温度'],  # 摄氏度
                    281: ['°f', '华氏度'],  # 华氏度
                    0: ['无单位', '状态', '比率'],  # 无单位
                },
                'default': 0
            },
            
            # aggregate (聚合类型) - field_2
            'aggregate': {
                'keywords': {
                    2: ['平均', 'average'],  # 平均
                    8: ['最大', '峰值', 'maximum'],  # 最大
                    9: ['最小', 'minimum'],  # 最小
                    26: ['合计', '总计', 'sum'],  # 合计
                },
                'default': 0
            },
            
            # macroPeriod (宏周期) - field_1
            'macroPeriod': {
                'keywords': {
                    8: ['计费', '账单', 'billing'],  # 计费周期
                    13: ['月度', '月'],  # 月度
                    11: ['日度', '日'],  # 日度
                    4: ['小时', '2小时'],  # 2小时周期
                },
                'default': 0
            }
        }
    
    def analyze_measurement_description(self, description: str) -> Dict[str, int]:
        """分析量测描述并推断字段值
        
        Args:
            description: 用户输入的量测描述
            
        Returns:
            字段值字典 {field_1: value1, field_2: value2, ...}
        """
        analysis = {f"field_{i+1}": 0 for i in range(16)}
        
        desc_lower = description.lower()
        
        # 分析每个字段
        for i, field_name in enumerate(self.field_names):
            field_key = f"field_{i+1}"
            
            if field_name in self.keyword_mappings:
                mapping = self.keyword_mappings[field_name]
                matched_value = self._match_keywords(desc_lower, mapping)
                analysis[field_key] = matched_value
        
        # 后处理逻辑
        analysis = self._post_process_analysis(analysis, desc_lower)
        
        return analysis
    
    def _match_keywords(self, text: str, mapping: Dict) -> int:
        """匹配关键词并返回对应值"""
        keywords = mapping.get('keywords', {})
        default = mapping.get('default', 0)
        
        # 按匹配权重排序 (更长的关键词优先)
        matched_items = []
        
        for value, keyword_list in keywords.items():
            for keyword in keyword_list:
                if keyword.lower() in text:
                    # 计算匹配权重 (关键词长度)
                    weight = len(keyword)
                    matched_items.append((value, weight, keyword))
        
        if matched_items:
            # 返回权重最高的匹配
            matched_items.sort(key=lambda x: x[1], reverse=True)
            return matched_items[0][0]
        
        return default
    
    def _post_process_analysis(self, analysis: Dict[str, int], description: str) -> Dict[str, int]:
        """后处理分析结果，修正不合理的组合"""
        
        # 如果是功率相关但没有单位，设置为W
        if (analysis.get('field_7') in [37, 53, 15] and  # 功率类型
            analysis.get('field_15') == 0):  # 没有单位
            analysis['field_15'] = 38  # W
        
        # 如果是电能相关但没有单位，设置为Wh
        if (analysis.get('field_7') == 12 and  # 能量
            analysis.get('field_15') == 0):  # 没有单位
            analysis['field_15'] = 72  # Wh
        
        # 如果是电压相关但没有单位，设置为V
        if (analysis.get('field_7') == 54 and  # 电压
            analysis.get('field_15') == 0):  # 没有单位
            analysis['field_15'] = 29  # V
        
        # 如果是电流相关但没有单位，设置为A
        if (analysis.get('field_7') == 4 and  # 电流
            analysis.get('field_15') == 0):  # 没有单位
            analysis['field_15'] = 5  # A
        
        # 如果是累积电能，设置累积行为
        if (analysis.get('field_7') == 12 and  # 能量
            ('累积' in description or '累计' in description or '总' in description)):
            analysis['field_4'] = 3  # 累积
        
        # 如果指定了间隔时间，设置累积行为为间隔
        if (analysis.get('field_3') in [2, 6, 15] and  # 有时间周期
            ('间隔' in description or '区间' in description)):
            analysis['field_4'] = 4  # 间隔
        
        # 如果是储能相关，调整商品类型
        if any(word in description.lower() for word in ['储能', '电池', 'pcs', 'ems']):
            analysis['field_6'] = 41  # 储能
        
        # 如果有千瓦等单位前缀，设置乘数
        if any(word in description.lower() for word in ['千瓦', 'kw', 'kwh']):
            analysis['field_14'] = 3  # kilo
        elif any(word in description.lower() for word in ['兆瓦', 'mw', 'mwh']):
            analysis['field_14'] = 6  # mega
        
        return analysis
    
    def build_reading_type_id(self, field_values: Dict[str, int]) -> str:
        """构建ReadingTypeID字符串"""
        values = []
        for i in range(16):
            field_key = f"field_{i+1}"
            values.append(str(field_values.get(field_key, 0)))
        return "-".join(values)
    
    def parse_reading_type_id(self, reading_type_id: str) -> Dict[str, int]:
        """解析ReadingTypeID字符串为字段值"""
        try:
            parts = reading_type_id.split('-')
            if len(parts) != 16:
                raise ValueError("ReadingTypeID必须包含16个字段")
            
            field_values = {}
            for i, value in enumerate(parts):
                field_key = f"field_{i+1}"
                field_values[field_key] = int(float(value))  # 支持小数转整数
            
            return field_values
        except Exception as e:
            raise ValueError(f"无效的ReadingTypeID格式: {e}")
    
    def extract_measurement_info(self, description: str) -> Dict[str, List[str]]:
        """提取量测信息的关键要素
        
        Args:
            description: 量测描述
            
        Returns:
            包含各种要素的字典
        """
        info = {
            'device_types': [],  # 设备类型
            'measurement_kinds': [],  # 测量类型
            'flow_directions': [],  # 流向
            'phases': [],  # 相位
            'time_periods': [],  # 时间周期
            'units': [],  # 单位
            'behaviors': []  # 行为
        }
        
        desc_lower = description.lower()
        
        # 设备类型
        if any(word in desc_lower for word in ['表计', '电表', '电能表']):
            info['device_types'].append('电表')
        if any(word in desc_lower for word in ['储能', '电池', 'pcs']):
            info['device_types'].append('储能')
        if any(word in desc_lower for word in ['气象', '环境']):
            info['device_types'].append('气象')
        
        # 测量类型
        if any(word in desc_lower for word in ['电压']):
            info['measurement_kinds'].append('电压')
        if any(word in desc_lower for word in ['电流']):
            info['measurement_kinds'].append('电流')
        if any(word in desc_lower for word in ['功率']):
            if '有功' in desc_lower:
                info['measurement_kinds'].append('有功功率')
            elif '无功' in desc_lower:
                info['measurement_kinds'].append('无功功率')
            else:
                info['measurement_kinds'].append('功率')
        if any(word in desc_lower for word in ['能量', '电能']):
            info['measurement_kinds'].append('电能')
        
        # 流向
        if any(word in desc_lower for word in ['正向', '充电']):
            info['flow_directions'].append('正向')
        if any(word in desc_lower for word in ['反向', '放电']):
            info['flow_directions'].append('反向')
        if any(word in desc_lower for word in ['净', '双向']):
            info['flow_directions'].append('净值')
        
        # 相位
        if 'a相' in desc_lower:
            info['phases'].append('A相')
        if 'b相' in desc_lower:
            info['phases'].append('B相')
        if 'c相' in desc_lower:
            info['phases'].append('C相')
        if '三相' in desc_lower:
            info['phases'].append('三相')
        
        # 时间周期
        if any(word in desc_lower for word in ['15分钟', '15min']):
            info['time_periods'].append('15分钟')
        if any(word in desc_lower for word in ['5分钟', '5min']):
            info['time_periods'].append('5分钟')
        if any(word in desc_lower for word in ['小时']):
            info['time_periods'].append('1小时')
        
        # 单位
        unit_patterns = [
            (r'\bkwh?\b', 'kWh'),
            (r'\bmwh?\b', 'MWh'), 
            (r'\bwh?\b', 'Wh'),
            (r'\bkw\b', 'kW'),
            (r'\bmw\b', 'MW'),
            (r'\bw\b', 'W'),
            (r'\bv\b', 'V'),
            (r'\ba\b', 'A'),
            (r'\bhz\b', 'Hz'),
            (r'°c\b', '°C')
        ]
        
        for pattern, unit in unit_patterns:
            if re.search(pattern, desc_lower):
                info['units'].append(unit)
        
        # 行为
        if any(word in desc_lower for word in ['累积', '累计', '总']):
            info['behaviors'].append('累积')
        if any(word in desc_lower for word in ['瞬时', '当前', '实时']):
            info['behaviors'].append('瞬时')
        if any(word in desc_lower for word in ['间隔', '区间']):
            info['behaviors'].append('间隔')
        
        return info
    
    def suggest_missing_fields(self, analysis: Dict[str, int], description: str) -> List[str]:
        """建议可能缺失的字段设置
        
        Args:
            analysis: 当前分析结果
            description: 原始描述
            
        Returns:
            建议列表
        """
        suggestions = []
        
        # 检查是否需要设置相位
        if (analysis.get('field_7') in [37, 53, 15, 54, 4] and  # 电量相关
            analysis.get('field_13') == 0):  # 没有设置相位
            suggestions.append("建议指定相位信息 (A相/B相/C相/三相)")
        
        # 检查是否需要设置时间周期
        if (analysis.get('field_7') == 12 and  # 能量
            analysis.get('field_3') == 0 and  # 没有设置周期
            '瞬时' not in description.lower()):
            suggestions.append("建议指定时间周期 (15分钟/5分钟/1小时)")
        
        # 检查是否需要设置流向
        if (analysis.get('field_7') in [12, 37] and  # 电能或功率
            analysis.get('field_5') == 0):  # 没有设置流向
            suggestions.append("建议指定流向 (正向/反向/净值)")
        
        # 检查是否需要设置累积行为
        if (analysis.get('field_7') == 12 and  # 能量
            analysis.get('field_4') == 6 and  # 默认瞬时
            '瞬时' not in description.lower()):
            suggestions.append("建议指定累积行为 (累积/间隔)")
        
        return suggestions
    
    def validate_field_combination(self, analysis: Dict[str, int]) -> Tuple[bool, List[str]]:
        """验证字段组合的合理性
        
        Args:
            analysis: 字段分析结果
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        # 检查功率类型与单位的匹配
        power_kinds = [37, 53, 15]  # 功率类型
        if (analysis.get('field_7') in power_kinds and
            analysis.get('field_15') not in [38, 0]):  # 不是W或无单位
            errors.append("功率类型应该使用瓦特(W)作为单位")
        
        # 检查能量类型与单位的匹配
        if (analysis.get('field_7') == 12 and  # 能量
            analysis.get('field_15') not in [72, 0]):  # 不是Wh或无单位
            errors.append("能量类型应该使用瓦时(Wh)作为单位")
        
        # 检查电压类型与单位的匹配
        if (analysis.get('field_7') == 54 and  # 电压
            analysis.get('field_15') not in [29, 0]):  # 不是V或无单位
            errors.append("电压类型应该使用伏特(V)作为单位")
        
        # 检查电流类型与单位的匹配
        if (analysis.get('field_7') == 4 and  # 电流
            analysis.get('field_15') not in [5, 0]):  # 不是A或无单位
            errors.append("电流类型应该使用安培(A)作为单位")
        
        # 检查状态类型不应有物理单位
        if (analysis.get('field_7') == 118 and  # 状态
            analysis.get('field_15') not in [0]):  # 有单位
            errors.append("状态类型不应该有物理单位")
        
        return len(errors) == 0, errors