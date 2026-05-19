from rest_framework import serializers
from .models import Activity, ActivityScore


class ActivitySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    max_category_score = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id", "student", "student_name", "semester", "category",
            "title", "description", "proof_url", "proof_file",
            "score", "status", "verified_by", "verified_at",
            "rejection_reason", "max_category_score",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "status", "verified_by", "verified_at", "created_at", "updated_at"]

    def get_max_category_score(self, obj) -> float:
        return Activity.get_max_score_for_category(obj.category)


class ActivityVerifySerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["approve", "reject"])
    score = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)


class ActivityScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)

    class Meta:
        model = ActivityScore
        fields = [
            "id", "student", "student_name", "semester",
            "competition_score", "certificate_score",
            "volunteering_score", "other_score",
            "total_score", "updated_at",
        ]
