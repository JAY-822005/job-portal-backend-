from rest_framework import serializers
from .models import JobApplication


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ["candidate", "applied_at"]