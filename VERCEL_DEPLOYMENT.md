# Vercel 部署指南

本项目已针对 Vercel 平台进行了优化，可以直接部署运行。

## 🚀 快速部署

### 1. 连接 GitHub 仓库

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 导入 GitHub 仓库：`https://github.com/jnhzzzk/readingtype-ai-assistant`

### 2. 配置环境变量

在 Vercel 项目设置中添加以下环境变量：

```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 3. 部署设置

Vercel 会自动识别这是一个 Next.js 项目并进行部署：

- **框架**: Next.js
- **构建命令**: `npm run build`
- **输出目录**: `.next`
- **安装命令**: `npm install`

## 📁 项目结构

```
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat/           # 原有聊天 API（兼容性）
│   │   │   └── readingtype/    # 新的 ReadingType API
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/             # React 组件
│   └── lib/                   # 工具库
├── public/                    # 静态资源
├── package.json              # 项目配置
├── vercel.json               # Vercel 配置
└── README.md                 # 项目说明
```

## 🔧 API 架构

### Next.js API Routes

项目使用 Next.js API Routes 替代了原有的 Python 后端：

- `/api/readingtype` - 主要的 ReadingType 编码处理 API
- `/api/chat` - 兼容性聊天 API

### 核心功能

1. **编码生成**: 基于自然语言描述生成 ReadingType 编码
2. **AI 对话**: 集成 DeepSeek API 进行智能对话
3. **字段解析**: 解析和验证 ReadingType 字段

## 🌐 环境配置

### 开发环境

```bash
# 安装依赖
npm install

# 创建环境文件
echo "DEEPSEEK_API_KEY=your_api_key" > .env.local

# 启动开发服务器
npm run dev
```

### 生产环境

1. **Vercel 环境变量**:
   - `DEEPSEEK_API_KEY`: DeepSeek API 密钥

2. **区域设置**: 
   - 默认使用香港区域 (`hkg1`) 以获得更好的中国大陆访问性能

## ⚡ 性能优化

### API 函数配置

- **超时时间**: 30秒
- **区域**: 香港 (hkg1)
- **运行时**: Node.js 18.x

### 前端优化

- Next.js 15 的最新特性
- React 19 服务器组件
- Tailwind CSS 4 样式优化
- TypeScript 类型安全

## 🔍 监控与调试

### Vercel 函数日志

1. 访问 Vercel Dashboard
2. 进入项目 > Functions 标签
3. 查看实时日志和性能指标

### 本地调试

```bash
# 安装 Vercel CLI
npm i -g vercel

# 本地运行（模拟 Vercel 环境）
vercel dev
```

## 🚨 故障排除

### 常见问题

1. **API 密钥错误**
   - 检查 Vercel 环境变量设置
   - 确认 DeepSeek API 密钥有效

2. **函数超时**
   - 当前设置为 30 秒
   - 如需更长时间，升级到 Pro 计划

3. **构建失败**
   - 检查 TypeScript 类型错误
   - 确认所有依赖正确安装

### 解决方案

1. **重新部署**: 在 Vercel Dashboard 点击 "Redeploy"
2. **检查日志**: 查看 Functions 和 Build 日志
3. **本地测试**: 使用 `vercel dev` 本地调试

## 📚 相关文档

- [Next.js 部署文档](https://nextjs.org/docs/deployment)
- [Vercel 函数文档](https://vercel.com/docs/functions)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)

## 🎯 部署检查清单

- [ ] GitHub 仓库已连接
- [ ] 环境变量已配置
- [ ] 构建成功
- [ ] API 功能正常
- [ ] 前端界面可访问
- [ ] DeepSeek API 调用正常

完成以上步骤后，您的 ReadingType 智能编码助手就可以在 Vercel 上正常运行了！ 