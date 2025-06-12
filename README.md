# ReadingType编码助手

基于Next.js的智能ReadingType编码生成和管理系统，遵循IEC61968-9-2024国际标准。

## 功能特性

### 🚀 智能生成
- 基于自然语言描述生成编码
- AI自动分析量测类型、设备类型、相位等关键信息
- 字段组合验证和规范性检查
- 缺失字段智能补全建议

### 🛑 流式控制
- 支持流式AI响应
- 实时显示生成过程
- 一键终止生成功能
- 用户完全控制交互体验

### 🔧 编码解析
- ReadingTypeID解析为可读描述
- 字段含义解释
- 编码规范性验证

## ReadingType编码结构

基于IEC61968-9-2024标准的16字段编码：

1. **macroPeriod** - 宏周期（0=无，1=年，2=月，3=日，4=时）
2. **aggregate** - 聚合（0=无，1=最大，2=最小，3=平均，4=总和）
3. **measurePeriod** - 测量周期（0=无，1=秒，2=分，3=时，4=日）
4. **accumulationBehaviour** - 累积行为（0=无，1=累积，2=差值，3=瞬时）
5. **flowDirection** - 流向（0=无，1=正向，2=反向，3=净值，19=全部）
6. **commodity** - 商品（0=无，1=电能，2=燃气，3=水，4=时间）
7. **measurementKind** - 测量类型（0=无，12=电流，13=电压，37=功率，38=电能）
8. **harmonic** - 谐波（0=无，1=基波，2=谐波）
9. **argumentNumerator** - 参数分子（0=无，1=A相，2=B相，3=C相）
10. **TOU** - 分时（0=无，1=峰时，2=平时，3=谷时）
11. **cpp** - 关键峰值价格（0=无）
12. **tier** - 阶梯（0=无，1=第一阶梯，2=第二阶梯）
13. **phase** - 相位（0=无，1=A相，2=B相，3=C相，64=三相）
14. **multiplier** - 乘数（0=1，3=1000，6=1000000）
15. **uom** - 单位（0=无，5=安培，29=伏特，38=瓦特，72=瓦时）
16. **currency** - 货币（0=无，978=人民币）

## 快速开始

### 环境要求
- Node.js 18+
- npm 或 yarn

### 安装依赖
```bash
npm install
```

### 环境配置
创建 `.env.local` 文件并添加DeepSeek API密钥：
```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 启动开发服务器
```bash
npm run dev
```

应用将在 http://localhost:3000 启动。

### 生产构建
```bash
npm run build
npm start
```

## 使用示例

### 搜索编码
```
用户: 搜索电压量测编码
助手: 为您找到相关的电压量测编码...
```

### 生成编码
```
用户: 生成A相电压量测的ReadingType编码
助手: 分析您的需求：A相电压量测
建议编码: 0.0.0.3.0.1.13.0.1.0.0.0.1.0.29.0
```

### 查询字典
```
用户: 查询measurementKind字段
助手: measurementKind字段（测量类型）的可选值：
12: 电流
13: 电压
37: 功率
38: 电能
...
```

## 技术架构

- **前端**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **后端**: Next.js API Routes
- **AI服务**: DeepSeek API
- **UI组件**: Heroicons, react-markdown

## 项目结构

```
ai-assistant-web/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── api/chat/          # API路由
│   │   ├── globals.css        # 全局样式
│   │   ├── layout.tsx         # 应用布局
│   │   └── page.tsx           # 主页面
│   ├── components/            # React组件
│   │   ├── ChatInterface.tsx  # 聊天界面
│   │   ├── ChatMessage.tsx    # 消息组件
│   │   ├── ChatInput.tsx      # 输入组件
│   │   ├── QuickActions.tsx   # 快速操作面板
│   │   └── ReadingTypeCard.tsx # 编码卡片组件
│   └── lib/                   # 工具库
│       └── chat-service.ts    # 聊天服务
├── public/                    # 静态资源
├── package.json              # 项目配置
└── README.md                 # 项目说明
```

## 开发团队

基于原有的AI助手前端工程改造，专门适配ReadingType编码应用场景。

## 许可证

MIT License
