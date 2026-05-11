from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import RecruiterProfile
from django.utils import timezone


class Job(models.Model):
    """
    Job posting model created by recruiters.
    """
    JOB_TYPE_CHOICES = (
        ("full-time", "Full Time"),
        ("part-time", "Part Time"),
        ("contract", "Contract"),
        ("temporary", "Temporary"),
        ("internship", "Internship"),
    )

    EXPERIENCE_LEVEL_CHOICES = (
        ("entry", "Entry Level"),
        ("junior", "Junior"),
        ("mid", "Mid Level"),
        ("senior", "Senior"),
        ("executive", "Executive"),
    )

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("closed", "Closed"),
        ("archived", "Archived"),
    )

    recruiter = models.ForeignKey(
        RecruiterProfile,
        on_delete=models.CASCADE,
        related_name='jobs',
        help_text="Recruiter who posted this job"
    )
    title = models.CharField(
        max_length=255,
        help_text="Job title"
    )
    slug = models.SlugField(
        unique=True,
        help_text="URL-friendly job title"
    )
    description = models.TextField(
        help_text="Detailed job description"
    )
    requirements = models.TextField(
        help_text="Required skills and qualifications"
    )
    responsibilities = models.TextField(
        help_text="Job responsibilities and duties"
    )
    location = models.CharField(
        max_length=255,
        help_text="Job location (city, country)"
    )
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default="full-time",
        help_text="Type of job position"
    )
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default="mid",
        help_text="Required experience level"
    )
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Minimum salary"
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Maximum salary"
    )
    salary_currency = models.CharField(
        max_length=10,
        default="USD",
        help_text="Salary currency (e.g., USD, EUR, INR)"
    )
    is_remote = models.BooleanField(
        default=False,
        help_text="Is this a remote job?"
    )
    benefits = models.TextField(
        blank=True,
        help_text="Job benefits and perks"
    )
    skills_required = models.TextField(
        help_text="Comma-separated list of required skills"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="published",
        help_text="Job posting status"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is the job active and accepting applications?"
    )
    views_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times job was viewed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Application deadline"
    )

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recruiter', 'status']),
            models.Index(fields=['location', 'job_type']),
            models.Index(fields=['experience_level']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.title} - {self.recruiter.company_name}"

    def get_skills_list(self):
        """Return required skills as a list."""
        return [skill.strip() for skill in self.skills_required.split(',') if skill.strip()]

    def is_deadline_passed(self):
        """Check if application deadline has passed."""
        if self.deadline:
            return timezone.now() > self.deadline
        return False

    def increment_views(self):
        """Increment views count."""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class JobCategory(models.Model):
    """
    Job categories for organization and filtering.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Category name (e.g., Backend, Frontend)"
    )
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome icon class"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Job Category"
        verbose_name_plural = "Job Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Skill(models.Model):
    """
    Skill tags for jobs and candidates.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Skill name (e.g., Python, Django)"
    )
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['name']

    def __str__(self):
        return self.name
