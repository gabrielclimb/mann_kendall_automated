# tests/infrastructure/repositories/test_django_analysis_repository.py
from datetime import datetime
from uuid import uuid4

import pytest
from django.contrib.auth.models import User
from src.domain.entities.analysis_result import AnalysisResult
from src.infrastructure.django.models import DatasetModel, ProjectModel
from src.infrastructure.repositories.django_analysis_repository import (
    DjangoAnalysisRepository,
)


@pytest.mark.django_db
class TestDjangoAnalysisRepository:
    @pytest.fixture(autouse=True)
    async def test_setup(self, request):
        """Setup test database and required objects"""
        self.repository = DjangoAnalysisRepository()

        # Create test user with unique username
        username = f"testuser_{uuid4().hex[:8]}"
        self.user = await User.objects.acreate(
            username=username, email=f"{username}@example.com", password="testpass123"
        )

        # Create test project
        self.project = await ProjectModel.objects.acreate(
            name="Test Project", owner=self.user
        )

        # Create test dataset
        self.dataset = await DatasetModel.objects.acreate(
            project=self.project, name="Test Dataset"
        )

        yield

        # Cleanup
        await self.dataset.adelete()
        await self.project.adelete()
        await self.user.adelete()

    def create_test_result(self):
        """Helper method to create a test result"""
        return AnalysisResult(
            id=uuid4(),
            dataset_id=self.dataset.id,
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

    @pytest.mark.asyncio
    async def test_save_and_retrieve_result(self):
        """Test saving and retrieving an analysis result"""
        # Create test result
        result = self.create_test_result()

        # Save result
        saved_result = await self.repository.save(result)

        # Retrieve saved result
        retrieved_result = await self.repository.get_by_id(saved_result.id)

        # Verify result
        assert retrieved_result is not None
        assert retrieved_result.well_name == result.well_name
        assert retrieved_result.trend == result.trend
        assert retrieved_result.statistic == result.statistic
        assert retrieved_result.dataset_id == self.dataset.id

    @pytest.mark.asyncio
    async def test_list_by_dataset(self):
        """Test listing results by dataset"""
        # Create multiple results with same dataset_id
        for i in range(3):
            result = AnalysisResult(
                id=uuid4(),
                dataset_id=self.dataset.id,
                well_name=f"TestWell{i}",
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
            await self.repository.save(result)

        # List results
        retrieved_results = await self.repository.list_by_dataset(self.dataset.id)

        # Verify results
        assert len(retrieved_results) == 3
        assert all(r.dataset_id == self.dataset.id for r in retrieved_results)
        assert (
            len({r.well_name for r in retrieved_results}) == 3
        )  # All well names are unique
