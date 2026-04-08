from task_router import TaskRouter

class TestTaskRouter:
    def test_init(self):
        """测试初始化"""
        router = TaskRouter()
        assert router is not None
    
    def test_route_task(self):
        """测试任务路由"""
        router = TaskRouter()
        
        # 测试代码生成任务路由
        result = router.route_task('生成Python代码')
        assert result['handler'] == 'Claude'
        assert result['status'] == 'success'
        assert len(result['result']) > 0
        
        # 测试代码分析任务路由
        result = router.route_task('分析Python代码')
        assert result['handler'] == 'Claude'
        assert result['status'] == 'success'
        assert len(result['result']) > 0
        
        # 测试财务任务路由
        result = router.route_task('分析财务报表')
        assert result['handler'] == 'Claude'
        assert result['status'] == 'success'
        assert len(result['result']) > 0
        
        # 测试法律任务路由
        result = router.route_task('分析合同')
        assert result['handler'] == 'Claude'
        assert result['status'] == 'success'
        assert len(result['result']) > 0
        
        # 测试战略任务路由
        result = router.route_task('制定企业战略')
        assert result['handler'] == 'OpenClaw'
        assert result['status'] == 'success'
        assert '战略决策咨询' in result['result']
        
        # 测试日常任务路由
        result = router.route_task('今天天气怎么样？')
        assert result['handler'] == 'OpenClaw'
        assert result['status'] == 'success'
        assert '日常任务' in result['result']
    
    def test_process_and_route(self):
        """测试处理和路由功能"""
        router = TaskRouter()
        
        # 测试代码生成任务
        result = router.process_and_route('生成Python代码')
        assert '🎯 Task routed to: Claude' in result
        assert len(result) > 0
        
        # 测试代码分析任务
        result = router.process_and_route('分析Python代码')
        assert '🎯 Task routed to: Claude' in result
        assert len(result) > 0
        
        # 测试财务任务
        result = router.process_and_route('分析财务报表')
        assert '🎯 Task routed to: Claude' in result
        assert len(result) > 0
        
        # 测试法律任务
        result = router.process_and_route('分析合同')
        assert '🎯 Task routed to: Claude' in result
        assert len(result) > 0
        
        # 测试战略任务
        result = router.process_and_route('制定企业战略')
        assert '🎯 Task routed to: OpenClaw' in result
        assert len(result) > 0
        
        # 测试日常任务
        result = router.process_and_route('今天天气怎么样？')
        assert '🎯 Task routed to: OpenClaw' in result
        assert len(result) > 0