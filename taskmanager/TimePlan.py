from enum import Enum


class TimePlanType(Enum):
    """Enum for schedule types."""

    INTERVAL = "Every Interval"
    DAILY_POINTS = "Multiple Times at Hours of the Day"
    WEEKLY_POINTS = "Multiple Times at Days of the Week"
    
class DayType(Enum):

    SUNDAY = "sunday"
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"

class TimePlan:

    @classmethod
    def create_interval_schedule(cls, day=0, hr=0, min=0, sec=0):
        interval = _TimeTransformer(day, hr, min, sec)
        if interval <= 0:
            raise ValueError("Interval must be positive")
        return cls(TimePlanType.INTERVAL, interval=interval)
 
    @classmethod
    def create_daily_schedule(cls, *time_points):
        return cls(TimePlanType.DAILY_POINTS, points=list(time_points))
 
    @classmethod
    def create_weekly_schedule(cls, **weekly_points):
        return cls(TimePlanType.WEEKLY_POINTS, points=weekly_points)
    
    def __init__(self, schedule_type, interval=None, points=None):

        if not isinstance(schedule_type, TimePlanType):
            raise ValueError("schedule_type must be TimePlanType")
        
        self._schedule_type = schedule_type

        # Set interval
        self._interval = None
        if interval is not None:
            if schedule_type == TimePlanType.INTERVAL:
                self._set_interval(interval)             

        # Set points
        self._daily_points = []
        self._weekly_points = {}
        if schedule_type == TimePlanType.DAILY_POINTS:
            if points is not None:
                self._verify_daily_points(points)
                self._daily_points = points
                self._weekly_points = {}
        elif schedule_type == TimePlanType.WEEKLY_POINTS:
            if points is not None:
                self._verify_weekly_points(points)
                self._daily_points = []
                self._weekly_points = points
    
    @property
    def time_plan_type(self):
        return self._schedule_type

    @property
    def is_valid(self):
        if self._schedule_type == TimePlanType.INTERVAL:
            return self._interval is not None
        elif self._schedule_type == TimePlanType.DAILY_POINTS:
            return len(self._daily_points) > 0
        elif self._schedule_type == TimePlanType.WEEKLY_POINTS:
            return len(self._weekly_points) > 0
        else:
            return False

    @property
    def plan(self):
        if self._schedule_type == TimePlanType.INTERVAL:
            return self._interval
        elif self._schedule_type == TimePlanType.DAILY_POINTS:
            return self._daily_points
        elif self._schedule_type == TimePlanType.WEEKLY_POINTS:
            return self._weekly_points
        else:
            return None

    def __str__(self):
        if self._schedule_type == TimePlanType.INTERVAL:
            return f"Interval Schedule: Every {self._interval} units"
        elif self._schedule_type == TimePlanType.DAILY_POINTS:
            times = ', '.join(self._daily_points)
            return f"Daily Points Schedule: {times}"
        elif self._schedule_type == TimePlanType.WEEKLY_POINTS:
            days_str = []
            for day, times in self._weekly_points.items():
                day_times = ', '.join(times)
                days_str.append(f"{day.capitalize()}: {day_times}")
            return "Weekly Points Schedule:\n" + '\n'.join(days_str)
        return "Undefined Schedule"
    
    def _set_interval(self, interval):
        if self._schedule_type != TimePlanType.INTERVAL:
            raise ValueError("schedule_type must be TimePlanType.INTERVAL")
        if not isinstance(interval, int):
            raise ValueError("interval must be int")
        if interval <= 0:
            raise ValueError("interval must be positive")
        
        self._interval = interval   

    def _verify_daily_points(self, points):
        if not isinstance(points, list):
            raise ValueError("For DAILY_POINTS, 'points' must be a list")
        for point in points:
            if not isinstance(point, str) or not self._is_valid_time_format(point):
                raise ValueError(f"Invalid time format: {point}")
 
    def _verify_weekly_points(self, points):
        if not isinstance(points, dict):
            raise ValueError("For WEEKLY_POINTS, 'points' must be a dictionary")
        for day, times in points.items():
            if day not in DayType._value2member_map_:
                raise ValueError(f"Invalid day: {day}")
            for time in times:
                if not self._is_valid_time_format(time):
                    raise ValueError(f"Invalid time format for {day}: {time}")
 
    @staticmethod
    def _is_valid_time_format(time_str):
        try:
            hour, minute = map(int, time_str.split(":"))
            return 0 <= hour < 24 and 0 <= minute < 60
        except ValueError:
            return False

def Timeout(day=0, hr=0, min=0, sec=0):
    s_value = _TimeTransformer(day, hr, min, sec)
    if s_value <= 0:
        raise ValueError("Timeout must be positive")
    return s_value

def _TimeTransformer(day=0, hr=0, min=0, sec=0):
    if not isinstance(hr, int):
        raise ValueError("hr must be int")
    if not isinstance(min, int):
        raise ValueError("min must be int")
    if not isinstance(sec, int):
        raise ValueError("sec must be int")
    if hr < 0 or hr > 23:
        raise ValueError("hr must be 0~23")
    if min < 0 or min > 59:
        raise ValueError("min must be 0~59")
    if sec < 0 or sec > 59:
        raise ValueError("sec must be 0~59")
    return day*24*60*60 + hr*60*60 + min*60 + sec
