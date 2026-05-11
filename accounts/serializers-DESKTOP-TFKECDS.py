"""
Serializers for the accounts app.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import User, CandidateProfile, RecruiterProfile
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'role', 
                  'profile_picture', 'bio', 'is_verified', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_verified')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role', 'phone')

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'candidate'),
            phone=validated_data.get('phone', ''),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials."}
            )

        user = authenticate(username=user.username, password=password)
        if user is None:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials."}
            )

        attrs['user'] = user
        return attrs


class CandidateProfileSerializer(serializers.ModelSerializer):
    """Serializer for CandidateProfile model."""
    user = UserSerializer(read_only=True)
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = CandidateProfile
        fields = ('id', 'user', 'headline', 'skills', 'skills_list', 'experience_level',
                  'years_of_experience', 'resume', 'portfolio_url', 'github_url',
                  'linkedin_url', 'is_available', 'preferred_job_titles',
                  'preferred_locations', 'expected_salary', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def get_skills_list(self, obj):
        return obj.get_skills_list()


class RecruiterProfileSerializer(serializers.ModelSerializer):
    """Serializer for RecruiterProfile model."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = ('id', 'user', 'company_name', 'company_logo', 'company_website',
                  'company_description', 'company_size', 'industry', 'office_location',
                  'is_verified', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'is_verified')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
