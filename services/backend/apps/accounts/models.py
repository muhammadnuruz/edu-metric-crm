from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        TEACHER = "teacher", "Teacher/Mentor"
        TUTOR = "tutor", "Tutor"
        PARENT = "parent", "Parent"
        STUDENT = "student", "Student"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    pnfl = models.CharField(max_length=14, blank=True, unique=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def is_admin_role(self) -> bool:
        return self.role == self.Role.ADMIN

    @property
    def is_teacher(self) -> bool:
        return self.role == self.Role.TEACHER

    @property
    def is_tutor(self) -> bool:
        return self.role == self.Role.TUTOR

    @property
    def is_parent(self) -> bool:
        return self.role == self.Role.PARENT

    @property
    def is_student_role(self) -> bool:
        return self.role == self.Role.STUDENT


class StudentProfile(models.Model):
    class Status(models.TextChoices):
        GRANT = "grant", "Grant"
        CONTRACT = "contract", "Kontrakt"

    class GrantStatus(models.TextChoices):
        ACTIVE = "active", "Faol"
        SUSPENDED = "suspended", "To'xtatilgan"
        CANCELLED = "cancelled", "Bekor qilingan"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.CharField(max_length=20, unique=True)
    group = models.CharField(max_length=20)
    course = models.PositiveSmallIntegerField(default=1)
    semester = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONTRACT)
    grant_status = models.CharField(max_length=20, choices=GrantStatus.choices, default=GrantStatus.ACTIVE)
    enrollment_date = models.DateField(null=True, blank=True)
    mentor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="mentored_students", limit_choices_to={"role": User.Role.TEACHER}
    )
    tutor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="tutored_students", limit_choices_to={"role": User.Role.TUTOR}
    )
    parent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="children", limit_choices_to={"role": User.Role.PARENT}
    )

    class Meta:
        ordering = ["student_id"]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"


class ActivityLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "create", "Yaratildi"
        UPDATE = "update", "Yangilandi"
        DELETE = "delete", "O'chirildi"
        SCORE_CHANGE = "score_change", "Ball o'zgarishi"
        GRANT_STATUS = "grant_status", "Grant holati"
        PENALTY = "penalty", "Jarima"
        RECOVERY = "recovery", "Tiklanish"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity_logs")
    target_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="target_logs"
    )
    action = models.CharField(max_length=30, choices=Action.choices)
    entity_type = models.CharField(max_length=50)
    entity_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["target_user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.entity_type}"
