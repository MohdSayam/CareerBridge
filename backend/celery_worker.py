from celery import Celery
from celery.schedules import crontab

import os
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "placement_portal",
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND")
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,

    # Serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],

    # Reliability
    task_acks_late=True,
    task_reject_on_worker_lost=True,

    beat_schedule={

        # ── Hourly: interview reminders ──────────────────────────────────────
        # Checks all interviews in the next 24 hours and emails student + company
        "interview-reminders-every-hour": {
            "task": "app.tasks.send_interview_reminders",
            "schedule": crontab(minute=0, hour="*")
        },

        # ── Monthly: placement report to companies ────────────────────────────
        # Emails each approved company a summary of their hiring pipeline
        # Runs on the 1st of every month at 9:00 AM IST
        "monthly-placement-report": {
            "task": "app.tasks.generate_monthly_reports",
            "schedule": crontab(day_of_month=1, hour=9, minute=0)
        },

        # ── Weekly: new jobs digest to students ───────────────────────────────
        # Every Monday at 9:00 AM IST, emails active students a list of
        # new job openings posted in the past 7 days
        "weekly-jobs-digest": {
            "task": "app.tasks.send_weekly_digest",
            "schedule": crontab(day_of_week=1, hour=9, minute=0)  # Monday 9 AM
        },

    }
)

import app.tasks