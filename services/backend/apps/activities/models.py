from django.db import models
from apps.accounts.models import StudentProfile, User
from apps.academic.models import Semester


class Activity(models.Model):
    class Category(models.TextChoices):
        COMPETITION = "competition", "Musobaqa"
        STARTUP = "startup", "Startup"
        MENTORING = "mentoring", "Mentorlik"
        CERTIFICATE_PDP = "cert_pdp", "PDP Sertifikat"
        CERTIFICATE_NATIONAL = "cert_national", "Milliy IT sertifikat"
        CERTIFICATE_LANGUAGE = "cert_language", "Til sertifikati"
        CERTIFICATE_INTERNATIONAL = "cert_international", "Xalqaro IT sertifikat"
        VOLUNTEERING = "volunteering", "Volontyorlik"
        SOFT_SKILLS = "soft_skills", "Soft Skills"
        NETWORKING = "networking", "Networking"
        PROJECT_PARTICIPANT = "project_participant", "Loyiha ishtirokchisi"
        DIRECTION_ASSISTANT = "direction_assistant", "Yo'nalish yordamchisi"
        STRATEGIC_ASSISTANT = "strategic_assistant", "Strategik yordamchi"

    class Status(models.TextChoices):
        PENDING = "pending", "Kutilmoqda"
        APPROVED = "approved", "Tasdiqlangan"
        REJECTED = "rejected", "Rad etilgan"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="activities")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="activities")
    category = models.CharField(max_length=30, choices=Category.choices)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    proof_url = models.URLField(blank=True)
    proof_file = models.FileField(upload_to="activity_proofs/", blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    verified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_activities"
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.student} - {self.title} ({self.category})"

    @staticmethod
    def get_max_score_for_category(category: str) -> float:
        max_scores = {
            "competition": 3,
            "startup": 7,
            "mentoring": 3,
            "cert_pdp": 3,
            "cert_national": 2,
            "cert_language": 5,
            "cert_international": 10,
            "volunteering": 2,
            "soft_skills": 1,
            "networking": 1,
            "project_participant": 2,
            "direction_assistant": 3,
            "strategic_assistant": 4,
        }
        return max_scores.get(category, 0)


class ActivityScore(models.Model):
    """Aggregated activity score per student per semester - max 10 ball"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="activity_scores")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="activity_scores")
    competition_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    certificate_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    volunteering_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    other_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "semester"]

    def recalculate(self):
        approved = Activity.objects.filter(
            student=self.student, semester=self.semester,
            status=Activity.Status.APPROVED,
        )
        from django.db.models import Sum
        self.competition_score = min(
            approved.filter(category__in=["competition", "startup"]).aggregate(s=Sum("score"))["s"] or 0, 10
        )
        self.certificate_score = min(
            approved.filter(category__startswith="cert_").aggregate(s=Sum("score"))["s"] or 0, 10
        )
        self.volunteering_score = min(
            approved.filter(category__in=["volunteering", "soft_skills", "networking"]).aggregate(s=Sum("score"))["s"] or 0, 4
        )
        self.other_score = min(
            approved.filter(category__in=["mentoring", "project_participant", "direction_assistant", "strategic_assistant"]).aggregate(s=Sum("score"))["s"] or 0, 10
        )
        self.total_score = min(
            self.competition_score + self.certificate_score + self.volunteering_score + self.other_score, 10
        )
        self.save()
