from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model with role-based access control.
    """
    ROLE_CHOICES = (
        ("candidate", "Candidate"),
        ("recruiter", "Recruiter"),
        ("admin", "Admin"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="candidate",
        help_text="User role in the system"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="User's phone number"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        help_text="User's profile picture"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        help_text="User's bio/about section"
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Email verification status"
    )
    verification_token = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    token_created_at = models.DateTimeField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def is_token_expired(self, hours=24):
        """Check if verification token has expired."""
        if not self.token_created_at:
            return True
        return (timezone.now() - self.token_created_at).total_seconds() > (hours * 3600)


class CandidateProfile(models.Model):
    """
    Extended profile model for job candidates.
    """
    EXPERIENCE_LEVEL_CHOICES = (
        ("entry", "Entry Level (0-2 years)"),
        ("junior", "Junior (2-5 years)"),
        ("mid", "Mid Level (5-10 years)"),
        ("senior", "Senior (10+ years)"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='candidate_profile',
        help_text="Associated user account"
    )
    headline = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Professional headline (e.g., Senior Python Developer)"
    )
    skills = models.TextField(
        blank=True,
        help_text="Comma-separated list of skills"
    )
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default="entry",
        help_text="Years of professional experience"
    )
    years_of_experience = models.PositiveIntegerField(
        default=0,
        help_text="Total years of work experience"
    )
    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True,
        help_text="PDF or Word document resume"
    )
    portfolio_url = models.URLField(
        blank=True,
        null=True,
        help_text="Link to portfolio or personal website"
    )
    github_url = models.URLField(
        blank=True,
        null=True,
        help_text="GitHub profile URL"
    )
    linkedin_url = models.URLField(
        blank=True,
        null=True,
        help_text="LinkedIn profile URL"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Availability for new opportunities"
    )
    preferred_job_titles = models.TextField(
        blank=True,
        help_text="Comma-separated list of preferred job titles"
    )
    preferred_locations = models.TextField(
        blank=True,
        help_text="Comma-separated list of preferred job locations"
    )
    expected_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Expected annual salary"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Candidate Profile"
        verbose_name_plural = "Candidate Profiles"
        ordering = ['-updated_at']

    def __str__(self):
        return f"Candidate: {self.user.get_full_name()}"

    def get_skills_list(self):
        """Return skills as a list."""
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]


class RecruiterProfile(models.Model):
    """
    Extended profile model for recruiters/HR professionals.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='recruiter_profile',
        help_text="Associated user account"
    )
    company_name = models.CharField(
        max_length=255,
        help_text="Name of the company"
    )
    company_logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True,
        help_text="Company logo image"
    )
    company_website = models.URLField(
        blank=True,
        null=True,
        help_text="Company website URL"
    )
    company_description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the company"
    )
    company_size = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Company size (e.g., 10-50, 50-200)"
    )
    industry = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Industry type (e.g., Technology, Finance)"
    )
    office_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Company office location"
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Company verification status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recruiter Profile"
        verbose_name_plural = "Recruiter Profiles"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['is_verified']),
        ]

    def __str__(self):
        return f"Recruiter: {self.user.get_full_name()} ({self.company_name})"
