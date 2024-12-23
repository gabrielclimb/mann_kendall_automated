from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.analysis_result import AnalysisResult


class AnalysisRepository(ABC):
    """Interface for analysis results repository"""

    @abstractmethod
    async def save(self, result: AnalysisResult) -> AnalysisResult:
        """Save analysis result"""
        pass

    @abstractmethod
    async def get_by_id(self, result_id: UUID) -> Optional[AnalysisResult]:
        """Get analysis result by ID"""
        pass

    @abstractmethod
    async def list_by_dataset(self, dataset_id: UUID) -> List[AnalysisResult]:
        """List all results for a dataset"""
        pass
