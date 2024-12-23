import uuid

from django.contrib.auth.models import User
from django.db import models


class ProjectModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "django"
        db_table = "projects"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class DatasetModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        ProjectModel, on_delete=models.CASCADE, related_name="datasets"
    )
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="datasets/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    class Meta:
        app_label = "django"
        db_table = "datasets"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.name} ({self.project.name})"


class AnalysisModel(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(
        DatasetModel, on_delete=models.CASCADE, related_name="analyses"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    parameters = models.JSONField(default=dict, null=True, blank=True)  # Made nullable
    results = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "django"
        db_table = "analyses"
        ordering = ["-created_at"]
        verbose_name_plural = "analyses"

    def __str__(self):
        return f"Analysis for {self.dataset.name}"
