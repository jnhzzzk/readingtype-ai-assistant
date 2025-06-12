# ReadingTypeID智能编码Agent需求文档

## 1. 项目概述

### 1.1 项目背景
基于IEC61968-9-2024标准，开发一个智能ReadingTypeID编码助手Agent，通过自然语言对话的方式帮助用户快速生成、查询和管理ReadingTypeID编码，提高电力系统量测配置的效率和准确性。

### 1.2 核心价值
- **智能化编码生成**: 通过AI理解用户意图，自动生成符合标准的ReadingTypeID
- **降低学习成本**: 用户无需深入学习复杂的编码规则
- **提高配置效率**: 大幅减少人工编码时间
- **保证标准合规**: 确保生成的编码符合IEC61968-9-2024标准

### 1.3 技术架构基础
基于项目现有的AI Agent架构：
- 继承`advanced_ai_agent.py`的工具调用能力
- 使用DeepSeek API进行自然语言理解
- 采用CSV文件存储，轻量化数据管理
- 保持chatbox对话交互方式

## 2. 功能需求详细说明

### 2.1 核心对话场景

#### 场景1: 精确匹配查询
**用户输入**: "有功电能"
**系统处理流程**:
1. 在编码库CSV中搜索匹配项
2. 找到完全匹配的编码
3. 返回编码详情和说明

**预期输出**:
```
✅ 找到匹配编码:
📊 名称: 有功电能
🔢 ReadingTypeID: 0-0-2-4-1-1-12-0-0-0-0-0-0-0-72-0
📝 说明: 电表有功电能累积量测，单位kWh
⏰ 创建时间: 2024-01-15
```

#### 场景2: 模糊匹配与确认
**用户输入**: "三相有功功率"
**系统处理流程**:
1. AI分析发现与"有功功率"相似
2. 识别出需要指定相位信息
3. 返回相似编码并询问具体需求

**预期输出**:
```
🔍 找到相似的编码:
1. 有功功率 (ReadingTypeID: 0-0-0-0-1-1-12-0-0-0-0-0-0-0-61-0)
2. A相有功功率 (ReadingTypeID: 0-0-0-0-1-1-12-0-0-0-0-0-128-0-61-0)

❓ 您需要的是哪种类型的三相有功功率？
- 三相总功率
- A相功率  
- B相功率
- C相功率
请告诉我具体需求，我将为您生成准确的编码。
```

#### 场景3: 智能编码生成
**用户输入**: "储能设备充电功率"
**系统处理流程**:
1. AI解析关键信息：储能+充电+功率
2. 映射到对应字段：commodity=电力, measurementKind=功率, flowDirection=充电
3. 生成编码建议

**预期输出**:
```
🤖 AI分析结果:
📋 识别要素:
- 设备类型: 储能设备
- 测量内容: 功率
- 流向: 充电 (正向)
- 商品类型: 电力 (commodity=1)
- 测量类型: 有功功率 (measurementKind=12)
- 流向: 正向 (flowDirection=1)

💡 建议编码: 0-0-0-0-1-1-12-0-0-0-0-0-0-0-61-0

是否采纳此编码？输入"是"确认，"否"取消，或提出修改建议。
```

#### 场景4: 字典扩展场景
**用户输入**: "氢能燃料电池功率"
**系统处理流程**:
1. AI发现"氢能"在commodity字典中不存在
2. 建议扩展字典
3. 用户确认后更新字典并生成编码

**预期输出**:
```
⚠️  字典扩展建议:
🔍 分析发现"氢能"在commodity字典中不存在。

💡 建议扩展方案:
- 字段: commodity (商品类型)
- 新增项: 氢能 (编码建议: 9)
- 说明: 氢能燃料相关的量测

是否同意扩展字典？
输入"扩展"确认，然后我将为您生成完整的ReadingTypeID。
```

### 2.2 数据管理功能

#### 2.2.1 编码库查询功能
**触发指令**: "查看编码库" / "显示所有编码" / "编码列表"
**功能说明**:
- 显示当前库中所有ReadingTypeID
- 支持分页显示（每页20条）
- 提供筛选和搜索功能

#### 2.2.2 编码库筛选功能  
**触发指令**: "筛选电表编码" / "查找功率类编码"
**功能说明**:
- 按设备类型筛选
- 按测量类型筛选
- 按时间范围筛选

#### 2.2.3 编码库导出功能
**触发指令**: "导出编码库" / "生成CSV文件"
**功能说明**:
- 导出为CSV格式
- 可选择导出全部或筛选后的数据
- 包含完整的字段说明

#### 2.2.4 字典管理功能
**触发指令**: "查看字典" / "显示标准字典"
**功能说明**:
- 查看ReadingType各字段的标准值
- 支持字典扩展和自定义
- 显示字典使用统计

### 2.3 工具集成需求

基于现有`advanced_ai_agent.py`的工具架构，需要实现以下专用工具：

#### 2.3.1 编码查询工具
```python
def search_reading_type(args):
    """在编码库中搜索ReadingTypeID"""
    # 参数: name (量测名称)
    # 返回: 匹配的编码列表
```

#### 2.3.2 编码生成工具
```python
def generate_reading_type(args):
    """根据解析的字段生成ReadingTypeID"""
    # 参数: 各字段值的字典
    # 返回: 生成的编码建议
```

#### 2.3.3 字典查询工具
```python
def query_dictionary(args):
    """查询字典信息"""
    # 参数: field_name (字段名)
    # 返回: 字段的所有可选值
```

#### 2.3.4 数据导出工具
```python
def export_data(args):
    """导出编码库数据"""
    # 参数: format, filter_conditions
    # 返回: 导出文件路径
```

## 3. 数据存储设计

### 3.1 编码库CSV结构 (reading_type_codes.csv)
```csv
id,name,description,reading_type_id,field_1,field_2,...,field_16,created_at,source,category
1,有功电能,电表有功电能累积量测,0-0-2-4-1-1-12-0-0-0-0-0-0-0-72-0,0,0,2,4,1,1,12,0,0,0,0,0,0,0,72,0,2024-01-15,标准库,表计
2,储能充电功率,储能设备充电功率监测,0-0-0-0-1-1-12-0-0-0-0-0-0-0-61-0,0,0,0,0,1,1,12,0,0,0,0,0,0,0,61,0,2024-01-15,用户生成,储能
```

### 3.2 字典库XML结构 (reading_type_dictionaries.xml)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ReadingTypeDictionaries version="IEC61968-9-2024" created="2024-01-15 10:30:00">
  <Field name="macroPeriod" chinese_name="宏周期">
    <Item value="0" name="none" description="不适用" is_custom="false"/>
    <Item value="8" name="billingPeriod" description="计费周期" is_custom="false"/>
  </Field>
  <Field name="commodity" chinese_name="商品类型">
    <Item value="1" name="电力" description="电力相关量测" is_custom="false"/>
    <Item value="9" name="氢能" description="氢能相关量测" is_custom="true"/>
  </Field>
</ReadingTypeDictionaries>
```

### 3.3 操作历史CSV结构 (operation_history.csv)
```csv
id,timestamp,input_text,operation_type,result,user_action
1,2024-01-15 10:30:00,有功电能,search,找到匹配编码,accepted
2,2024-01-15 10:35:00,氢能燃料电池功率,extend_generate,扩展字典+生成编码,accepted
```

## 4. 用户交互设计

### 4.1 对话流程设计

#### 4.1.1 欢迎消息
```
🔌 ReadingTypeID智能编码助手已就绪！

我可以帮您：
✨ 查询已有的ReadingTypeID编码
🤖 智能生成新的编码
📚 管理编码库和字典
📊 导出编码数据

请告诉我您需要什么量测编码，或者输入以下指令：
- "查看编码库" - 浏览所有编码
- "查看字典" - 查看标准字典
- "导出数据" - 导出编码库
- "帮助" - 查看更多功能
```

#### 4.1.2 错误处理消息
```
❌ 抱歉，我没有理解您的需求。

💡 建议：
- 描述具体的量测内容，如"有功电能"、"三相电压"
- 使用标准术语，如"功率"、"电能"、"电压"、"电流"
- 或者输入"帮助"查看使用指南
```

### 4.2 确认机制设计

#### 4.2.1 编码生成确认
```
🔍 请确认编码信息:
📝 名称: {用户输入的名称}
🔢 编码: {生成的ReadingTypeID}
📋 字段解析:
  - 商品类型: {commodity_name} ({commodity_value})
  - 测量类型: {measurement_kind_name} ({measurement_kind_value})
  - 其他重要字段...

✅ 输入"确认"保存编码
❌ 输入"取消"放弃
🔧 输入"修改"进行调整
```

#### 4.2.2 字典扩展确认
```
📚 字典扩展确认:
🔧 字段: {field_name}
🆕 新增值: {new_value}
📝 说明: {description}

⚠️  注意: 扩展字典将影响标准合规性，请谨慎操作。

✅ 输入"确认扩展"执行
❌ 输入"取消"放弃
```

## 5. 技术实现规划

### 5.1 基础架构改造

#### 5.1.1 继承现有Agent类
```python
from advanced_ai_agent import AdvancedAIAgent

class ReadingTypeIDAgent(AdvancedAIAgent):
    def __init__(self):
        super().__init__()
        self.encoding_db = ReadingTypeDatabase()
        self.dictionary_db = DictionaryDatabase()
        self.semantic_parser = SemanticParser()
        # 添加专用工具
        self.available_tools.update({
            "search_reading_type": self.search_reading_type,
            "generate_reading_type": self.generate_reading_type,
            "query_dictionary": self.query_dictionary,
            "export_data": self.export_data
        })
```

#### 5.1.2 CSV数据库管理类
```python
class ReadingTypeDatabase:
    def __init__(self, csv_file="reading_type_codes.csv"):
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame()
    
    def search(self, name):
        """搜索编码"""
        pass
    
    def add(self, record):
        """添加新编码"""
        pass
    
    def export(self, filters=None):
        """导出数据"""
        pass
```

### 5.2 AI语义解析模块

#### 5.2.1 关键词映射表
```python
KEYWORD_MAPPING = {
    # 测量类型
    "功率": {"measurementKind": 12, "uom": 61},
    "电能": {"measurementKind": 12, "uom": 72},
    "电压": {"measurementKind": 7, "uom": 29},
    "电流": {"measurementKind": 5, "uom": 5},
    
    # 相位
    "A相": {"phase": 128},
    "B相": {"phase": 256}, 
    "C相": {"phase": 512},
    "三相": {"phase": 896},
    
    # 时间周期
    "15分钟": {"measurePeriod": 2},
    "30分钟": {"measurePeriod": 5},
    "1小时": {"measurePeriod": 7},
    
    # 聚合方式
    "平均": {"aggregate": 2},
    "最大": {"aggregate": 8},
    "最小": {"aggregate": 9},
    
    # 设备类型
    "表计": {"category": "表计"},
    "储能": {"category": "储能"},
    "告警": {"category": "告警"}
}
```

### 5.3 部署方案

#### 5.3.1 命令行版本 (基于现有架构)
直接扩展`advanced_ai_agent.py`，添加ReadingTypeID专用功能

#### 5.3.2 Web版本 (基于现有Web架构)
在`ai-assistant-web`基础上添加：
- ReadingTypeID专用界面
- 编码库管理页面
- 数据导出功能
- 字典管理界面

## 6. 开发计划

### 6.1 第一阶段 (1-2周)
- [ ] 基础CSV数据库设计和实现
- [ ] 从Excel文件导入初始数据
- [ ] 基础编码查询功能
- [ ] 简单的关键词匹配算法

### 6.2 第二阶段 (1-2周)
- [ ] AI语义解析模块
- [ ] 编码生成算法
- [ ] 工具函数集成
- [ ] 命令行Agent完整功能

### 6.3 第三阶段 (1-2周)
- [ ] 字典扩展功能
- [ ] 批量处理能力
- [ ] 数据导出功能
- [ ] 操作历史记录

### 6.4 第四阶段 (可选)
- [ ] Web界面开发
- [ ] 高级筛选和搜索
- [ ] 编码验证功能
- [ ] 用户权限管理

## 7. 测试计划

### 7.1 功能测试用例
- [ ] 精确匹配场景测试
- [ ] 模糊匹配场景测试  
- [ ] 编码生成场景测试
- [ ] 字典扩展场景测试
- [ ] 数据导出测试
- [ ] 错误处理测试

### 7.2 性能测试
- [ ] 大量编码库查询性能
- [ ] 批量处理性能
- [ ] AI响应时间测试

## 8. 风险与挑战

### 8.1 技术风险
- **AI理解准确性**: 自然语言理解可能存在歧义
- **编码标准合规**: 确保生成的编码符合IEC61968-9标准
- **数据一致性**: CSV文件的并发读写问题

### 8.2 缓解措施
- 建立完善的测试用例库
- 增加用户确认机制
- 实现数据备份和恢复机制
- 添加编码验证功能

这个需求文档为ReadingTypeID智能编码Agent提供了完整的功能规划和技术实现指导，确保项目能够高效、准确地满足用户需求。 