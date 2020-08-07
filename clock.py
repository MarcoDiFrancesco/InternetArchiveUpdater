from apscheduler.schedulers.blocking import BlockingScheduler
from main import main

sched = BlockingScheduler()


@sched.scheduled_job("interval", minutes=11)
def timed_job():
    """
    Repeat this every 11 minutes
    """
    main()
    print("This job is run every 1 minute.")


sched.start()
