from rest_framework import serializers
from .models import Assignment, AssignmentSubmission, AssignmentScore


class AssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = Assignment
        fields = [
            "id", "title", "description", "subject", "subject_name",
            "semester", "assignment_type", "deadline", "max_score",
            "created_by", "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    assignment_title = serializers.CharField(source="assignment.title", read_only=True)
    assignment_type = serializers.CharField(source="assignment.assignment_type", read_only=True)
    status = serializers.SerializerMethodField()
    quality_score = serializers.DecimalField(source="score", max_digits=5, decimal_places=2, read_only=True)
    deadline_score = serializers.SerializerMethodField()
    independence_score = serializers.SerializerMethodField()
    total_score = serializers.DecimalField(source="score", max_digits=5, decimal_places=2, read_only=True)
    graded_by_name = serializers.CharField(source="graded_by.get_full_name", read_only=True, default=None)

    class Meta:
        model = AssignmentSubmission
        fields = [
            "id", "assignment", "assignment_title", "assignment_type", "student", "student_name",
            "submitted_at", "file_url", "github_url", "note",
            "is_late", "quality", "is_independent", "score",
            "feedback", "graded_by", "graded_at",
            "status", "quality_score", "deadline_score", "independence_score",
            "total_score", "graded_by_name",
        ]
        read_only_fields = ["id", "student", "submitted_at", "graded_at"]

    def get_status(self, obj) -> str:
        if obj.quality == "plagiarism":
            return "plagiarism"
        return "graded" if obj.score is not None else "pending"

    def get_deadline_score(self, obj) -> int:
        return 0 if obj.is_late else 1

    def get_independence_score(self, obj) -> int:
        return 1 if obj.is_independent else 0


class AssignmentGradeSerializer(serializers.Serializer):
    quality = serializers.ChoiceField(choices=AssignmentSubmission.Quality.choices)
    is_independent = serializers.BooleanField()
    score = serializers.DecimalField(max_digits=5, decimal_places=2)
    feedback = serializers.CharField(required=False, allow_blank=True)


class AssignmentScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)

    class Meta:
        model = AssignmentScore
        fields = [
            "id", "student", "student_name", "semester",
            "total_assignments", "completed_assignments",
            "average_quality_score", "score", "updated_at",
        ]
