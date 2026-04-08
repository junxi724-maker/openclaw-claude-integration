from plugin import ClaudeIntegration

class TaskRouter:
    def __init__(self):
        # 初始化Claude集成
        self.claude_integration = ClaudeIntegration()
        
        # 定义任务分类
        self.task_categories = {
            'code': {
                'keywords': [
                    'code', '编程', '写代码', '生成代码', '代码生成',
                    '代码分析', '分析代码', 'debug', '调试', 'bug',
                    '修复', '优化', '重构', 'refactor', 'optimize',
                    'algorithm', '算法', '实现', 'implement', '开发'
                ],
                'languages': [
                    'python', 'javascript', 'java', 'c++', 'c#',
                    'go', 'rust', 'php', 'ruby', 'swift',
                    'kotlin', 'typescript', 'html', 'css', 'sql', 'shell'
                ]
            },
            'finance': {
                'keywords': [
                    '财务', '金融', '投资', '股票', '债券',
                    '预算', '报表', '分析', '财务模型', '现金流'
                ]
            },
            'legal': {
                'keywords': [
                    '法律', '合同', '法规', '合规', '条款',
                    '协议', '法律分析', '风险评估'
                ]
            },
            'strategy': {
                'keywords': [
                    '战略', '策略', '规划', '计划', '决策',
                    '分析', '建议', '咨询'
                ]
            },
            'daily': {
                'keywords': [
                    '提醒', '日程', '安排', '计划', '任务',
                    '天气', '时间', '日期', '帮助', '指导'
                ]
            }
        }
    
    def route_task(self, task):
        """
        路由任务
        
        Args:
            task: 任务描述
            
        Returns:
            dict: 路由结果
        """
        task_lower = task.lower()
        
        # 分析任务类别
        category = self._identify_category(task_lower)
        
        # 根据类别决定处理方式
        if category == 'code':
            # 代码相关任务，使用Claude处理
            return self._route_to_claude(task)
        elif category in ['finance', 'legal']:
            # 财务和法律任务，可以使用Claude的专业能力
            return self._route_to_claude(task)
        elif category == 'strategy':
            # 战略决策任务，使用OpenClaw处理
            return self._route_to_openclaw(task, "战略决策咨询")
        elif category == 'daily':
            # 日常任务，使用OpenClaw处理
            return self._route_to_openclaw(task, "日常任务")
        else:
            # 其他任务，默认使用OpenClaw处理
            return self._route_to_openclaw(task, "通用任务")
    
    def _identify_category(self, task):
        """
        识别任务类别
        
        Args:
            task: 任务描述（小写）
            
        Returns:
            str: 任务类别
        """
        # 检查代码类别
        if any(keyword in task for keyword in self.task_categories['code']['keywords']):
            return 'code'
        if any(lang in task for lang in self.task_categories['code']['languages']):
            return 'code'
        
        # 检查其他类别
        for category, info in self.task_categories.items():
            if category == 'code':
                continue
            if any(keyword in task for keyword in info['keywords']):
                return category
        
        # 默认类别
        return 'other'
    
    def _route_to_claude(self, task):
        """
        路由到Claude处理
        
        Args:
            task: 任务描述
            
        Returns:
            dict: 处理结果
        """
        try:
            result = self.claude_integration.process_task(task)
            return {
                'handler': 'Claude',
                'result': result,
                'status': 'success'
            }
        except Exception as e:
            return {
                'handler': 'Claude',
                'result': f"Error: {str(e)}",
                'status': 'error'
            }
    
    def _route_to_openclaw(self, task, task_type):
        """
        路由到OpenClaw处理
        
        Args:
            task: 任务描述
            task_type: 任务类型
            
        Returns:
            dict: 处理结果
        """
        # 这里返回一个提示，实际集成时会调用OpenClaw的相应功能
        return {
            'handler': 'OpenClaw',
            'result': f"This {task_type} will be handled by OpenClaw's regular functionality.",
            'status': 'success'
        }
    
    def process_and_route(self, task):
        """
        处理并路由任务
        
        Args:
            task: 任务描述
            
        Returns:
            str: 处理结果
        """
        route_result = self.route_task(task)
        
        # 生成用户友好的输出
        output = []
        output.append(f"🎯 Task routed to: {route_result['handler']}")
        output.append("")
        output.append(route_result['result'])
        
        return '\n'.join(output)