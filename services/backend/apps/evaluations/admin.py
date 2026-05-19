from django.contrib import admin
from .models import TutorEvaluation, MentorFeedback, DisciplineRecord

@admin.register(TutorEvaluation)
class TutorEvaluationAdmin(admin.ModelAdmin):
    list_display = ["student", "evaluator", "total_score", "semester"]

@admin.register(MentorFeedback)
class MentorFeedbackAdmin(admin.ModelAdmin):
    list_display = ["student", "mentor", "semester"]

@admin.register(DisciplineRecord)
class DisciplineRecordAdmin(admin.ModelAdmin):
    list_display = ["student", "academic_honesty", "semester"]
