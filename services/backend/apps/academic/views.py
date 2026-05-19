from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.accounts.permissions import IsAdmin, IsAdminOrTeacher, IsAdminOrReadOnly
from .models import Semester, Subject, AcademicRecord
from .serializers import SemesterSerializer, SubjectSerializer, AcademicRecordSerializer


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAdminOrReadOnly]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related("teacher", "semester")
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["course", "semester", "teacher", "is_specialization"]


class AcademicRecordViewSet(viewsets.ModelViewSet):
    queryset = AcademicRecord.objects.select_related("student__user", "subject", "semester")
    serializer_class = AcademicRecordSerializer
    filterset_fields = ["student", "subject", "semester"]
    ordering_fields = ["grade_percentage", "created_at"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdminOrTeacher()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        if user.role == "teacher":
            return qs.filter(subject__teacher=user)
        return qs
