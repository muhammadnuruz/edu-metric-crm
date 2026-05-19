from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsAdmin, IsTutor, IsTeacher, IsAdminOrReadOnly, IsStaff, IsAdminOrStaff
from .models import TutorEvaluation, MentorFeedback, DisciplineRecord
from .serializers import (
    TutorEvaluationSerializer, MentorFeedbackSerializer, DisciplineRecordSerializer,
)


class TutorEvaluationViewSet(viewsets.ModelViewSet):
    queryset = TutorEvaluation.objects.select_related("student__user", "evaluator", "semester")
    serializer_class = TutorEvaluationSerializer
    filterset_fields = ["student", "semester", "evaluator"]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update"):
            return [IsStaff()]
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdmin()]

    def perform_create(self, serializer):
        serializer.save(evaluator=self.request.user)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role in ("tutor", "komendant", "manager"):
            return qs.filter(evaluator=user)
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        return qs


class MentorFeedbackViewSet(viewsets.ModelViewSet):
    queryset = MentorFeedback.objects.select_related("student__user", "mentor", "semester")
    serializer_class = MentorFeedbackSerializer
    filterset_fields = ["student", "semester", "mentor"]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update"):
            return [IsTeacher()]
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdmin()]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "teacher":
            return qs.filter(mentor=user)
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        return qs


class DisciplineRecordViewSet(viewsets.ModelViewSet):
    queryset = DisciplineRecord.objects.select_related("student__user", "semester")
    serializer_class = DisciplineRecordSerializer
    filterset_fields = ["student", "semester"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdminOrStaff()]

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)
