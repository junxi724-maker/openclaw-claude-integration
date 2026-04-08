from task_router import TaskRouter

# 初始化任务路由器
task_router = TaskRouter()

# 测试用例
test_cases = [
    # 代码相关任务
    "生成一个Python函数，计算斐波那契数列的第n项",
    "分析以下Python代码:\n```python\ndef factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)\n```",
    "修复这个JavaScript代码中的bug:\n```javascript\nfunction sum(a, b) {\n    return a + b + c;\n}\n```",
    
    # 财务任务
    "分析一家公司的财务报表，找出潜在的风险",
    
    # 法律任务
    "分析一份合同的法律风险",
    
    # 战略任务
    "为一家科技公司制定五年发展战略",
    
    # 日常任务
    "提醒我明天上午10点开会",
    "今天天气怎么样？"
]

# 运行测试
print("=== 集成测试 ===")
print("="*60)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n=== 测试用例 #{i} ===")
    print(f"任务: {test_case}")
    print("-"*60)
    
    try:
        result = task_router.process_and_route(test_case)
        print(result)
    except Exception as e:
        print(f"测试失败: {str(e)}")
    
    print("="*60)