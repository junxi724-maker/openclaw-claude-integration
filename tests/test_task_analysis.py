from task_analysis import TaskAnalyzer

class TestTaskAnalyzer:
    def test_init(self):
        """测试初始化"""
        analyzer = TaskAnalyzer()
        assert analyzer is not None
    
    def test_is_code_related(self):
        """测试代码相关任务识别"""
        analyzer = TaskAnalyzer()
        
        # 测试代码相关任务
        assert analyzer.is_code_related('生成一个Python函数')
        assert analyzer.is_code_related('分析JavaScript代码')
        assert analyzer.is_code_related('修复bug')
        assert analyzer.is_code_related('优化算法')
        
        # 测试非代码相关任务
        assert not analyzer.is_code_related('今天天气怎么样？')
        assert not analyzer.is_code_related('提醒我明天开会')
        assert not analyzer.is_code_related('分析财务报表')
    
    def test_detect_language(self):
        """测试编程语言检测"""
        analyzer = TaskAnalyzer()
        
        # 测试编程语言检测
        assert analyzer.detect_language('生成Python代码') == 'python'
        assert analyzer.detect_language('JavaScript函数') == 'javascript'
        assert analyzer.detect_language('Java程序') == 'java'
        assert analyzer.detect_language('C++代码') == 'c++'
        assert analyzer.detect_language('Go语言') == 'go'
        assert analyzer.detect_language('Rust程序') == 'rust'
        
        # 测试未检测到语言
        assert analyzer.detect_language('分析代码') is None
        assert analyzer.detect_language('今天天气怎么样？') is None
    
    def test_identify_task_type(self):
        """测试任务类型分类"""
        analyzer = TaskAnalyzer()
        
        # 测试代码生成任务
        assert analyzer.identify_task_type('生成Python代码') == 'code_generation'
        assert analyzer.identify_task_type('写一个JavaScript函数') == 'code_generation'
        
        # 测试代码分析任务
        assert analyzer.identify_task_type('分析Python代码') == 'code_analysis'
        assert analyzer.identify_task_type('检查JavaScript代码') == 'code_analysis'
        
        # 测试代码修复任务
        assert analyzer.identify_task_type('修复bug') == 'code_fix'
        assert analyzer.identify_task_type('调试代码') == 'code_fix'
        
        # 测试代码优化任务
        assert analyzer.identify_task_type('优化代码') == 'code_optimization'
        assert analyzer.identify_task_type('提高代码性能') == 'code_optimization'
        
        # 测试未识别任务类型
        assert analyzer.identify_task_type('今天天气怎么样？') is None
    
    def test_analyze_task(self):
        """测试任务分析功能"""
        analyzer = TaskAnalyzer()
        
        # 测试代码生成任务
        result = analyzer.analyze_task('生成Python代码')
        assert result['is_code_related'] is True
        assert result['language'] == 'python'
        assert result['task_type'] == 'code_generation'
        assert result['original_task'] == '生成Python代码'
        
        # 测试代码分析任务
        result = analyzer.analyze_task('分析JavaScript代码')
        assert result['is_code_related'] is True
        assert result['language'] == 'javascript'
        assert result['task_type'] == 'code_analysis'
        assert result['original_task'] == '分析JavaScript代码'
        
        # 测试非代码任务
        result = analyzer.analyze_task('今天天气怎么样？')
        assert result['is_code_related'] is False
        assert result['language'] is None
        assert result['task_type'] is None
        assert result['original_task'] == '今天天气怎么样？'