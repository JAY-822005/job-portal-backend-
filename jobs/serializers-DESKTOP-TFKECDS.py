"""
Serializers for the jobs app.
"""

from rest_framework import serializers
from jobs.models import Job, JobCategory, Skill
from accounts.models import RecruiterProfile


class JobCategorySerializer(serializers.ModelSerializer):
    """Serializer for JobCategory model."""
    
    class Meta:
        model = JobCategory
        fields = ('id', 'name', 'slug', 'description', 'icon', 'created_at')
        read_only_fields = ('id', 'slug', 'created_at')


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model."""
    
    class Meta:
        model = Skill
        fields = ('id', 'name', 'slug', 'description', 'created_at')
        read_only_fields = ('id', 'slug', 'created_at')


class JobListSerializer(serializers.ModelSerializer):
    """Serializer for listing jobs (basic information)."""
    company_name = serializers.CharField(source='recruiter.company_name', read_only=True)
    company_logo = serializers.ImageField(source='recruiter.company_logo', read_only=True)
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('id', 'title', 'slug', 'company_name', 'company_logo', 'location',
                  'job_type', 'salary_min', 'salary_max', 'salary_currency',
                  'is_remote', 'experience_level', 'skills_list', 'is_active',
                  'views_count', 'created_at')
        read_only_fields = fields

    def get_skills_list(self, obj):
        return obj.get_skills_list()


class JobDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed job information."""
    recruiter_detail = serializers.SerializerMethodField()
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('id', 'title', 'slug', 'description', 'requirements',
                  'responsibilities', 'location', 'job_type', 'experience_level',
                  'salary_min', 'salary_max', 'salary_currency', 'is_remote',
                  'benefits', 'skills_required', 'skills_list', 'status',
                  'is_active', 'views_count', 'deadline', 'recruiter_detail',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'views_count', 'created_at', 'updated_at')

    def get_recruiter_detail(self, obj):
        return {
            'id': obj.recruiter.id,
            'name': obj.recruiter.user.get_full_name(),
            'company_name': obj.recruiter.company_name,
            'company_website': obj.recruiter.company_website,
            'company_logo': obj.recruiter.company_logo.url if obj.recruiter.company_logo else None,
        }

    def get_skills_list(self, obj):
        return obj.get_skills_list()


class JobCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating jobs."""
    
    class Meta:
        model = Job
        fields = ('title', 'slug', 'description', 'requirements', 'responsibilities',
                  'location', 'job_type', 'experience_level', 'salary_min',
                  'salary_max', 'salary_currency', 'is_remote', 'benefits',
                  'skills_required', 'status', 'is_active', 'deadline')

    def create(self, validated_data):
        user = self.context['request'].user
        recruiter = RecruiterProfile.objects.get(user=user)
        job = Job.objects.create(recruiter=recruiter, **validated_data)
        return job