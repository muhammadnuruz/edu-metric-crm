from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomTokenObtainPairView, UserViewSet, StudentProfileViewSet, ActivityLogViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("students", StudentProfileViewSet)
router.register("logs", ActivityLogViewSet, basename="activity-log")

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
