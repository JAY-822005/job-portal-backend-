"""
Serializers for the interviews app.
"""

from rest_framework import serializers
from interviews.models import Interview, InterviewScheduleTemplate, InterviewFeedback


class InterviewListSerializer(serializers.ModelSerializer):
    """Serializer for listing interviews."""
    candidate_name = serializers.CharField(source='application.candidate.user.get_full_name', read_only=True)
    job_title = serializers.CharField(source='application.job.title', read_only=True)

    class Meta:
        model = Interview
        fields = ('id', 'candidate_name', 'job_title', 'interview_type', 'status',
                  'scheduled_at', 'interviewer', 'rating', 'created_at')
        read_only_fields = fields


class InterviewDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed interview information."""
    candidate_info = serializers.SerializerMethodField()
    job_info = serializers.SerializerMethodField()
    interviewer_name = serializers.CharField(source='interviewer.get_full_name', read_only=True)

    class Meta:
        model = Interview
        fields = ('id', 'candidate_info', 'job_info', 'interview_type', 'status',
                  'scheduled_at', 'duration_minutes', 'interviewer', 'interviewer_name',
                  'meeting_link', 'location', 'notes', 'feedback', 'rating',
                  'completed_at', 'created_at', 'updated_at')
        read_only_fields = ('id', 'completed_at', 'created_at', 'updated_at')

    def get_candidate_info(self, obj):
        return {
            'id': obj.application.candidate.id,
            'name': obj.application.candidate.user.get_full_name(),
            'email': obj.application.candidate.user.email,
        }

    def get_job_info(self, obj):
        return {
            'id': obj.application.job.id,
            'title': obj.application.job.title,
            'company': obj.application.job.recruiter.company_name,
        }


class InterviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating interviews."""
    
    class Meta:
        model = Interview
        fields = ('application', 'interview_type', 'scheduled_at', 'duration_minutes',
                  'interviewer', 'meeting_link', 'location', 'notes')


class InterviewFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for interview feedback."""
    interview_detail = serializers.SerializerMethodField()

    class Meta:
        model = InterviewFeedback
        fields = ('id', 'interview', 'interview_detail', 'technical_skills_score',
                  'communication_score', 'problem_solving_score', 'cultural_fit_score',
                  'strengths', 'areas_for_improvement', 'overall_recommendation',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_interview_detail(self, obj):
        return {
            'id': obj.interview.id,
            'candidate_name': obj.interview.application.candidate.user.get_full_name(),
            'job_title': obj.interview.application.job.title,
            'interview_type': obj.interview.get_interview_type_display(),
        }


class InterviewScheduleTemplateSerializer(serializers.ModelSerializer):
    """Serializer for interview schedule templates."""
    recruiter_name = serializers.CharField(source='recruiter.get_full_name', read_only=True)

    class Meta:
        model = InterviewScheduleTemplate
        fields = ('id', 'name', 'description', 'interview_rounds', 'recruiter_name',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'recruiter_name', 'created_at', 'updated_at')