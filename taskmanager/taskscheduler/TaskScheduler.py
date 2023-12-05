from schedule import Scheduler

class TaskScheduler:

    def __init__(self) -> None:
        
        self._scehduler = Scheduler()

    def create_interval_schedule(self, interval, task_run):

        if interval is None:
            raise ValueError("interval must be int")
        if interval <= 0:
            raise ValueError("interval must be positive int")
        
        if task_run is None:
            raise ValueError("task must be Task")

        self._scehduler.every(interval).seconds.do(task_run)

    def create_daily_schedule(self, time_points, task_run):

        if time_points is None:
            raise ValueError("time_points must be list")
        if len(time_points) <= 0:
            raise ValueError("time_points must be positive list")
        
        if task_run is None:
            raise ValueError("task must be Task")

        for time_point in time_points:
            self._scehduler.every().day.at(time_point).do(task_run)

    def create_weekly_schedule(self, weekly_points, task_run):
            
        if weekly_points is None:
            raise ValueError("weekly_points must be dict")
        if len(weekly_points) <= 0:
            raise ValueError("weekly_points must be positive dict")
        
        if task_run is None:
            raise ValueError("task must be Task")

        for weekday in weekly_points:
            time_points = weekly_points[weekday]
            for time_point in time_points:
                if weekday.lower() == 'monday':
                    self._scehduler.every().monday.at(time_point).do(task_run)
                elif weekday.lower() == 'tuesday':
                    self._scehduler.every().tuesday.at(time_point).do(task_run)
                elif weekday.lower() == 'wednesday':
                    self._scehduler.every().wednesday.at(time_point).do(task_run)
                elif weekday.lower() == 'thursday':
                    self._scehduler.every().thursday.at(time_point).do(task_run)
                elif weekday.lower() == 'friday':
                    self._scehduler.every().friday.at(time_point).do(task_run)
                elif weekday.lower() == 'saturday':
                    self._scehduler.every().saturday.at(time_point).do(task_run)
                elif weekday.lower() == 'sunday':
                    self._scehduler.every().sunday.at(time_point).do(task_run)
                else:
                    raise ValueError("weekday must be monday, tuesday, wednesday, thursday, friday, saturday or sunday")
                
    def run_pending(self):
        self._scehduler.run_pending()