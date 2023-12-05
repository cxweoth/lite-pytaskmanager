# lite-pytaskmanager

**A Versatile Task Scheduling and Lifecycle Management Library**

lite-pytaskmanager is a robust and versatile Python library designed for efficient task scheduling and lifecycle management across multiple platforms. Worked for both Windows and Linux systems, and without the need for heavy external dependencies or specialized setups.

## Key Features

- **Flexible Scheduling Options**: Supports a variety of scheduling needs, including periodic tasks, daily fixed-time tasks, and weekly tasks set to specific times.

- **Lifecycle Management**: Advanced lifecycle control monitors the execution status of tasks, issuing events when tasks exceed their allotted time and forcibly stopping them if they do not terminate within this period.

- **Automatic Logging**: Features automatic logging capability, allowing users to specify the path for storing logs, crucial for tracking and analyzing system operations.

- **Lite Installation**: No need to install any 3-party library and easy to install.

- **Cross-Platform Compatibility**: Delivers consistent performance and user experience on both Windows and Linux operating systems.

## Installation

```bash
pip install lite-pytaskmanager
```

## Usage
Here's a quick start example of how to use lite-pytaskmanager:

```python
from threading import Event
from taskmanager import Manager, TimePlan, Timeout

def period_func(terminate_event:Event):
    print('period_func')
    return True, None

def daily_point_func(terminate_event:Event):
    print('daily_point_func')
    return True, None

def weekly_point_func(terminate_event:Event):
    print('weekly_point_func')
    return True, None

# Create a new manager instance
manager = Manager(manager_name='taskmanager')
manager.enable_physical_logging(".")

# Add tasks
manager.add_task('period_func', period_func, TimePlan.create_interval_schedule(min=10), Timeout(hr=1))
manager.add_task('daily_point_func', daily_point_func, TimePlan.create_daily_schedule("22:00"), Timeout(hr=1))
manager.add_task('weekly_point_func', weekly_point_func, TimePlan.create_weekly_schedule(saturday=["22:00"]), Timeout(hr=1))

# Start the manager
manager.start()
```

For more detailed usage, please refer to the [documentation (TBD)]().

## Contributing
Contributions to lite-pytaskmanager are welcome! Please refer to the [contributing guidelines (TBD)]() for more information.

