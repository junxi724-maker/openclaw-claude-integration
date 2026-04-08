import re

class TaskAnalyzer:
    def __init__(self):
        # 代码相关关键词
        self.code_keywords = [
            'code', '编程', '写代码', '生成代码', '代码生成',
            '代码分析', '分析代码', 'debug', '调试', 'bug',
            '修复', '优化', '重构', 'refactor', 'optimize',
            'algorithm', '算法', '实现', 'implement', '开发'
        ]
        
        # 编程语言关键词
        self.language_keywords = {
            'python': ['python', 'py'],
            'javascript': ['javascript', 'js'],
            'java': ['java'],
            'c++': ['c++', 'cpp'],
            'c#': ['c#', 'csharp'],
            'go': ['go', 'golang'],
            'rust': ['rust'],
            'php': ['php'],
            'ruby': ['ruby'],
            'swift': ['swift'],
            'kotlin': ['kotlin'],
            'typescript': ['typescript', 'ts'],
            'html': ['html'],
            'css': ['css'],
            'sql': ['sql'],
            'shell': ['shell', 'bash', 'sh']
        }
        
        # 任务类型模式
        self.task_patterns = {
            'code_generation': [
                r'生成.*代码', r'写.*代码', r'编写.*代码',
                r'实现.*功能', r'code.*generate', r'generate.*code',
                r'写一个.*函数', r'创建.*函数', r'编写.*函数'
            ],
            'code_analysis': [
                r'分析.*代码', r'检查.*代码', r'代码.*分析',
                r'code.*analysis', r'analyze.*code'
            ],
            'code_fix': [
                r'修复.*bug', r'调试.*代码', r'解决.*问题',
                r'fix.*bug', r'debug.*code', r'troubleshoot'
            ],
            'code_optimization': [
                r'优化.*代码', r'提高.*性能', r'代码.*优化',
                r'optimize.*code', r'performance.*improvement'
            ]
        }
    
    def is_code_related(self, task):
        """
        判断任务是否与代码相关
        
        Args:
            task: 任务描述
            
        Returns:
            bool: 是否与代码相关
        """
        task_lower = task.lower()
        
        # 检查代码相关关键词
        for keyword in self.code_keywords:
            if keyword in task_lower:
                return True
        
        # 检查编程语言关键词
        for lang_keywords in self.language_keywords.values():
            for keyword in lang_keywords:
                if keyword in task_lower:
                    return True
        
        return False
    
    def detect_language(self, task):
        """
        检测任务中的编程语言
        
        Args:
            task: 任务描述
            
        Returns:
            str: 检测到的编程语言，未检测到返回None
        """
        task_lower = task.lower()
        
        for language, keywords in self.language_keywords.items():
            for keyword in keywords:
                if keyword in task_lower:
                    return language
        
        return None
    
    def identify_task_type(self, task):
        """
        识别任务类型
        
        Args:
            task: 任务描述
            
        Returns:
            str: 任务类型，未识别返回None
        """
        task_lower = task.lower()
        
        for task_type, patterns in self.task_patterns.items():
            for pattern in patterns:
                if re.search(pattern, task_lower):
                    return task_type
        
        return None
    
    def analyze_task(self, task):
        """
        分析任务，提取相关信息
        
        Args:
            task: 任务描述
            
        Returns:
            dict: 任务分析结果
        """
        is_code = self.is_code_related(task)
        language = self.detect_language(task)
        task_type = self.identify_task_type(task)
        
        return {
            'is_code_related': is_code,
            'language': language,
            'task_type': task_type,
            'original_task': task
        }