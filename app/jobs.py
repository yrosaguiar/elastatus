from apscheduler.scheduler import Scheduler
from apscheduler.events import EVENT_JOB_EXECUTED,EVENT_JOB_ERROR

sched = Scheduler()
sched.start()

# Example job
# @sched.interval_schedule(seconds=2)
# def job_function():
#     print "Hello World"
