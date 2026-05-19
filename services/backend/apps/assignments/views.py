from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsAdminOrTeacher, IsStudent
from .models import Assignment, AssignmentSubmission, AssignmentScore
from .serializers import (
    AssignmentSerializer, AssignmentSubmissionSerializer,
    AssignmentGradeSerializer, AssignmentScoreSerializer,
)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related("subject", "semester")
    serializer_class = AssignmentSerializer
    filterset_fields = ["subject", "semester", "assignment_type"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdminOrTeacher()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.select_related("assignment", "student__user")
    serializer_class = AssignmentSubmissionSerializer
    filterset_fields = ["assignment", "student", "quality", "is_late"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        if user.role == "teacher":
            return qs.filter(assignment__subject__teacher=user)
        return qs

    def get_permissions(self):
        if self.action == "create":
            return [IsStudent()]
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdminOrTeacher()]

    def perform_create(self, serializer):
        assignment = Assignment.objects.get(id=self.request.data.get("assignment"))
        is_late = timezone.now() > assignment.deadline
        serializer.save(
            student=self.request.user.student_profile,
            is_late=is_late,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrTeacher])
    def grade(self, request, pk=None):
        submission = self.get_object()
        serializer = AssignmentGradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission.quality = serializer.validated_data["quality"]
        submission.is_independent = serializer.validated_data["is_independent"]
        submission.score = serializer.validated_data["score"]
        submission.feedback = serializer.validated_data.get("feedback", "")
        submission.graded_by = request.user
        submission.graded_at = timezone.now()

        if submission.quality == AssignmentSubmission.Quality.PLAGIARISM:
            submission.score = 0
            submission.is_independent = False

        submission.save()
        return Response(AssignmentSubmissionSerializer(submission).data)


class AssignmentScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssignmentScore.objects.select_related("student__user", "semester")
    serializer_class = AssignmentScoreSerializer
    filterset_fields = ["student", "semester"]
