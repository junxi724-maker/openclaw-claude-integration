from api_client import ClaudeClient
from task_analysis import TaskAnalyzer
from result_processing import ResultProcessor

class ClaudeIntegration:
    def __init__(self):
        # 初始化各个模块
        self.claude_client = ClaudeClient()
        self.task_analyzer = TaskAnalyzer()
        self.result_processor = ResultProcessor()
    
    def process_task(self, task):
        """
        处理任务
        
        Args:
            task: 任务描述
            
        Returns:
            str: 处理结果
        """
        try:
            # 分析任务
            task_info = self.task_analyzer.analyze_task(task)
            
            # 检查是否是代码相关任务
            if task_info['is_code_related']:
                return self._process_code_task(task_info)
            else:
                # 检查是否是财务或法律任务
                task_lower = task.lower()
                if any(keyword in task_lower for keyword in ['财务', '金融', '投资', '股票', '债券', '预算', '报表', '分析', '财务模型', '现金流']):
                    # 财务任务
                    response = self.claude_client.send_message(task)
                    formatted_result = self.result_processor.format_result(response, 'finance')
                    return self.result_processor.generate_user_friendly_output(formatted_result)
                elif any(keyword in task_lower for keyword in ['法律', '合同', '法规', '合规', '条款', '协议', '法律分析', '风险评估']):
                    # 法律任务
                    response = self.claude_client.send_message(task)
                    formatted_result = self.result_processor.format_result(response, 'legal')
                    return self.result_processor.generate_user_friendly_output(formatted_result)
                else:
                    # 其他非代码任务
                    return "This task is not code-related. Please use OpenClaw's regular functionality."
                
        except Exception as e:
            return f"Error processing task: {str(e)}"
    
    def _process_code_task(self, task_info):
        """
        处理代码相关任务
        
        Args:
            task_info: 任务信息
            
        Returns:
            str: 处理结果
        """
        task = task_info['original_task']
        language = task_info['language']
        task_type = task_info['task_type']
        
        # 根据任务类型调用不同的Claude功能
        if task_type == 'code_generation':
            # 代码生成
            response = self.claude_client.generate_code(task, language)
        elif task_type == 'code_analysis':
            # 代码分析
            # 提取代码部分
            code = self._extract_code_from_task(task)
            if code:
                response = self.claude_client.analyze_code(code, language)
            else:
                return "Please provide the code to analyze."
        else:
            # 其他代码相关任务
            response = self.claude_client.send_message(task)
        
        # 处理结果
        formatted_result = self.result_processor.format_result(response, task_type)
        return self.result_processor.generate_user_friendly_output(formatted_result)
    
    def _extract_code_from_task(self, task):
        """
        从任务描述中提取代码
        
        Args:
            task: 任务描述
            
        Returns:
            str: 提取的代码
        """
        # 简单的代码提取逻辑
        # 查找代码块
        import re
        code_block_pattern = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)
        matches = code_block_pattern.findall(task)
        
        if matches:
            return matches[0][1].strip()
        
        # 如果没有代码块，返回整个任务描述
        return task