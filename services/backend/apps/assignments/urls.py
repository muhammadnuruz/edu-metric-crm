from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, AssignmentSubmissionViewSet, AssignmentScoreViewSet

router = DefaultRouter()
router.register("tasks", AssignmentViewSet)
router.register("submissions", AssignmentSubmissionViewSet)
router.register("scores", AssignmentScoreViewSet)

urlpatterns = [path("", include(router.urls))]
