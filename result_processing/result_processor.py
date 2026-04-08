import re
import json

class ResultProcessor:
    def __init__(self):
        # 代码块正则表达式
        self.code_block_pattern = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)
        
        # 语言映射
        self.language_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'cpp': 'c++',
            'cs': 'c#',
            'go': 'go',
            'rs': 'rust',
            'php': 'php',
            'rb': 'ruby',
            'swift': 'swift',
            'kt': 'kotlin',
            'html': 'html',
            'css': 'css',
            'sql': 'sql',
            'sh': 'shell'
        }
    
    def extract_code_blocks(self, content):
        """
        提取内容中的代码块
        
        Args:
            content: Claude的响应内容
            
        Returns:
            list: 提取的代码块列表
        """
        code_blocks = []
        matches = self.code_block_pattern.findall(content)
        
        for lang, code in matches:
            # 规范化语言名称
            normalized_lang = self._normalize_language(lang)
            code_blocks.append({
                'language': normalized_lang,
                'code': code.strip()
            })
        
        return code_blocks
    
    def _normalize_language(self, lang):
        """
        规范化语言名称
        
        Args:
            lang: 语言代码
            
        Returns:
            str: 规范化后的语言名称
        """
        lang = lang.lower()
        return self.language_map.get(lang, lang) if lang else 'code'
    
    def format_result(self, content, task_type=None):
        """
        格式化结果

        Args:
            content: Claude的响应内容
            task_type: 任务类型

        Returns:
            dict: 格式化后的结果
        """
        # 处理JSON格式的响应（Claude CLI --print模式）
        content = self._parse_claude_json_response(content)

        # 提取代码块
        code_blocks = self.extract_code_blocks(content)

        # 提取纯文本内容（去除代码块）
        text_content = self.code_block_pattern.sub('', content).strip()

        # 根据任务类型进行不同的格式化
        if task_type == 'code_generation':
            return self._format_code_generation_result(code_blocks, text_content)
        elif task_type == 'code_analysis':
            return self._format_code_analysis_result(text_content)
        elif task_type == 'code_fix':
            return self._format_code_fix_result(code_blocks, text_content)
        elif task_type == 'code_optimization':
            return self._format_code_optimization_result(code_blocks, text_content)
        else:
            return self._format_generic_result(code_blocks, text_content)

    def _parse_claude_json_response(self, content):
        """
        解析Claude CLI返回的JSON格式响应

        Args:
            content: 原始响应内容

        Returns:
            str: 解析后的文本内容
        """
        # 尝试解析JSON
        if content.strip().startswith('{'):
            try:
                data = json.loads(content)
                # 检查是否是Claude的JSON响应格式
                if 'type' in data and data['type'] == 'result':
                    # 返回result字段的内容
                    return data.get('result', content)
                elif 'message' in data:
                    # 可能是完整的消息格式
                    msg = data['message']
                    if isinstance(msg, dict) and 'content' in msg:
                        contents = msg['content']
                        text_parts = []
                        for c in contents:
                            if c.get('type') == 'text':
                                text_parts.append(c.get('text', ''))
                        return '\n'.join(text_parts)
                elif 'text' in data:
                    return data['text']
            except json.JSONDecodeError:
                pass

        # 如果不是JSON，返回原始内容
        return content
    
    def _format_code_generation_result(self, code_blocks, text_content):
        """
        格式化代码生成结果
        """
        return {
            'type': 'code_generation',
            'code_blocks': code_blocks,
            'explanation': text_content,
            'summary': f"Generated {len(code_blocks)} code block(s)"
        }
    
    def _format_code_analysis_result(self, text_content):
        """
        格式化代码分析结果
        """
        # 尝试提取分析的各个部分
        sections = {
            'quality': self._extract_section(text_content, r'1\. Code quality assessment:(.*?)2\.'),
            'issues': self._extract_section(text_content, r'2\. Potential bugs or issues:(.*?)3\.'),
            'optimization': self._extract_section(text_content, r'3\. Optimization suggestions:(.*?)4\.'),
            'best_practices': self._extract_section(text_content, r'4\. Best practices recommendations:(.*?)$')
        }
        
        return {
            'type': 'code_analysis',
            'sections': sections,
            'full_analysis': text_content,
            'summary': "Code analysis completed"
        }
    
    def _format_code_fix_result(self, code_blocks, text_content):
        """
        格式化代码修复结果
        """
        return {
            'type': 'code_fix',
            'fixed_code': code_blocks[0]['code'] if code_blocks else '',
            'explanation': text_content,
            'summary': "Code fix completed"
        }
    
    def _format_code_optimization_result(self, code_blocks, text_content):
        """
        格式化代码优化结果
        """
        return {
            'type': 'code_optimization',
            'optimized_code': code_blocks[0]['code'] if code_blocks else '',
            'explanation': text_content,
            'summary': "Code optimization completed"
        }
    
    def _format_generic_result(self, code_blocks, text_content):
        """
        格式化通用结果
        """
        return {
            'type': 'generic',
            'code_blocks': code_blocks,
            'text_content': text_content,
            'summary': f"Processed result with {len(code_blocks)} code block(s)"
        }
    
    def _extract_section(self, content, pattern):
        """
        提取内容中的特定部分
        
        Args:
            content: 完整内容
            pattern: 正则表达式模式
            
        Returns:
            str: 提取的部分内容
        """
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def generate_user_friendly_output(self, formatted_result):
        """
        生成用户友好的输出
        
        Args:
            formatted_result: 格式化后的结果
            
        Returns:
            str: 用户友好的输出
        """
        output = []
        
        # 添加摘要
        output.append(f"📋 {formatted_result['summary']}")
        output.append("")
        
        # 根据结果类型添加不同内容
        if formatted_result['type'] == 'code_generation':
            # 代码生成结果
            if formatted_result['code_blocks']:
                for i, block in enumerate(formatted_result['code_blocks'], 1):
                    output.append(f"💻 Code Block #{i} ({block['language']}):")
                    output.append("```" + block['language'])
                    output.append(block['code'])
                    output.append("```")
                    output.append("")
            
            if formatted_result['explanation']:
                output.append("📝 Explanation:")
                output.append(formatted_result['explanation'])
                output.append("")
        
        elif formatted_result['type'] == 'code_analysis':
            # 代码分析结果
            sections = formatted_result['sections']
            
            if sections['quality']:
                output.append("🔍 Code Quality Assessment:")
                output.append(sections['quality'])
                output.append("")
            
            if sections['issues']:
                output.append("🐛 Potential Bugs or Issues:")
                output.append(sections['issues'])
                output.append("")
            
            if sections['optimization']:
                output.append("⚡ Optimization Suggestions:")
                output.append(sections['optimization'])
                output.append("")
            
            if sections['best_practices']:
                output.append("✅ Best Practices Recommendations:")
                output.append(sections['best_practices'])
                output.append("")
        
        elif formatted_result['type'] in ['code_fix', 'code_optimization']:
            # 代码修复或优化结果
            code_key = 'fixed_code' if formatted_result['type'] == 'code_fix' else 'optimized_code'
            
            if formatted_result[code_key]:
                output.append(f"✅ {'Fixed' if formatted_result['type'] == 'code_fix' else 'Optimized'} Code:")
                output.append("```code")
                output.append(formatted_result[code_key])
                output.append("```")
                output.append("")
            
            if formatted_result['explanation']:
                output.append("📝 Explanation:")
                output.append(formatted_result['explanation'])
                output.append("")
        
        else:
            # 通用结果
            if formatted_result['code_blocks']:
                for i, block in enumerate(formatted_result['code_blocks'], 1):
                    output.append(f"💻 Code Block #{i} ({block['language']}):")
                    output.append("```" + block['language'])
                    output.append(block['code'])
                    output.append("```")
                    output.append("")
            
            if formatted_result['text_content']:
                output.append("📝 Content:")
                output.append(formatted_result['text_content'])
                output.append("")
        
        return '\n'.join(output)