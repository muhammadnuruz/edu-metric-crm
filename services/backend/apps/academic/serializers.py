from rest_framework import serializers
from .models import Semester, Subject, AcademicRecord


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.get_full_name", read_only=True, default=None)

    class Meta:
        model = Subject
        fields = ["id", "name", "code", "course", "semester", "teacher", "teacher_name", "is_specialization"]


class AcademicRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    gpa_score = serializers.SerializerMethodField()

    class Meta:
        model = AcademicRecord
        fields = [
            "id", "student", "student_name", "subject", "subject_name",
            "semester", "grade_percentage", "gpa_score",
            "created_by", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def get_gpa_score(self, obj) -> float:
        return AcademicRecord.calculate_gpa_score(float(obj.grade_percentage))
