from django.contrib import admin
from .models import Activity, ActivityScore

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["student", "category", "title", "score", "status"]
    list_filter = ["category", "status"]

@admin.register(ActivityScore)
class ActivityScoreAdmin(admin.ModelAdmin):
    list_display = ["student", "semester", "total_score"]
