from rest_framework import serializers
from .models import GrantScore, EmploymentRecord, GrantAllocation


class GrantScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    student_id = serializers.CharField(source="student.student_id", read_only=True)
    group = serializers.CharField(source="student.group", read_only=True)

    class Meta:
        model = GrantScore
        fields = [
            "id", "student", "student_name", "student_id", "group", "semester",
            "academic_score", "attendance_score", "assignment_score",
            "activity_score", "tutor_score", "discipline_score",
            "base_total", "penalty_score", "recovery_score", "employment_score",
            "final_score", "gpa_percentage", "gpa_eligible",
            "status", "rank", "calculated_at", "approved_by", "updated_at",
        ]
        read_only_fields = [
            "id", "base_total", "final_score", "rank",
            "calculated_at", "updated_at",
        ]


class GrantScorePublicSerializer(serializers.ModelSerializer):
    """Public rating view - limited fields for guest access"""
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    group = serializers.CharField(source="student.group", read_only=True)

    class Meta:
        model = GrantScore
        fields = [
            "rank", "student_name", "group",
            "academic_score", "attendance_score", "assignment_score",
            "activity_score", "tutor_score", "discipline_score",
            "base_total", "final_score", "status",
        ]


class EmploymentRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)

    class Meta:
        model = EmploymentRecord
        fields = [
            "id", "student", "student_name", "semester",
            "employment_type", "company_name", "position",
            "is_it_company", "start_date", "end_date",
            "proof_url", "score", "status",
            "verified_by", "created_at",
        ]
        read_only_fields = ["id", "status", "verified_by", "created_at"]


class GrantAllocationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)

    class Meta:
        model = GrantAllocation
        fields = [
            "id", "student", "student_name", "semester", "grant_score",
            "stage", "decision", "interview_score", "interview_notes",
            "covers_tuition", "tuition_percentage",
            "covers_dormitory", "covers_meals",
            "decided_by", "decided_at", "notes",
        ]
        read_only_fields = ["id", "decided_by", "decided_at"]


class CalculateScoresSerializer(serializers.Serializer):
    semester_id = serializers.IntegerField()
