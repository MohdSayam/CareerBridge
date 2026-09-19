from celery import Celery
from celery.schedules import crontab

import os
from dotenv import load_dotenv

load_dotenv()

# Auto-fix Upstash URLs to use TLS (rediss://)
# We must mutate os.environ because Celery automatically reads CELERY_BROKER_URL natively
if "CELERY_BROKER_URL" in os.environ and os.environ["CELERY_BROKER_URL"].startswith("redis://") and "upstash" in os.environ["CELERY_BROKER_URL"]:
    os.environ["CELERY_BROKER_URL"] = os.environ["CELERY_BROKER_URL"].replace("redis://", "rediss://", 1)

if "CELERY_RESULT_BACKEND" in os.environ and os.environ["CELERY_RESULT_BACKEND"].startswith("redis://") and "upstash" in os.environ["CELERY_RESULT_BACKEND"]:
    os.environ["CELERY_RESULT_BACKEND"] = os.environ["CELERY_RESULT_BACKEND"].replace("redis://", "rediss://", 1)

broker_url = os.environ.get("CELERY_BROKER_URL", "")
backend_url = os.environ.get("CELERY_RESULT_BACKEND", "")

celery = Celery(
    "placement_portal",
    broker=broker_url if broker_url else None,
    backend=backend_url if backend_url else None
)

import ssl

celery_conf = {
    "timezone": "Asia/Kolkata",
    "enable_utc": False,

    # Serialization
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],

    # Reliability
    "task_acks_late": True,
    "task_reject_on_worker_lost": True,
}

if broker_url and broker_url.startswith("rediss://"):
    celery_conf["broker_use_ssl"] = {"ssl_cert_reqs": ssl.CERT_NONE}

if backend_url and backend_url.startswith("rediss://"):
    celery_conf["redis_backend_use_ssl"] = {"ssl_cert_reqs": ssl.CERT_NONE}

celery.conf.update(
    **celery_conf,
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

        # ── Keep-alive ────────────────────────────────────────────────────────
        # Pings the Render app every 13 minutes so the free tier never sleeps
        "keep-alive-every-13-mins": {
            "task": "app.tasks.keep_alive_ping",
            "schedule": crontab(minute="*/13")
        },

    }
)

import app.tasks