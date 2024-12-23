# src/infrastructure/django/views.py
import pandas as pd
from asgiref.sync import async_to_sync
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.application.use_cases.perform_mann_kendall_analysis import (
    PerformMannKendallAnalysis,
)
from src.infrastructure.django.serializers import (
    AnalysisSerializer,
    DatasetSerializer,
    ProjectSerializer,
)
from src.infrastructure.repositories.django_analysis_repository import (
    DjangoAnalysisRepository,
)

from .models import AnalysisModel, DatasetModel, ProjectModel


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = DatasetModel.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(project__owner=self.request.user)

    @action(detail=True, methods=["post"])
    def analyze(self, request: Request, pk=None) -> Response:
        """
        Perform Mann-Kendall analysis on the dataset
        """
        dataset = self.get_object()

        try:
            # Read the dataset file
            file_path = dataset.file.path
            df = pd.read_excel(file_path, header=None, index_col=0)

            # Initialize use case and repository
            repository = DjangoAnalysisRepository()
            use_case = PerformMannKendallAnalysis(repository)

            # Execute analysis using async_to_sync
            results = async_to_sync(use_case.execute)(dataset.id, df)

            # Update dataset status
            dataset.processed = True
            dataset.save()

            # Return success response
            return Response(
                {
                    "message": "Analysis completed successfully",
                    "results_count": len(results),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"Analysis failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = AnalysisModel.objects.all()
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(dataset__project__owner=self.request.user)

    @action(detail=False, methods=["get"])
    def dataset_results(self, request):
        """
        Get all analysis results for a specific dataset
        """
        dataset_id = request.query_params.get("dataset_id")
        if not dataset_id:
            return Response(
                {"error": "dataset_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        repository = DjangoAnalysisRepository()
        # Convert async operation to sync
        results = async_to_sync(repository.list_by_dataset)(dataset_id)

        return Response(
            [
                {
                    "well_name": r.well_name,
                    "parameter": r.parameter,
                    "trend": r.trend,
                    "statistic": r.statistic,
                    "coefficient_variation": r.coefficient_variation,
                    "confidence_factor": r.confidence_factor,
                    "data_points": r.data_points,
                    "minimum_value": r.minimum_value,
                    "maximum_value": r.maximum_value,
                    "mean_value": r.mean_value,
                    "analysis_date": r.analysis_date,
                }
                for r in results
            ]
        )
