# ReadingTypeID Agent 测试套件

本目录包含ReadingTypeID智能编码Agent的完整测试套件，采用TDD（测试驱动开发）方法。

## 📁 目录结构

```
tests/
├── __init__.py              # 测试模块初始化
├── conftest.py              # 全局测试夹具和配置
├── pytest.ini              # pytest配置
├── requirements-test.txt    # 测试依赖
├── run_tests.py            # 测试运行脚本
├── README.md               # 本文档
├── unit/                   # 单元测试
│   ├── test_reading_type_database.py
│   ├── test_dictionary_manager.py  
│   ├── test_semantic_parser.py
│   └── test_reading_type_agent.py
├── integration/            # 集成测试
│   └── test_agent_integration.py
├── data/                   # 测试数据
│   └── test_reading_types.csv
└── fixtures/               # 测试夹具数据
```

## 🧪 测试类型

### 单元测试 (Unit Tests)
- **test_reading_type_database.py**: 数据库操作测试
- **test_dictionary_manager.py**: 字典管理测试
- **test_semantic_parser.py**: AI语义解析测试
- **test_reading_type_agent.py**: Agent主类测试

### 集成测试 (Integration Tests)
- **test_agent_integration.py**: 端到端工作流测试

## 🚀 运行测试

### 安装测试依赖
```bash
pip install -r tests/requirements-test.txt
```

### 运行所有测试
```bash
python tests/run_tests.py
```

### 运行特定类型测试
```bash
# 仅运行单元测试
python tests/run_tests.py --type unit

# 仅运行集成测试  
python tests/run_tests.py --type integration

# 生成覆盖率报告
python tests/run_tests.py --coverage
```

### 使用pytest直接运行
```bash
# 运行所有测试
pytest tests/ -v

# 运行单元测试
pytest tests/unit/ -v -m unit

# 运行集成测试
pytest tests/integration/ -v -m integration

# 运行AI相关测试
pytest tests/ -v -m ai

# 生成覆盖率报告
pytest tests/ --cov=reading_type_agent --cov-report=html
```

## 📊 测试标记 (Markers)

- `unit`: 单元测试
- `integration`: 集成测试
- `slow`: 慢速测试
- `database`: 数据库相关测试
- `ai`: AI功能相关测试
- `export`: 数据导出相关测试

## 🔧 测试夹具 (Fixtures)

### 全局夹具 (conftest.py)
- `temp_dir`: 临时目录
- `sample_reading_type_data`: 示例ReadingType数据
- `sample_csv_file`: 示例CSV文件
- `sample_dictionary_xml`: 示例字典XML数据
- `sample_dictionary_xml_file`: 示例字典XML文件
- `mock_ai_responses`: 模拟AI响应数据
- `operation_history_data`: 操作历史示例数据

## 📈 覆盖率目标

- **总体覆盖率**: ≥ 90%
- **核心业务逻辑**: ≥ 95%
- **数据库操作**: ≥ 90%
- **AI解析模块**: ≥ 85%

## 🛠️ 测试最佳实践

### 1. 测试命名约定
- 测试文件: `test_<模块名>.py`
- 测试类: `Test<功能名>`
- 测试方法: `test_<具体功能描述>`

### 2. 测试结构
```python
def test_function_behavior(self, fixtures):
    """测试函数行为的描述"""
    # Arrange - 准备测试数据
    # Act - 执行被测试的操作
    # Assert - 验证结果
```

### 3. Mock使用
- 使用Mock隔离外部依赖（AI API、文件系统等）
- 确保测试的独立性和可重复性

### 4. 数据驱动测试
- 使用`@pytest.mark.parametrize`进行参数化测试
- 覆盖边界条件和异常情况

## ⚠️ 注意事项

1. **测试数据隔离**: 每个测试使用独立的临时数据，避免测试间干扰
2. **AI API模拟**: AI相关测试使用Mock，避免真实API调用
3. **性能测试**: 标记为`slow`的测试仅在特定条件下运行
4. **并发测试**: 验证多线程环境下的数据一致性

## 🐛 调试测试

### 查看详细错误信息
```bash
pytest tests/ -v --tb=long
```

### 运行特定测试
```bash
pytest tests/unit/test_database.py::TestReadingTypeDatabase::test_search_exact_match -v
```

### 进入调试模式
```bash
pytest tests/ --pdb
```

## 📝 添加新测试

1. 确定测试类型（单元/集成）
2. 选择合适的测试文件或创建新文件
3. 编写测试用例，遵循AAA模式
4. 添加适当的测试标记
5. 确保测试独立且可重复

## 🔄 持续集成

测试套件设计为支持CI/CD集成：
- 快速测试用于Pull Request验证
- 完整测试套件用于主分支部署
- 覆盖率报告用于代码质量监控

---

通过完整的测试套件，确保ReadingTypeID Agent的可靠性、稳定性和可维护性。 