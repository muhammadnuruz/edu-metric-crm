from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsAdminOrTeacher
from apps.accounts.models import StudentProfile
from apps.academic.models import Subject, Semester
from .models import AttendanceRecord, AttendanceSummary
from .serializers import AttendanceRecordSerializer, AttendanceSummarySerializer, BulkAttendanceSerializer


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related("student__user", "subject", "semester")
    serializer_class = AttendanceRecordSerializer
    filterset_fields = ["student", "subject", "semester", "date", "status"]
    ordering_fields = ["date"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdminOrTeacher()]

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

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

    @action(detail=False, methods=["post"], permission_classes=[IsAdminOrTeacher])
    def bulk_create(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        subject = Subject.objects.get(id=data["subject"])
        semester = Semester.objects.get(id=data["semester"])
        created = []

        for record in data["records"]:
            student = StudentProfile.objects.get(id=record["student_id"])
            obj, _ = AttendanceRecord.objects.update_or_create(
                student=student, subject=subject, date=data["date"],
                defaults={
                    "status": record["status"],
                    "semester": semester,
                    "recorded_by": request.user,
                },
            )
            created.append(obj)

            summary, _ = AttendanceSummary.objects.get_or_create(
                student=student, semester=semester,
            )
            summary.recalculate()

        return Response(
            AttendanceRecordSerializer(created, many=True).data,
            status=status.HTTP_201_CREATED,
        )


class AttendanceSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AttendanceSummary.objects.select_related("student__user", "semester")
    serializer_class = AttendanceSummarySerializer
    filterset_fields = ["student", "semester"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "student":
            return qs.filter(student__user=user)
        if user.role == "parent":
            return qs.filter(student__parent=user)
        return qs
