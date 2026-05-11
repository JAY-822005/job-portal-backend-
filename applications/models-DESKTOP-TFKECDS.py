from django.db import models
from django.utils import timezone
from accounts.models import CandidateProfile, User
from jobs.models import Job


class JobApplication(models.Model):
    """
    Model to track job applications from candidates.
    """
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("under_review", "Under Review"),
        ("shortlisted", "Shortlisted"),
        ("interviewed", "Interviewed"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
        ("withdrawn", "Withdrawn"),
    )

    RATING_CHOICES = (
        (1, "Poor"),
        (2, "Fair"),
        (3, "Good"),
        (4, "Very Good"),
        (5, "Excellent"),
    )

    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name='applications',
        help_text="Candidate applying for the job"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
        help_text="Job being applied for"
    )
    cover_letter = models.TextField(
        blank=True,
        help_text="Candidate's cover letter"
    )
    resume_file = models.FileField(
        upload_to="application_resumes/",
        blank=True,
        null=True,
        help_text="Resume submitted with application"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="applied",
        help_text="Current application status"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        blank=True,
        null=True,
        help_text="Recruiter's rating of the application"
    )
    recruiter_notes = models.TextField(
        blank=True,
        help_text="Notes from the recruiter"
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rejected_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When the application was rejected"
    )
    hired_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When the candidate was hired"
    )

    class Meta:
        unique_together = ("candidate", "job")
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['status', 'applied_at']),
            models.Index(fields=['job', 'status']),
            models.Index(fields=['candidate']),
        ]

    def __str__(self):
        return f"{self.candidate.user.get_full_name()} -> {self.job.title}"

    def mark_rejected(self):
        """Mark application as rejected."""
        self.status = 'rejected'
        self.rejected_at = timezone.now()
        self.save()

    def mark_hired(self):
        """Mark application as hired."""
        self.status = 'hired'
        self.hired_at = timezone.now()
        self.save()


class ApplicationRejection(models.Model):
    """
    Model to track rejection reasons for applications.
    """
    application = models.OneToOneField(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='rejection',
        help_text="Associated application"
    )
    reason = models.TextField(
        help_text="Reason for rejection"
    )
    rejected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Recruiter who rejected the application"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Application Rejection"
        verbose_name_plural = "Application Rejections"

    def __str__(self):
        return f"Rejection for {self.application}"
