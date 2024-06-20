import time

from .TimePlan import TimePlan, TimePlanType

from .task import TaskConfig, Task
from .taskscheduler import TaskScheduler
from .logutil import Logger


class Manager:

    def __init__(self, manager_name, sleep_time=1, streaming_log_level="DEBUG") -> None:

        self._manager_name = manager_name
        self._sleep_time = sleep_time

        # Initialize logging and task dictionary
        self._initialize_logging(streaming_log_level)
        self._initialize_task_dict()

        # scheduler
        self._task_scheduler = TaskScheduler()

    def _initialize_logging(self, streaming_log_level):
        # logging setting
        self._log_title = f"[{self.__class__.__name__}]"
        logger_name = f"{self._manager_name}"
        self._logger = Logger(logger_name, streaming_log_level)

    def _initialize_task_dict(self):
        # task dict
        self._task_dict = {}

    @property
    def manager_name(self):
        return self._manager_name
    
    @property
    def logger(self):
        return self._logger
    
    @property
    def task_dict(self):
        return self._task_dict
    
    ###################################### enable tools ######################################
    def enable_physical_logging(self, log_folder_path, log_level="DEBUG", rotate_days=30):
        """
        Enables physical logging to a file.

        Parameters:
        - log_folder_path (str): The path to the folder where the log file should be stored.
        - log_level (str, optional): The logging level to use.
        - rotate_days (int, optional): The number of days after which the log file should be rotated.
        Returns:
        None
        """
        
        if not isinstance(log_folder_path, str):
            raise ValueError("log_folder_path must be string")
        
        try:
            self._logger.enable_physical_logging(log_folder_path, log_level, rotate_days)
        except Exception as e:
            raise Exception(f"enable physical logging failed: {str(e)}")

    ###########################################################################################

    ###################################### add task ###########################################

    def add_task(self, task_name:str, task_func, time_plan:TimePlan, timeout:int, *args, **kwargs):
        """
        Adds a task to the manager.
 
        Parameters:
        - task_name (str): The name of the task.
        - task_func (callable): The function that implements the task.
        - time_plan (TimePlan): The schedule on which the task should run.
        - timeout (int): Maximum allowed runtime for the task in seconds.
        - args (tuple, optional): Positional arguments to pass to task_func.
        - kwargs (dict, optional): Keyword arguments to pass to task_func.
 
        Returns:
        None
        """

        task_config = TaskConfig(task_func, timeout, args, kwargs)
        task = Task(task_config, task_name, self._logger)

        # According time plan to create schedule
        try:
            time_plan_type = time_plan.time_plan_type
            if time_plan_type == TimePlanType.INTERVAL:
                self._task_scheduler.create_interval_schedule(time_plan.plan, task.run)
            elif time_plan_type == TimePlanType.DAILY_POINTS:
                self._task_scheduler.create_daily_schedule(time_plan.plan, task.run)
            elif time_plan_type == TimePlanType.WEEKLY_POINTS:
                self._task_scheduler.create_weekly_schedule(time_plan.plan, task.run)
        except Exception as e:
            raise Exception(f"create schedule failed: {str(e)}")

        # add task to task dict
        self._task_dict[task_name] = task

        # memo to logs
        log_msg = f"{self._log_title} Add task: {task_name} to manager: {self._manager_name}"
        self._logger.info(log_msg)

    ###########################################################################################

    def start(self):
        """
        Starts the manager. This includes an initial run of all tasks and then 
        continuous management of task scheduling and state handling.
        Returns:
        None
        """

        # start
        self._logger.info(f"{self._log_title} Start manager")

        # first run
        self._logger.info(f"{self._log_title} First run")
        try:
            self._first_run()
        except Exception as e:
            self._logger.critical(f"{self._log_title} first run failed: {str(e)}")
            raise Exception(f"first run failed: {str(e)}")

        # run management
        self._logger.info(f"{self._log_title} Run management")
        try:
            self._run_management()        
        except Exception as e:
            self._logger.critical(f"{self._log_title} run management failed: {str(e)}")
            raise Exception(f"run management failed: {str(e)}")

    ###########################################################################################

    def _first_run(self):
        # run immediately
        for _, task in self._task_dict.items():
            task.run()

    def _run_management(self):
        while True:  
            try:
                # trigger task by scheduling and do management
                self._schedule_tasks()
                self._manage_tasks()
            except Exception as err:
                log_msg = f"{self._log_title} main process occur problem: {str(err)}"
                self._logger.critical(log_msg)
            time.sleep(self._sleep_time)

    def _schedule_tasks(self):
        self._task_scheduler.run_pending()

    def _manage_tasks(self):
        for task_name, task in self._task_dict.items():
            if task.is_running:
                self._handle_running_state(task)                
            elif task.is_terminating:
                self._handle_terminating_state(task)
            elif task.is_done:
                self._handle_done_state(task)                
            elif task.is_terminated:
                self._handle_terminated_state(task)
            elif task.is_killed:
                self._handle_killed_state(task)

    def _handle_running_state(self, task):
        if task.is_timeout:
            task.terminate()

    def _handle_terminating_state(self, task):
        if task.is_finish_terminating:
            task.set_terminating_reslt()

    def _handle_done_state(self, task):
        result_bool, log_msg = self._take_report_and_gen_log(task)
        if result_bool:
            self._logger.info(log_msg)
        else:
            self._logger.critical(log_msg)

    def _handle_terminated_state(self, task):
        result_bool, log_msg = self._take_report_and_gen_log(task)
        self._logger.critical(log_msg)

    def _handle_killed_state(self, task):
        result_bool, log_msg = self._take_report_and_gen_log(task)
        self._logger.critical(log_msg)

    def _take_report_and_gen_log(self, task):
        result_bool, result_msg, result_args, job_status, start_datetime, finish_datetime, running_time = task.take_report()
        log_msg = f"{self._log_title} Task name: {task.task_name}, Result: {result_bool}, msg: {result_msg}, Output: {result_args}, Job Status: {job_status}, Start datetime: {str(start_datetime)}, Finish datetime: {str(finish_datetime)}, Running time: {running_time}"
        return result_bool, log_msg
    
