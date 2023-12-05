from enum import Enum

class TaskState(Enum):
    INIT = 'init'
    RUNNING = 'running'
    DONE = 'done'
    TERMINATING = 'terminating'
    TERMINATED = 'terminated'
    KILLED = 'killed'     
