from django.contrib import admin
from .models import Semester, Subject, AcademicRecord


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ["name", "year", "semester_number", "is_active"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "course", "teacher"]
    list_filter = ["course", "is_specialization"]


@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ["student", "subject", "grade_percentage", "semester"]
    list_filter = ["semester"]
