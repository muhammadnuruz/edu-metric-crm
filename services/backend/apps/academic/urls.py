from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SemesterViewSet, SubjectViewSet, AcademicRecordViewSet

router = DefaultRouter()
router.register("semesters", SemesterViewSet)
router.register("subjects", SubjectViewSet)
router.register("records", AcademicRecordViewSet)

urlpatterns = [path("", include(router.urls))]
