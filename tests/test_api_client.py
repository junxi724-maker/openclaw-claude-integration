import os
import pytest
from api_client import ClaudeClient

class TestClaudeClient:
    def test_init_with_api_key(self):
        """测试使用API密钥初始化"""
        # 保存原始API密钥
        original_api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        try:
            # 设置测试API密钥
            os.environ['ANTHROPIC_API_KEY'] = 'test_api_key'
            client = ClaudeClient()
            assert client.api_key == 'test_api_key'
            assert client.api_url == 'https://api.anthropic.com/v1/messages'
            assert client.model == 'claude-3-opus-20240229'
        finally:
            # 恢复原始API密钥
            if original_api_key:
                os.environ['ANTHROPIC_API_KEY'] = original_api_key
            else:
                del os.environ['ANTHROPIC_API_KEY']
    
    def test_init_without_api_key(self):
        """测试没有API密钥时的初始化"""
        # 保存原始API密钥
        original_api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        try:
            # 删除API密钥
            if 'ANTHROPIC_API_KEY' in os.environ:
                del os.environ['ANTHROPIC_API_KEY']
            
            # 初始化客户端（应该使用默认的测试API密钥）
            client = ClaudeClient()
            assert client.api_key == 'test_api_key'
        finally:
            # 恢复原始API密钥
            if original_api_key:
                os.environ['ANTHROPIC_API_KEY'] = original_api_key
    
    def test_send_message(self):
        """测试发送消息功能"""
        client = ClaudeClient()
        response = client.send_message('Hello, Claude!')
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_generate_code(self):
        """测试生成代码功能"""
        client = ClaudeClient()
        code = client.generate_code('生成一个Python函数，计算两个数的和', 'python')
        assert isinstance(code, str)
        assert 'def' in code
        assert 'return' in code
    
    def test_analyze_code(self):
        """测试分析代码功能"""
        client = ClaudeClient()
        code = "def add(a, b):\n    return a + b"
        analysis = client.analyze_code(code, 'python')
        assert isinstance(analysis, str)
        assert len(analysis) > 0