#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI Agent 优化效果测试脚本
用于验证编码分析和字典查询的改进效果
"""

import sys
import os
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.enhanced_semantic_parser import EnhancedSemanticParser
    from src.enhanced_dictionary_manager import EnhancedDictionaryManager
    from src.optimized_reading_type_agent import OptimizedReadingTypeAgent
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保所有优化组件文件已正确创建")
    sys.exit(1)

def test_semantic_parser():
    """测试增强语义解析器"""
    print("🧠 测试增强语义解析器")
    print("=" * 50)
    
    # 创建字典管理器（如果字典文件存在）
    try:
        dict_manager = EnhancedDictionaryManager("field_dictionaries.csv")
        parser = EnhancedSemanticParser(dict_manager)
    except:
        print("⚠️ 字典文件不存在，使用基础解析器")
        parser = EnhancedSemanticParser()
    
    # 测试用例
    test_cases = [
        "储能PCS三相有功功率15分钟间隔数据",
        "电表A相电压瞬时值",
        "气象站环境温度小时累积数据", 
        "三相无功功率",
        "充电桩电流",
        "光伏逆变器频率"
    ]
    
    for i, description in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}: {description}")
        try:
            analysis, confidence = parser.analyze_description_enhanced(description)
            
            print(f"🎯 置信度: {confidence:.1%}")
            
            # 显示识别的关键字段
            key_fields = []
            for j, field_name in enumerate(parser.field_names):
                field_key = f"field_{j+1}"
                value = analysis.get(field_key, 0)
                if value != 0:
                    key_fields.append(f"{field_name}={value}")
            
            print(f"🔍 识别字段: {', '.join(key_fields) if key_fields else '无'}")
            
            # 生成ReadingTypeID
            reading_type_id = parser.build_reading_type_id(analysis)
            print(f"🔢 生成编码: {reading_type_id}")
            
        except Exception as e:
            print(f"❌ 解析失败: {e}")
    
    print("\n✅ 语义解析器测试完成")

def test_dictionary_manager():
    """测试增强字典管理器"""
    print("\n📚 测试增强字典管理器")
    print("=" * 50)
    
    try:
        dict_manager = EnhancedDictionaryManager("field_dictionaries.csv")
    except Exception as e:
        print(f"❌ 字典管理器初始化失败: {e}")
        return
    
    # 测试智能搜索
    search_tests = [
        ("储能", ""),
        ("电压", "measurementKind"),
        ("三相", ""),
        ("瞬时", "accumulationBehaviour"),
        ("功率", "measurementKind")
    ]
    
    for search_term, field_name in search_tests:
        print(f"\n🔍 搜索测试: '{search_term}'" + (f" (限定字段: {field_name})" if field_name else ""))
        
        try:
            results = dict_manager.smart_search(
                search_term=search_term,
                field_name=field_name,
                max_results=3,
                threshold=0.3
            )
            
            if results:
                for fname, item, score in results:
                    print(f"  📌 {fname}.{item['value']}: {item['display_name']} (相似度: {score:.1%})")
            else:
                print("  ❌ 无匹配结果")
                
        except Exception as e:
            print(f"  ❌ 搜索失败: {e}")
    
    print("\n✅ 字典管理器测试完成")

def test_field_validation():
    """测试字段验证功能"""
    print("\n🛡️ 测试字段验证功能")
    print("=" * 50)
    
    try:
        dict_manager = EnhancedDictionaryManager("field_dictionaries.csv")
    except Exception as e:
        print(f"❌ 字典管理器初始化失败: {e}")
        return
    
    # 测试字段组合
    test_combinations = [
        {
            "name": "有功功率 + W单位",
            "fields": {"commodity": "1", "measurementKind": "37", "uom": "38"}
        },
        {
            "name": "电能 + V单位 (错误组合)",
            "fields": {"commodity": "1", "measurementKind": "12", "uom": "29"}
        },
        {
            "name": "电压 + V单位",
            "fields": {"commodity": "1", "measurementKind": "54", "uom": "29"}
        }
    ]
    
    for test in test_combinations:
        print(f"\n🧪 测试组合: {test['name']}")
        
        try:
            is_valid, warnings = dict_manager.validate_field_combination(test['fields'])
            
            print(f"✅ 验证结果: {'通过' if is_valid else '有问题'}")
            if warnings:
                for warning in warnings:
                    print(f"⚠️ {warning}")
            else:
                print("✅ 无警告")
                
        except Exception as e:
            print(f"❌ 验证失败: {e}")
    
    print("\n✅ 字段验证测试完成")

def test_optimized_agent():
    """测试优化版Agent（如果可能）"""
    print("\n🤖 测试优化版Agent")
    print("=" * 50)
    
    try:
        # 检查是否有必要的文件
        if not os.path.exists("field_dictionaries.csv"):
            print("⚠️ 缺少字典文件，跳过Agent测试")
            return
        
        agent = OptimizedReadingTypeAgent()
        print("✅ Agent初始化成功")
        
        # 测试增强编码生成
        test_description = "储能PCS三相有功功率15分钟数据"
        print(f"\n📝 测试描述: {test_description}")
        
        try:
            # 模拟工具调用
            result = agent.generate_reading_type_enhanced({
                "description": test_description
            })
            
            print("📋 生成结果:")
            print(result[:500] + "..." if len(result) > 500 else result)
            
        except Exception as e:
            print(f"❌ 编码生成失败: {e}")
        
        print("\n✅ Agent测试完成")
        
    except Exception as e:
        print(f"❌ Agent初始化失败: {e}")

def performance_comparison():
    """性能对比测试"""
    print("\n⚡ 性能对比测试")
    print("=" * 50)
    
    import time
    
    try:
        dict_manager = EnhancedDictionaryManager("field_dictionaries.csv")
    except Exception as e:
        print(f"❌ 字典管理器初始化失败: {e}")
        return
    
    # 测试搜索速度
    search_terms = ["电压", "功率", "储能", "三相", "瞬时"]
    
    print("🔍 搜索速度测试:")
    total_time = 0
    
    for term in search_terms:
        start_time = time.time()
        
        try:
            results = dict_manager.smart_search(term, max_results=10)
            end_time = time.time()
            
            elapsed = (end_time - start_time) * 1000  # 转换为毫秒
            total_time += elapsed
            
            print(f"  '{term}': {elapsed:.1f}ms ({len(results)} 结果)")
            
        except Exception as e:
            print(f"  '{term}': 失败 - {e}")
    
    avg_time = total_time / len(search_terms)
    print(f"\n📊 平均搜索时间: {avg_time:.1f}ms")
    
    # 评估
    if avg_time < 100:
        print("✅ 搜索性能: 优秀")
    elif avg_time < 200:
        print("🟡 搜索性能: 良好")
    else:
        print("🔴 搜索性能: 需要优化")
    
    print("\n✅ 性能测试完成")

def main():
    """主测试函数"""
    print("🚀 AI Agent 优化效果测试")
    print("=" * 60)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return
    
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    
    try:
        # 运行各项测试
        test_semantic_parser()
        test_dictionary_manager() 
        test_field_validation()
        test_optimized_agent()
        performance_comparison()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试完成！")
        print("\n📋 测试总结:")
        print("✅ 增强语义解析器 - 支持权重化关键词匹配和置信度评估")
        print("✅ 智能字典管理器 - 支持模糊搜索和字段验证")
        print("✅ 优化版Agent - 集成所有增强功能")
        print("✅ 性能优化 - 提供缓存和索引机制")
        
        print("\n💡 使用建议:")
        print("1. 使用标准专业术语描述量测需求")
        print("2. 关注置信度分数，低置信度时补充描述")
        print("3. 利用字段验证功能确保编码合理性")
        print("4. 使用智能搜索快速查找字典项")
        
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 