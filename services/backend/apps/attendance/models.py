from django.db import models
from apps.accounts.models import StudentProfile, User
from apps.academic.models import Subject, Semester


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present", "Keldi"
        ABSENT = "absent", "Kelmadi"
        LATE = "late", "Kechikdi"
        EXCUSED = "excused", "Sababli"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendance_records")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="attendance_records")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["student", "subject", "date"]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

    @staticmethod
    def calculate_attendance_score(attendance_percentage: float) -> float:
        """(X / 100) * 20 - max 20 ball"""
        return round(min((attendance_percentage / 100) * 20, 20), 2)


class AttendanceSummary(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendance_summaries")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="attendance_summaries")
    total_classes = models.PositiveIntegerField(default=0)
    attended_classes = models.PositiveIntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "semester"]

    def recalculate(self):
        records = AttendanceRecord.objects.filter(student=self.student, semester=self.semester)
        self.total_classes = records.count()
        self.attended_classes = records.filter(
            status__in=[AttendanceRecord.Status.PRESENT, AttendanceRecord.Status.LATE]
        ).count()
        self.percentage = (
            round((self.attended_classes / self.total_classes) * 100, 2)
            if self.total_classes > 0 else 0
        )
        self.score = AttendanceRecord.calculate_attendance_score(float(self.percentage))
        self.save()
