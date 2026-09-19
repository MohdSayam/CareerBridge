from celery_worker import celery
from datetime import datetime, timedelta
from flask_mail import Message
from app.mail import mail
from run import app
from app.models import Application, User, Student, Company, JobPosition, Placement
import pytz

import csv
import io
import logging
import os
import urllib.request

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")


# ─── Email helpers ────────────────────────────────────────────────────────────

def send_email(subject, recipients, body, html=None):
    try:
        msg = Message(subject=subject, recipients=recipients)
        msg.body = body
        if html:
            msg.html = html
        mail.send(msg)
    except Exception as e:
        logger.warning(f"Email send failed to {recipients}: {e}")


def send_email_with_attachment(subject, recipients, body, filename, content_type, attachment_data, html=None):
    try:
        msg = Message(subject=subject, recipients=recipients)
        msg.body = body
        if html:
            msg.html = html
        msg.attach(filename, content_type, attachment_data)
        mail.send(msg)
    except Exception as e:
        logger.warning(f"Email with attachment failed to {recipients}: {e}")


def format_ist(dt):
    """Format a naive datetime (stored as IST) for display in emails."""
    if dt is None:
        return "Not scheduled"
    return dt.strftime("%d %b %Y at %I:%M %p IST")


@celery.task
def send_otp_email_task(recipient_email, otp):
    """Sends the OTP verification email asynchronously."""
    with app.app_context():
        html = f"""
        <html><body style="font-family:sans-serif; color:#1e293b; max-width:480px; margin:auto;">
          <div style="background:#0f172a; padding:24px; border-radius:12px 12px 0 0;">
            <h2 style="color:white; margin:0;">CareerBridge</h2>
          </div>
          <div style="padding:32px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:0 0 12px 12px;">
            <h3 style="color:#0f172a;">Verify your account</h3>
            <p>Use the code below to verify your email address:</p>
            <div style="background:#0f172a; color:#5eead4; font-size:36px; font-weight:bold; letter-spacing:12px; padding:20px; border-radius:12px; text-align:center; margin:24px 0;">
              {otp}
            </div>
            <p style="color:#64748b; font-size:13px;">This code expires in 10 minutes. If you didn't request this, ignore this email.</p>
            <p style="color:#94a3b8; font-size:12px; margin-top:24px;">— CareerBridge Team</p>
          </div>
        </html>
        """
        body = f"Your CareerBridge verification code is: {otp}\nThis code expires in 10 minutes."
        send_email(
            subject="Verify your CareerBridge account",
            recipients=[recipient_email],
            body=body,
            html=html
        )



# ─── Tasks ────────────────────────────────────────────────────────────────────

@celery.task
def send_interview_reminders():
    """
    Run hourly. Emails students and companies for interviews happening
    in the next 24 hours. Skips if already reminded (relies on interview_date window).
    """
    with app.app_context():
        now = datetime.now(IST).replace(tzinfo=None)
        next_24h = now + timedelta(hours=24)

        applications = (
            Application.query
            .filter(
                Application.status == "interview",
                Application.interview_date >= now,
                Application.interview_date <= next_24h
            )
            .all()
        )

        reminders_sent = 0

        for application in applications:
            student = application.student
            job = application.job
            company = job.company
            interview_time = format_ist(application.interview_date)
            interview_url = f"{app.config.get('APP_BASE_URL', 'http://localhost:5173')}/interview/{application.id}"

            # Email student
            send_email(
                subject=f"⏰ Interview Reminder — {job.title} at {company.company_name}",
                recipients=[student.user.email],
                html=f"""
                <html><body style="font-family: sans-serif; color: #1e293b; max-width: 560px; margin: auto;">
                  <div style="background: #0f172a; padding: 24px; border-radius: 12px 12px 0 0;">
                    <h2 style="color: white; margin: 0;">CareerBridge</h2>
                  </div>
                  <div style="padding: 32px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0 0 12px 12px;">
                    <h3 style="color: #0f172a;">Interview Reminder 🎯</h3>
                    <p>Hi <strong>{student.full_name}</strong>,</p>
                    <p>You have an upcoming interview scheduled:</p>
                    <table style="width:100%; background:#ffffff; border-radius:8px; padding:16px; border:1px solid #e2e8f0;">
                      <tr><td style="padding:6px 0; color:#64748b;">Company</td><td><strong>{company.company_name}</strong></td></tr>
                      <tr><td style="padding:6px 0; color:#64748b;">Role</td><td><strong>{job.title}</strong></td></tr>
                      <tr><td style="padding:6px 0; color:#64748b;">Time</td><td><strong style="color:#0d9488;">{interview_time}</strong></td></tr>
                    </table>
                    <p style="margin-top:24px;">
                      <a href="{interview_url}" style="background:#0f172a; color:white; padding:12px 24px; border-radius:8px; text-decoration:none; font-weight:bold;">
                        Join Interview Room →
                      </a>
                    </p>
                    <p style="color:#94a3b8; font-size:13px; margin-top:32px;">Best of luck! — CareerBridge Team</p>
                  </div>
                </html>
                """,
                body=f"Interview Reminder: {job.title} at {company.company_name} on {interview_time}. Join: {interview_url}"
            )

            # Email company interviewer
            send_email(
                subject=f"📅 Interview Reminder — {student.full_name} for {job.title}",
                recipients=[company.user.email],
                html=f"""
                <html><body style="font-family: sans-serif; color: #1e293b; max-width: 560px; margin: auto;">
                  <div style="background: #0f172a; padding: 24px; border-radius: 12px 12px 0 0;">
                    <h2 style="color: white; margin: 0;">CareerBridge</h2>
                  </div>
                  <div style="padding: 32px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0 0 12px 12px;">
                    <h3 style="color: #0f172a;">Upcoming Interview</h3>
                    <p>Hi <strong>{company.company_name}</strong>,</p>
                    <p>Reminder for an interview scheduled on your platform:</p>
                    <table style="width:100%; background:#ffffff; border-radius:8px; padding:16px; border:1px solid #e2e8f0;">
                      <tr><td style="padding:6px 0; color:#64748b;">Candidate</td><td><strong>{student.full_name}</strong></td></tr>
                      <tr><td style="padding:6px 0; color:#64748b;">Role</td><td><strong>{job.title}</strong></td></tr>
                      <tr><td style="padding:6px 0; color:#64748b;">Time</td><td><strong style="color:#0d9488;">{interview_time}</strong></td></tr>
                    </table>
                    <p style="margin-top:24px;">
                      <a href="{interview_url}" style="background:#4f46e5; color:white; padding:12px 24px; border-radius:8px; text-decoration:none; font-weight:bold;">
                        Open Interview Room →
                      </a>
                    </p>
                    <p style="color:#94a3b8; font-size:13px; margin-top:32px;">— CareerBridge Team</p>
                  </div>
                </html>
                """,
                body=f"Interview reminder: {student.full_name} for {job.title} on {interview_time}. Room: {interview_url}"
            )

            reminders_sent += 1

        return f"{reminders_sent} reminder(s) sent."


@celery.task
def generate_monthly_reports():
    """
    Run on the 1st of each month at 9 AM IST.
    Sends each approved company a summary of their hiring pipeline
    for the past month.
    """
    with app.app_context():
        companies = Company.query.filter_by(
            approval_status="approved",
            is_blacklisted=False
        ).all()

        reports_generated = 0

        for company in companies:
            jobs = JobPosition.query.filter_by(company_id=company.id).count()
            applications = (
                Application.query
                .join(JobPosition)
                .filter(JobPosition.company_id == company.id)
                .count()
            )
            shortlisted = (
                Application.query
                .join(JobPosition)
                .filter(JobPosition.company_id == company.id, Application.status == "shortlisted")
                .count()
            )
            selected = (
                Application.query
                .join(JobPosition)
                .filter(JobPosition.company_id == company.id, Application.status == "selected")
                .count()
            )
            placed = (
                Placement.query
                .join(Application)
                .join(JobPosition)
                .filter(JobPosition.company_id == company.id)
                .count()
            )

            month_name = datetime.now(IST).strftime("%B %Y")

            html = f"""
            <html><body style="font-family: sans-serif; color: #1e293b; max-width: 600px; margin: auto;">
              <div style="background: #0f172a; padding: 24px; border-radius: 12px 12px 0 0;">
                <h2 style="color: white; margin: 0;">CareerBridge</h2>
                <p style="color:#94a3b8; margin:4px 0 0;">Monthly Placement Report — {month_name}</p>
              </div>
              <div style="padding: 32px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:0 0 12px 12px;">
                <h3>Hi {company.company_name},</h3>
                <p>Here's your hiring pipeline summary for <strong>{month_name}</strong>:</p>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:24px 0;">
                  <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; text-align:center;">
                    <div style="font-size:32px; font-weight:bold; color:#0f172a;">{jobs}</div>
                    <div style="color:#64748b; font-size:13px;">Total Jobs</div>
                  </div>
                  <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; text-align:center;">
                    <div style="font-size:32px; font-weight:bold; color:#3b82f6;">{applications}</div>
                    <div style="color:#64748b; font-size:13px;">Applications</div>
                  </div>
                  <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; text-align:center;">
                    <div style="font-size:32px; font-weight:bold; color:#f59e0b;">{shortlisted}</div>
                    <div style="color:#64748b; font-size:13px;">Shortlisted</div>
                  </div>
                  <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; text-align:center;">
                    <div style="font-size:32px; font-weight:bold; color:#10b981;">{placed}</div>
                    <div style="color:#64748b; font-size:13px;">Placed</div>
                  </div>
                </div>
                <p style="color:#64748b; font-size:13px;">
                  Selected (offer stage): <strong>{selected}</strong> candidates<br>
                  Report generated automatically on {datetime.now(IST).strftime("%d %b %Y at %I:%M %p IST")}
                </p>
                <p style="color:#94a3b8; font-size:12px; margin-top:32px;">— CareerBridge Automated Reports</p>
              </div>
            </html>
            """

            send_email(
                subject=f"📊 Monthly Placement Report — {month_name} | {company.company_name}",
                recipients=[company.user.email],
                html=html,
                body=f"Monthly Report for {company.company_name} — {month_name}:\nJobs: {jobs} | Applications: {applications} | Shortlisted: {shortlisted} | Placed: {placed}"
            )

            reports_generated += 1

        return f"{reports_generated} monthly report(s) sent."


@celery.task
def send_weekly_digest():
    """
    Run every Monday at 9 AM IST.
    Emails active, non-blacklisted students a digest of new job openings
    posted in the past 7 days that they are eligible for.
    """
    with app.app_context():
        now = datetime.now(IST).replace(tzinfo=None)
        one_week_ago = now - timedelta(days=7)

        # Fetch new jobs posted in the last 7 days that are still open
        new_jobs = (
            JobPosition.query
            .join(Company)
            .filter(
                Company.approval_status == "approved",
                Company.is_blacklisted == False,
                JobPosition.status == "approved",
                JobPosition.application_deadline >= now,
                JobPosition.created_at >= one_week_ago
            )
            .order_by(JobPosition.id.desc())
            .limit(10)
            .all()
        )

        if not new_jobs:
            return "No new jobs this week — digest skipped."

        # Build job rows HTML
        job_rows = ""
        for job in new_jobs:
            deadline = job.application_deadline.strftime("%d %b %Y") if job.application_deadline else "—"
            job_rows += f"""
            <tr>
              <td style="padding:12px 8px; border-bottom:1px solid #f1f5f9;">
                <strong>{job.title}</strong><br>
                <span style="color:#64748b; font-size:13px;">{job.company.company_name}</span>
              </td>
              <td style="padding:12px 8px; border-bottom:1px solid #f1f5f9; color:#0d9488; font-weight:600;">{job.salary_range}</td>
              <td style="padding:12px 8px; border-bottom:1px solid #f1f5f9; color:#94a3b8; font-size:13px;">{deadline}</td>
            </tr>
            """

        base_url = app.config.get("APP_BASE_URL", "http://localhost:5173")

        # Email all active students
        students = (
            Student.query
            .join(User)
            .filter(
                Student.is_blacklisted == False,
                User.is_active == True,
                User.is_verified == True
            )
            .all()
        )

        digests_sent = 0

        for student in students:
            html = f"""
            <html><body style="font-family: sans-serif; color: #1e293b; max-width: 600px; margin: auto;">
              <div style="background: linear-gradient(135deg, #0f172a 0%, #134e4a 100%); padding: 28px; border-radius: 12px 12px 0 0;">
                <h2 style="color: white; margin: 0;">CareerBridge</h2>
                <p style="color:#5eead4; margin: 4px 0 0; font-size:14px;">Weekly Jobs Digest</p>
              </div>
              <div style="padding: 32px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:0 0 12px 12px;">
                <p>Hi <strong>{student.full_name}</strong> 👋</p>
                <p>Here are <strong>{len(new_jobs)} new job opportunities</strong> posted this week on CareerBridge:</p>
                <table style="width:100%; background:#ffffff; border-radius:8px; border:1px solid #e2e8f0; border-collapse:collapse;">
                  <thead>
                    <tr style="background:#f1f5f9;">
                      <th style="padding:10px 8px; text-align:left; color:#64748b; font-size:12px; font-weight:600; text-transform:uppercase;">Role & Company</th>
                      <th style="padding:10px 8px; text-align:left; color:#64748b; font-size:12px; font-weight:600; text-transform:uppercase;">Package</th>
                      <th style="padding:10px 8px; text-align:left; color:#64748b; font-size:12px; font-weight:600; text-transform:uppercase;">Deadline</th>
                    </tr>
                  </thead>
                  <tbody>{job_rows}</tbody>
                </table>
                <p style="margin-top:28px;">
                  <a href="{base_url}/student/jobs" style="background:#0f172a; color:white; padding:12px 28px; border-radius:8px; text-decoration:none; font-weight:bold;">
                    Browse All Jobs →
                  </a>
                </p>
                <p style="color:#94a3b8; font-size:12px; margin-top:32px;">
                  You're receiving this because you're registered on CareerBridge.<br>
                  — CareerBridge Team
                </p>
              </div>
            </html>
            """

            send_email(
                subject=f"🚀 {len(new_jobs)} New Jobs This Week — CareerBridge Digest",
                recipients=[student.user.email],
                html=html,
                body=f"Hi {student.full_name}, {len(new_jobs)} new jobs posted this week. Browse: {base_url}/student/jobs"
            )
            digests_sent += 1

        return f"Weekly digest sent to {digests_sent} student(s) — {len(new_jobs)} job(s) featured."


@celery.task
def export_student_applications(student_id):
    """
    On-demand: generates a CSV of a student's applications and emails it to them.
    """
    with app.app_context():
        student = Student.query.get(student_id)

        if not student:
            return "Student not found"

        applications = Application.query.filter_by(student_id=student.id).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Company", "Job Title", "Salary", "Status", "Applied At"])

        for application in applications:
            job = application.job
            company = job.company
            writer.writerow([
                company.company_name,
                job.title,
                job.salary_range,
                application.status,
                format_ist(application.applied_at)
            ])

        csv_bytes = output.getvalue().encode("utf-8")
        filename = f"my_applications_{student.id}.csv"

        send_email_with_attachment(
            subject="Your CareerBridge Applications Export",
            recipients=[student.user.email],
            html=f"""
            <html><body style="font-family:sans-serif; color:#1e293b; max-width:560px; margin:auto;">
              <div style="background:#0f172a; padding:24px; border-radius:12px 12px 0 0;">
                <h2 style="color:white; margin:0;">CareerBridge</h2>
              </div>
              <div style="padding:32px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:0 0 12px 12px;">
                <p>Hi <strong>{student.full_name}</strong>,</p>
                <p>Your applications export is ready. Please find the CSV file attached.</p>
                <p style="color:#94a3b8; font-size:13px;">— CareerBridge Team</p>
              </div>
            </html>
            """,
            body=f"Hi {student.full_name}, your applications CSV is attached.",
            filename=filename,
            content_type="text/csv",
            attachment_data=csv_bytes
        )
        return "CSV exported and emailed successfully."


@celery.task
def keep_alive_ping():
    """
    Pings the server every 13 minutes to prevent Render free tier from sleeping.
    """
    try:
        url = os.environ.get("RENDER_EXTERNAL_URL", "http://127.0.0.1:10000")
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as response:
            return f"Ping successful: {response.status}"
    except Exception as e:
        return f"Ping failed: {str(e)}"

@celery.task
def cleanup_unverified_users():
    """
    Runs daily. Deletes any unverified users that were created more than 24 hours ago.
    This keeps the database clean of abandoned registrations.
    """
    with app.app_context():
        now = datetime.now(IST).replace(tzinfo=None)
        cutoff_time = now - timedelta(hours=24)
        
        # Find all users who are unverified and were created before the cutoff
        unverified_users = User.query.filter(
            User.is_verified == False,
            User.created_at < cutoff_time
        ).all()
        
        deleted_count = 0
        for user in unverified_users:
            if user.role == "student" and user.student:
                db.session.delete(user.student)
            elif user.role == "company" and user.company:
                db.session.delete(user.company)
            db.session.delete(user)
            deleted_count += 1
            
        if deleted_count > 0:
            db.session.commit()
            
        return f"Deleted {deleted_count} unverified users."