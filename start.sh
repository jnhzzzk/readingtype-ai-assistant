#!/bin/bash

echo "==============================================="
echo "     ReadingType编码助手启动脚本"
echo "==============================================="

# 确保环境变量文件存在
if [ ! -f .env.local ]; then
  echo "创建.env.local文件..."
  echo "DEEPSEEK_API_KEY=sk-4410ee046236482dbe48aa527ca4f120" > .env.local
  echo "已使用示例API密钥创建.env.local文件"
  echo "⚠️  请确保替换为您的实际DeepSeek API密钥"
fi

# 安装依赖
echo "安装依赖..."
npm install

# 启动开发服务器
echo "启动ReadingType编码助手..."
echo "应用将在 http://localhost:3000 上运行"
echo "功能包括：编码搜索、智能生成、字典查询、编码管理等"
npm run dev 