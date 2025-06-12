import os
import json
from openai import OpenAI
import datetime
import requests
from dotenv import load_dotenv
import sys

# 加载环境变量
load_dotenv()

# 设置DeepSeek API密钥
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class AdvancedAIAgent:
    def __init__(self):
        self.conversation_history = []
        # 使用OpenAI客户端，配置DeepSeek基础URL
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        self.available_tools = {
            "get_current_time": self.get_current_time,
            "search_weather": self.search_weather,
            "calculate": self.calculate
        }
    
    def add_message(self, role, content):
        """添加消息到对话历史"""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_current_time(self, args=None):
        """获取当前时间的工具"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"当前时间是: {current_time}"
    
    def search_weather(self, args):
        """获取天气信息的工具 (模拟)"""
        city = args.get("city", "北京")
        return f"模拟天气数据: {city}，晴天，温度22°C"
    
    def calculate(self, args):
        """简单计算器工具"""
        expression = args.get("expression", "")
        try:
            # 警告: eval函数在生产环境中存在安全风险，这里仅用于演示
            result = eval(expression)
            return f"计算结果: {expression} = {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"
    
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
                        "name": "get_current_time",
                        "description": "获取当前系统时间",
                        "parameters": {"type": "object", "properties": {}}
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search_weather",
                        "description": "获取指定城市的天气信息",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city": {
                                    "type": "string",
                                    "description": "要查询天气的城市名称"
                                }
                            },
                            "required": ["city"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "calculate",
                        "description": "计算数学表达式",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "expression": {
                                    "type": "string",
                                    "description": "要计算的数学表达式，例如 '2 + 2'"
                                }
                            },
                            "required": ["expression"]
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
                print("\nAI助手正在思考...")
                
                # 添加助手的响应到对话历史
                self.add_message("assistant", response_message)
                
                # 处理每个工具调用
                for tool_call in response_message.tool_calls:
                    function_info = {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                    tool_result = self.handle_function_call(function_info)
                    print(f"工具使用: {tool_call.function.name} - {tool_result}")
                
                # 再次调用API获取最终回复，这次使用流式输出
                if stream:
                    print("\nAI助手: ", end="", flush=True)
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
                    print(f"\nAI助手: {ai_response}")
                
                self.add_message("assistant", ai_response)
            else:
                # 没有工具调用，直接返回回复
                if stream:
                    # 由于已经获取了非流式响应，直接打印
                    ai_response = response_message.content
                    print(f"\nAI助手: {ai_response}")
                else:
                    ai_response = response_message.content
                    print(f"\nAI助手: {ai_response}")
                
                self.add_message("assistant", ai_response)
            
            return ai_response
        
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            print(f"\nAI助手: {error_msg}")
            return error_msg

    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []


def main():
    print("高级AI助手 (输入'退出'结束对话)")
    print("这个助手有工具使用能力，可以执行特定任务")
    print("确保您已在.env文件中设置了DEEPSEEK_API_KEY")
    
    # 创建AI助手实例
    agent = AdvancedAIAgent()
    
    # 设置系统消息
    agent.add_message("system", "你是一个有帮助的AI助手，能够使用工具来完成任务。你可以获取当前时间、查询天气信息和进行简单计算。")
    
    # 对话循环
    while True:
        user_input = input("\n你: ")
        
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("再见!")
            break
        
        if user_input.strip() == "":
            continue
        
        # 获取AI回复（内部已处理输出）
        agent.get_response(user_input)


if __name__ == "__main__":
    main() 