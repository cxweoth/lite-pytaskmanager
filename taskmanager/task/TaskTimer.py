import time
import datetime

class TaskTimer:

    def __init__(self, timeout) -> None:
        # running datetime
        self._start_datetime = None # datetime
        self._finish_datetime = None # datetime

        # running time
        self._start_time = None # seconds
        self._finish_time = None # seconds

        # timeout
        self._timeout = timeout
    
    @property
    def is_timeout(self):
        now_time = time.time()
        now_running_time = now_time-self._start_time
        if now_running_time > self._timeout:
            return True
        return False

    def timer_start(self):
        self._start_datetime = datetime.datetime.now()
        self._start_time = time.time()

    def timer_stop(self):
        self._finish_datetime = datetime.datetime.now()
        self._finish_time = time.time()

    def time_report(self):
        running_time = self._finish_time - self._start_time
        return self._start_datetime, self._finish_datetime, running_time

