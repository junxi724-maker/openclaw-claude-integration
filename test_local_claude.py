import os
from api_client import ClaudeClient

# 打印环境变量调试信息
print("=== 环境变量调试 ===")
print(f"USE_LOCAL_CLAUDE: {os.getenv('USE_LOCAL_CLAUDE')}")
print(f"LOCAL_CLAUDE_API_URL: {os.getenv('LOCAL_CLAUDE_API_URL')}")
print(f"ANTHROPIC_API_KEY: {os.getenv('ANTHROPIC_API_KEY')}")
print()

# 初始化Claude客户端
client = ClaudeClient()

# 检查本地Claude状态
print("=== 检查本地Claude状态 ===")
health_status = client.check_local_claude_health()
print(f"状态: {health_status['status']}")
print(f"消息: {health_status['message']}")
print()

# 测试发送消息
print("=== 测试发送消息 ===")
try:
    response = client.send_message("Hello, Claude! 这是一个测试消息。")
    print("响应:")
    print(response)
except Exception as e:
    print(f"错误: {str(e)}")
print()

# 测试代码生成
print("=== 测试代码生成 ===")
try:
    code = client.generate_code("生成一个Python函数，计算两个数的和", "python")
    print("生成的代码:")
    print(code)
except Exception as e:
    print(f"错误: {str(e)}")
print()

# 测试代码分析
print("=== 测试代码分析 ===")
try:
    test_code = "def add(a, b):\n    return a + b"
    analysis = client.analyze_code(test_code, "python")
    print("代码分析结果:")
    print(analysis)
except Exception as e:
    print(f"错误: {str(e)}")
print()

print("=== 测试完成 ===")