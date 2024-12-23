from datetime import datetime
from typing import List
from uuid import UUID, uuid4

import numpy as np
import pandas as pd
from scipy.stats import norm

from src.domain.entities.analysis_result import AnalysisResult
from src.domain.ports.analysis_repository import AnalysisRepository


class PerformMannKendallAnalysis:
    """Use case for performing Mann-Kendall trend analysis"""

    def __init__(self, analysis_repository: AnalysisRepository):
        self.analysis_repository = analysis_repository

    def _transpose_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transposes the given DataFrame, replaces "ND" with 0.5, and renames columns.
        Uses position-based column naming.

        Args:
            data: DataFrame with wells as columns and dates as first row

        Returns:
            pd.DataFrame: Transposed DataFrame with modified columns.
        """
        df = data.replace("ND", 0.5)
        df_transposto = df.T
        # Use positions to rename columns, not names
        df_transposto.columns.values[0] = "well"
        df_transposto.columns.values[1] = "Date"
        return df_transposto

    async def execute(
        self, dataset_id: UUID, data: pd.DataFrame
    ) -> List[AnalysisResult]:
        """Execute Mann-Kendall analysis on the provided dataset"""
        try:
            # Transform the data using original position-based method
            df_transformed = self._transpose_dataframe(data)

            # Get wells with sufficient data points (>4)
            wells = pd.DataFrame(df_transformed.well.value_counts() > 4).reset_index()
            wells.columns = ["index", "well"]
            wells = wells[wells.well].iloc[:, 0]

            # Parameters to analyze (all columns except well and date)
            parameters = df_transformed.columns[2:]

            results = []

            # Perform analysis for each well and parameter
            for well in wells:
                df_well = df_transformed[df_transformed.well == well]

                for param in parameters:
                    try:
                        if df_well.loc[:, param].dropna().count() > 3:
                            values = df_well.loc[:, param].dropna().values

                            trend, s, cv, cf = self._mann_kendall_test(values)

                            result = AnalysisResult(
                                id=uuid4(),
                                dataset_id=dataset_id,
                                well_name=well,
                                parameter=param,
                                trend=trend,
                                statistic=s,
                                coefficient_variation=cv,
                                confidence_factor=cf,
                                analysis_date=datetime.utcnow(),
                                data_points=len(values),
                                minimum_value=float(np.min(values)),
                                maximum_value=float(np.max(values)),
                                mean_value=float(np.mean(values)),
                            )

                            await self.analysis_repository.save(result)
                            results.append(result)
                    except TypeError:
                        continue

            return results

        except Exception as e:
            raise ValueError(f"Error performing Mann-Kendall analysis: {str(e)}")

    def _mann_kendall_test(self, x: np.ndarray, alpha: float = 0.05) -> tuple:
        """
        Perform Mann-Kendall trend test.
        This is the same as your original implementation.
        """
        n = len(x)

        # Calculate S
        s = 0
        for k in range(n - 1):
            for j in range(k + 1, n):
                s += np.sign(x[j] - x[k])

        # Calculate variance
        unique_x = np.unique(x)
        g = len(unique_x)

        if n == g:  # No ties
            var_s = (n * (n - 1) * (2 * n + 5)) / 18
        else:  # Handle ties
            tp = np.zeros(unique_x.shape)
            for i, val in enumerate(unique_x):
                tp[i] = sum(x == val)
            var_s = (
                n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))
            ) / 18

        # Calculate Z
        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
        else:
            z = 0

        # Calculate coefficient of variation and confidence factor
        cv = np.std(x, ddof=1) / np.mean(x)
        p = 1 - norm.cdf(abs(z))
        cf = 1 - p

        # Determine trend
        if cf < 0.9:
            trend = "Stable" if s <= 0 and cv < 1 else "No Trend"
        else:
            if cf <= 0.95:
                trend = "Prob. Increasing" if s > 0 else "Prob. Decreasing"
            else:
                trend = "Increasing" if s > 0 else "Decreasing"

        return trend, round(s, 4), round(cv, 2), round(cf, 3)
