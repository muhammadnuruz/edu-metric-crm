from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import StudentProfile, User
from apps.academic.models import Semester


class TutorEvaluation(models.Model):
    """Tyutor bahosi - max 5 ball"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="tutor_evaluations")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="tutor_evaluations")
    evaluator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="given_evaluations",
        limit_choices_to={"role": "tutor"},
    )
    corporate_culture = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Korporativ madaniyat va Etika (0-1)",
    )
    social_activity = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Ijtimoiy va Ma'naviy-ma'rifiy faollik (0-1)",
    )
    soft_skills = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Soft Skills va Shaxsiy rivojlanish (0-1)",
    )
    discipline = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Intizom va Mas'uliyat (0-1)",
    )
    dormitory = models.DecimalField(
        max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Yotoqxona va Universitet hayoti (0-1)",
    )
    total_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "semester", "evaluator"]

    def save(self, *args, **kwargs):
        self.total_score = min(
            self.corporate_culture + self.social_activity +
            self.soft_skills + self.discipline + self.dormitory,
            5,
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tutor eval: {self.student} - {self.total_score}/5"


class MentorFeedback(models.Model):
    """Mentor feedback on student performance"""
    class Rating(models.TextChoices):
        EXCELLENT = "excellent", "A'lo"
        GOOD = "good", "Yaxshi"
        AVERAGE = "average", "O'rtacha"
        BELOW_AVERAGE = "below_average", "O'rtachadan past"
        POOR = "poor", "Yomon"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="mentor_feedbacks")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="mentor_feedbacks")
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="given_feedbacks",
        limit_choices_to={"role": "teacher"},
    )
    technical_skills = models.CharField(max_length=20, choices=Rating.choices)
    participation = models.CharField(max_length=20, choices=Rating.choices)
    teamwork = models.CharField(max_length=20, choices=Rating.choices)
    initiative = models.CharField(max_length=20, choices=Rating.choices)
    overall_comment = models.TextField()
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Mentor feedback: {self.student} by {self.mentor}"


class DisciplineRecord(models.Model):
    """Korporativ madaniyat va Intizom - max 10 ball"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="discipline_records")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="discipline_records")
    academic_honesty = models.DecimalField(
        max_digits=4, decimal_places=2, default=10,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "semester"]

    @property
    def score(self) -> float:
        return min(float(self.academic_honesty), 10)
