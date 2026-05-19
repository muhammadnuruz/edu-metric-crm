from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import StudentProfile, User
from apps.academic.models import Semester


class GrantScore(models.Model):
    """Master scoring table - aggregates all component scores"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="grant_scores")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="grant_scores")

    # Component scores
    academic_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)       # max 40
    attendance_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)      # max 20
    assignment_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)      # max 15
    activity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)        # max 10
    tutor_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)           # max 5
    discipline_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)      # max 10

    # Base total (max 100)
    base_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Bonus & Penalty
    penalty_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)         # max -20
    recovery_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)        # max +10
    employment_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)      # max +10

    # Final score
    final_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # GPA check
    gpa_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gpa_eligible = models.BooleanField(default=True)

    # Status
    class Status(models.TextChoices):
        PENDING = "pending", "Hisoblash kutilmoqda"
        CALCULATED = "calculated", "Hisoblangan"
        APPROVED = "approved", "Tasdiqlangan"
        GRANT_ACTIVE = "grant_active", "Grant faol"
        GRANT_SUSPENDED = "grant_suspended", "Grant to'xtatilgan"
        GRANT_CANCELLED = "grant_cancelled", "Grant bekor qilingan"

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    rank = models.PositiveIntegerField(null=True, blank=True)

    calculated_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "semester"]
        ordering = ["-final_score"]
        indexes = [
            models.Index(fields=["-final_score"]),
            models.Index(fields=["semester", "-final_score"]),
        ]

    def __str__(self):
        return f"{self.student} - {self.final_score} (Rank: {self.rank})"

    def calculate_total(self):
        self.base_total = min(
            float(self.academic_score) + float(self.attendance_score) +
            float(self.assignment_score) + float(self.activity_score) +
            float(self.tutor_score) + float(self.discipline_score),
            100,
        )
        self.final_score = max(
            float(self.base_total) + float(self.penalty_score) +
            float(self.recovery_score) + float(self.employment_score),
            0,
        )
        self.gpa_eligible = float(self.gpa_percentage) >= 80


class EmploymentRecord(models.Model):
    class Type(models.TextChoices):
        INTERNSHIP = "internship", "Amaliyot (0-5 ball)"
        PART_TIME = "part_time", "Part-time (5-7 ball)"
        FULL_TIME = "full_time", "Full-time (7-10 ball)"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="employment_records")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="employment_records")
    employment_type = models.CharField(max_length=20, choices=Type.choices)
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    is_it_company = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    proof_url = models.URLField(blank=True)
    score = models.DecimalField(
        max_digits=4, decimal_places=1, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Kutilmoqda"), ("approved", "Tasdiqlangan"), ("rejected", "Rad etilgan")],
        default="pending",
    )
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} - {self.company_name} ({self.employment_type})"


class GrantAllocation(models.Model):
    """Grant allocation decision after two-stage selection"""
    class Stage(models.TextChoices):
        RATING_FILTER = "rating", "Reyting saralash"
        INTERVIEW = "interview", "Suhbat"
        FINAL = "final", "Yakuniy"

    class Decision(models.TextChoices):
        APPROVED = "approved", "Grant ajratildi"
        WAITLIST = "waitlist", "Kutish ro'yxatida"
        REJECTED = "rejected", "Rad etildi"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="grant_allocations")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="grant_allocations")
    grant_score = models.ForeignKey(GrantScore, on_delete=models.CASCADE, related_name="allocations")
    stage = models.CharField(max_length=20, choices=Stage.choices)
    decision = models.CharField(max_length=20, choices=Decision.choices)
    interview_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    interview_notes = models.TextField(blank=True)
    covers_tuition = models.BooleanField(default=True)
    tuition_percentage = models.PositiveSmallIntegerField(
        default=100, validators=[MinValueValidator(50), MaxValueValidator(100)],
    )
    covers_dormitory = models.BooleanField(default=True)
    covers_meals = models.BooleanField(default=True)
    decided_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    decided_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-decided_at"]

    def __str__(self):
        return f"{self.student} - {self.decision} ({self.stage})"
