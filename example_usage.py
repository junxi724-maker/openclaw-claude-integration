from plugin import ClaudeIntegration

# 初始化Claude集成
claude_integration = ClaudeIntegration()

# 示例1: 代码生成任务
print("=== 示例1: 代码生成任务 ===")
task1 = "生成一个Python函数，计算斐波那契数列的第n项"
try:
    result1 = claude_integration.process_task(task1)
    print(result1)
except Exception as e:
    print(f"Error: {str(e)}")

print("\n" + "="*50 + "\n")

# 示例2: 代码分析任务
print("=== 示例2: 代码分析任务 ===")
task2 = "分析以下Python代码:\n```python\ndef factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)\n```"
try:
    result2 = claude_integration.process_task(task2)
    print(result2)
except Exception as e:
    print(f"Error: {str(e)}")

print("\n" + "="*50 + "\n")

# 示例3: 非代码任务
print("=== 示例3: 非代码任务 ===")
task3 = "今天天气怎么样？"
try:
    result3 = claude_integration.process_task(task3)
    print(result3)
except Exception as e:
    print(f"Error: {str(e)}")