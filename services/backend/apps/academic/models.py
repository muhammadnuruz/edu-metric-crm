from django.db import models
from apps.accounts.models import StudentProfile, User


class Semester(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    semester_number = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ["year", "semester_number"]
        ordering = ["-year", "-semester_number"]

    def __str__(self):
        return f"{self.year} - {self.semester_number}-semestr"


class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    course = models.PositiveSmallIntegerField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects")
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name="taught_subjects", limit_choices_to={"role": "teacher"}
    )
    is_specialization = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"


class AcademicRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="academic_records")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="records")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="academic_records")
    grade_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "subject", "semester"]

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade_percentage}%"

    @staticmethod
    def calculate_gpa_score(gpa_percentage: float) -> float:
        """(GPA% / 100) * 40 - max 40 ball"""
        return round(min((gpa_percentage / 100) * 40, 40), 2)
