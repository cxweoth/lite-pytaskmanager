import inspect

class TaskConfig:
    def __init__(self, task_func, timeout, args=(), kwargs={}, terminate_limit=30*60) -> None:
        self.task_func = task_func
        self.timeout = timeout
        self.args = args
        self.kwargs = kwargs
        self.terminate_limit = terminate_limit
        if not 'terminate_event' in inspect.signature(self.task_func).parameters:
            raise ValueError("task_func must have terminate_event parameter")