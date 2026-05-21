from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsAdmin, IsEvaluatorOrAdmin, IsAdminOrStaff
from .models import Penalty, Recovery, PenaltySummary
from .serializers import PenaltySerializer, RecoverySerializer, PenaltySummarySerializer


class PenaltyViewSet(viewsets.ModelViewSet):
    queryset = Penalty.objects.select_related("student__user", "issued_by", "semester")
    serializer_class = PenaltySerializer
    filterset_fields = ["student", "semester", "severity", "category"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsEvaluatorOrAdmin()]
        return [IsAdmin()]

    def perform_create(self, serializer):
        penalty = serializer.save(issued_by=self.request.user)
        summary, _ = PenaltySummary.objects.get_or_create(
            student=penalty.student, semester=penalty.semester,
        )
        summary.recalculate()

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        return qs


class RecoveryViewSet(viewsets.ModelViewSet):
    queryset = Recovery.objects.select_related("student__user", "assigned_by", "semester")
    serializer_class = RecoverySerializer
    filterset_fields = ["student", "semester", "status"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsEvaluatorOrAdmin()]
        return [IsAdmin()]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        return qs

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        recovery = self.get_object()
        if request.user.role == "student":
            if recovery.student.user_id != request.user.id:
                return Response({"detail": "Bu vazifa sizga tegishli emas"}, status=status.HTTP_403_FORBIDDEN)
            recovery.status = Recovery.Status.IN_PROGRESS
            recovery.review_note = request.data.get("review_note", recovery.review_note)
            recovery.save()
            return Response(RecoverySerializer(recovery).data)

        if request.user.role not in ("admin", "manager"):
            return Response({"detail": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

        recovery.status = Recovery.Status.COMPLETED
        recovery.completed_at = timezone.now()
        recovery.review_note = request.data.get("review_note", "")
        recovery.recovery_points = request.data.get("recovery_points", recovery.recovery_points)
        recovery.save()

        summary, _ = PenaltySummary.objects.get_or_create(
            student=recovery.student, semester=recovery.semester,
        )
        summary.recalculate()

        return Response(RecoverySerializer(recovery).data)


class PenaltySummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PenaltySummary.objects.select_related("student__user", "semester")
    serializer_class = PenaltySummarySerializer
    filterset_fields = ["student", "semester"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        return qs
