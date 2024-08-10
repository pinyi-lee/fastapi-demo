from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.manager.logger import LoggerManager
from app.manager.config import ConfigManager

class SchedulerManager:
    _scheduler_instance = None

    @classmethod
    def init_scheduler(cls) -> None:
        try:
            if cls._scheduler_instance is None:
                cls._scheduler_instance = BackgroundScheduler(option={'logger': LoggerManager.get_scheduler_logging_instance()})
                cls._scheduler_instance.start()
                cls._scheduler_instance.add_job(my_scheduled_job, IntervalTrigger(seconds=ConfigManager.get_config().scheduler_interval_seconds))
        except Exception as e:
                raise RuntimeError(f"Init Scheduler Fail, Error: {e}")

    @classmethod
    def close_scheduler(cls) -> None:
        if cls._scheduler_instance is not None:
            cls._scheduler_instance.shutdown()

def my_scheduled_job():
    LoggerManager.get_scheduler_logging_instance().info("This job is run.")