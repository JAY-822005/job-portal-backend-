from rest_framework.routers import DefaultRouter
from .views import InterviewViewSet

router = DefaultRouter()
router.register("", InterviewViewSet, basename="interviews")

urlpatterns = router.urls