from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PenaltyViewSet, RecoveryViewSet, PenaltySummaryViewSet

router = DefaultRouter()
router.register("items", PenaltyViewSet)
router.register("recovery", RecoveryViewSet)
router.register("summary", PenaltySummaryViewSet)

urlpatterns = [path("", include(router.urls))]
