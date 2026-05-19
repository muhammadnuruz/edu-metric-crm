from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GrantScoreViewSet, EmploymentRecordViewSet, GrantAllocationViewSet

router = DefaultRouter()
router.register("scores", GrantScoreViewSet)
router.register("employment", EmploymentRecordViewSet)
router.register("allocations", GrantAllocationViewSet)

urlpatterns = [path("", include(router.urls))]
