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

export interface SearchResult {
  field: DictionaryField;
  value: DictionaryValue;
  matchType: 'code' | 'english' | 'chinese';
}

// ReadingType编码字典数据
export const readingTypeDictionary: DictionaryField[] = [
  {
    position: 1,
    name: "宏周期",
    englishName: "macroPeriod",
    description: "用于描述数据的宏观时间周期",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "annually", chinese: "年" },
      { code: "2", english: "monthly", chinese: "月" },
      { code: "3", english: "daily", chinese: "日" },
      { code: "4", english: "hourly", chinese: "时" }
    ]
  },
  {
    position: 2,
    name: "聚合",
    englishName: "aggregate",
    description: "数据聚合方式",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "maximum", chinese: "最大值" },
      { code: "2", english: "minimum", chinese: "最小值" },
      { code: "3", english: "average", chinese: "平均值" },
      { code: "4", english: "sum", chinese: "总和" }
    ]
  },
  {
    position: 3,
    name: "测量周期",
    englishName: "measurePeriod",
    description: "测量数据的时间间隔",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "second", chinese: "秒" },
      { code: "2", english: "minute", chinese: "分钟" },
      { code: "3", english: "hour", chinese: "小时" },
      { code: "4", english: "day", chinese: "天" }
    ]
  },
  {
    position: 4,
    name: "累积行为",
    englishName: "accumulationBehaviour",
    description: "数据的累积特性",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "accumulating", chinese: "累积" },
      { code: "2", english: "delta", chinese: "差值" },
      { code: "3", english: "instantaneous", chinese: "瞬时" }
    ]
  },
  {
    position: 5,
    name: "流向",
    englishName: "flowDirection",
    description: "能量流动方向",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "forward", chinese: "正向" },
      { code: "2", english: "reverse", chinese: "反向" },
      { code: "3", english: "net", chinese: "净值" },
      { code: "19", english: "total", chinese: "全部" }
    ]
  },
  {
    position: 6,
    name: "商品",
    englishName: "commodity",
    description: "测量的商品类型",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "electricity", chinese: "电能" },
      { code: "2", english: "gas", chinese: "燃气" },
      { code: "3", english: "water", chinese: "水" },
      { code: "4", english: "time", chinese: "时间" }
    ]
  },
  {
    position: 7,
    name: "测量类型",
    englishName: "measurementKind",
    description: "具体的测量种类",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "12", english: "current", chinese: "电流" },
      { code: "13", english: "voltage", chinese: "电压" },
      { code: "37", english: "power", chinese: "功率" },
      { code: "38", english: "energy", chinese: "电能" }
    ]
  },
  {
    position: 8,
    name: "谐波",
    englishName: "harmonic",
    description: "谐波特性",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "fundamental", chinese: "基波" },
      { code: "2", english: "harmonic", chinese: "谐波" }
    ]
  },
  {
    position: 9,
    name: "参数分子",
    englishName: "argumentNumerator",
    description: "参数的分子部分",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "A-phase", chinese: "A相" },
      { code: "2", english: "B-phase", chinese: "B相" },
      { code: "3", english: "C-phase", chinese: "C相" }
    ]
  },
  {
    position: 10,
    name: "分时",
    englishName: "TOU",
    description: "分时电价时段",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "peak", chinese: "峰时" },
      { code: "2", english: "flat", chinese: "平时" },
      { code: "3", english: "valley", chinese: "谷时" }
    ]
  },
  {
    position: 11,
    name: "关键峰值价格",
    englishName: "cpp",
    description: "关键峰值价格标识",
    values: [
      { code: "0", english: "none", chinese: "无" }
    ]
  },
  {
    position: 12,
    name: "阶梯",
    englishName: "tier",
    description: "阶梯电价级别",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "tier1", chinese: "第一阶梯" },
      { code: "2", english: "tier2", chinese: "第二阶梯" },
      { code: "3", english: "tier3", chinese: "第三阶梯" }
    ]
  },
  {
    position: 13,
    name: "相位",
    englishName: "phase",
    description: "电气相位",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "1", english: "A-phase", chinese: "A相" },
      { code: "2", english: "B-phase", chinese: "B相" },
      { code: "3", english: "C-phase", chinese: "C相" },
      { code: "64", english: "three-phase", chinese: "三相" }
    ]
  },
  {
    position: 14,
    name: "乘数",
    englishName: "multiplier",
    description: "数值乘数",
    values: [
      { code: "0", english: "1", chinese: "1" },
      { code: "3", english: "1000", chinese: "1000" },
      { code: "6", english: "1000000", chinese: "1000000" }
    ]
  },
  {
    position: 15,
    name: "单位",
    englishName: "uom",
    description: "测量单位",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "5", english: "ampere", chinese: "安培(A)" },
      { code: "29", english: "volt", chinese: "伏特(V)" },
      { code: "38", english: "watt", chinese: "瓦特(W)" },
      { code: "72", english: "watthour", chinese: "瓦时(Wh)" }
    ]
  },
  {
    position: 16,
    name: "货币",
    englishName: "currency",
    description: "货币代码",
    values: [
      { code: "0", english: "none", chinese: "无" },
      { code: "978", english: "EUR", chinese: "欧元" },
      { code: "156", english: "CNY", chinese: "人民币" }
    ]
  }
];

// 搜索功能
export function searchDictionary(query: string): SearchResult[] {
  const results: SearchResult[] = [];
  const lowerQuery = query.toLowerCase();

  for (const field of readingTypeDictionary) {
    for (const value of field.values) {
      let matchType: 'code' | 'english' | 'chinese' | null = null;

      if (value.code.toLowerCase().includes(lowerQuery)) {
        matchType = 'code';
      } else if (value.english.toLowerCase().includes(lowerQuery)) {
        matchType = 'english';
      } else if (value.chinese.toLowerCase().includes(lowerQuery)) {
        matchType = 'chinese';
      }

      if (matchType) {
        results.push({
          field,
          value,
          matchType
        });
      }
    }
  }

  return results;
}

// 根据编码获取字典值
export function getValueByCode(position: number, code: string): DictionaryValue | null {
  const field = readingTypeDictionary.find(f => f.position === position);
  if (!field) return null;
  
  return field.values.find(v => v.code === code) || null;
}

// 解析ReadingType编码
export function parseReadingType(code: string): Array<{field: DictionaryField, value: DictionaryValue | null}> {
  const parts = code.split('.');
  const result: Array<{field: DictionaryField, value: DictionaryValue | null}> = [];

  for (let i = 0; i < Math.min(parts.length, 16); i++) {
    const field = readingTypeDictionary[i];
    const value = getValueByCode(field.position, parts[i]);
    result.push({ field, value });
  }

  return result;
} 