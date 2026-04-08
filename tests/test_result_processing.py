from result_processing import ResultProcessor

class TestResultProcessor:
    def test_init(self):
        """测试初始化"""
        processor = ResultProcessor()
        assert processor is not None
    
    def test_extract_code_blocks(self):
        """测试代码块提取"""
        processor = ResultProcessor()
        
        # 测试提取单个代码块
        content = "```python\ndef add(a, b):\n    return a + b\n```"
        code_blocks = processor.extract_code_blocks(content)
        assert len(code_blocks) == 1
        assert code_blocks[0]['language'] == 'python'
        assert code_blocks[0]['code'] == 'def add(a, b):\n    return a + b'
        
        # 测试提取多个代码块
        content = "```python\ndef add(a, b):\n    return a + b\n```\n```javascript\nfunction add(a, b) {\n    return a + b;\n}\n```"
        code_blocks = processor.extract_code_blocks(content)
        assert len(code_blocks) == 2
        assert code_blocks[0]['language'] == 'python'
        assert code_blocks[1]['language'] == 'javascript'
        
        # 测试无代码块
        content = "这是一个没有代码块的内容"
        code_blocks = processor.extract_code_blocks(content)
        assert len(code_blocks) == 0
    
    def test_format_result(self):
        """测试结果格式化"""
        processor = ResultProcessor()
        
        # 测试代码生成结果格式化
        content = "```python\ndef add(a, b):\n    return a + b\n```"
        result = processor.format_result(content, 'code_generation')
        assert result['type'] == 'code_generation'
        assert len(result['code_blocks']) == 1
        assert result['code_blocks'][0]['language'] == 'python'
        assert result['summary'] == 'Generated 1 code block(s)'
        
        # 测试代码分析结果格式化
        content = "1. Code quality assessment: Good\n2. Potential bugs or issues: None\n3. Optimization suggestions: None\n4. Best practices recommendations: None"
        result = processor.format_result(content, 'code_analysis')
        assert result['type'] == 'code_analysis'
        assert result['sections']['quality'] == 'Good'
        assert result['summary'] == 'Code analysis completed'
        
        # 测试通用结果格式化
        content = "这是一个通用结果"
        result = processor.format_result(content)
        assert result['type'] == 'generic'
        assert result['text_content'] == '这是一个通用结果'
        assert result['summary'] == 'Processed result with 0 code block(s)'
    
    def test_generate_user_friendly_output(self):
        """测试用户友好输出生成"""
        processor = ResultProcessor()
        
        # 测试代码生成结果的用户友好输出
        formatted_result = {
            'type': 'code_generation',
            'code_blocks': [{'language': 'python', 'code': 'def add(a, b):\n    return a + b'}],
            'explanation': '这是一个加法函数',
            'summary': 'Generated 1 code block(s)'
        }
        output = processor.generate_user_friendly_output(formatted_result)
        assert '📋 Generated 1 code block(s)' in output
        assert '💻 Code Block #1 (python):' in output
        assert 'def add(a, b):' in output
        assert '📝 Explanation:' in output
        assert '这是一个加法函数' in output
        
        # 测试代码分析结果的用户友好输出
        formatted_result = {
            'type': 'code_analysis',
            'sections': {
                'quality': 'Good',
                'issues': 'None',
                'optimization': 'None',
                'best_practices': 'None'
            },
            'full_analysis': '1. Code quality assessment: Good\n2. Potential bugs or issues: None\n3. Optimization suggestions: None\n4. Best practices recommendations: None',
            'summary': 'Code analysis completed'
        }
        output = processor.generate_user_friendly_output(formatted_result)
        assert '📋 Code analysis completed' in output
        assert '🔍 Code Quality Assessment:' in output
        assert 'Good' in output
        assert '🐛 Potential Bugs or Issues:' in output
        assert 'None' in output