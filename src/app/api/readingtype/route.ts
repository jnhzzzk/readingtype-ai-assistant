import { NextRequest, NextResponse } from 'next/server';

// DeepSeek API配置
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';

interface FieldValues {
  [key: string]: number;
}

class ReadingTypeAgent {
  private fieldNames: string[] = [
    "macroPeriod", "aggregate", "measurePeriod", "accumulationBehaviour",
    "flowDirection", "commodity", "measurementKind", "harmonic",
    "argumentNumerator", "TOU", "cpp", "tier", "phase", "multiplier", "uom", "currency"
  ];

  private fieldDictionaries: { [key: string]: Array<{ value: number; display_name: string; description: string }> } = {
    "measurementKind": [
      { value: 12, display_name: "电流", description: "Current" },
      { value: 13, display_name: "电压", description: "Voltage" },
      { value: 37, display_name: "功率", description: "Power" },
      { value: 38, display_name: "电能", description: "Energy" }
    ],
    "phase": [
      { value: 0, display_name: "无", description: "None" },
      { value: 1, display_name: "A相", description: "Phase A" },
      { value: 2, display_name: "B相", description: "Phase B" },
      { value: 3, display_name: "C相", description: "Phase C" },
      { value: 64, display_name: "三相", description: "Three Phase" }
    ],
    "uom": [
      { value: 5, display_name: "安培", description: "Amperes" },
      { value: 29, display_name: "伏特", description: "Volts" },
      { value: 38, display_name: "瓦特", description: "Watts" },
      { value: 72, display_name: "瓦时", description: "Watt Hours" }
    ],
    "accumulationBehaviour": [
      { value: 0, display_name: "无", description: "None" },
      { value: 1, display_name: "累积", description: "Accumulating" },
      { value: 2, display_name: "差值", description: "Delta" },
      { value: 3, display_name: "瞬时", description: "Instantaneous" }
    ],
    "commodity": [
      { value: 0, display_name: "无", description: "None" },
      { value: 1, display_name: "电能", description: "Electricity" },
      { value: 2, display_name: "燃气", description: "Gas" },
      { value: 3, display_name: "水", description: "Water" }
    ]
  };

  analyzeDescription(description: string): FieldValues {
    const fieldValues: FieldValues = {};
    
    // 初始化所有字段为0
    for (let i = 1; i <= 16; i++) {
      fieldValues[`field_${i}`] = 0;
    }
    
    const descLower = description.toLowerCase();
    
    // 测量类型识别
    if (description.includes("电压") || descLower.includes("voltage")) {
      fieldValues["field_7"] = 13; // measurementKind = 电压
      fieldValues["field_15"] = 29; // uom = 伏特
    } else if (description.includes("电流") || descLower.includes("current")) {
      fieldValues["field_7"] = 12; // measurementKind = 电流
      fieldValues["field_15"] = 5;  // uom = 安培
    } else if (description.includes("功率") || descLower.includes("power")) {
      fieldValues["field_7"] = 37; // measurementKind = 功率
      fieldValues["field_15"] = 38; // uom = 瓦特
    } else if (description.includes("电能") || descLower.includes("energy")) {
      fieldValues["field_7"] = 38; // measurementKind = 电能
      fieldValues["field_15"] = 72; // uom = 瓦时
    }
    
    // 相位识别
    if (description.includes("A相") || description.includes("a相")) {
      fieldValues["field_13"] = 1; // phase = A相
    } else if (description.includes("B相") || description.includes("b相")) {
      fieldValues["field_13"] = 2; // phase = B相
    } else if (description.includes("C相") || description.includes("c相")) {
      fieldValues["field_13"] = 3; // phase = C相
    } else if (description.includes("三相")) {
      fieldValues["field_13"] = 64; // phase = 三相
    }
    
    // 累积行为识别
    if (description.includes("瞬时") || description.includes("瞬间")) {
      fieldValues["field_4"] = 3; // accumulationBehaviour = 瞬时
    } else if (description.includes("累积")) {
      fieldValues["field_4"] = 1; // accumulationBehaviour = 累积
    }
    
    // 商品类型
    if (description.includes("电")) {
      fieldValues["field_6"] = 1; // commodity = 电能
    }
    
    return fieldValues;
  }

  buildReadingTypeId(fieldValues: FieldValues): string {
    const parts: string[] = [];
    for (let i = 1; i <= 16; i++) {
      const value = fieldValues[`field_${i}`] || 0;
      parts.push(value.toString());
    }
    return parts.join(".");
  }

  getFieldDescription(fieldName: string, value: number): string {
    if (this.fieldDictionaries[fieldName]) {
      const item = this.fieldDictionaries[fieldName].find(item => item.value === value);
      if (item) {
        return item.display_name;
      }
    }
    return `值 ${value}`;
  }

  generateDetailedResponse(description: string): string {
    const fieldValues = this.analyzeDescription(description);
    const readingTypeId = this.buildReadingTypeId(fieldValues);
    
    let response = "🤖 AI分析结果:\n";
    response += `📝 输入描述: ${description}\n\n`;
    response += `💡 建议编码: ${readingTypeId}\n\n`;
    response += "📋 字段详情:\n";
    
    // 显示非零字段
    for (let i = 0; i < this.fieldNames.length; i++) {
      const fieldName = this.fieldNames[i];
      const value = fieldValues[`field_${i + 1}`];
      if (value !== 0) {
        const fieldDesc = this.getFieldDescription(fieldName, value);
        response += `  ${i + 1}. ${fieldName}: ${value} (${fieldDesc})\n`;
      }
    }
    
    response += "\n✅ 此编码遵循IEC61968-9-2024标准规范。";
    
    return response;
  }
}

export async function POST(req: NextRequest) {
  try {
    const { message, action } = await req.json();
    
    if (!message) {
      return NextResponse.json({ error: '请提供消息内容' }, { status: 400 });
    }
    
    const agent = new ReadingTypeAgent();
    
    // 检查是否是编码生成请求
    if (action === 'generate' || message.includes('生成') || message.includes('编码')) {
      const response = agent.generateDetailedResponse(message);
      return NextResponse.json({ 
        response,
        type: 'generate',
        status: 'success' 
      });
    }
    
    // 其他请求使用AI对话
    if (!DEEPSEEK_API_KEY) {
      const mockResponse = `👋 欢迎使用ReadingType编码助手！

我可以帮助您：
🚀 **生成编码** - 基于描述智能生成ReadingType编码
🔍 **编码解析** - 解析ReadingTypeID为可读描述
✅ **规范验证** - 检查编码的有效性

请告诉我您需要什么帮助！

💡 提示：配置DeepSeek API密钥以获得完整的AI功能。`;
      
      return NextResponse.json({ 
        response: mockResponse,
        type: 'chat',
        status: 'demo' 
      });
    }
    
    // 使用DeepSeek API
    const systemPrompt = `您是ReadingType智能编码助手，专门帮助用户进行IEC61968-9-2024标准的ReadingType编码生成和管理。

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

请用专业、准确的方式回答用户关于ReadingType编码的问题。`;
    
    const response = await fetch(DEEPSEEK_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: message }
        ],
        temperature: 0.3,
        max_tokens: 2000
      })
    });
    
    if (!response.ok) {
      throw new Error(`DeepSeek API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    return NextResponse.json({
      response: data.choices[0].message.content,
      type: 'chat',
      status: 'success'
    });
    
  } catch (error) {
    console.error('ReadingType API Error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : '处理请求时发生错误' },
      { status: 500 }
    );
  }
} 