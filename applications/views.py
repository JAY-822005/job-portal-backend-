from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import JobApplication
from .serializers import ApplicationSerializer
from accounts.models import CandidateProfile


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all().order_by("-applied_at")
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        candidate = CandidateProfile.objects.get(user=self.request.user)
        serializer.save(candidate=candidate)