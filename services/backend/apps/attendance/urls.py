from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceRecordViewSet, AttendanceSummaryViewSet

router = DefaultRouter()
router.register("records", AttendanceRecordViewSet)
router.register("summary", AttendanceSummaryViewSet)

urlpatterns = [path("", include(router.urls))]
