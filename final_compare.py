#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from collections import OrderedDict

def parse_xml_dictionaries(xml_file):
    """解析XML文件中的字典数据"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    dictionaries = {}
    
    for dictionary in root.findall('Dictionary'):
        dict_name = dictionary.get('name')
        items = OrderedDict()
        
        for item in dictionary.findall('Item'):
            key = item.get('key')
            value = item.get('value')
            is_custom = item.get('is_custom', 'False')
            comment = item.get('comment', '')
            
            items[key] = {
                'value': value,
                'is_custom': is_custom,
                'comment': comment
            }
        
        dictionaries[dict_name] = items
    
    return dictionaries

def parse_excel_main_dict(excel_file, sheet_name='Reading types dict.'):
    """解析Excel主要字典数据"""
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    dictionaries = {}
    
    num_cols = len(df.columns)
    dict_index = 1
    
    # 每3列为一个字典
    for start_col in range(0, num_cols, 3):
        if start_col + 2 >= num_cols:
            break
            
        # 从第一行获取字典名称
        dict_name_cell = df.iloc[0, start_col + 1]
        dict_name = str(dict_name_cell).strip()
        
        if dict_name and dict_name != 'nan':
            # 清洁字典名称，移除换行符和多余空格
            dict_name = dict_name.replace('\n', ' ').strip()
            
            items = OrderedDict()
            
            # 从第二行开始读取数据
            for i in range(1, len(df)):
                key_cell = df.iloc[i, start_col]
                value_cell = df.iloc[i, start_col + 1]
                comment_cell = df.iloc[i, start_col + 2] if start_col + 2 < num_cols else ''
                
                # 检查是否有有效的键和值
                if pd.notna(key_cell) and pd.notna(value_cell):
                    key = str(key_cell).strip()
                    value = str(value_cell).strip()
                    comment = str(comment_cell).strip() if pd.notna(comment_cell) else ''
                    
                    if key and value and key != 'nan' and value != 'nan':
                        items[key] = {
                            'value': value,
                            'comment': comment,
                            'is_custom': 'False'
                        }
            
            if items:
                dictionaries[dict_name] = items
                print(f"解析字典 '{dict_name}': {len(items)} 个条目")
        
        dict_index += 1
    
    return dictionaries

def parse_excel_other_dict(excel_file, sheet_name='Other dict.'):
    """解析Excel其他字典数据"""
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    dictionaries = {}
    
    # 定义三个字典的列映射
    dict_mappings = [
        {
            'name': 'argumentNumerator',
            'key_col': 0,
            'value_col': 1,
            'comment_col': 2
        },
        {
            'name': 'cpp',
            'key_col': 3,
            'value_col': 4,
            'comment_col': 5
        },
        {
            'name': 'currency',
            'key_col': 6,
            'value_col': 7,
            'comment_col': 8
        }
    ]
    
    for mapping in dict_mappings:
        dict_name = mapping['name']
        items = OrderedDict()
        
        for i in range(1, len(df)):  # 跳过标题行
            key_cell = df.iloc[i, mapping['key_col']]
            value_cell = df.iloc[i, mapping['value_col']]
            comment_cell = df.iloc[i, mapping['comment_col']] if mapping['comment_col'] < len(df.columns) else ''
            
            if pd.notna(key_cell) and pd.notna(value_cell):
                key = str(key_cell).strip()
                value = str(value_cell).strip()
                comment = str(comment_cell).strip() if pd.notna(comment_cell) else ''
                
                if key and value and key != 'nan' and value != 'nan':
                    items[key] = {
                        'value': value,
                        'comment': comment,
                        'is_custom': 'False'
                    }
        
        if items:
            dictionaries[dict_name] = items
            print(f"解析字典 '{dict_name}': {len(items)} 个条目")
    
    return dictionaries

def analyze_key_gaps(keys_dict, dict_name):
    """分析键的间隔"""
    numeric_keys = []
    non_numeric_keys = []
    
    for key in keys_dict.keys():
        try:
            if '.' in key:
                numeric_keys.append(float(key))
            else:
                numeric_keys.append(int(key))
        except ValueError:
            non_numeric_keys.append(key)
    
    gaps = []
    if numeric_keys:
        numeric_keys.sort()
        for i in range(len(numeric_keys) - 1):
            curr = numeric_keys[i]
            next_val = numeric_keys[i + 1]
            if isinstance(curr, int) and isinstance(next_val, int):
                if next_val - curr > 1:
                    missing_count = int(next_val - curr - 1)
                    missing_keys = [str(curr + j) for j in range(1, missing_count + 1)]
                    gaps.append({
                        'start': curr,
                        'end': next_val,
                        'missing_keys': missing_keys
                    })
    
    return gaps, non_numeric_keys

def compare_dictionaries(xml_dicts, excel_dicts):
    """比较XML和Excel字典"""
    print("\n" + "="*60)
    print("字典比较结果")
    print("="*60)
    
    xml_names = set(xml_dicts.keys())
    excel_names = set(excel_dicts.keys())
    
    print(f"\nXML中的字典数量: {len(xml_names)}")
    print(f"Excel中的字典数量: {len(excel_names)}")
    
    # 字典名称映射（处理名称差异）
    name_mapping = {
        'macroPeriod 宏周期': 'macroPeriod',
        'aggregate 聚合方式': 'aggregate',
        'measurePeriod 测量周期': 'measurePeriod',
        'accumulationBehaviour 累积行为': 'accumulationBehaviour',
        'flowDirection 流向': 'flowDirection',
        'commodity 商品类型': 'commodity',
        'measurementKind 测量类型': 'measurementKind',
        'harmonic 谐波': 'harmonic',
        'argumentNumerator 分子参数': 'argumentNumerator',
        'TOU 分时电价': 'TOU',
        'cpp 临界峰值': 'cpp',
        '16.phaseN 相位': '16.phaseN',
        'multiplier 乘数': 'multiplier',
        'uom 计量单位': 'uom',
        'currency 货币计量单位': 'currency'
    }
    
    # 反向映射
    reverse_mapping = {v: k for k, v in name_mapping.items()}
    
    print(f"\nXML字典名称:")
    for name in sorted(xml_names):
        print(f"  - {name}")
    
    print(f"\nExcel字典名称:")
    for name in sorted(excel_names):
        print(f"  - {name}")
    
    # 比较每个字典
    all_issues = []
    
    for xml_name in sorted(xml_names):
        # 查找对应的Excel字典
        excel_name = None
        if xml_name in excel_names:
            excel_name = xml_name
        else:
            # 尝试通过映射查找
            for excel_n in excel_names:
                if (excel_n in name_mapping and name_mapping[excel_n] == xml_name) or \
                   (xml_name in reverse_mapping and reverse_mapping[xml_name] == excel_n):
                    excel_name = excel_n
                    break
        
        if excel_name:
            issues = compare_single_dictionary(xml_dicts[xml_name], excel_dicts[excel_name], xml_name)
            all_issues.extend(issues)
        else:
            print(f"\n⚠️  警告: 字典 '{xml_name}' 在Excel中未找到对应项")
            all_issues.append(f"字典 '{xml_name}' 在Excel中缺失")
    
    # 检查Excel中独有的字典
    for excel_name in excel_names:
        xml_name = None
        if excel_name in xml_names:
            continue
        else:
            # 尝试通过映射查找
            found = False
            for xml_n in xml_names:
                if (excel_name in name_mapping and name_mapping[excel_name] == xml_n) or \
                   (xml_n in reverse_mapping and reverse_mapping[xml_n] == excel_name):
                    found = True
                    break
            if not found:
                print(f"\n⚠️  警告: 字典 '{excel_name}' 在XML中未找到对应项")
                all_issues.append(f"字典 '{excel_name}' 在XML中缺失")
    
    # 汇总问题
    print(f"\n" + "="*60)
    print("问题汇总")
    print("="*60)
    if all_issues:
        for i, issue in enumerate(all_issues, 1):
            print(f"{i}. {issue}")
    else:
        print("✅ 未发现明显问题")

def compare_single_dictionary(xml_dict, excel_dict, dict_name):
    """比较单个字典"""
    print(f"\n--- 比较字典: {dict_name} ---")
    
    xml_keys = set(xml_dict.keys())
    excel_keys = set(excel_dict.keys())
    
    print(f"XML条目数: {len(xml_keys)}")
    print(f"Excel条目数: {len(excel_keys)}")
    
    issues = []
    
    # 检查缺失的键
    xml_only = xml_keys - excel_keys
    excel_only = excel_keys - xml_keys
    common_keys = xml_keys & excel_keys
    
    if xml_only:
        print(f"❌ 只在XML中存在的键 ({len(xml_only)}):")
        for key in sorted(xml_only, key=lambda x: float(x) if x.replace('.', '').isdigit() else float('inf')):
            print(f"    {key}: {xml_dict[key]['value']}")
            issues.append(f"字典 '{dict_name}' 缺少键 {key}")
    
    if excel_only:
        print(f"⚠️  只在Excel中存在的键 ({len(excel_only)}):")
        for key in sorted(excel_only, key=lambda x: float(x) if x.replace('.', '').isdigit() else float('inf')):
            print(f"    {key}: {excel_dict[key]['value']}")
            issues.append(f"字典 '{dict_name}' 多出键 {key}")
    
    # 检查值差异
    value_diffs = []
    for key in common_keys:
        xml_val = xml_dict[key]['value']
        excel_val = excel_dict[key]['value']
        if xml_val != excel_val:
            value_diffs.append((key, xml_val, excel_val))
    
    if value_diffs:
        print(f"⚠️  值不同的键 ({len(value_diffs)}):")
        for key, xml_val, excel_val in value_diffs[:5]:
            print(f"    {key}: XML='{xml_val}' ≠ Excel='{excel_val}'")
            issues.append(f"字典 '{dict_name}' 键 {key} 值不同")
        if len(value_diffs) > 5:
            print(f"    ... 还有 {len(value_diffs) - 5} 个值差异")
    
    # 分析键的间隔
    gaps, non_numeric = analyze_key_gaps(xml_dict, dict_name)
    if gaps:
        print(f"⚠️  XML中发现键间隔:")
        for gap in gaps[:3]:
            print(f"    {gap['start']} -> {gap['end']} (缺少: {', '.join(gap['missing_keys'])})")
            issues.append(f"字典 '{dict_name}' 键序列中断: {gap['start']} -> {gap['end']}")
    
    if not xml_only and not excel_only and not value_diffs and not gaps:
        print("✅ 该字典无问题")
    
    return issues

def main():
    xml_file = 'field_dictionaries.xml'
    excel_file = '02量测配置（IEC61968-9-2024版）.xlsx'
    
    print("开始解析文件...")
    
    # 解析XML
    xml_dicts = parse_xml_dictionaries(xml_file)
    print(f"\nXML解析完成，共 {len(xml_dicts)} 个字典")
    
    # 解析Excel
    print(f"\n解析Excel主字典...")
    excel_main_dicts = parse_excel_main_dict(excel_file)
    
    print(f"\n解析Excel其他字典...")
    excel_other_dicts = parse_excel_other_dict(excel_file)
    
    # 合并Excel字典
    excel_dicts = {**excel_main_dicts, **excel_other_dicts}
    print(f"\nExcel解析完成，共 {len(excel_dicts)} 个字典")
    
    # 比较字典
    compare_dictionaries(xml_dicts, excel_dicts)

if __name__ == "__main__":
    main() 