# ReadingType编码助手使用说明

## 快速开始

### 1. 安装依赖
```bash
npm install
```

### 2. 配置API密钥（可选）

创建 `.env.local` 文件：
```bash
# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

> **注意：** 如果不配置API密钥，应用将以演示模式运行，提供基本的模拟功能。

### 3. 启动应用
```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动。

## 主要功能

### 🚀 生成编码
- 点击"生成编码"按钮或使用快速生成选项
- 输入量测描述，如："A相电压"、"三相有功功率"
- 系统将智能分析并生成对应的ReadingTypeID

### 🛑 流式控制
- AI回复过程中会实时显示生成内容
- 点击输入框右侧的红色停止按钮可随时终止
- 完全控制AI响应的开始和结束

### 💬 对话交互
- 支持自然语言对话
- 可以询问字段含义、编码规范等
- 提供专业的技术解释

## 快速生成示例

应用预置了常用编码的快速生成：
- **A相电压** - 生成A相电压量测编码
- **三相有功功率** - 生成三相有功功率编码
- **正向有功电能** - 生成正向有功电能编码
- **储能SOC** - 生成储能系统SOC编码
- **B相电流** - 生成B相电流编码
- **瞬时无功功率** - 生成瞬时无功功率编码

## 技术规范

基于 **IEC61968-9-2024** 国际标准：

- 16个字段的完整编码结构
- 标准字段定义和取值范围
- 规范的编码验证机制

## API密钥获取

1. 访问 [DeepSeek平台](https://platform.deepseek.com)
2. 注册并登录账户
3. 创建API密钥
4. 将密钥添加到 `.env.local` 文件中

## 故障排除

### 500错误
- 检查API密钥是否正确配置
- 确认网络连接正常
- 查看控制台错误信息

### 终止功能异常
- 确认点击的是红色停止按钮
- 检查是否在AI生成过程中使用

## 开发模式

```bash
# 开发模式
npm run dev

# 构建应用
npm run build

# 生产模式
npm start
```

## 支持

如有问题，请检查：
1. Node.js版本是否兼容
2. 依赖是否正确安装
3. API密钥配置是否正确 