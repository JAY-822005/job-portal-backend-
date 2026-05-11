"""
Serializers for the applications app.
"""

from rest_framework import serializers
from applications.models import JobApplication, ApplicationRejection
from accounts.models import CandidateProfile
from jobs.models import Job


class JobApplicationListSerializer(serializers.ModelSerializer):
    """Serializer for listing job applications."""
    candidate_name = serializers.CharField(source='candidate.user.get_full_name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = JobApplication
        fields = ('id', 'candidate_name', 'job_title', 'status', 'rating', 'applied_at', 'updated_at')
        read_only_fields = fields


class JobApplicationDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed job application information."""
    candidate_info = serializers.SerializerMethodField()
    job_info = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = ('id', 'candidate_info', 'job_info', 'cover_letter', 'resume_file',
                  'status', 'rating', 'recruiter_notes', 'applied_at', 'updated_at',
                  'rejected_at', 'hired_at')
        read_only_fields = ('id', 'applied_at', 'updated_at', 'rejected_at', 'hired_at')

    def get_candidate_info(self, obj):
        return {
            'id': obj.candidate.id,
            'name': obj.candidate.user.get_full_name(),
            'email': obj.candidate.user.email,
            'phone': obj.candidate.user.phone,
            'skills': obj.candidate.get_skills_list(),
            'experience_level': obj.candidate.experience_level,
            'years_of_experience': obj.candidate.years_of_experience,
        }

    def get_job_info(self, obj):
        return {
            'id': obj.job.id,
            'title': obj.job.title,
            'company': obj.job.recruiter.company_name,
            'location': obj.job.location,
        }


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating job applications."""
    
    class Meta:
        model = JobApplication
        fields = ('job', 'cover_letter', 'resume_file')

    def create(self, validated_data):
        user = self.context['request'].user
        candidate = CandidateProfile.objects.get(user=user)
        application = JobApplication.objects.create(
            candidate=candidate,
            **validated_data
        )
        return application


class ApplicationRejectionSerializer(serializers.ModelSerializer):
    """Serializer for application rejections."""
    rejected_by_name = serializers.CharField(source='rejected_by.get_full_name', read_only=True)

    class Meta:
        model = ApplicationRejection
        fields = ('id', 'application', 'reason', 'rejected_by_name', 'created_at')
        read_only_fields = ('id', 'created_at')