# ReadingType编码智能助手系统

基于AI的IEC61968-9-2024标准ReadingType编码生成和管理系统，包含后端AI Agent和前端Web界面。

## 项目概述

这是一个专门用于处理ReadingType编码的智能系统，遵循IEC61968-9-2024国际标准，提供编码生成、解析、验证等功能。

### 主要功能

- 🚀 **智能编码生成**: 基于自然语言描述生成符合标准的ReadingType编码
- 🔍 **编码解析**: 将编码转换为可读的描述信息
- ✅ **规范性验证**: 检查编码是否符合IEC61968-9-2024标准
- 🛑 **流式交互**: 支持实时AI响应和用户控制
- 📊 **字典管理**: 完整的字段字典和数据库支持

## 项目结构

```
├── src/                          # 后端核心代码
│   ├── reading_type_agent.py    # 主要AI Agent
│   ├── enhanced_semantic_parser.py # 语义解析器
│   ├── enhanced_dictionary_manager.py # 字典管理器
│   └── optimized_reading_type_agent.py # 优化版本
├── ai-assistant-web/            # 前端Web应用
│   ├── src/app/                 # Next.js页面和API
│   ├── src/components/          # React组件
│   └── src/lib/                 # 工具库
├── web/                         # 简单Web界面
├── tests/                       # 测试文件
├── data/                        # 数据文件
│   ├── field_dictionaries.xml   # 字段字典
│   ├── reading_type_codes.csv   # 编码数据
│   └── *.xlsx                   # IEC标准文档
└── requirements.txt             # Python依赖
```

## ReadingType编码标准

基于IEC61968-9-2024标准的16字段编码结构：

| 字段 | 名称 | 说明 | 示例值 |
|------|------|------|---------|
| 1 | macroPeriod | 宏周期 | 0=无，1=年，2=月，3=日，4=时 |
| 2 | aggregate | 聚合 | 0=无，1=最大，2=最小，3=平均，4=总和 |
| 3 | measurePeriod | 测量周期 | 0=无，1=秒，2=分，3=时，4=日 |
| 4 | accumulationBehaviour | 累积行为 | 0=无，1=累积，2=差值，3=瞬时 |
| 5 | flowDirection | 流向 | 0=无，1=正向，2=反向，3=净值，19=全部 |
| 6 | commodity | 商品 | 0=无，1=电能，2=燃气，3=水，4=时间 |
| 7 | measurementKind | 测量类型 | 0=无，12=电流，13=电压，37=功率，38=电能 |
| 8 | harmonic | 谐波 | 0=无，1=基波，2=谐波 |
| 9 | argumentNumerator | 参数分子 | 0=无，1=A相，2=B相，3=C相 |
| 10 | TOU | 分时 | 0=无，1=峰时，2=平时，3=谷时 |
| 11 | cpp | 关键峰值价格 | 0=无 |
| 12 | tier | 阶梯 | 0=无，1=第一阶梯，2=第二阶梯 |
| 13 | phase | 相位 | 0=无，1=A相，2=B相，3=C相，64=三相 |
| 14 | multiplier | 乘数 | 0=1，3=1000，6=1000000 |
| 15 | uom | 单位 | 0=无，5=安培，29=伏特，38=瓦特，72=瓦时 |
| 16 | currency | 货币 | 0=无，978=人民币 |

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 18+
- DeepSeek API密钥

### 后端设置

1. 安装Python依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
```bash
cp env.example .env
# 编辑.env文件，添加DEEPSEEK_API_KEY
```

3. 运行后端AI Agent：
```bash
python main.py                    # 基础版本
python reading_type_agent.py      # 完整版本
python advanced_ai_agent.py       # 高级功能
```

### 前端设置

1. 进入前端目录：
```bash
cd ai-assistant-web
```

2. 安装依赖：
```bash
npm install
```

3. 设置环境变量：
```bash
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env.local
```

4. 启动开发服务器：
```bash
npm run dev
```

5. 访问应用：http://localhost:3000

## 使用示例

### 编码生成
```
用户: 生成A相电压量测的ReadingType编码
助手: 分析您的需求：A相电压量测
建议编码: 0.0.0.3.0.1.13.0.1.0.0.0.1.0.29.0
```

### 编码解析
```
用户: 解析编码 0.0.0.3.0.1.13.0.1.0.0.0.1.0.29.0
助手: 这是一个A相电压瞬时量测编码，单位为伏特...
```

### 字典查询
```
用户: 查询measurementKind字段
助手: measurementKind字段的可选值：
12: 电流 (Current)
13: 电压 (Voltage)
37: 功率 (Power)
38: 电能 (Energy)
```

## 技术架构

### 后端技术栈
- **Python 3.8+**: 核心开发语言
- **DeepSeek API**: AI推理服务
- **XML/CSV**: 数据存储格式
- **正则表达式**: 编码解析和验证

### 前端技术栈
- **Next.js 15**: React全栈框架
- **TypeScript**: 类型安全
- **Tailwind CSS**: 样式框架
- **React Hooks**: 状态管理
- **Heroicons**: 图标库

### AI功能
- **语义解析**: 理解用户自然语言需求
- **智能推荐**: 基于上下文的字段推荐
- **规范验证**: 确保编码符合IEC标准
- **流式交互**: 实时响应和控制

## 开发和测试

### 运行测试
```bash
python -m pytest tests/           # 运行所有测试
python test_optimization.py       # 性能测试
python final_compare.py          # 功能对比测试
```

### 代码规范
项目遵循Python PEP8和TypeScript/React最佳实践。

## 部署

### 生产构建
```bash
# 前端
cd ai-assistant-web
npm run build
npm start

# 后端
python reading_type_agent.py --production
```

### Docker部署
```bash
# 构建镜像
docker build -t readingtype-agent .

# 运行容器
docker run -p 3000:3000 -p 8000:8000 readingtype-agent
```

## 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 更新日志

详见各模块的README文件：
- [后端Agent说明](README_Agent.md)
- [前端Web说明](README-WEB.md)
- [优化指南](OPTIMIZATION_GUIDE.md)

## 联系方式

如有问题或建议，请提交Issue或联系开发团队。 