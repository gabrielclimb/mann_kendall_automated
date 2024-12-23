from uuid import uuid4

import pandas as pd
import pytest
from src.application.use_cases.perform_mann_kendall_analysis import (
    PerformMannKendallAnalysis,
)


@pytest.mark.asyncio
async def test_analysis_with_invalid_data(mock_repository):
    """Test analysis with invalid data"""
    use_case = PerformMannKendallAnalysis(mock_repository)
    dataset_id = uuid4()

    # Test case 1: Missing required column
    with pytest.raises(ValueError, match="Missing required columns"):
        invalid_data = pd.DataFrame(
            {
                "well": ["Well1"],
                "Parameter1": [1.0],  # Missing Date column
            }
        )
        await use_case.execute(dataset_id, invalid_data)

    # Test case 2: Empty DataFrame
    with pytest.raises(ValueError, match="Input data is empty"):
        empty_data = pd.DataFrame(columns=["well", "Date", "Parameter1"])
        await use_case.execute(dataset_id, empty_data)

    # Test case 3: Null values in required columns
    with pytest.raises(ValueError, match="Null values found in required columns"):
        null_data = pd.DataFrame(
            {"well": [None], "Date": ["2020-01-01"], "Parameter1": [1.0]}
        )
        await use_case.execute(dataset_id, null_data)

    # Test case 4: Non-numeric parameter values
    with pytest.raises(
        ValueError,
        match="Error validating column Parameter1: No valid numeric values found in column: Parameter1",
    ):
        non_numeric_data = pd.DataFrame(
            {"well": ["Well1"], "Date": ["2020-01-01"], "Parameter1": ["invalid"]}
        )
        await use_case.execute(dataset_id, non_numeric_data)
