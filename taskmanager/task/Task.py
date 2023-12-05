import threading

from .TaskConfig import TaskConfig
from .TaskState import TaskState
from .TaskTimer import TaskTimer
from .TaskResult import TaskResult
from .TaskTerminator import TaskTerminator

from ..logutil import Logger


class Task:

    def __init__(self, config:TaskConfig, task_name:str, logger:Logger) -> None:
        
        self._current_state = TaskState.INIT

        self._log_title = f"[{self.__class__.__name__}][{task_name}]"
        self._task_name = task_name
        self._logger = logger
        self._config = config

        # set task related params
        self._task_func = config.task_func
        self._timeout = config.timeout
        self._args = config.args
        self._kwargs = config.kwargs
        self._terminate_limit = config.terminate_limit

        self.init_basic_params()

    def _state_checker(self, state):
        return self._current_state == state
    
    # state check
    @property
    def is_init(self):
        return self._state_checker(TaskState.INIT)
    
    @property
    def is_running(self):
        return self._state_checker(TaskState.RUNNING)
    
    @property
    def is_done(self):
        return self._state_checker(TaskState.DONE)
    
    @property
    def is_terminating(self):
        return self._state_checker(TaskState.TERMINATING)
    
    @property
    def is_terminated(self):
        return self._state_checker(TaskState.TERMINATED)
    
    @property
    def is_killed(self):
        return self._state_checker(TaskState.KILLED)

    def init_basic_params(self):

         # empty task thread
        self._task_thread = None

        self._result_manager = TaskResult()
        self._task_timer = TaskTimer(self._timeout)
        self._terminator = TaskTerminator(self, self._terminate_limit, self._logger)

    @property
    def task_name(self):
        return self._task_name
    
    @property
    def task_thread(self):
        return self._task_thread
    
    # =========================================== State Change Functions =========================================

    def init(self):
        if self.is_done or self.is_terminated:
            self._current_state = TaskState.INIT
            self.init_basic_params()

    def run(self):
        if self.is_init:
            self._current_state = TaskState.RUNNING
            self._task_timer.timer_start()

            try:
                self._task_thread = threading.Thread(target=self._task_wrapper)
                self._task_thread.start()        
            except Exception as msg:
                raise(Exception(f"{self._log_title} run task thread failed: {str(msg)}"))

    def finish(self):
        if self.is_running:
            self._current_state = TaskState.DONE
            self._task_timer.timer_stop()
    
    def terminate(self):
        if self.is_running:
            self._current_state = TaskState.TERMINATING
            self._terminator.terminate()

    def set_terminating_reslt(self):
        if self.is_terminating:
            if self._terminator.is_force_kill:
                self._current_state = TaskState.KILLED
                _result_msg = Exception(f"task is killed due timeout and it is force killed")
            else:
                self._current_state = TaskState.TERMINATED   
                _result_msg = Exception(f"task is killed due timeout and it is terminated correctly")           

            _result_bool = False
            _result_args = []

            self._result_manager.insert_result(_result_bool, _result_msg, _result_args)
            self._task_timer.timer_stop()

    @property
    def is_timeout(self):
        return self._task_timer.is_timeout

    @property
    def is_finish_terminating(self):
        if self.is_terminating:
            return self._terminator.is_finish_terminating
        return False
    
    # ======================================================================================================================

    def take_report(self):
        result_bool, result_msg, result_args = self._result_manager.take_report()
        start_datetime, finish_datetime, running_time = self._task_timer.time_report()
        task_status = self._current_state.value

        if not self.is_killed:
            self.init()

        return result_bool, result_msg, result_args, task_status, start_datetime, finish_datetime, running_time

    def _task_wrapper(self):
        try:
            terminate_event = self._terminator.terminate_event
            result_bool, result_msg, *result_args = self._task_func(terminate_event, *self._args, **self._kwargs)
        except Exception as msg:
            result_bool = False
            result_msg = msg
            result_args = []

        if self._terminator.is_terminate:
            return

        self._result_manager.insert_result(result_bool, result_msg, result_args)
        self.finish()


    
