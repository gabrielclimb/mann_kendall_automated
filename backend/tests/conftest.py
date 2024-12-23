# tests/conftest.py
from datetime import datetime
from uuid import UUID, uuid4

import numpy as np
import pandas as pd
import pytest
from src.domain.entities.analysis_result import AnalysisResult
from src.domain.ports.analysis_repository import AnalysisRepository


class MockAnalysisRepository(AnalysisRepository):
    def __init__(self):
        self.results = {}

    async def save(self, result: AnalysisResult) -> AnalysisResult:
        self.results[result.id] = result
        return result

    async def get_by_id(self, result_id: UUID) -> AnalysisResult:
        return self.results.get(result_id)

    async def list_by_dataset(self, dataset_id: UUID) -> list[AnalysisResult]:
        return [r for r in self.results.values() if r.dataset_id == dataset_id]


@pytest.fixture
def mock_repository():
    return MockAnalysisRepository()


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame(
        {
            "well": ["Well1"] * 10,
            "Date": pd.date_range(
                start="2020-01-01", periods=10, freq="ME"
            ),  # Changed from M to ME
            "Parameter1": np.linspace(1, 10, 10),  # Increasing trend
            "Parameter2": np.linspace(10, 1, 10),  # Decreasing trend
            "Parameter3": [5] * 10,  # No trend
        }
    )


@pytest.fixture
def sample_analysis_result():
    """Create a sample analysis result"""
    return AnalysisResult(
        id=uuid4(),
        dataset_id=uuid4(),
        well_name="TestWell",
        parameter="TestParam",
        trend="Increasing",
        statistic=1.23,
        coefficient_variation=0.5,
        confidence_factor=0.95,
        analysis_date=datetime.utcnow(),
        data_points=10,
        minimum_value=1.0,
        maximum_value=10.0,
        mean_value=5.5,
    )
