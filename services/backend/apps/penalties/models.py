from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import StudentProfile, User
from apps.academic.models import Semester


class Penalty(models.Model):
    class Severity(models.TextChoices):
        LIGHT = "light", "Yengil (-1)"
        MEDIUM = "medium", "O'rtacha (-3)"
        HEAVY = "heavy", "Og'ir (-5 to -15)"

    class Category(models.TextChoices):
        LATE = "late", "Kechikish"
        PHONE = "phone", "Telefon ishlatish"
        DORMITORY = "dormitory", "Yotoqxona qoidalari"
        ABSENT = "absent", "Sababsiz dars qoldirish"
        IGNORE_WARNING = "ignore_warning", "Ogohlantirishni e'tiborsiz qoldirish"
        RULE_VIOLATION = "rule_violation", "Tartib qoidalarini buzish"
        SYSTEMATIC_ABSENT = "systematic_absent", "Tizimli dars qoldirish"
        DISCIPLINE_ISSUE = "discipline_issue", "Intizomiy muammolar"
        CHEATING = "cheating", "Akademik firibgarlik"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="penalties")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="penalties")
    severity = models.CharField(max_length=10, choices=Severity.choices)
    category = models.CharField(max_length=30, choices=Category.choices)
    points = models.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(-20), MaxValueValidator(0)],
    )
    description = models.TextField()
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="issued_penalties")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Penalties"

    def __str__(self):
        return f"{self.student} - {self.category}: {self.points}"


class Recovery(models.Model):
    class Status(models.TextChoices):
        ASSIGNED = "assigned", "Tayinlangan"
        IN_PROGRESS = "in_progress", "Bajarilmoqda"
        COMPLETED = "completed", "Bajarildi"
        FAILED = "failed", "Bajarilmadi"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="recoveries")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="recoveries")
    penalty = models.ForeignKey(Penalty, on_delete=models.CASCADE, related_name="recoveries", null=True, blank=True)
    task_description = models.TextField()
    recovery_points = models.DecimalField(
        max_digits=4, decimal_places=1, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ASSIGNED)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_recoveries")
    completed_at = models.DateTimeField(null=True, blank=True)
    review_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Recoveries"

    def __str__(self):
        return f"{self.student} - Recovery: {self.recovery_points}"


class PenaltySummary(models.Model):
    """Aggregated penalty/recovery per student per semester"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="penalty_summaries")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="penalty_summaries")
    total_penalty = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    total_recovery = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    net_penalty = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "semester"]

    def recalculate(self):
        from django.db.models import Sum
        penalties = Penalty.objects.filter(
            student=self.student, semester=self.semester,
        ).aggregate(total=Sum("points"))["total"] or 0
        self.total_penalty = max(penalties, -20)

        recoveries = Recovery.objects.filter(
            student=self.student, semester=self.semester,
            status=Recovery.Status.COMPLETED,
        ).aggregate(total=Sum("recovery_points"))["total"] or 0
        max_recovery = min(abs(float(self.total_penalty)) * 0.5, 10)
        self.total_recovery = min(float(recoveries), max_recovery)

        self.net_penalty = float(self.total_penalty) + float(self.total_recovery)
        self.save()
