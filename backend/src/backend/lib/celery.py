# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ lib: celery                                                                                      │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from celery import Celery
from celery.schedules import crontab
from backend.extensions import celery as celery_ext


def make_celery(app, celery_instance=None):
    celery = (
        celery_instance
        or celery_ext
        or Celery(
            app.import_name,
            broker=app.config["CELERY_BROKER_URL"],
            backend=app.config["CELERY_RESULT_BACKEND"],
        )
    )

    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone=app.config["CELERY_TIMEZONE"],
        enable_utc=False,
        beat_schedule={
            "daily-reminders": {
                "task": "app.tasks.reminders.send_daily_reminders",
                "schedule": crontab(hour=9, minute=0),
            },
            "monthly-report": {
                "task": "app.tasks.reports.generate_monthly_admin_report",
                "schedule": crontab(day_of_month=1, hour=9, minute=0),
            },
        },
    )

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery_ext.conf.update(celery.conf) if celery_ext is not None else None
    return celery
