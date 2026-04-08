# OpenClaw与Claude Code集成指南

## 系统架构

本项目实现了OpenClaw与Claude Code的集成，采用双层架构设计：

- **OpenClaw**：作为调度层，负责任务分析、路由分发和结果整合
- **Claude Code**：作为执行层，负责专业的代码生成和分析任务

## 目录结构

```
openclaw-claude-integration/
├── api_client/          # Claude API客户端
├── task_analysis/       # 任务分析模块
├── result_processing/   # 结果处理模块
├── plugin/              # OpenClaw插件
├── .env.example         # 环境变量配置模板
├── requirements.txt     # 依赖包配置
├── task_router.py       # 任务路由器
├── example_usage.py     # 使用示例
├── test_integration.py  # 集成测试
└── README.md            # 本指南
```

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd openclaw-claude-integration
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

复制环境变量模板文件并填写相关配置：

```bash
cp .env.example .env
```

编辑`.env`文件，设置以下环境变量：

```
# Claude API配置
ANTHROPIC_API_KEY=your_anthropic_api_key
ANTHROPIC_API_URL=https://api.anthropic.com/v1/messages

# 本地Claude Code配置
USE_LOCAL_CLAUDE=false
LOCAL_CLAUDE_API_URL=http://localhost:8080/api/messages

# 模型配置
CLAUDE_MODEL=claude-3-opus-20240229

# 超时设置
API_TIMEOUT=30

# 日志级别
LOG_LEVEL=INFO
```

## 使用方法

### 1. 作为OpenClaw插件使用

将`plugin`目录复制到OpenClaw的插件目录中，然后在OpenClaw中启用该插件。

### 2. 独立使用

```python
from task_router import TaskRouter

# 初始化任务路由器
task_router = TaskRouter()

# 处理任务
task = "生成一个Python函数，计算斐波那契数列的第n项"
result = task_router.process_and_route(task)
print(result)
```

### 3. 支持的任务类型

- **代码生成**：生成各种编程语言的代码
- **代码分析**：分析代码质量、潜在问题和优化建议
- **代码修复**：修复代码中的bug
- **财务分析**：分析财务报表和财务风险
- **法律分析**：分析合同和法律风险
- **战略决策**：由OpenClaw处理
- **日常任务**：由OpenClaw处理

## 测试

运行集成测试以验证系统功能：

```bash
python test_integration.py
```

## 示例

### 代码生成

**任务**：生成一个Python函数，计算斐波那契数列的第n项

**结果**：
```
🎯 Task routed to: Claude

📋 Processed result with 1 code block(s)

💻 Code Block #1 (python):
```python
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```
```

### 代码分析

**任务**：分析以下Python代码
```python
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
```

**结果**：
```
🎯 Task routed to: Claude

📋 Code analysis completed

🔍 Code Quality Assessment:
The code is simple and straightforward, implementing a recursive factorial function. It follows basic Python syntax and structure.

🐛 Potential Bugs or Issues:
- The function doesn't handle negative numbers, which would cause infinite recursion.
- For large values of n, the recursive approach may lead to stack overflow.
- There's no type checking, so passing non-integer values would cause errors.

⚡ Optimization Suggestions:
- Consider using an iterative approach for better performance with large n.
- Add input validation to handle negative numbers and non-integer inputs.
- Use memoization if the function will be called multiple times with the same inputs.

✅ Best Practices Recommendations:
- Add docstring to explain the function's purpose and usage.
- Include type hints for the parameter and return value.
- Add unit tests to verify the function works correctly.
```

## 本地Claude Code集成

### 配置本地Claude Code

1. **安装本地Claude Code**
   从GitHub克隆并安装本地Claude Code：
   ```bash
   git clone https://github.com/claude-code-best/claude-code
   cd claude-code
   bun install
   ```

2. **启动本地Claude Code**
   ```bash
   bun run dev
   ```

3. **配置OpenClaw集成**
   在`.env`文件中设置：
   ```
   # 本地Claude Code配置
   USE_LOCAL_CLAUDE=true
   LOCAL_CLAUDE_API_URL=http://localhost:8080/api/messages
   ```

### 本地Claude Code优势

- **更低的延迟**：本地部署，响应速度更快
- **离线使用**：不依赖外部网络连接
- **自定义配置**：可以根据需要调整模型和参数
- **成本效益**：避免API调用费用

### 故障排除

#### 常见问题

1. **本地Claude Code连接失败**
   - 检查本地Claude Code是否正在运行
   - 确认`LOCAL_CLAUDE_API_URL`配置正确
   - 验证本地端口是否被占用

2. **自动fallback到官方API**
   - 当本地Claude Code不可用时，系统会自动切换到官方API
   - 检查终端输出，了解fallback原因

3. **环境变量未加载**
   - 确保安装了`python-dotenv`：`pip install python-dotenv`
   - 验证`.env`文件格式正确

4. **API密钥问题**
   - 确保`ANTHROPIC_API_KEY`设置正确
   - 对于本地Claude Code，可能需要在其配置中设置API密钥

#### 检查本地Claude Code状态

使用以下命令检查本地Claude Code的运行状态：

```bash
curl http://localhost:8080/api/health
```

## 注意事项

1. **API密钥**：需要在`.env`文件中设置有效的Anthropic API密钥
2. **网络连接**：确保系统能够访问Anthropic API（当本地Claude不可用时）
3. **性能**：对于复杂任务，可能需要较长的处理时间
4. **成本**：使用官方Claude API会产生费用，请合理使用
5. **本地部署**：本地Claude Code需要足够的系统资源来运行

## 扩展建议

1. **添加更多任务类型**：扩展任务分类和处理逻辑
2. **优化路由策略**：根据任务复杂度和优先级进行更智能的路由
3. **添加缓存机制**：缓存常见任务的结果，提高响应速度
4. **集成更多工具**：除了Claude，还可以集成其他专业工具

## 故障排除

### 常见问题

1. **API连接失败**：检查网络连接和API密钥是否正确
2. **任务路由错误**：检查任务描述是否清晰，是否包含足够的信息
3. **结果格式问题**：检查Claude的响应格式是否符合预期

### 日志

系统会记录详细的日志信息，可用于排查问题。

## 版本信息

- **当前版本**：1.0.0
- **更新日期**：2026-04-07

## 联系信息

如有问题或建议，请联系项目维护人员。