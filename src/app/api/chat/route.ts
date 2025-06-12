import { NextRequest, NextResponse } from 'next/server';

// DeepSeek API配置
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';

// ReadingType编码助手的系统提示
const READING_TYPE_SYSTEM_PROMPT = `你是ReadingType智能编码助手，专门帮助用户进行IEC61968-9-2024标准的ReadingType编码生成和管理。

ReadingType编码结构（16个字段）：
1. macroPeriod - 宏周期（0=无，1=年，2=月，3=日，4=时）
2. aggregate - 聚合（0=无，1=最大，2=最小，3=平均，4=总和）
3. measurePeriod - 测量周期（0=无，1=秒，2=分，3=时，4=日）
4. accumulationBehaviour - 累积行为（0=无，1=累积，2=差值，3=瞬时）
5. flowDirection - 流向（0=无，1=正向，2=反向，3=净值，19=全部）
6. commodity - 商品（0=无，1=电能，2=燃气，3=水，4=时间）
7. measurementKind - 测量类型（0=无，12=电流，13=电压，37=功率，38=电能）
8. harmonic - 谐波（0=无，1=基波，2=谐波）
9. argumentNumerator - 参数分子（0=无，1=A相，2=B相，3=C相）
10. TOU - 分时（0=无，1=峰时，2=平时，3=谷时）
11. cpp - 关键峰值价格（0=无）
12. tier - 阶梯（0=无，1=第一阶梯，2=第二阶梯）
13. phase - 相位（0=无，1=A相，2=B相，3=C相，64=三相）
14. multiplier - 乘数（0=1，3=1000，6=1000000）
15. uom - 单位（0=无，5=安培，29=伏特，38=瓦特，72=瓦时）
16. currency - 货币（0=无，978=人民币）

你的主要功能：
1. 生成ReadingType编码 - 基于用户描述智能生成新的编码
2. 编码验证 - 检查编码的有效性和规范性
3. 编码解析 - 将16位编码解析为可读的中文描述
4. 字段解释 - 解释各字段的含义和取值规范

专注于根据用户的量测需求描述，智能分析并生成准确的ReadingTypeID编码。

请用专业、准确的方式回答用户关于ReadingType编码的问题。`;

// 处理聊天API的POST请求
export async function POST(req: NextRequest) {
  try {
    console.log('收到ReadingType编码助手请求');
    
    // 解析请求内容
    const { message, messages, stream = false } = await req.json();
    
    // 确保有消息历史，如果没有则使用单个消息
    let messageHistory = messages;
    if (!messageHistory && message) {
      messageHistory = [
        { role: 'system', content: READING_TYPE_SYSTEM_PROMPT },
        { role: 'user', content: message }
      ];
    }
    
    // 确保系统消息是ReadingType相关的
    if (messageHistory && messageHistory.length > 0) {
      if (messageHistory[0].role === 'system') {
        messageHistory[0].content = READING_TYPE_SYSTEM_PROMPT;
      } else {
        messageHistory.unshift({ role: 'system', content: READING_TYPE_SYSTEM_PROMPT });
      }
    }
    
    if (!messageHistory || messageHistory.length === 0) {
      console.error('无效的请求：缺少消息');
      return NextResponse.json({ error: '请提供消息内容' }, { status: 400 });
    }
    
    // 检查API密钥是否配置
    if (!DEEPSEEK_API_KEY || DEEPSEEK_API_KEY === 'your_deepseek_api_key_here' || DEEPSEEK_API_KEY === 'your_api_key_here') {
      console.log('API密钥未配置，使用模拟响应');
      
      // 提取用户消息
      const userMessage = messageHistory[messageHistory.length - 1]?.content || '';
      
      // 生成模拟响应
      let mockResponse = '';
      if (userMessage.includes('生成') || userMessage.includes('编码')) {
        mockResponse = `🤖 智能生成ReadingType编码

基于您的描述"${userMessage}"，我为您分析并生成以下编码：

📋 分析结果：
- 设备类型：电力设备
- 测量内容：根据描述推断
- 相位信息：需要进一步确认

💡 建议编码：0-0-0-6-1-1-37-0-0-0-0-0-224-0-38-0

📖 字段解释：
1. macroPeriod: 0 (无特定宏周期)
2. aggregate: 0 (无聚合)
3. measurePeriod: 0 (无特定测量周期)
4. accumulationBehaviour: 6 (瞬时值)
5. flowDirection: 1 (正向)
6. commodity: 1 (电能)
7. measurementKind: 37 (有功功率)
8. harmonic: 0 (基波)
9. argumentNumerator: 0 (无特定参数)
10. TOU: 0 (无分时)
11. cpp: 0 (无关键峰值价格)
12. tier: 0 (无阶梯)
13. phase: 224 (三相)
14. multiplier: 0 (乘数为1)
15. uom: 38 (瓦特)
16. currency: 0 (无货币)

✅ 此编码遵循IEC61968-9-2024标准规范。

💡 注意：这是演示模式，请配置DeepSeek API密钥以获得完整的AI功能。`;
      
      } else {
                 mockResponse = `👋 欢迎使用ReadingType编码助手！

我可以帮助您：

🚀 **生成编码**
- 基于描述智能生成ReadingType编码
- 示例："生成A相电压量测的编码"

🔧 **编码解析**
- 解析ReadingTypeID为可读描述
- 字段含义解释

🛑 **终止功能**
- 生成过程中点击红色停止按钮可随时终止

请告诉我您需要什么帮助，或者尝试快速生成常用编码！

💡 注意：这是演示模式，请配置DeepSeek API密钥以获得完整的AI功能。`;
      }
      
      return NextResponse.json({ content: mockResponse });
    }
    
    console.log(`准备发送 ${messageHistory.length} 条消息到DeepSeek API`);
    
    try {
      // 调用DeepSeek API
      const response = await fetch(DEEPSEEK_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
        },
        body: JSON.stringify({
          model: 'deepseek-chat',
          messages: messageHistory,
          temperature: 0.3, // 降低温度以提高准确性
          max_tokens: 3000, // 增加最大token数
          stream // 根据请求参数设置流式模式
        }),
      });
      
      // 检查响应状态
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('DeepSeek API响应错误:', response.status, errorData);
        
        return NextResponse.json({ 
          error: errorData.error?.message || `API响应错误: ${response.status}` 
        }, { status: 500 });
      }
      
      // 处理流式响应
      if (stream) {
        const encoder = new TextEncoder();
        
        // 创建一个可读流
        const readableStream = new ReadableStream({
          async start(controller) {
            // 处理来自DeepSeek API的流
            if (!response.body) {
              controller.close();
              return;
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            try {
              while (true) {
                const { done, value } = await reader.read();
                
                if (done) {
                  // 发送结束标记
                  controller.enqueue(encoder.encode("data: [DONE]\n\n"));
                  controller.close();
                  break;
                }
                
                // 解码DeepSeek响应
                const chunkText = decoder.decode(value);
                
                // DeepSeek API返回的是多个SSE事件，按行分割
                const lines = chunkText.split('\n');
                
                for (const line of lines) {
                  // 排除空行和不是data:开头的行
                  if (line.trim() === '' || !line.startsWith('data:')) continue;
                  
                  // 直接将DeepSeek返回的data行发送给客户端
                  controller.enqueue(encoder.encode(line + '\n\n'));
                }
              }
            } catch (e) {
              console.error('流处理错误:', e);
              controller.error(e);
            }
          }
        });

        // 返回流式响应
        return new Response(readableStream, {
          headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
          }
        });
      }
      
      // 非流式模式处理
      const data = await response.json();
      console.log('DeepSeek API响应成功');
      
      if (!data.choices || !data.choices[0] || !data.choices[0].message) {
        console.error('无效的API响应格式');
        return NextResponse.json({ error: '无效的API响应格式' }, { status: 500 });
      }
      
      // 提取回复内容
      const content = data.choices[0].message.content;
      
      // 返回成功响应
      return NextResponse.json({ content });
      
    } catch (error) {
      console.error('处理API请求时出错:', error);
      return NextResponse.json({ 
        error: error instanceof Error ? error.message : '调用API时遇到网络问题'
      }, { status: 500 });
    }
    
  } catch (error) {
    console.error('处理请求时出错:', error);
    return NextResponse.json({ 
      error: error instanceof Error ? error.message : '处理请求时出错' 
    }, { status: 400 });
  }
} 