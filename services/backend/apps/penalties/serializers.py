from rest_framework import serializers
from .models import Penalty, Recovery, PenaltySummary


class PenaltySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    issued_by_name = serializers.CharField(source="issued_by.get_full_name", read_only=True, default=None)
    points_deducted = serializers.DecimalField(source="points", max_digits=4, decimal_places=1, read_only=True)

    class Meta:
        model = Penalty
        fields = [
            "id", "student", "student_name", "semester",
            "severity", "category", "points", "points_deducted", "description",
            "issued_by", "issued_by_name", "created_at",
        ]
        read_only_fields = ["id", "issued_by", "created_at"]


class RecoverySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    assigned_by_name = serializers.CharField(source="assigned_by.get_full_name", read_only=True, default=None)
    points_recovery = serializers.DecimalField(source="recovery_points", max_digits=4, decimal_places=1, read_only=True)

    class Meta:
        model = Recovery
        fields = [
            "id", "student", "student_name", "semester", "penalty",
            "task_description", "recovery_points", "points_recovery", "status",
            "assigned_by", "assigned_by_name", "completed_at", "review_note", "created_at",
        ]
        read_only_fields = ["id", "assigned_by", "created_at"]


class PenaltySummarySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)

    class Meta:
        model = PenaltySummary
        fields = [
            "id", "student", "student_name", "semester",
            "total_penalty", "total_recovery", "net_penalty", "updated_at",
        ]
