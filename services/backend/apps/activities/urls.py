from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivityScoreViewSet

router = DefaultRouter()
router.register("items", ActivityViewSet)
router.register("scores", ActivityScoreViewSet)

urlpatterns = [path("", include(router.urls))]
