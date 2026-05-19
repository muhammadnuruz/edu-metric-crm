from django.contrib import admin
from .models import Penalty, Recovery, PenaltySummary

@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ["student", "category", "severity", "points"]

@admin.register(Recovery)
class RecoveryAdmin(admin.ModelAdmin):
    list_display = ["student", "status", "recovery_points"]

@admin.register(PenaltySummary)
class PenaltySummaryAdmin(admin.ModelAdmin):
    list_display = ["student", "semester", "total_penalty", "total_recovery", "net_penalty"]
