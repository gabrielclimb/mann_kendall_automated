from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class AnalysisResult:
    """Entity representing the result of a Mann-Kendall analysis"""

    well_name: str
    parameter: str
    trend: str
    statistic: float
    coefficient_variation: float
    confidence_factor: float
    analysis_date: datetime
    id: UUID
    dataset_id: UUID
    data_points: int
    minimum_value: float
    maximum_value: float
    mean_value: float
