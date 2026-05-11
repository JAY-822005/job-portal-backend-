"""
Permission classes for the Job Portal API.
"""

from rest_framework.permissions import BasePermission


class IsCandidate(BasePermission):
    """
    Permission to check if user is a Candidate.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'candidate'


class IsRecruiter(BasePermission):
    """
    Permission to check if user is a Recruiter.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'recruiter'


class IsAdmin(BasePermission):
    """
    Permission to check if user is an Admin.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser)


class IsRecruiterOrReadOnly(BasePermission):
    """
    Permission to allow recruiters to edit, others can only read.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read for everyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Allow write only for recruiters
        return request.user.role == 'recruiter'


class IsCandidateOwner(BasePermission):
    """
    Permission to check if user is the owner of the candidate profile.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsRecruiterOwner(BasePermission):
    """
    Permission to check if user is the owner of the recruiter profile.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
