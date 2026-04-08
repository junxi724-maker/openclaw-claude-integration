import os
import subprocess
import json
import tempfile
import shutil

# 尝试加载.env文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class ClaudeClient:
    def __init__(self):
        """初始化Claude客户端"""
        # 获取配置
        self.use_local_claude = os.getenv('USE_LOCAL_CLAUDE', 'true').lower() == 'true'
        self.claude_path = os.getenv('CLAUDE_BIN_PATH', '/Users/wjx/.bun/bin/claude-code-best')
        self.model = os.getenv('CLAUDE_MODEL', 'MiniMax-M2.5')
        self.timeout = int(os.getenv('API_TIMEOUT', '120'))
        self.workspace_dir = os.getenv('CLAUDE_WORKSPACE_DIR', '/tmp/openclaw-claude-workspace')

        # 确保工作目录存在
        os.makedirs(self.workspace_dir, exist_ok=True)

    def _run_claude(self, prompt, purpose="general"):
        """
        通过子进程运行Claude Code CLI

        Args:
            prompt: 提示内容
            purpose: 任务目的（general/code/analyze）

        Returns:
            Claude的响应内容
        """
        if not self.use_local_claude:
            return self._get_mock_response(prompt)

        # 使用--print模式非交互式运行
        cmd = [
            self.claude_path,
            '--print',
            '--output-format', 'json',
            '--no-session-persistence',
            '--bare',
            '--add-dir', self.workspace_dir,
            '--model', self.model,
            prompt
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.workspace_dir
            )

            if result.returncode != 0:
                # 如果CLI出错，尝试解析错误信息
                error_msg = result.stderr or result.stdout
                print(f"Claude CLI error: {error_msg}")
                return self._get_mock_response(prompt)

            # 解析JSON输出
            output = result.stdout.strip()
            if not output:
                return "No response from Claude"

            # 尝试解析JSON，提取文本内容
            try:
                # Claude可能输出多行JSON，需要找到最后一个有效的JSON对象
                lines = output.split('\n')
                for line in reversed(lines):
                    line = line.strip()
                    if line.startswith('{') and line.endswith('}'):
                        data = json.loads(line)
                        # 提取text字段
                        if 'type' in data and data['type'] == 'content':
                            return data.get('text', '')
                        elif 'message' in data:
                            # 可能是完整响应
                            msg = data.get('message', {})
                            if isinstance(msg, dict) and 'content' in msg:
                                contents = msg['content']
                                text_parts = []
                                for c in contents:
                                    if c.get('type') == 'text':
                                        text_parts.append(c.get('text', ''))
                                return '\n'.join(text_parts)
                        elif 'text' in data:
                            return data['text']
                # 如果没有找到JSON，返回原始输出
                return output

            except json.JSONDecodeError:
                # 如果不是JSON，直接返回输出
                return output

        except subprocess.TimeoutExpired:
            return f"Claude CLI timeout after {self.timeout} seconds"
        except FileNotFoundError:
            return f"Claude CLI not found at {self.claude_path}"
        except Exception as e:
            print(f"Claude CLI error: {str(e)}")
            return self._get_mock_response(prompt)

    def send_message(self, prompt, max_tokens=4096, temperature=0.7):
        """
        发送消息到Claude

        Args:
            prompt: 提示内容
            max_tokens: 最大令牌数（用于提示Claude）
            temperature: 温度参数

        Returns:
            Claude的响应
        """
        return self._run_claude(prompt, purpose="general")

    def generate_code(self, prompt, language=None):
        """
        生成代码

        Args:
            prompt: 代码生成提示
            language: 编程语言

        Returns:
            生成的代码
        """
        lang = language or "python"
        full_prompt = f"""请生成{language}代码来完成以下任务：

{prompt}

请只提供代码，不要包含解释。如果需要注释，请用中文注释。"""

        return self._run_claude(full_prompt, purpose="code")

    def analyze_code(self, code, language=None):
        """
        分析代码

        Args:
            code: 要分析的代码
            language: 编程语言

        Returns:
            代码分析结果
        """
        lang = language or "python"
        full_prompt = f"""请分析以下{language}代码：

```{lang}
{code}
```

请提供：
1. 代码质量评估
2. 潜在问题或bug
3. 优化建议
4. 最佳实践建议"""

        return self._run_claude(full_prompt, purpose="analyze")

    def fix_code(self, code, language=None, description=None):
        """
        修复代码

        Args:
            code: 要修复的代码
            language: 编程语言
            description: 问题描述

        Returns:
            修复后的代码
        """
        lang = language or "python"
        desc = description or "修复代码中的bug"
        full_prompt = f"""请修复以下{language}代码中的bug：

```{lang}
{code}
```

问题描述：{desc}

请提供修复后的代码，并解释修复的内容。"""

        return self._run_claude(full_prompt, purpose="fix")

    def check_local_claude_health(self):
        """
        检查本地Claude Code的健康状态

        Returns:
            dict: 健康状态信息
        """
        if not self.use_local_claude:
            return {
                'status': 'inactive',
                'message': 'Local Claude is not enabled'
            }

        # 检查CLI是否存在
        if not os.path.exists(self.claude_path):
            return {
                'status': 'unavailable',
                'message': f'Claude CLI not found at {self.claude_path}'
            }

        # 检查是否可以运行
        try:
            result = subprocess.run(
                [self.claude_path, '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return {
                    'status': 'healthy',
                    'message': f'Claude CLI is available: {result.stdout.strip()}'
                }
            else:
                return {
                    'status': 'unhealthy',
                    'message': f'Claude CLI error: {result.stderr}'
                }
        except Exception as e:
            return {
                'status': 'unavailable',
                'message': f'Failed to run Claude CLI: {str(e)}'
            }

    def _get_mock_response(self, prompt):
        """获取模拟响应（备用）"""
        prompt_lower = prompt.lower()

        if '斐波那契' in prompt_lower:
            return "```python\ndef fibonacci(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    else:\n        return fibonacci(n-1) + fibonacci(n-2)\n```"
        elif '生成' in prompt_lower and '代码' in prompt_lower:
            if 'python' in prompt_lower:
                return "```python\ndef add(a, b):\n    return a + b\n```"
            elif 'javascript' in prompt_lower or 'js' in prompt_lower:
                return "```javascript\nfunction add(a, b) {\n    return a + b;\n}\n```"
            else:
                return "```python\ndef add(a, b):\n    return a + b\n```"
        elif '分析' in prompt_lower and '代码' in prompt_lower:
            return "1. 代码质量：代码结构清晰，符合基本语法规范\n\n2. 潜在问题：\n- 没有处理边界情况\n- 缺少输入验证\n\n3. 优化建议：\n- 添加参数验证\n- 添加类型提示\n\n4. 最佳实践：\n- 添加文档字符串\n- 添加单元测试"
        elif '修复' in prompt_lower and 'bug' in prompt_lower:
            return "修复已完成。问题是使用了未定义的变量 `c`，已将其移除。"
        elif '财务' in prompt_lower:
            return "财务分析：\n1. 流动性风险\n2. 盈利能力下降\n3. 债务负担\n4. 客户集中度风险"
        elif '法律' in prompt_lower or '合同' in prompt_lower:
            return "法律风险分析：\n1. 条款模糊\n2. 责任限制\n3. 知识产权不明确\n4. 终止条款不平衡"
        else:
            return "这是测试响应。请配置有效的API后端以获取真实响应。"