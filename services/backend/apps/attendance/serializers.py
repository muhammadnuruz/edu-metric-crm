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

    class Meta:
        model = AttendanceSummary
        fields = [
            "id", "student", "student_name", "semester",
            "total_classes", "attended_classes", "percentage", "score", "updated_at",
        ]


class BulkAttendanceSerializer(serializers.Serializer):
    subject = serializers.IntegerField()
    semester = serializers.IntegerField()
    date = serializers.DateField()
    records = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
    )
