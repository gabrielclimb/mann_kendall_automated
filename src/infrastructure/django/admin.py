from django.contrib import admin

from .models import AnalysisModel, DatasetModel, ProjectModel


@admin.register(ProjectModel)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "description", "owner__username")
    date_hierarchy = "created_at"


@admin.register(DatasetModel)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "uploaded_at", "processed")
    list_filter = ("processed", "uploaded_at")
    search_fields = ("name", "project__name")
    date_hierarchy = "uploaded_at"


@admin.register(AnalysisModel)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("dataset", "status", "created_at", "completed_at")
    list_filter = ("status", "created_at", "completed_at")
    search_fields = ("dataset__name", "error_message")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "completed_at")
