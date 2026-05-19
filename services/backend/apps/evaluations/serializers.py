from rest_framework import serializers
from .models import TutorEvaluation, MentorFeedback, DisciplineRecord


class TutorEvaluationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    evaluator_name = serializers.CharField(source="evaluator.get_full_name", read_only=True)

    class Meta:
        model = TutorEvaluation
        fields = [
            "id", "student", "student_name", "semester", "evaluator", "evaluator_name",
            "corporate_culture", "social_activity", "soft_skills",
            "discipline", "dormitory", "total_score", "comment",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "total_score", "created_at", "updated_at"]


class MentorFeedbackSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    mentor_name = serializers.CharField(source="mentor.get_full_name", read_only=True)

    class Meta:
        model = MentorFeedback
        fields = [
            "id", "student", "student_name", "semester",
            "mentor", "mentor_name",
            "technical_skills", "participation", "teamwork", "initiative",
            "overall_comment", "recommendations", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class DisciplineRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)

    class Meta:
        model = DisciplineRecord
        fields = [
            "id", "student", "student_name", "semester",
            "academic_honesty", "score", "recorded_by", "note", "updated_at",
        ]
        read_only_fields = ["id", "score", "updated_at"]
