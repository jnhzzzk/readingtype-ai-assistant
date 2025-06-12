export interface DictionaryValue {
  code: string;
  english: string;
  chinese: string;
  description?: string;
}

export interface DictionaryField {
  position: number;
  name: string;
  englishName: string;
  description: string;
  values: DictionaryValue[];
}

// ReadingType 16字段编码字典 - 基于IEC61968-9-2024标准
const mockDictionary: DictionaryField[] = [
  {
    position: 1,
    name: 'macroPeriod',
    englishName: 'Macro Period',
    description: '宏周期',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Year', chinese: '年' },
      { code: '2', english: 'Month', chinese: '月' },
      { code: '3', english: 'Day', chinese: '日' },
      { code: '4', english: 'Hour', chinese: '时' },
    ],
  },
  {
    position: 2,
    name: 'aggregate',
    englishName: 'Aggregate',
    description: '聚合',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Maximum', chinese: '最大' },
      { code: '2', english: 'Minimum', chinese: '最小' },
      { code: '3', english: 'Average', chinese: '平均' },
      { code: '4', english: 'Sum', chinese: '总和' },
    ],
  },
  {
    position: 3,
    name: 'measurePeriod',
    englishName: 'Measure Period',
    description: '测量周期',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Second', chinese: '秒' },
      { code: '2', english: 'Minute', chinese: '分' },
      { code: '3', english: 'Hour', chinese: '时' },
      { code: '4', english: 'Day', chinese: '日' },
    ],
  },
  {
    position: 4,
    name: 'accumulationBehaviour',
    englishName: 'Accumulation Behaviour',
    description: '累积行为',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Cumulative', chinese: '累积' },
      { code: '2', english: 'Delta', chinese: '差值' },
      { code: '3', english: 'Instantaneous', chinese: '瞬时' },
    ],
  },
  {
    position: 5,
    name: 'flowDirection',
    englishName: 'Flow Direction',
    description: '流向',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Forward', chinese: '正向' },
      { code: '2', english: 'Reverse', chinese: '反向' },
      { code: '3', english: 'Net', chinese: '净值' },
      { code: '19', english: 'Total', chinese: '全部' },
    ],
  },
  {
    position: 6,
    name: 'commodity',
    englishName: 'Commodity',
    description: '商品',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Electricity', chinese: '电能' },
      { code: '2', english: 'Gas', chinese: '燃气' },
      { code: '3', english: 'Water', chinese: '水' },
      { code: '4', english: 'Time', chinese: '时间' },
    ],
  },
  {
    position: 7,
    name: 'measurementKind',
    englishName: 'Measurement Kind',
    description: '测量类型',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '12', english: 'Current', chinese: '电流' },
      { code: '13', english: 'Voltage', chinese: '电压' },
      { code: '37', english: 'Power', chinese: '功率' },
      { code: '38', english: 'Energy', chinese: '电能' },
    ]
  },
  {
    position: 8,
    name: 'harmonic',
    englishName: 'Harmonic',
    description: '谐波',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Fundamental', chinese: '基波' },
      { code: '2', english: 'Harmonic', chinese: '谐波' },
    ],
  },
  {
    position: 9,
    name: 'argumentNumerator',
    englishName: 'Argument Numerator',
    description: '参数分子',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Phase A', chinese: 'A相' },
      { code: '2', english: 'Phase B', chinese: 'B相' },
      { code: '3', english: 'Phase C', chinese: 'C相' },
    ],
  },
  {
    position: 10,
    name: 'TOU',
    englishName: 'Time of Use',
    description: '分时',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Peak', chinese: '峰时' },
      { code: '2', english: 'Off-peak', chinese: '平时' },
      { code: '3', english: 'Valley', chinese: '谷时' },
    ],
  },
  {
    position: 11,
    name: 'cpp',
    englishName: 'Critical Peak Pricing',
    description: '关键峰值价格',
    values: [
      { code: '0', english: 'None', chinese: '无' },
    ],
  },
  {
    position: 12,
    name: 'tier',
    englishName: 'Tier',
    description: '阶梯',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Tier 1', chinese: '第一阶梯' },
      { code: '2', english: 'Tier 2', chinese: '第二阶梯' },
    ],
  },
  {
    position: 13,
    name: 'phase',
    englishName: 'Phase',
    description: '相位',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '1', english: 'Phase A', chinese: 'A相' },
      { code: '2', english: 'Phase B', chinese: 'B相' },
      { code: '3', english: 'Phase C', chinese: 'C相' },
      { code: '64', english: 'Three Phase', chinese: '三相' },
    ],
  },
  {
    position: 14,
    name: 'multiplier',
    englishName: 'Multiplier',
    description: '乘数',
    values: [
      { code: '0', english: '1', chinese: '1' },
      { code: '3', english: '1000', chinese: '1000' },
      { code: '6', english: '1000000', chinese: '1000000' },
    ],
  },
  {
    position: 15,
    name: 'uom',
    englishName: 'Unit of Measure',
    description: '单位',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '5', english: 'Ampere', chinese: '安培' },
      { code: '29', english: 'Volt', chinese: '伏特' },
      { code: '38', english: 'Watt', chinese: '瓦特' },
      { code: '72', english: 'Watt-hour', chinese: '瓦时' },
    ],
  },
  {
    position: 16,
    name: 'currency',
    englishName: 'Currency',
    description: '货币',
    values: [
      { code: '0', english: 'None', chinese: '无' },
      { code: '978', english: 'CNY', chinese: '人民币' },
    ],
  }
];

export const readingTypeDictionary = mockDictionary;

export const searchDictionary = (query: string): Array<{field: DictionaryField, value: DictionaryValue}> => {
  if (!query) return [];
  const lowerCaseQuery = query.toLowerCase();
  
  const results: Array<{field: DictionaryField, value: DictionaryValue}> = [];
  
  mockDictionary.forEach(field => {
    // 搜索字段名称和描述
    if (field.name.toLowerCase().includes(lowerCaseQuery) || 
        field.englishName.toLowerCase().includes(lowerCaseQuery) ||
        field.description.toLowerCase().includes(lowerCaseQuery)) {
      
      // 如果字段匹配，添加所有值
      field.values.forEach(value => {
        results.push({ field, value });
      });
    } else {
      // 搜索值
      field.values.forEach(value => {
        if (value.code.includes(lowerCaseQuery) || 
            value.english.toLowerCase().includes(lowerCaseQuery) ||
            value.chinese.toLowerCase().includes(lowerCaseQuery)) {
          results.push({ field, value });
        }
      });
    }
  });

  return results;
} 