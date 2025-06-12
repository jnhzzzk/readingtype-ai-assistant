import os
from openai import OpenAI
from dotenv import load_dotenv
import sys

# 加载环境变量
load_dotenv()

# 设置DeepSeek API密钥
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class SimpleAIAgent:
    def __init__(self):
        self.conversation_history = []
        # 使用OpenAI客户端，配置DeepSeek基础URL
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        
    def add_message(self, role, content):
        """添加消息到对话历史"""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_response(self, user_input, stream=True):
        """获取AI的回复"""
        # 添加用户输入到对话历史
        self.add_message("user", user_input)
        
        try:
            # 调用DeepSeek API获取回复，启用流式输出
            response = self.client.chat.completions.create(
                model="deepseek-chat",  # DeepSeek-V3模型
                messages=self.conversation_history,
                stream=stream
            )
            
            # 处理流式响应
            if stream:
                full_response = ""
                print("\nAI助手: ", end="", flush=True)
                
                for chunk in response:
                    if chunk.choices and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.content
                        if content:
                            print(content, end="", flush=True)
                            full_response += content
                
                print()  # 换行
                ai_response = full_response
            else:
                # 非流式响应处理
                ai_response = response.choices[0].message.content
                
            # 将AI回复添加到对话历史
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
    print("简单AI助手 (输入'退出'结束对话)")
    print("确保您已在.env文件中设置了DEEPSEEK_API_KEY")
    
    # 创建AI助手实例
    agent = SimpleAIAgent()
    
    # 设置系统消息
    agent.add_message("system", "你是一个有帮助的AI助手，可以回答问题并协助用户完成任务。")
    
    # 对话循环
    while True:
        user_input = input("\n你: ")
        
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("再见!")
            break
        
        if user_input.strip() == "":
            continue
        
        # 获取AI回复（流式输出，不需要额外打印）
        agent.get_response(user_input)


if __name__ == "__main__":
    main() 