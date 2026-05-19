from django.contrib import admin
from .models import Assignment, AssignmentSubmission, AssignmentScore

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["title", "subject", "assignment_type", "deadline"]

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ["student", "assignment", "quality", "score", "is_late"]

@admin.register(AssignmentScore)
class AssignmentScoreAdmin(admin.ModelAdmin):
    list_display = ["student", "semester", "score"]
