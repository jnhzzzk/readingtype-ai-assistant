# AI Agent 项目 - Web应用版本

本项目包含一个基于DeepSeek API的AI助手，提供命令行和Web应用两种使用方式。

## 项目结构

- **命令行版本**:
  - `simple_ai_agent.py`: 简单的AI聊天机器人，能够进行基本对话，使用流式输出。
  - `advanced_ai_agent.py`: 高级AI Agent，具有工具使用能力，可以执行特定任务，并使用流式输出。

- **Web应用版本**:
  - `ai-assistant-web/`: Next.js项目目录
    - 使用现代化的Web技术构建
    - 提供与命令行版本相同的功能
    - 美观友好的界面设计

## 使用方法

### 命令行版本

1. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

2. 运行简单版本:
   ```
   python simple_ai_agent.py
   ```

3. 运行高级版本:
   ```
   python advanced_ai_agent.py
   ```

### Web应用版本

1. 进入web应用目录:
   ```
   cd ai-assistant-web
   ```

2. 运行启动脚本:
   ```
   ./start.sh
   ```

3. 打开浏览器访问: http://localhost:3000

## 技术特点

- 使用DeepSeek API提供强大的AI能力
- 支持流式输出，提供更好的用户体验
- 多种访问方式，适合不同场景和用户需求
- 开放的结构便于扩展和定制

## 注意事项

- 确保已设置有效的DeepSeek API密钥
- Web应用必须在Node.js环境下运行
- 命令行版本需要Python 3.8+环境 