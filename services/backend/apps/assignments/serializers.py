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

    class Meta:
        model = AssignmentSubmission
        fields = [
            "id", "assignment", "assignment_title", "student", "student_name",
            "submitted_at", "file_url", "github_url", "note",
            "is_late", "quality", "is_independent", "score",
            "feedback", "graded_by", "graded_at",
        ]
        read_only_fields = ["id", "submitted_at", "graded_at"]


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
