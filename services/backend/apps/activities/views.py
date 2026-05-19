from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsAdmin, IsStudent
from .models import Activity, ActivityScore
from .serializers import ActivitySerializer, ActivityVerifySerializer, ActivityScoreSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.select_related("student__user", "semester", "verified_by")
    serializer_class = ActivitySerializer
    filterset_fields = ["student", "semester", "category", "status"]
    search_fields = ["title"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        return qs

    def get_permissions(self):
        if self.action == "create":
            return [IsStudent()]
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        if self.action == "verify":
            return [IsAdmin()]
        return [IsAdmin()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def verify(self, request, pk=None):
        activity = self.get_object()
        serializer = ActivityVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["action"] == "approve":
            activity.status = Activity.Status.APPROVED
            if "score" in serializer.validated_data:
                max_score = Activity.get_max_score_for_category(activity.category)
                activity.score = min(serializer.validated_data["score"], max_score)
        else:
            activity.status = Activity.Status.REJECTED
            activity.rejection_reason = serializer.validated_data.get("rejection_reason", "")

        activity.verified_by = request.user
        activity.verified_at = timezone.now()
        activity.save()

        score_obj, _ = ActivityScore.objects.get_or_create(
            student=activity.student, semester=activity.semester,
        )
        score_obj.recalculate()

        return Response(ActivitySerializer(activity).data)


class ActivityScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityScore.objects.select_related("student__user", "semester")
    serializer_class = ActivityScoreSerializer
    filterset_fields = ["student", "semester"]
