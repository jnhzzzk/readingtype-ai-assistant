from typing import Dict, List, Optional, Tuple, Set
import csv
import datetime
import json
from difflib import SequenceMatcher
import re
from collections import defaultdict

class EnhancedDictionaryManager:
    """增强版ReadingType字典管理类"""
    
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
        
        # 构建反向索引
        self.build_reverse_index()
        
        # 初始化同义词
        self.synonyms = self._init_synonyms()
        
        # 缓存常用查询结果
        self.query_cache = {}
    
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
    
    def build_reverse_index(self):
        """构建反向索引，用于快速查找"""
        self.value_to_field = {}  # 值 -> 字段名列表
        self.keyword_to_items = defaultdict(list)  # 关键词 -> 项目列表
        
        for field_name, items in self.field_dictionaries.items():
            for item in items:
                # 构建值索引
                value = str(item['value'])
                if value not in self.value_to_field:
                    self.value_to_field[value] = []
                self.value_to_field[value].append((field_name, item))
                
                # 构建关键词索引
                keywords = self._extract_keywords(item['display_name'] + ' ' + str(item.get('description', '')))
                for keyword in keywords:
                    self.keyword_to_items[keyword].append((field_name, item))
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """从文本中提取关键词"""
        # 清理文本
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text.lower())
        
        # 分词
        words = set()
        for word in text.split():
            if len(word) >= 2:  # 过滤太短的词
                words.add(word)
        
        return words
    
    def _init_synonyms(self) -> Dict[str, Set[str]]:
        """初始化同义词词典"""
        return {
            '电力': {'电', '电能', '电量', '电度', 'electricity', 'electric'},
            '功率': {'power', '瓦', 'w', '有功', '无功', '视在'},
            '电压': {'voltage', '伏', 'v', '电位', 'potential'},
            '电流': {'current', '安', 'a'},
            '频率': {'frequency', 'hz', '赫兹'},
            '温度': {'temperature', '温', '摄氏', '华氏', '°c', '°f'},
            '瞬时': {'实时', '当前', '即时', '现时', 'instantaneous'},
            '累积': {'累计', '总计', '合计', '总', 'cumulative'},
            '正向': {'充电', '进', '输入', '送电', 'forward'},
            '反向': {'放电', '出', '输出', '回电', 'reverse'},
            '三相': {'三相制', '三相系统', 'three phase'},
            '储能': {'电池', '蓄电池', '储电', 'battery', 'energy storage'},
            '状态': {'告警', '报警', '开关', '遥信', 'status', 'alarm'}
        }
    
    def smart_search(self, search_term: str, field_name: str = "", 
                    max_results: int = 10, threshold: float = 0.3) -> List[Tuple[str, Dict, float]]:
        """智能搜索功能
        
        Args:
            search_term: 搜索词
            field_name: 指定字段名（可选）
            max_results: 最大结果数
            threshold: 相似度阈值
            
        Returns:
            [(字段名, 字典项, 相似度分数)] 列表
        """
        # 检查缓存
        cache_key = f"{search_term}_{field_name}_{max_results}_{threshold}"
        if cache_key in self.query_cache:
            return self.query_cache[cache_key]
        
        results = []
        search_lower = search_term.lower()
        
        # 预处理搜索词（同义词扩展）
        expanded_terms = self._expand_with_synonyms(search_lower)
        
        # 确定搜索范围
        target_fields = [field_name] if field_name else self.field_dictionaries.keys()
        
        for fname in target_fields:
            if fname not in self.field_dictionaries:
                continue
            
            for item in self.field_dictionaries[fname]:
                score = self._calculate_item_score(expanded_terms, item)
                
                if score >= threshold:
                    results.append((fname, item, score))
        
        # 排序并限制结果数量
        results.sort(key=lambda x: x[2], reverse=True)
        results = results[:max_results]
        
        # 缓存结果
        self.query_cache[cache_key] = results
        
        return results
    
    def _expand_with_synonyms(self, search_term: str) -> Set[str]:
        """使用同义词扩展搜索词"""
        expanded = {search_term}
        
        for main_word, synonyms in self.synonyms.items():
            if search_term in synonyms or search_term == main_word.lower():
                expanded.update(synonyms)
                expanded.add(main_word.lower())
        
        return expanded
    
    def _calculate_item_score(self, search_terms: Set[str], item: Dict) -> float:
        """计算项目的相关性分数"""
        display_name = str(item['display_name']).lower()
        description = str(item.get('description', '')).lower()
        value = str(item['value'])
        
        scores = []
        
        # 1. 精确值匹配（最高优先级）
        for term in search_terms:
            if term == value:
                scores.append(1.0)
        
        # 2. 显示名称匹配
        for term in search_terms:
            if term in display_name:
                # 完整词匹配
                if f" {term} " in f" {display_name} ":
                    scores.append(0.9)
                else:
                    scores.append(0.7)
            
            # 模糊匹配
            similarity = SequenceMatcher(None, term, display_name).ratio()
            if similarity > 0.6:
                scores.append(similarity * 0.8)
        
        # 3. 描述匹配
        if description:
            for term in search_terms:
                if term in description:
                    scores.append(0.6)
                
                # 模糊匹配描述
                similarity = SequenceMatcher(None, term, description).ratio()
                if similarity > 0.5:
                    scores.append(similarity * 0.5)
        
        # 4. 关键词匹配
        item_keywords = self._extract_keywords(display_name + ' ' + description)
        for term in search_terms:
            if term in item_keywords:
                scores.append(0.5)
        
        return max(scores) if scores else 0.0
    
    def get_field_suggestions(self, partial_name: str) -> List[Tuple[str, str]]:
        """获取字段名建议
        
        Args:
            partial_name: 部分字段名
            
        Returns:
            [(英文名, 中文名)] 列表
        """
        suggestions = []
        partial_lower = partial_name.lower()
        
        for eng_name, chi_name in self.chinese_field_names.items():
            if (partial_lower in eng_name.lower() or 
                partial_lower in chi_name or
                SequenceMatcher(None, partial_lower, eng_name.lower()).ratio() > 0.6):
                suggestions.append((eng_name, chi_name))
        
        return suggestions
    
    def get_value_context(self, field_name: str, value: str) -> Dict:
        """获取字段值的上下文信息
        
        Args:
            field_name: 字段名
            value: 字段值
            
        Returns:
            上下文信息字典
        """
        if field_name not in self.field_dictionaries:
            return {}
        
        # 找到匹配项
        target_item = None
        for item in self.field_dictionaries[field_name]:
            if str(item['value']) == str(value):
                target_item = item
                break
        
        if not target_item:
            return {}
        
        # 构建上下文
        context = {
            'current': target_item,
            'field_chinese_name': self.chinese_field_names.get(field_name, field_name),
            'related_values': [],
            'usage_examples': []
        }
        
        # 查找相关值（数值相近或功能相似）
        try:
            current_val = float(str(value).replace('–', '-'))
            for item in self.field_dictionaries[field_name]:
                try:
                    item_val = float(str(item['value']).replace('–', '-'))
                    if abs(item_val - current_val) <= 5 and item_val != current_val:
                        context['related_values'].append(item)
                except:
                    continue
        except:
            # 非数值字段，基于关键词查找相关项
            target_keywords = self._extract_keywords(target_item['display_name'])
            for item in self.field_dictionaries[field_name]:
                if item['value'] != target_item['value']:
                    item_keywords = self._extract_keywords(item['display_name'])
                    if target_keywords & item_keywords:  # 有共同关键词
                        context['related_values'].append(item)
        
        # 限制相关值数量
        context['related_values'] = context['related_values'][:5]
        
        return context
    
    def validate_field_combination(self, field_values: Dict[str, str]) -> Tuple[bool, List[str]]:
        """验证字段组合的合理性
        
        Args:
            field_values: 字段值字典 {field_name: value}
            
        Returns:
            (是否有效, 警告信息列表)
        """
        warnings = []
        is_valid = True
        
        # 1. 检查基本字段完整性
        required_fields = ['commodity', 'measurementKind']
        for field in required_fields:
            if field not in field_values or field_values[field] == '0':
                warnings.append(f"建议设置{self.chinese_field_names.get(field, field)}字段")
        
        # 2. 检查字段逻辑一致性
        commodity = field_values.get('commodity', '0')
        measurement_kind = field_values.get('measurementKind', '0')
        uom = field_values.get('uom', '0')
        
        # 电力相关检查
        if commodity == '1':  # 电力
            power_measurements = ['37', '53', '15']  # 有功功率、无功功率、视在功率
            if measurement_kind in power_measurements and uom != '38':  # W单位
                warnings.append("功率测量建议使用瓦特(W)单位")
            
            if measurement_kind == '12' and uom != '72':  # 电能应该用Wh
                warnings.append("电能测量建议使用瓦时(Wh)单位")
            
            if measurement_kind == '54' and uom != '29':  # 电压应该用V
                warnings.append("电压测量建议使用伏特(V)单位")
        
        # 3. 检查累积行为与测量类型的匹配
        accumulation = field_values.get('accumulationBehaviour', '0')
        if measurement_kind == '12':  # 电能
            if accumulation not in ['1', '3']:  # 应该是容量或累积
                warnings.append("电能测量建议使用累积或容量累积行为")
        elif measurement_kind in ['37', '53', '15', '54', '4']:  # 功率、电压、电流
            if accumulation != '6':  # 应该是瞬时
                warnings.append("功率/电压/电流测量建议使用瞬时累积行为")
        
        return is_valid, warnings
    
    def export_enhanced_report(self, field_name: str = "") -> str:
        """导出增强版字典报告"""
        report = []
        report.append("📚 ReadingType字典增强报告")
        report.append("=" * 60)
        
        if field_name:
            # 单字段详细报告
            if field_name not in self.field_dictionaries:
                return f"❌ 字段 '{field_name}' 不存在"
            
            items = self.field_dictionaries[field_name]
            chinese_name = self.chinese_field_names.get(field_name, field_name)
            
            report.append(f"🔍 字段: {field_name} ({chinese_name})")
            report.append(f"📊 总计: {len(items)} 个值")
            report.append("")
            
            # 统计信息
            custom_count = sum(1 for item in items if item.get('is_custom', False))
            standard_count = len(items) - custom_count
            
            report.append("📈 统计信息:")
            report.append(f"  标准值: {standard_count}")
            report.append(f"  自定义值: {custom_count}")
            report.append("")
            
            # 值分布
            report.append("📋 值列表:")
            sorted_items = sorted(items, key=lambda x: float(str(x['value']).replace('–', '-')))
            
            for i, item in enumerate(sorted_items[:20]):  # 显示前20个
                marker = "🔧" if item.get('is_custom', False) else "📌"
                report.append(f"  {marker} {item['value']}: {item['display_name']}")
                if item.get('description'):
                    report.append(f"    📝 {item['description'][:100]}...")
            
            if len(items) > 20:
                report.append(f"  ... 还有 {len(items) - 20} 个值")
        
        else:
            # 全局统计报告
            total_items = sum(len(items) for items in self.field_dictionaries.values())
            total_custom = sum(sum(1 for item in items if item.get('is_custom', False)) 
                             for items in self.field_dictionaries.values())
            
            report.append(f"📊 总体统计:")
            report.append(f"  字段数量: {len(self.field_dictionaries)}")
            report.append(f"  总值数量: {total_items}")
            report.append(f"  自定义值: {total_custom}")
            report.append("")
            
            # 各字段统计
            report.append("📋 各字段统计:")
            for field_name, items in self.field_dictionaries.items():
                chinese_name = self.chinese_field_names.get(field_name, field_name)
                custom_count = sum(1 for item in items if item.get('is_custom', False))
                report.append(f"  {field_name} ({chinese_name}): {len(items)} 个值 ({custom_count} 自定义)")
        
        return "\n".join(report)
    
    def get_field_usage_statistics(self) -> Dict[str, Dict]:
        """获取字段使用统计"""
        stats = {}
        
        for field_name, items in self.field_dictionaries.items():
            stats[field_name] = {
                'total_values': len(items),
                'custom_values': sum(1 for item in items if item.get('is_custom', False)),
                'standard_values': sum(1 for item in items if not item.get('is_custom', False)),
                'chinese_name': self.chinese_field_names.get(field_name, field_name),
                'most_common_values': self._get_most_common_values(items)
            }
        
        return stats
    
    def _get_most_common_values(self, items: List[Dict], top_k: int = 5) -> List[Dict]:
        """获取最常用的值（基于描述复杂度等启发式规则）"""
        # 简单启发式：描述较短且不是自定义的值通常是常用值
        scored_items = []
        
        for item in items:
            score = 0
            
            # 非自定义值加分
            if not item.get('is_custom', False):
                score += 10
            
            # 描述简洁加分
            desc_len = len(str(item.get('description', '')))
            if desc_len < 50:
                score += 5
            elif desc_len < 100:
                score += 3
            
            # 显示名称简洁加分
            name_len = len(str(item['display_name']))
            if name_len < 20:
                score += 3
            
            scored_items.append((item, score))
        
        # 排序并返回前k个
        scored_items.sort(key=lambda x: x[1], reverse=True)
        return [item for item, score in scored_items[:top_k]]
    
    def clear_cache(self):
        """清除查询缓存"""
        self.query_cache.clear()
    
    def rebuild_index(self):
        """重建索引"""
        self.build_reverse_index()
        self.clear_cache()
    
    def get_field_description(self, field_name: str, value: str) -> str:
        """获取字段值的描述"""
        if field_name in self.field_dictionaries:
            for item in self.field_dictionaries[field_name]:
                if str(item['value']) == str(value):
                    return item['display_name']
        return f"值: {value}" 