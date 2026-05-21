from rest_framework import serializers
from .models import TutorEvaluation, MentorFeedback, DisciplineRecord


class TutorEvaluationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    evaluator_name = serializers.CharField(source="evaluator.get_full_name", read_only=True)
    tutor_name = serializers.CharField(source="evaluator.get_full_name", read_only=True)
    behavior_score = serializers.DecimalField(source="discipline", max_digits=3, decimal_places=1, read_only=True)
    social_responsibility = serializers.DecimalField(source="social_activity", max_digits=3, decimal_places=1, read_only=True)
    communication = serializers.DecimalField(source="soft_skills", max_digits=3, decimal_places=1, read_only=True)
    initiative = serializers.DecimalField(source="corporate_culture", max_digits=3, decimal_places=1, read_only=True)
    teamwork = serializers.DecimalField(source="dormitory", max_digits=3, decimal_places=1, read_only=True)
    comments = serializers.CharField(source="comment", read_only=True)

    class Meta:
        model = TutorEvaluation
        fields = [
            "id", "student", "student_name", "semester", "evaluator", "evaluator_name", "tutor_name",
            "corporate_culture", "social_activity", "soft_skills",
            "discipline", "dormitory", "total_score", "comment",
            "behavior_score", "social_responsibility", "communication",
            "initiative", "teamwork", "comments",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "total_score", "created_at", "updated_at"]


class MentorFeedbackSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    mentor_name = serializers.CharField(source="mentor.get_full_name", read_only=True)
    comments = serializers.CharField(source="overall_comment", read_only=True)

    class Meta:
        model = MentorFeedback
        fields = [
            "id", "student", "student_name", "semester",
            "mentor", "mentor_name",
            "technical_skills", "participation", "teamwork", "initiative",
            "overall_comment", "comments", "recommendations", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class DisciplineRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    semester_name = serializers.CharField(source="semester.name", read_only=True)
    total_score = serializers.FloatField(source="score", read_only=True)
    evaluated_by_name = serializers.CharField(source="recorded_by.get_full_name", read_only=True, default=None)
    created_at = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = DisciplineRecord
        fields = [
            "id", "student", "student_name", "semester", "semester_name",
            "academic_honesty", "score", "total_score", "recorded_by",
            "evaluated_by_name", "note", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "score", "updated_at"]
