from rest_framework import serializers
from .models import AttendanceRecord, AttendanceSummary


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = [
            "id", "student", "student_name", "subject", "subject_name",
            "semester", "date", "status", "recorded_by", "note", "created_at",
        ]
        read_only_fields = ["id", "recorded_by", "created_at"]


class AttendanceSummarySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    semester_name = serializers.CharField(source="semester.name", read_only=True)
    present_count = serializers.SerializerMethodField()
    absent_count = serializers.SerializerMethodField()
    late_count = serializers.SerializerMethodField()
    excused_count = serializers.SerializerMethodField()
    attendance_percentage = serializers.DecimalField(source="percentage", max_digits=5, decimal_places=2, read_only=True)
    attendance_score = serializers.DecimalField(source="score", max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = AttendanceSummary
        fields = [
            "id", "student", "student_name", "semester", "semester_name",
            "total_classes", "attended_classes", "present_count", "absent_count",
            "late_count", "excused_count", "percentage", "score",
            "attendance_percentage", "attendance_score", "updated_at",
        ]

    def _count_status(self, obj, status: str) -> int:
        return obj.student.attendance_records.filter(semester=obj.semester, status=status).count()

    def get_present_count(self, obj) -> int:
        return self._count_status(obj, "present")

    def get_absent_count(self, obj) -> int:
        return self._count_status(obj, "absent")

    def get_late_count(self, obj) -> int:
        return self._count_status(obj, "late")

    def get_excused_count(self, obj) -> int:
        return self._count_status(obj, "excused")


class BulkAttendanceSerializer(serializers.Serializer):
    subject = serializers.IntegerField()
    semester = serializers.IntegerField()
    date = serializers.DateField()
    records = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
    )
