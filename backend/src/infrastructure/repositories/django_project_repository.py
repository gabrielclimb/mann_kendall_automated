from typing import List, Optional
from uuid import UUID

from src.domain.entities.project import Project
from src.domain.ports.project_repository import ProjectRepository
from src.infrastructure.django.models import ProjectModel


class DjangoProjectRepository(ProjectRepository):
    async def save(self, project: Project) -> Project:
        project_model = await ProjectModel.objects.aupdate_or_create(
            id=project.id,
            defaults={
                "name": project.name,
                "description": project.description,
                "owner_id": project.owner_id,
            },
        )
        return self._to_entity(project_model[0])

    async def get_by_id(self, project_id: UUID) -> Optional[Project]:
        try:
            project_model = await ProjectModel.objects.aget(id=project_id)
            return self._to_entity(project_model)
        except ProjectModel.DoesNotExist:
            return None

    async def list_by_owner(self, owner_id: UUID) -> List[Project]:
        project_models = await ProjectModel.objects.filter(owner_id=owner_id)
        return [self._to_entity(pm) for pm in project_models]

    async def delete(self, project_id: UUID) -> None:
        await ProjectModel.objects.filter(id=project_id).adelete()

    async def update(self, project: Project) -> Project:
        project_model = await ProjectModel.objects.aget(id=project.id)
        project_model.name = project.name
        project_model.description = project.description
        await project_model.asave()
        return self._to_entity(project_model)

    def _to_entity(self, model: ProjectModel) -> Project:
        return Project(
            id=model.id,
            name=model.name,
            description=model.description,
            owner_id=model.owner.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
