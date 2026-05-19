from django.db import models
from apps.accounts.models import StudentProfile, User
from apps.academic.models import Subject, Semester


class Assignment(models.Model):
    class Type(models.TextChoices):
        HOMEWORK = "homework", "Uy vazifasi"
        PROJECT = "project", "Loyiha"
        LAB = "lab", "Laboratoriya"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="assignments")
    assignment_type = models.CharField(max_length=20, choices=Type.choices, default=Type.HOMEWORK)
    deadline = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-deadline"]

    def __str__(self):
        return f"{self.title} - {self.subject.name}"


class AssignmentSubmission(models.Model):
    class Quality(models.TextChoices):
        EXCELLENT = "excellent", "A'lo"
        GOOD = "good", "Yaxshi"
        AVERAGE = "average", "O'rtacha"
        POOR = "poor", "Yomon"
        PLAGIARISM = "plagiarism", "Ko'chirma"

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)
    file_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    note = models.TextField(blank=True)
    is_late = models.BooleanField(default=False)
    quality = models.CharField(max_length=20, choices=Quality.choices, null=True, blank=True)
    is_independent = models.BooleanField(default=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="graded_submissions")
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["assignment", "student"]
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"


class AssignmentScore(models.Model):
    """Aggregated assignment score per student per semester - max 15 ball"""
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="assignment_scores")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="assignment_scores")
    total_assignments = models.PositiveIntegerField(default=0)
    completed_assignments = models.PositiveIntegerField(default=0)
    average_quality_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "semester"]

    def recalculate(self):
        submissions = AssignmentSubmission.objects.filter(
            student=self.student,
            assignment__semester=self.semester,
            score__isnull=False,
        )
        self.total_assignments = Assignment.objects.filter(
            semester=self.semester,
            subject__in=self.student.user.student_profile.group
        ).count() or 1
        self.completed_assignments = submissions.count()

        if submissions.exists():
            from django.db.models import Avg
            avg = submissions.aggregate(avg=Avg("score"))["avg"] or 0
            self.average_quality_score = avg
            self.score = round(min((avg / 100) * 15, 15), 2)
        else:
            self.score = 0

        self.save()
