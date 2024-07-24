from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.INFO)

class SchedulerManager:
    _scheduler_instance = None

    @classmethod
    def init_scheduler(cls) -> None:
        try:
            if cls._scheduler_instance is None:
                cls._scheduler_instance = BackgroundScheduler()
                cls._scheduler_instance.start()
                cls._scheduler_instance.add_job(my_scheduled_job, IntervalTrigger(seconds=30))
        except Exception as e:
                raise RuntimeError(f"Init Scheduler Fail, Error: {e}")

    @classmethod
    def close_scheduler(cls) -> None:
        if cls._scheduler_instance is not None:
            cls._scheduler_instance.shutdown()

def my_scheduled_job():
    print("This job is run.")