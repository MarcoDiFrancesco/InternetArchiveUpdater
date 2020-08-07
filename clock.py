from apscheduler.schedulers.blocking import BlockingScheduler
from main import main

sched = BlockingScheduler()


@sched.scheduled_job("interval", minutes=12)
def timed_job():
    """
    Repeat this every n minutes
    """
    main()


sched.start()
