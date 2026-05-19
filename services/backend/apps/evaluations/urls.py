from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorEvaluationViewSet, MentorFeedbackViewSet, DisciplineRecordViewSet

router = DefaultRouter()
router.register("tutor", TutorEvaluationViewSet)
router.register("mentor", MentorFeedbackViewSet)
router.register("discipline", DisciplineRecordViewSet)

urlpatterns = [path("", include(router.urls))]
