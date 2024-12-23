# src/infrastructure/repositories/django_analysis_repository.py
from typing import List, Optional
from uuid import UUID

from asgiref.sync import sync_to_async
from src.domain.entities.analysis_result import AnalysisResult
from src.domain.ports.analysis_repository import AnalysisRepository
from src.infrastructure.django.models import AnalysisModel


class DjangoAnalysisRepository(AnalysisRepository):
    async def save(self, result: AnalysisResult) -> AnalysisResult:
        """Save analysis result to Django database"""
        analysis_dict = {
            "dataset_id": result.dataset_id,
            "status": "completed",
            "parameters": {
                "well_name": result.well_name,
                "parameter": result.parameter,
                "data_points": result.data_points,
                "minimum_value": result.minimum_value,
                "maximum_value": result.maximum_value,
                "mean_value": result.mean_value,
            },
            "results": {
                "trend": result.trend,
                "statistic": result.statistic,
                "coefficient_variation": result.coefficient_variation,
                "confidence_factor": result.confidence_factor,
            },
        }

        analysis_model = await AnalysisModel.objects.acreate(**analysis_dict)
        return self._to_entity(analysis_model)

    async def get_by_id(self, result_id: UUID) -> Optional[AnalysisResult]:
        """Retrieve analysis result by ID"""
        try:
            model = await AnalysisModel.objects.aget(id=result_id)
            return self._to_entity(model)
        except AnalysisModel.DoesNotExist:
            return None

    async def list_by_dataset(self, dataset_id: UUID) -> List[AnalysisResult]:
        """List all results for a dataset"""
        queryset = AnalysisModel.objects.filter(dataset_id=dataset_id)
        models = await sync_to_async(list)(queryset)
        results = []
        for model in models:
            try:
                result = self._to_entity(model)
                if result:
                    results.append(result)
            except (KeyError, TypeError):
                continue
        return results

    def _to_entity(self, model: AnalysisModel) -> Optional[AnalysisResult]:
        """Convert Django model to domain entity"""
        params = model.parameters or {}
        results = model.results or {}

        # Skip records without required data
        if not params or not results:
            return None

        try:
            return AnalysisResult(
                id=model.id,
                dataset_id=model.dataset_id,
                well_name=params.get("well_name", "Unknown"),
                parameter=params.get("parameter", "Unknown"),
                trend=results.get("trend", "No Trend"),
                statistic=results.get("statistic", 0.0),
                coefficient_variation=results.get("coefficient_variation", 0.0),
                confidence_factor=results.get("confidence_factor", 0.0),
                analysis_date=model.completed_at or model.created_at,
                data_points=params.get("data_points", 0),
                minimum_value=params.get("minimum_value", 0.0),
                maximum_value=params.get("maximum_value", 0.0),
                mean_value=params.get("mean_value", 0.0),
            )
        except Exception:
            return None
