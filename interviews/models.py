from django.db import models
from applications.models import JobApplication


class Interview(models.Model):
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    meeting_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Interview for {self.application}"