from django.contrib import admin
from .models import GrantScore, EmploymentRecord, GrantAllocation

@admin.register(GrantScore)
class GrantScoreAdmin(admin.ModelAdmin):
    list_display = ["student", "semester", "final_score", "rank", "gpa_eligible", "status"]
    list_filter = ["semester", "status", "gpa_eligible"]
    ordering = ["rank"]

@admin.register(EmploymentRecord)
class EmploymentRecordAdmin(admin.ModelAdmin):
    list_display = ["student", "employment_type", "company_name", "score", "status"]
    list_filter = ["employment_type", "status"]

@admin.register(GrantAllocation)
class GrantAllocationAdmin(admin.ModelAdmin):
    list_display = ["student", "semester", "stage", "decision"]
    list_filter = ["stage", "decision"]
