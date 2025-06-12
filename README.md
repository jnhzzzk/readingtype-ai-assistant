# AI Agent 智能助手项目

一个基于DeepSeek API的智能AI助手项目，提供命令行和Web应用两种使用方式。

## 📁 项目结构

```
├── ai-assistant-web/          # 前端Web应用 (Next.js)
├── src/                       # 后端核心模块
│   ├── reading_type_agent.py  # 阅读类型代理
│   ├── semantic_parser.py     # 语义解析器
│   ├── dictionary_manager.py  # 字典管理器
│   └── ...
├── web/                       # 传统Web模板
├── tests/                     # 测试文件
├── simple_ai_agent.py         # 简单AI聊天机器人
├── advanced_ai_agent.py       # 高级AI Agent
├── main.py                    # 主应用入口
├── requirements.txt           # Python依赖
└── README.md                  # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 18+
- DeepSeek API Key

### 1. 克隆仓库

```bash
git clone <repository-url>
cd ai-agent-project
```

### 2. 后端设置

1. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 创建环境配置文件：
   ```bash
   cp env.example .env
   ```

3. 在`.env`文件中添加你的DeepSeek API密钥：
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   ```

### 3. 前端设置

1. 进入前端目录：
   ```bash
   cd ai-assistant-web
   ```

2. 安装依赖并启动：
   ```bash
   ./start.sh
   ```

   或手动执行：
   ```bash
   npm install
   npm run dev
   ```

3. 访问 http://localhost:3000

## 💻 使用方式

### 命令行版本

#### 简单AI聊天机器人
```bash
python simple_ai_agent.py
```

#### 高级AI Agent
```bash
python advanced_ai_agent.py
```

#### 主应用
```bash
python main.py
```

### Web应用版本

启动Web应用后，在浏览器中访问 http://localhost:3000，即可使用图形化界面与AI助手交互。

## 🛠️ 功能特性

### 🤖 AI助手功能
- 智能对话交互
- 流式输出响应
- 上下文记忆
- 多轮对话支持

### 🔧 高级功能
- 工具调用能力
- 语义解析
- 字典管理
- 阅读类型识别

### 🎨 前端特性
- 现代化UI设计
- 响应式布局
- 实时消息传递
- 用户友好界面

## 📚 技术栈

### 后端
- Python 3.8+
- DeepSeek API
- OpenAI兼容接口
- 异步编程支持

### 前端
- Next.js 14
- TypeScript
- TailwindCSS
- 现代React Hooks

## 🔧 开发指南

### 项目架构

1. **后端架构**：
   - `main.py`: 主应用入口
   - `src/`: 核心业务逻辑模块
   - 各种AI Agent实现

2. **前端架构**：
   - Next.js框架
   - 组件化设计
   - API路由处理

### 添加新功能

1. 后端新功能：在`src/`目录下添加新模块
2. 前端新功能：在`ai-assistant-web/src/`下添加组件

## 📝 API文档

项目使用DeepSeek API，兼容OpenAI接口格式。详细API文档请参考DeepSeek官方文档。

## 🤝 贡献指南

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com/) - 提供强大的AI API
- [Next.js](https://nextjs.org/) - 优秀的React框架
- [OpenAI](https://openai.com/) - API接口标准参考

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue：[GitHub Issues](../../issues)
- 邮箱：[您的邮箱]

---

⭐ 如果这个项目对你有帮助，请给它一个星标！ 