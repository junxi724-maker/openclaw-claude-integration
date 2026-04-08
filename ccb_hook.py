#!/usr/bin/env python3
"""
Claude Code CLI 优化Hook (跨平台)
支持 Windows/Mac/Linux
"""
import os
import sys
import subprocess
import json
import shutil

# 检测平台
IS_WINDOWS = sys.platform.startswith('win')

# 配置 - 根据平台自动选择
if IS_WINDOWS:
    # Windows路径
    CLAUDE_PATH = shutil.which('claude-code-best') or shutil.which('claude') or r"C:\Users\USERNAME\AppData\Roaming\npm\claude-code-best.cmd"
    MODEL = 'MiniMax-M2.5'
    WORKSPACE = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'openclaw-ccb-workspace')
else:
    # Mac/Linux路径
    CLAUDE_PATH = '/Users/wjx/.bun/bin/claude-code-best'
    MODEL = 'MiniMax-M2.5'
    WORKSPACE = '/tmp/openclaw-ccb-workspace'

EFFORT = 'low'
TIMEOUT = 60

os.makedirs(WORKSPACE, exist_ok=True)

def execute(prompt):
    """执行Claude Code CLI"""
    cmd = [
        CLAUDE_PATH,
        '--print',
        '--output-format', 'json',
        '--no-session-persistence',
        '--bare',
        '--effort', EFFORT,
        '--model', MODEL,
        prompt
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            cwd=WORKSPACE,
            shell=IS_WINDOWS
        )

        if result.returncode != 0:
            return f"❌ 错误: {result.stderr}"

        output = result.stdout.strip()
        try:
            data = json.loads(output)
            if data.get('type') == 'result':
                return data.get('result', output)
        except json.JSONDecodeError:
            return output

    except subprocess.TimeoutExpired:
        return f"⏱️ 超时（{TIMEOUT}秒）"
    except Exception as e:
        return f"❌ 执行错误: {str(e)}"

    return "无响应"

if __name__ == '__main__':
    task = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else "写一个Hello World函数"
    print(f"🔄 任务: {task}")
    result = execute(task)
    print(result)