# OpenClaw Claude Code 集成

在OpenClaw中调用本地Claude Code CLI进行代码生成和分析。

## 快速部署

### 1. 克隆项目
```bash
git clone https://github.com/junxi724-maker/openclaw-claude-integration.git
cd openclaw-claude-integration
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

### Python调用
```python
from api_client import ClaudeClient

client = ClaudeClient()
result = client.generate_code("写一个斐波那契函数", "python")
print(result)
```

### OpenClaw调用
```
/ccb 生成一个Python函数
```

### 终端直接运行
```bash
python ccb_hook.py "你的任务"
```

## 文件说明

| 文件 | 说明 |
|-----|------|
| `api_client/claude_client.py` | Claude CLI调用 |
| `ccb_hook.py` | 跨平台Hook |
| `task_router.py` | 任务路由 |