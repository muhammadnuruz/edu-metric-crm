from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.accounts.permissions import IsAdmin, IsStudent
from apps.academic.models import Semester
from .models import GrantScore, EmploymentRecord, GrantAllocation
from .serializers import (
    GrantScoreSerializer, GrantScorePublicSerializer,
    EmploymentRecordSerializer, GrantAllocationSerializer,
    CalculateScoresSerializer,
)
from .services import GrantScoringService


class GrantScoreViewSet(viewsets.ModelViewSet):
    queryset = GrantScore.objects.select_related("student__user", "semester")
    serializer_class = GrantScoreSerializer
    filterset_fields = ["student", "semester", "status", "gpa_eligible"]
    ordering_fields = ["final_score", "rank", "academic_score"]

    def get_permissions(self):
        if self.action == "public_rating":
            return [AllowAny()]
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdmin()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()
        qs = super().get_queryset()
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        return qs

    @action(detail=False, methods=["post"], permission_classes=[IsAdmin])
    def calculate(self, request):
        serializer = CalculateScoresSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        semester = Semester.objects.get(id=serializer.validated_data["semester_id"])
        count = GrantScoringService.calculate_all_scores(semester)
        return Response({"message": f"{count} talaba uchun ballar hisoblandi", "count": count})

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def calculate_single(self, request, pk=None):
        score = self.get_object()
        semester = score.semester
        updated = GrantScoringService.calculate_student_score(score.student, semester)
        return Response(GrantScoreSerializer(updated).data)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def public_rating(self, request):
        semester_id = request.query_params.get("semester")
        if not semester_id:
            semester = Semester.objects.filter(is_active=True).first()
        else:
            semester = Semester.objects.get(id=semester_id)

        if not semester:
            return Response({"detail": "Faol semestr topilmadi"}, status=404)

        scores = GrantScoringService.get_rating_table(semester)
        serializer = GrantScorePublicSerializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAdmin])
    def eligible(self, request):
        semester_id = request.query_params.get("semester")
        min_score = float(request.query_params.get("min_score", 80))
        semester = Semester.objects.get(id=semester_id)
        eligible = GrantScoringService.get_grant_eligible(semester, min_score)
        return Response(GrantScoreSerializer(eligible, many=True).data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def dashboard_stats(self, request):
        semester_id = request.query_params.get("semester")
        if not semester_id:
            semester = Semester.objects.filter(is_active=True).first()
        else:
            semester = Semester.objects.get(id=semester_id)

        if not semester:
            return Response({"detail": "Faol semestr topilmadi"}, status=404)

        scores = GrantScore.objects.filter(semester=semester)
        total = scores.count()
        eligible = scores.filter(final_score__gte=80, gpa_eligible=True).count()
        from django.db.models import Avg, Max, Min
        stats = scores.aggregate(
            avg_score=Avg("final_score"),
            max_score=Max("final_score"),
            min_score=Min("final_score"),
        )

        return Response({
            "semester": str(semester),
            "total_students": total,
            "eligible_count": eligible,
            "average_score": round(stats["avg_score"] or 0, 2),
            "max_score": stats["max_score"] or 0,
            "min_score": stats["min_score"] or 0,
        })


class EmploymentRecordViewSet(viewsets.ModelViewSet):
    queryset = EmploymentRecord.objects.select_related("student__user", "semester")
    serializer_class = EmploymentRecordSerializer
    filterset_fields = ["student", "semester", "employment_type", "status"]

    def get_permissions(self):
        if self.action == "create":
            return [IsStudent()]
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdmin()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def verify(self, request, pk=None):
        record = self.get_object()
        action_type = request.data.get("action", "approve")
        if action_type == "approve":
            record.status = "approved"
            record.score = request.data.get("score", record.score)
        else:
            record.status = "rejected"
        record.verified_by = request.user
        record.save()
        return Response(EmploymentRecordSerializer(record).data)


class GrantAllocationViewSet(viewsets.ModelViewSet):
    queryset = GrantAllocation.objects.select_related("student__user", "semester", "grant_score")
    serializer_class = GrantAllocationSerializer
    filterset_fields = ["student", "semester", "stage", "decision"]
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        allocation = serializer.save(decided_by=self.request.user)
        if allocation.decision == GrantAllocation.Decision.APPROVED:
            profile = allocation.student
            profile.grant_status = "active"
            profile.status = "grant"
            profile.save()
