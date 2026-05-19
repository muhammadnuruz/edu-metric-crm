from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, StudentProfile, ActivityLog
from .serializers import (
    UserSerializer, UserCreateSerializer, StudentProfileSerializer,
    StudentProfileCreateSerializer, ActivityLogSerializer,
    UserMeSerializer, CustomTokenObtainPairSerializer,
)
from .permissions import IsAdmin, IsAdminOrReadOnly


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["role", "is_active"]
    search_fields = ["first_name", "last_name", "username", "email"]
    ordering_fields = ["created_at", "first_name"]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdmin()]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAdmin])
    def teachers(self, request):
        qs = User.objects.filter(role=User.Role.TEACHER, is_active=True)
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAdmin])
    def tutors(self, request):
        qs = User.objects.filter(role=User.Role.TUTOR, is_active=True)
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related("user", "mentor", "tutor", "parent")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["group", "course", "semester", "status", "grant_status"]
    search_fields = ["user__first_name", "user__last_name", "student_id"]
    ordering_fields = ["student_id", "course"]

    def get_serializer_class(self):
        if self.action == "create":
            return StudentProfileCreateSerializer
        return StudentProfileSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdmin()]


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["action", "entity_type", "user", "target_user"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return ActivityLog.objects.all()
        return ActivityLog.objects.filter(
            models.Q(user=user) | models.Q(target_user=user)
        )


from django.db import models  # noqa: E402 - needed for Q objects in get_queryset
