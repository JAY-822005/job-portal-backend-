"""
Example tasks for Celery
Add these to your respective app's tasks.py file
"""

# accounts/tasks.py
from celery import shared_task
from accounts.models import User
from django.utils import timezone
from datetime import timedelta

@shared_task
def cleanup_expired_tokens():
    """Remove expired verification tokens"""
    cutoff_time = timezone.now() - timedelta(days=1)
    User.objects.filter(
        token_created_at__lt=cutoff_time,
        is_verified=False
    ).update(verification_token=None, token_created_at=None)
    return "Cleaned up expired tokens"


# jobs/tasks.py
from celery import shared_task
from jobs.models import Job
from applications.models import JobApplication
from django.utils import timezone
from django.core.mail import send_mail

@shared_task
def close_expired_jobs():
    """Close job listings that have passed their deadline"""
    expired_jobs = Job.objects.filter(
        deadline__lt=timezone.now(),
        is_active=True
    )
    expired_jobs.update(is_active=False)
    return f"Closed {expired_jobs.count()} expired jobs"

@shared_task
def send_job_recommendations(candidate_id):
    """Send personalized job recommendations to candidate"""
    from accounts.models import CandidateProfile
    try:
        candidate = CandidateProfile.objects.get(user_id=candidate_id)
        # Logic to find matching jobs
        # Send email with recommendations
        return f"Sent recommendations to {candidate.user.email}"
    except CandidateProfile.DoesNotExist:
        return f"Candidate {candidate_id} not found"


# applications/tasks.py
from celery import shared_task
from applications.models import JobApplication

@shared_task
def send_application_status_update(application_id):
    """Send status update email to candidate"""
    try:
        app = JobApplication.objects.get(id=application_id)
        # Send email about application status
        return f"Sent status update for application {application_id}"
    except JobApplication.DoesNotExist:
        return f"Application {application_id} not found"


# interviews/tasks.py
from celery import shared_task
from interviews.models import Interview
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_interview_reminders():
    """Send reminders for interviews happening soon"""
    tomorrow = timezone.now() + timedelta(days=1)
    interviews = Interview.objects.filter(
        scheduled_at__date=tomorrow.date(),
        status='scheduled'
    )
    
    for interview in interviews:
        # Send reminder email to candidate and recruiter
        pass
    
    return f"Sent {interviews.count()} interview reminders"
