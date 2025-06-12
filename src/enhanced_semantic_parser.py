import re
import json
from typing import Dict, List, Optional, Tuple, Set
from difflib import SequenceMatcher
from collections import defaultdict

class EnhancedSemanticParser:
    """增强版语义解析器，提供更准确的ReadingType字段值解析"""
    
    def __init__(self, dictionary_manager=None):
        self.dictionary_manager = dictionary_manager
        
        # ReadingType字段定义
        self.field_names = [
            "macroPeriod", "aggregate", "measurePeriod", "accumulationBehaviour",
            "flowDirection", "commodity", "measurementKind", "harmonic",
            "argumentNumerator", "TOU", "cpp", "tier", "phase", "multiplier", "uom", "currency"
        ]
        
        # 初始化增强的关键词映射
        self.enhanced_mappings = self._init_enhanced_mappings()
        
        # 同义词词典
        self.synonyms = self._init_synonyms()
        
        # 上下文规则
        self.context_rules = self._init_context_rules()
        
        # 字段依赖关系
        self.field_dependencies = self._init_field_dependencies()
    
    def _init_enhanced_mappings(self) -> Dict:
        """初始化增强的关键词映射规则"""
        return {
            'commodity': {
                'patterns': [
                    # 电力相关
                    {'value': 1, 'keywords': ['电', '电力', '电能', '电压', '电流', '功率'], 'weight': 10},
                    {'value': 1, 'keywords': ['electricity', 'electric', 'power', 'voltage', 'current'], 'weight': 8},
                    
                    # 储能相关
                    {'value': 41, 'keywords': ['储能', '电池', 'PCS', '充电', '放电'], 'weight': 15},
                    {'value': 41, 'keywords': ['battery', 'energy storage', 'pcs', 'charge', 'discharge'], 'weight': 12},
                    
                    # 水相关
                    {'value': 4, 'keywords': ['水'], 'weight': 10},
                    {'value': 4, 'keywords': ['water'], 'weight': 8},
                    
                    # 气体相关
                    {'value': 7, 'keywords': ['气', '天然气', '燃气'], 'weight': 10},
                    {'value': 7, 'keywords': ['gas', 'natural gas'], 'weight': 8},
                    
                    # 热能相关
                    {'value': 6, 'keywords': ['热', '蒸汽', '热能'], 'weight': 10},
                    {'value': 6, 'keywords': ['heat', 'steam', 'thermal'], 'weight': 8},
                    
                    # 气象相关
                    {'value': 40, 'keywords': ['气象', '环境', '天气', '温度', '湿度', '风速'], 'weight': 12},
                    {'value': 40, 'keywords': ['weather', 'environment', 'temperature', 'humidity'], 'weight': 10}
                ],
                'default': 1
            },
            
            'measurementKind': {
                'patterns': [
                    # 电压相关
                    {'value': 54, 'keywords': ['电压', '电位', '线电压', '相电压'], 'weight': 15},
                    {'value': 158, 'keywords': ['单相电压', '相电压'], 'weight': 16},
                    {'value': 54, 'keywords': ['voltage', 'potential'], 'weight': 12},
                    
                    # 电流相关
                    {'value': 4, 'keywords': ['电流'], 'weight': 15},
                    {'value': 4, 'keywords': ['current'], 'weight': 12},
                    
                    # 功率相关
                    {'value': 37, 'keywords': ['有功功率', '有功'], 'weight': 16},
                    {'value': 53, 'keywords': ['无功功率', '无功'], 'weight': 16},
                    {'value': 15, 'keywords': ['视在功率', '视在'], 'weight': 16},
                    {'value': 37, 'keywords': ['active power'], 'weight': 13},
                    {'value': 53, 'keywords': ['reactive power'], 'weight': 13},
                    {'value': 15, 'keywords': ['apparent power'], 'weight': 13},
                    
                    # 能量相关
                    {'value': 12, 'keywords': ['能量', '电能', '电度'], 'weight': 15},
                    {'value': 12, 'keywords': ['energy'], 'weight': 12},
                    
                    # 频率相关
                    {'value': 46, 'keywords': ['频率'], 'weight': 15},
                    {'value': 46, 'keywords': ['frequency'], 'weight': 12},
                    
                    # 温度相关
                    {'value': 139, 'keywords': ['温度'], 'weight': 15},
                    {'value': 139, 'keywords': ['temperature'], 'weight': 12},
                    
                    # 状态相关
                    {'value': 118, 'keywords': ['状态', '告警', '报警', '开关', '遥信'], 'weight': 14},
                    {'value': 183, 'keywords': ['充电状态', '放电状态'], 'weight': 16},
                    {'value': 904, 'keywords': ['远方', '就地', '本地'], 'weight': 14},
                    {'value': 11, 'keywords': ['并网', '离网'], 'weight': 14},
                    
                    # 容量相关
                    {'value': 119, 'keywords': ['容量', 'soc', '荷电状态'], 'weight': 15},
                    
                    # 功率因数
                    {'value': 38, 'keywords': ['功率因数', '功因'], 'weight': 16},
                    
                    # 控制系数
                    {'value': 121, 'keywords': ['控制系数'], 'weight': 16}
                ],
                'default': 0
            },
            
            'flowDirection': {
                'patterns': [
                    {'value': 1, 'keywords': ['正向', '充电', '进', '输入', '送电'], 'weight': 15},
                    {'value': 19, 'keywords': ['反向', '放电', '出', '输出', '回电'], 'weight': 15},
                    {'value': 4, 'keywords': ['净', '双向', '净值'], 'weight': 14},
                    {'value': 20, 'keywords': ['充放电', 'pcs'], 'weight': 16}
                ],
                'default': 0
            },
            
            'accumulationBehaviour': {
                'patterns': [
                    {'value': 3, 'keywords': ['累积', '累计', '总', '合计'], 'weight': 15},
                    {'value': 6, 'keywords': ['瞬时', '当前', '实时', '即时'], 'weight': 15},
                    {'value': 4, 'keywords': ['间隔', '区间', '差值'], 'weight': 14},
                    {'value': 1, 'keywords': ['容量', '总量'], 'weight': 13},
                    {'value': 10, 'keywords': ['计划'], 'weight': 12}
                ],
                'default': 6
            },
            
            'measurePeriod': {
                'patterns': [
                    {'value': 2, 'keywords': ['15分钟', '15min'], 'weight': 18},
                    {'value': 6, 'keywords': ['5分钟', '5min'], 'weight': 18},
                    {'value': 3, 'keywords': ['1分钟', '1min'], 'weight': 18},
                    {'value': 7, 'keywords': ['60分钟', '1小时', '小时'], 'weight': 16},
                    {'value': 4, 'keywords': ['24小时', '日', '天'], 'weight': 15},
                    {'value': 0, 'keywords': ['瞬时', '实时', '无周期'], 'weight': 14}
                ],
                'default': 0
            },
            
            'phase': {
                'patterns': [
                    {'value': 128, 'keywords': ['a相', '甲相'], 'weight': 18},
                    {'value': 64, 'keywords': ['b相', '乙相'], 'weight': 18},
                    {'value': 32, 'keywords': ['c相', '丙相'], 'weight': 18},
                    {'value': 224, 'keywords': ['三相', '总', '合计'], 'weight': 16},
                    {'value': 225, 'keywords': ['平均'], 'weight': 15}
                ],
                'default': 0
            },
            
            'multiplier': {
                'patterns': [
                    {'value': 3, 'keywords': ['k', 'kw', 'kwh', '千'], 'weight': 15},
                    {'value': 6, 'keywords': ['m', 'mw', 'mwh', '兆'], 'weight': 15},
                    {'value': 0, 'keywords': ['基本', '基础'], 'weight': 10}
                ],
                'default': 0
            },
            
            'uom': {
                'patterns': [
                    {'value': 72, 'keywords': ['wh', '瓦时', '电能'], 'weight': 16},
                    {'value': 38, 'keywords': ['w', '瓦', '功率'], 'weight': 16},
                    {'value': 29, 'keywords': ['v', '伏', '电压'], 'weight': 16},
                    {'value': 5, 'keywords': ['a', '安', '电流'], 'weight': 16},
                    {'value': 23, 'keywords': ['hz', '赫兹', '频率'], 'weight': 16},
                    {'value': 109, 'keywords': ['°c', '摄氏度', '温度'], 'weight': 15},
                    {'value': 0, 'keywords': ['无单位', '状态', '比率'], 'weight': 12}
                ],
                'default': 0
            }
        }
    
    def _init_synonyms(self) -> Dict[str, Set[str]]:
        """初始化同义词词典"""
        return {
            '电力': {'电', '电能', '电量', '电度'},
            '功率': {'power', '瓦', 'w'},
            '电压': {'voltage', '伏', 'v', '电位'},
            '电流': {'current', '安', 'a'},
            '频率': {'frequency', 'hz', '赫兹'},
            '温度': {'temperature', '温', '摄氏', '华氏'},
            '瞬时': {'实时', '当前', '即时', '现时'},
            '累积': {'累计', '总计', '合计', '总'},
            '三相': {'三相制', '三相系统'},
            '储能': {'电池', '蓄电池', '储电'},
            '充电': {'充', '进电', '输入'},
            '放电': {'放', '出电', '输出'}
        }
    
    def _init_context_rules(self) -> List[Dict]:
        """初始化上下文规则"""
        return [
            # 储能相关组合
            {
                'conditions': ['储能', 'pcs'],
                'field_updates': {
                    'commodity': 41,
                    'flowDirection': 20
                }
            },
            
            # 电能表相关
            {
                'conditions': ['电能', '累积'],
                'field_updates': {
                    'commodity': 1,
                    'measurementKind': 12,
                    'accumulationBehaviour': 3,
                    'uom': 72
                }
            },
            
            # 功率表相关
            {
                'conditions': ['功率', '瞬时'],
                'field_updates': {
                    'commodity': 1,
                    'accumulationBehaviour': 6,
                    'uom': 38
                }
            },
            
            # 气象站相关
            {
                'conditions': ['温度', '环境'],
                'field_updates': {
                    'commodity': 40,
                    'measurementKind': 139,
                    'uom': 109
                }
            }
        ]
    
    def _init_field_dependencies(self) -> Dict[str, List[Tuple[str, Dict]]]:
        """初始化字段依赖关系"""
        return {
            'measurementKind': [
                # 电能 -> Wh单位
                (12, {'uom': 72}),
                # 功率 -> W单位
                (37, {'uom': 38}),
                (53, {'uom': 38}),
                (15, {'uom': 38}),
                # 电压 -> V单位
                (54, {'uom': 29}),
                # 电流 -> A单位
                (4, {'uom': 5}),
                # 频率 -> Hz单位
                (46, {'uom': 23}),
                # 温度 -> °C单位
                (139, {'uom': 109})
            ],
            
            'commodity': [
                # 储能 -> 充放电流向
                (41, {'flowDirection': 20})
            ]
        }
    
    def analyze_description_enhanced(self, description: str) -> Tuple[Dict[str, int], float]:
        """增强版描述分析，返回结果和置信度
        
        Args:
            description: 用户输入的描述
            
        Returns:
            (字段值字典, 置信度分数 0-1)
        """
        # 预处理文本
        processed_text = self._preprocess_text(description)
        
        # 初始化分析结果
        analysis = {f"field_{i+1}": 0 for i in range(16)}
        confidence_scores = {}
        
        # 1. 基于模式匹配的分析
        pattern_results = self._analyze_with_patterns(processed_text)
        
        # 2. 应用上下文规则
        context_results = self._apply_context_rules(processed_text, pattern_results)
        
        # 3. 应用字段依赖关系
        final_results = self._apply_field_dependencies(context_results)
        
        # 4. 计算置信度
        total_confidence = self._calculate_confidence(processed_text, final_results)
        
        # 转换为最终格式
        for i, field_name in enumerate(self.field_names):
            field_key = f"field_{i+1}"
            if field_name in final_results:
                analysis[field_key] = final_results[field_name]['value']
                confidence_scores[field_key] = final_results[field_name]['confidence']
        
        return analysis, total_confidence
    
    def _preprocess_text(self, text: str) -> str:
        """预处理文本"""
        # 转换为小写
        text = text.lower()
        
        # 标准化单位
        unit_replacements = {
            'kw': 'k w', 'mw': 'm w', 'kwh': 'k wh', 'mwh': 'm wh',
            'kv': 'k v', 'mv': 'm v', 'ka': 'k a', 'ma': 'm a'
        }
        
        for old, new in unit_replacements.items():
            text = text.replace(old, new)
        
        # 同义词替换
        for main_word, synonyms in self.synonyms.items():
            for synonym in synonyms:
                text = text.replace(synonym, main_word)
        
        return text
    
    def _analyze_with_patterns(self, text: str) -> Dict[str, Dict]:
        """基于模式匹配进行分析"""
        results = {}
        
        for field_name, mapping in self.enhanced_mappings.items():
            best_match = {'value': mapping['default'], 'confidence': 0.1, 'matched_keywords': []}
            
            for pattern in mapping['patterns']:
                matched_keywords = []
                total_weight = 0
                
                for keyword in pattern['keywords']:
                    if keyword in text:
                        matched_keywords.append(keyword)
                        # 计算权重，考虑关键词长度和完整匹配
                        weight = pattern['weight'] * len(keyword)
                        if f" {keyword} " in text:  # 完整词匹配额外加权
                            weight *= 1.5
                        total_weight += weight
                
                if matched_keywords:
                    confidence = min(0.95, total_weight / 100)  # 归一化置信度
                    if confidence > best_match['confidence']:
                        best_match = {
                            'value': pattern['value'],
                            'confidence': confidence,
                            'matched_keywords': matched_keywords
                        }
            
            results[field_name] = best_match
        
        return results
    
    def _apply_context_rules(self, text: str, pattern_results: Dict) -> Dict:
        """应用上下文规则"""
        results = pattern_results.copy()
        
        for rule in self.context_rules:
            # 检查是否满足条件
            conditions_met = all(condition in text for condition in rule['conditions'])
            
            if conditions_met:
                # 应用字段更新
                for field_name, value in rule['field_updates'].items():
                    if field_name in results:
                        # 提升置信度
                        results[field_name]['value'] = value
                        results[field_name]['confidence'] = min(0.95, results[field_name]['confidence'] + 0.2)
                        results[field_name]['matched_keywords'].extend(rule['conditions'])
        
        return results
    
    def _apply_field_dependencies(self, results: Dict) -> Dict:
        """应用字段依赖关系"""
        updated_results = results.copy()
        
        for field_name, dependencies in self.field_dependencies.items():
            if field_name in results:
                current_value = results[field_name]['value']
                
                for dep_value, updates in dependencies:
                    if current_value == dep_value:
                        for update_field, update_value in updates.items():
                            if update_field in updated_results:
                                # 如果依赖字段的置信度较低，则应用更新
                                if updated_results[update_field]['confidence'] < 0.7:
                                    updated_results[update_field]['value'] = update_value
                                    updated_results[update_field]['confidence'] = 0.8
        
        return updated_results
    
    def _calculate_confidence(self, text: str, results: Dict) -> float:
        """计算总体置信度"""
        confidences = [result['confidence'] for result in results.values() if result['confidence'] > 0.1]
        
        if not confidences:
            return 0.1
        
        # 计算加权平均置信度
        avg_confidence = sum(confidences) / len(confidences)
        
        # 根据识别的字段数量调整
        recognized_fields = len([r for r in results.values() if r['confidence'] > 0.3])
        field_bonus = min(0.2, recognized_fields * 0.05)
        
        return min(0.95, avg_confidence + field_bonus)
    
    def enhanced_fuzzy_search(self, field_name: str, search_term: str, 
                            threshold: float = 0.6) -> List[Tuple[Dict, float]]:
        """增强的模糊搜索功能
        
        Args:
            field_name: 字段名
            search_term: 搜索词
            threshold: 相似度阈值
            
        Returns:
            [(字典项, 相似度分数)] 列表
        """
        if not self.dictionary_manager or field_name not in self.dictionary_manager.field_dictionaries:
            return []
        
        results = []
        search_lower = search_term.lower()
        
        # 预处理搜索词
        processed_search = self._preprocess_text(search_term)
        
        for item in self.dictionary_manager.field_dictionaries[field_name]:
            scores = []
            
            # 1. 显示名称匹配
            display_name = str(item['display_name']).lower()
            scores.append(SequenceMatcher(None, search_lower, display_name).ratio())
            
            # 2. 描述匹配
            description = str(item.get('description', '')).lower()
            if description:
                scores.append(SequenceMatcher(None, search_lower, description).ratio() * 0.8)
            
            # 3. 关键词匹配
            for keyword in processed_search.split():
                if keyword in display_name:
                    scores.append(0.9)
                if keyword in description:
                    scores.append(0.7)
            
            # 4. 值精确匹配
            if str(item['value']) == search_term:
                scores.append(1.0)
            
            # 取最高分
            max_score = max(scores) if scores else 0
            
            if max_score >= threshold:
                results.append((item, max_score))
        
        # 按相似度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def suggest_alternatives(self, analysis: Dict[str, int], confidence: float) -> List[str]:
        """基于置信度建议替代方案"""
        suggestions = []
        
        if confidence < 0.5:
            suggestions.append("⚠️ 解析置信度较低，建议：")
            suggestions.append("1. 提供更详细的描述")
            suggestions.append("2. 使用标准术语（如：有功功率、三相电压等）")
            suggestions.append("3. 明确设备类型和测量内容")
        
        elif confidence < 0.7:
            suggestions.append("💡 为提高准确性，建议补充：")
            
            # 检查关键字段是否为默认值
            key_fields = ['commodity', 'measurementKind', 'accumulationBehaviour']
            for i, field_name in enumerate(self.field_names):
                if field_name in key_fields:
                    field_key = f"field_{i+1}"
                    if analysis[field_key] == 0:
                        chinese_name = self._get_field_chinese_name(field_name)
                        suggestions.append(f"- 明确{chinese_name}信息")
        
        return suggestions
    
    def _get_field_chinese_name(self, field_name: str) -> str:
        """获取字段中文名"""
        chinese_names = {
            "commodity": "商品类型",
            "measurementKind": "测量类型",
            "accumulationBehaviour": "累积行为",
            "flowDirection": "流向",
            "measurePeriod": "测量周期",
            "phase": "相位",
            "multiplier": "乘数",
            "uom": "单位"
        }
        return chinese_names.get(field_name, field_name)
    
    def export_analysis_report(self, description: str, analysis: Dict[str, int], 
                             confidence: float) -> str:
        """导出分析报告"""
        report = []
        report.append("📊 编码分析报告")
        report.append("=" * 50)
        report.append(f"📝 输入描述: {description}")
        report.append(f"🎯 置信度: {confidence:.2%}")
        report.append("")
        
        # 构建ReadingTypeID
        values = [str(analysis[f"field_{i+1}"]) for i in range(16)]
        reading_type_id = "-".join(values)
        report.append(f"🔢 生成编码: {reading_type_id}")
        report.append("")
        
        # 字段详情
        report.append("📋 字段解析详情:")
        for i, field_name in enumerate(self.field_names):
            field_key = f"field_{i+1}"
            value = analysis[field_key]
            if value != 0:  # 只显示非零字段
                chinese_name = self._get_field_chinese_name(field_name)
                field_desc = self._get_field_value_description(field_name, value)
                report.append(f"  {chinese_name}: {value} ({field_desc})")
        
        # 建议
        suggestions = self.suggest_alternatives(analysis, confidence)
        if suggestions:
            report.append("")
            report.extend(suggestions)
        
        return "\n".join(report)
    
    def _get_field_value_description(self, field_name: str, value: int) -> str:
        """获取字段值描述"""
        if self.dictionary_manager:
            return self.dictionary_manager.get_field_description(field_name, str(value))
        return f"值: {value}"
    
    def build_reading_type_id(self, field_values: Dict[str, int]) -> str:
        """构建ReadingTypeID字符串"""
        values = []
        for i in range(16):
            field_key = f"field_{i+1}"
            values.append(str(field_values.get(field_key, 0)))
        return "-".join(values)
    
    def parse_reading_type_id(self, reading_type_id: str) -> Dict[str, int]:
        """解析ReadingTypeID字符串
        
        Args:
            reading_type_id: ReadingTypeID字符串，格式如 "0-0-2-6-1-1-37-0-0-0-0-0-224-3-38-0"
            
        Returns:
            字段值字典 {field_1: value1, field_2: value2, ...}
        """
        parts = reading_type_id.split('-')
        
        if len(parts) != 16:
            raise ValueError(f"ReadingTypeID格式错误，应包含16个字段，实际包含{len(parts)}个")
        
        field_values = {}
        for i, value in enumerate(parts):
            try:
                field_values[f"field_{i+1}"] = int(value)
            except ValueError:
                raise ValueError(f"字段{i+1}的值'{value}'不是有效的整数")
        
        return field_values 