# ReadingTypeID 智能编码助手

基于IEC61968-9-2024标准的ReadingType智能编码助手，提供编码搜索、生成和管理功能。

## 🚀 功能特性

### 核心功能
- **智能搜索**: 精确匹配和模糊搜索现有编码
- **智能生成**: 根据自然语言描述生成ReadingType编码
- **字典查询**: 查看字段定义和可选值
- **编码管理**: 浏览、筛选、添加编码到库中
- **数据导出**: 支持CSV/JSON格式导出
- **统计分析**: 编码库统计信息

### 技术特性
- **AI驱动**: 基于DeepSeek大模型的智能对话
- **模块化架构**: 清晰的代码结构，易于维护和扩展
- **CSV存储**: 轻量级数据存储，无需数据库
- **实时流式输出**: 提供流畅的对话体验
- **命令行界面**: 简单易用的文本界面

## 📁 项目结构

```
ReadingType_Agent/
├── main.py                    # 主应用入口
├── src/                       # 核心模块
│   ├── reading_type_agent.py  # 主Agent类
│   ├── reading_type_database.py # 数据库管理
│   ├── dictionary_manager.py  # 字典管理
│   └── semantic_parser.py     # 语义解析
├── tests/                     # 测试用例
├── data/                      # 数据文件
│   ├── reading_type_codes.csv # 编码库
│   ├── field_dictionaries.csv # 字段字典
│   └── operation_history.csv  # 操作历史
├── requirements.txt           # 依赖包
├── env.example               # 环境变量示例
└── README_Agent.md           # 使用说明
```

## 🔧 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制环境变量示例文件：
```bash
cp env.example .env
```

编辑`.env`文件，设置您的API密钥：
```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 3. 检查数据文件

确保以下数据文件存在：
- `reading_type_codes.csv` - 编码库数据
- `field_dictionaries.csv` - 字段字典数据

## 🚀 使用方法

### 启动应用

```bash
python main.py
```

### 基本对话示例

```
💬 您: 搜索有功电能
🤖 ReadingType助手: 
✅ 找到精确匹配:
📊 名称: 有功电能
🔢 ReadingTypeID: 0-0-0-3-1-1-12-0-0-0-0-0-224-3-72-0
📝 说明: 三相有功电能累积量
🏷️ 类别: 表计
⏰ 创建时间: 2024-01-15 10:30:00
```

```
💬 您: 生成储能充电功率编码
🤖 ReadingType助手: 
🤖 AI分析结果:
📝 输入描述: 储能充电功率编码

🔍 识别要素:
  - 设备类型: 储能
  - 测量类型: 功率
  - 流向: 充电

💡 建议编码: 0-0-0-6-1-41-37-0-0-0-0-0-0-3-38-0

📋 字段映射:
   4. 累积行为(accumulationBehaviour): 6 = 瞬时
   5. 流向(flowDirection): 1 = 正向
   6. 商品类型(commodity): 41 = 储能系统
   7. 测量类型(measurementKind): 37 = 有功功率
  14. 乘数(multiplier): 3 = kilo (×10³)
  15. 单位(uom): 38 = W

✅ 是否采纳此编码？输入'是'确认，'否'取消，或提出修改建议。
```

### 支持的命令类型

1. **搜索编码**
   - "搜索有功电能"
   - "查找储能相关编码"
   - "寻找温度测量"

2. **生成编码**
   - "生成三相电压编码"
   - "我需要储能放电功率编码"
   - "帮我创建频率测量编码"

3. **查询字典**
   - "查询字典"
   - "查询commodity字段"
   - "measurementKind有哪些值"

4. **浏览管理**
   - "查看编码库"
   - "查看表计类编码"
   - "统计信息"

5. **数据导出**
   - "导出数据"
   - "导出CSV格式"
   - "导出储能类编码"

6. **系统命令**
   - "帮助" - 显示使用指南
   - "清除历史" - 清除对话历史
   - "退出" - 退出程序

## 🔧 高级配置

### 命令行参数

```bash
# 禁用流式输出
python main.py --no-stream

# 查看帮助
python main.py --help
```

### 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | 必填 |
| `CODES_FILE` | 编码库文件路径 | `reading_type_codes.csv` |
| `DICTIONARIES_FILE` | 字典文件路径 | `field_dictionaries.csv` |
| `HISTORY_FILE` | 历史文件路径 | `operation_history.csv` |
| `API_BASE_URL` | API基础URL | `https://api.deepseek.com` |
| `MODEL_NAME` | 模型名称 | `deepseek-chat` |

## 📊 数据格式

### 编码库格式 (reading_type_codes.csv)

| 字段 | 说明 | 示例 |
|------|------|------|
| id | 编码ID | 1 |
| name | 编码名称 | 有功电能 |
| description | 编码说明 | 三相有功电能累积量 |
| reading_type_id | ReadingType编码 | 0-0-0-3-1-1-12-0-0-0-0-0-224-3-72-0 |
| category | 编码类别 | 表计 |
| source | 编码来源 | IEC61968-9-2024 |
| created_at | 创建时间 | 2024-01-15 10:30:00 |
| field_1 ~ field_16 | 各字段值 | 0, 0, 0, 3, 1, 1, 12, ... |

### 字典格式 (field_dictionaries.csv)

| 字段 | 说明 | 示例 |
|------|------|------|
| field_name | 字段名 | commodity |
| field_chinese_name | 中文名 | 商品类型 |
| field_value | 字段值 | 1 |
| display_name | 显示名称 | 电力 |
| description | 详细说明 | 电力商品 |
| is_custom | 是否自定义 | false |

## 🧪 测试

运行测试用例：
```bash
# 运行所有测试
cd tests
python run_tests.py

# 运行特定测试
pytest tests/unit/test_reading_type_agent.py -v

# 运行覆盖率测试
pytest --cov=src tests/
```

## 🔍 故障排除

### 常见问题

1. **API密钥错误**
   ```
   ❌ 初始化失败: Invalid API key
   ```
   解决方案：检查`.env`文件中的`DEEPSEEK_API_KEY`是否正确

2. **数据文件缺失**
   ```
   警告: 编码库文件 reading_type_codes.csv 未找到
   ```
   解决方案：确保数据文件存在于项目根目录

3. **网络连接错误**
   ```
   ❌ 发生错误: Connection timeout
   ```
   解决方案：检查网络连接和防火墙设置

4. **依赖包错误**
   ```
   ModuleNotFoundError: No module named 'openai'
   ```
   解决方案：运行`pip install -r requirements.txt`

### 调试模式

设置环境变量启用调试：
```bash
export DEBUG=true
python main.py
```

## 🤝 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📝 版本历史

- **v1.0.0** (2024-01-15)
  - 初始版本发布
  - 基本搜索和生成功能
  - 字典查询和编码管理
  - 数据导出和统计功能

## 📄 许可证

本项目基于MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 支持

如有问题或建议，请通过以下方式联系：
- 创建Issue
- 发送邮件
- 查看文档

## 🙏 致谢

- 感谢IEC61968-9-2024标准制定者
- 感谢DeepSeek提供的AI服务
- 感谢开源社区的支持 