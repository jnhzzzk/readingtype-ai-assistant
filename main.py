#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.reading_type_agent import ReadingTypeAgent

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="ReadingTypeID智能编码助手")
    parser.add_argument("--stream", action="store_true", default=True,
                       help="启用流式输出 (默认开启)")
    parser.add_argument("--no-stream", action="store_true",
                       help="禁用流式输出")
    
    args = parser.parse_args()
    
    # 处理流式输出参数
    stream = args.stream and not args.no_stream
    
    print("🚀 ReadingTypeID智能编码助手")
    print("=" * 60)
    print("💡 我可以帮您:")
    print("   • 搜索现有的ReadingType编码")
    print("   • 根据描述生成新的ReadingTypeID")
    print("   • 查询字段字典信息")
    print("   • 管理和浏览编码库")
    print("   • 导出数据和统计信息")
    print("\n📝 支持自然语言对话，输入'退出'结束对话")
    print("🔍 示例:")
    print("   - '搜索有功电能'")
    print("   - '生成储能充电功率编码'")
    print("   - '查看编码库'")
    print("   - '查询commodity字段'")
    print("=" * 60)
    
    # 创建AI助手实例
    try:
        agent = ReadingTypeAgent()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("请检查:")
        print("1. DEEPSEEK_API_KEY环境变量是否设置")
        print("2. 数据文件是否存在 (reading_type_codes.csv, field_dictionaries.csv)")
        print("3. 网络连接是否正常")
        return 1
    
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
当用户询问字典信息时，提供清晰的字段说明。

可用的工具函数：
- search_reading_type: 搜索编码库
- generate_reading_type: 生成新编码
- query_dictionary: 查询字典
- view_codes_library: 浏览编码库
- filter_codes: 筛选编码
- add_to_library: 添加编码
- export_data: 导出数据
- get_statistics: 获取统计信息""")
    
    # 显示数据库状态
    stats = agent.database.get_statistics()
    print(f"\n📊 数据库状态: {stats['total_codes']}个编码, {len(agent.dictionary.field_dictionaries)}个字段")
    
    # 对话循环
    while True:
        try:
            user_input = input("\n💬 您: ").strip()
            
            if user_input.lower() in ["退出", "exit", "quit", "再见", "bye"]:
                print("👋 再见！感谢使用ReadingTypeID编码助手!")
                break
            
            if user_input == "":
                continue
            
            # 特殊命令处理
            if user_input.lower() in ["清除历史", "clear", "重置"]:
                agent.clear_history()
                print("🧹 对话历史已清除")
                continue
            
            if user_input.lower() in ["帮助", "help", "?"]:
                print_help()
                continue
            
            # 获取AI回复
            agent.get_response(user_input, stream=stream)
            
        except KeyboardInterrupt:
            print("\n👋 再见！感谢使用ReadingTypeID编码助手!")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            print("请重试或输入'退出'结束程序")

def print_help():
    """显示帮助信息"""
    print("\n📖 ReadingTypeID助手使用指南")
    print("=" * 50)
    print("🔍 搜索功能:")
    print("   '搜索 有功电能' - 搜索现有编码")
    print("   '查找 储能' - 模糊搜索相关编码")
    
    print("\n🤖 生成功能:")
    print("   '生成 三相有功功率编码' - 根据描述生成")
    print("   '我需要电压测量编码' - 自然语言生成")
    
    print("\n📚 浏览功能:")
    print("   '查看编码库' - 浏览所有编码")
    print("   '查看表计类编码' - 按类别查看")
    
    print("\n📖 字典功能:")
    print("   '查询字典' - 查看所有字段")
    print("   '查询commodity字段' - 查看具体字段值")
    
    print("\n📊 管理功能:")
    print("   '统计信息' - 查看数据库统计")
    print("   '导出数据' - 导出编码库")
    
    print("\n🔧 系统命令:")
    print("   '清除历史' - 清除对话历史")
    print("   '帮助' - 显示此帮助")
    print("   '退出' - 退出程序")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code if exit_code else 0) 