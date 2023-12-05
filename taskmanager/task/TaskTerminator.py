import time
import ctypes, inspect
import threading
from threading import Event

from ..logutil import Logger

class TaskTerminator:

    def __init__(self, task, terminate_limit, logger:Logger) -> None:
        
        self._task = task

        self._logger = logger
        self._log_title = f"[{self.__class__.__name__}][{self._task.task_name}]"

        self._is_terminate = False
        self._is_force_kill = False
        self._terminate_start_time = None
        self._terminate_limit = terminate_limit
        self._terminate_event = Event()

    @property
    def is_terminate(self):
        return self._is_terminate

    @property
    def terminate_event(self):
        return self._terminate_event
    
    @property
    def is_force_kill(self):
        return self._is_force_kill
    
    @property
    def is_finish_terminating(self):

        if not self._task.task_thread in threading.enumerate():
            return True
        
        now_time = time.time()
        now_running_time = now_time-self._terminate_start_time
        if now_running_time <= self._terminate_limit:
            return False
        
        if not self._is_force_kill:
            self._force_kill_task_thread()
            self._logger.critical(f"{self._log_title} force kill task thread due to terminate event set timeout")

        return False

    def terminate(self):
        self._is_terminate = True
        self._terminate_task_thread()
    
    def _terminate_task_thread(self): 
        self._terminate_event.set()
        self._terminate_start_time = time.time()

    def _force_kill_task_thread(self): 
        self._is_force_kill = True
        try:
            self._async_raise(self._task.task_thread.ident, SystemExit)
        except Exception as err:
            self._logger.critical(f"{self._log_title} force kill task thread failed: {str(err)}")

    @staticmethod
    def _async_raise(tid, exctype): 
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid) 
        if not inspect.isclass(exctype): 
            exctype = type(exctype) 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype)) 
        if res == 0: 
            raise ValueError("invalid thread id") 
        elif res != 1: 
            """ 
            if it returns a number greater than one, you’re in 
            trouble, # and you should call it again with exc=NULL to  
            revert the effect
            """
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None) 
            raise SystemError("PyThreadState_SetAsyncExc failed") 