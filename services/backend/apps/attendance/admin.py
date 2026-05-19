from django.contrib import admin
from .models import AttendanceRecord, AttendanceSummary

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ["student", "subject", "date", "status"]
    list_filter = ["status", "date"]

@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = ["student", "semester", "percentage", "score"]
