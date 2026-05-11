from django.db import models
from django.utils import timezone
from applications.models import JobApplication
from accounts.models import User


class Interview(models.Model):
    """
    Model to track interviews scheduled for job applications.
    """
    INTERVIEW_TYPE_CHOICES = (
        ("phone", "Phone Interview"),
        ("video", "Video Interview"),
        ("in_person", "In-Person Interview"),
        ("technical", "Technical Interview"),
        ("hr", "HR Round"),
        ("panel", "Panel Interview"),
    )

    INTERVIEW_STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("rescheduled", "Rescheduled"),
    )

    application = models.OneToOneField(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='interview',
        help_text="Associated job application"
    )
    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPE_CHOICES,
        default="phone",
        help_text="Type of interview"
    )
    status = models.CharField(
        max_length=20,
        choices=INTERVIEW_STATUS_CHOICES,
        default="scheduled",
        help_text="Current interview status"
    )
    scheduled_at = models.DateTimeField(
        help_text="Interview scheduled date and time"
    )
    duration_minutes = models.PositiveIntegerField(
        default=30,
        help_text="Interview duration in minutes"
    )
    interviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interviews_conducted',
        help_text="Interviewer/Recruiter"
    )
    meeting_link = models.URLField(
        blank=True,
        null=True,
        help_text="Video conference link (for remote interviews)"
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Interview location (for in-person interviews)"
    )
    notes = models.TextField(
        blank=True,
        help_text="Interview notes and observations"
    )
    feedback = models.TextField(
        blank=True,
        help_text="Structured interview feedback"
    )
    rating = models.PositiveIntegerField(
        choices=((i, str(i)) for i in range(1, 6)),
        blank=True,
        null=True,
        help_text="Interview rating (1-5)"
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When the interview was completed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Interview"
        verbose_name_plural = "Interviews"
        ordering = ['-scheduled_at']
        indexes = [
            models.Index(fields=['status', 'scheduled_at']),
            models.Index(fields=['interviewer']),
        ]

    def __str__(self):
        return f"Interview for {self.application} - {self.get_interview_type_display()}"

    def is_scheduled_soon(self, hours=24):
        """Check if interview is scheduled within the next specified hours."""
        if self.status in ['completed', 'cancelled']:
            return False
        time_until_interview = (self.scheduled_at - timezone.now()).total_seconds() / 3600
        return 0 <= time_until_interview <= hours

    def is_overdue(self):
        """Check if scheduled interview time has passed but not marked completed."""
        if self.status == 'completed':
            return False
        return timezone.now() > self.scheduled_at

    def mark_completed(self):
        """Mark interview as completed."""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()


class InterviewScheduleTemplate(models.Model):
    """
    Model to create interview schedule templates for recruiters.
    """
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='interview_templates',
        help_text="Recruiter who created the template"
    )
    name = models.CharField(
        max_length=255,
        help_text="Template name (e.g., 'Junior Developer Interview')"
    )
    description = models.TextField(
        blank=True,
        help_text="Template description and guidelines"
    )
    interview_rounds = models.PositiveIntegerField(
        default=1,
        help_text="Number of interview rounds in this template"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Interview Schedule Template"
        verbose_name_plural = "Interview Schedule Templates"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.recruiter.get_full_name()}"


class InterviewFeedback(models.Model):
    """
    Model to store structured interview feedback.
    """
    FEEDBACK_SCORE_CHOICES = (
        (1, "Poor - Does not meet requirements"),
        (2, "Below Average - Needs improvement"),
        (3, "Average - Meets requirements"),
        (4, "Good - Exceeds requirements"),
        (5, "Excellent - Exceptional"),
    )

    interview = models.OneToOneField(
        Interview,
        on_delete=models.CASCADE,
        related_name='structured_feedback',
        help_text="Associated interview"
    )
    technical_skills_score = models.IntegerField(
        choices=FEEDBACK_SCORE_CHOICES,
        blank=True,
        null=True,
        help_text="Technical skills assessment"
    )
    communication_score = models.IntegerField(
        choices=FEEDBACK_SCORE_CHOICES,
        blank=True,
        null=True,
        help_text="Communication skills assessment"
    )
    problem_solving_score = models.IntegerField(
        choices=FEEDBACK_SCORE_CHOICES,
        blank=True,
        null=True,
        help_text="Problem solving ability assessment"
    )
    cultural_fit_score = models.IntegerField(
        choices=FEEDBACK_SCORE_CHOICES,
        blank=True,
        null=True,
        help_text="Cultural fit assessment"
    )
    strengths = models.TextField(
        blank=True,
        help_text="Candidate's strengths"
    )
    areas_for_improvement = models.TextField(
        blank=True,
        help_text="Areas where candidate can improve"
    )
    overall_recommendation = models.CharField(
        max_length=20,
        choices=(
            ("move_forward", "Move Forward to Next Round"),
            ("maybe", "Uncertain - Need More Info"),
            ("no_pass", "Do Not Move Forward"),
        ),
        help_text="Interviewer's overall recommendation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Interview Feedback"
        verbose_name_plural = "Interview Feedbacks"

    def __str__(self):
        return f"Feedback for {self.interview}"
