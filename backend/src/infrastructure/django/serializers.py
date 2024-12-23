from rest_framework import serializers

from .models import AnalysisModel, DatasetModel, ProjectModel


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = ProjectModel
        fields = ["id", "name", "description", "owner", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetModel
        fields = ["id", "project", "name", "file", "uploaded_at", "processed"]
        read_only_fields = ["uploaded_at", "processed"]


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisModel
        fields = [
            "id",
            "dataset",
            "status",
            "parameters",
            "results",
            "error_message",
            "created_at",
            "completed_at",
        ]
        read_only_fields = [
            "status",
            "results",
            "error_message",
            "created_at",
            "completed_at",
        ]

    def create(self, validated_data):
        # Ensure parameters has a default value if not provided
        if "parameters" not in validated_data:
            validated_data["parameters"] = {}
        return super().create(validated_data)
