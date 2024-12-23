from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.project import Project


class ProjectRepository(ABC):
    """Interface para repositório de projetos"""

    @abstractmethod
    async def save(self, project: Project) -> Project:
        """Salva um projeto no repositório"""
        pass

    @abstractmethod
    async def get_by_id(self, project_id: UUID) -> Optional[Project]:
        """Recupera um projeto pelo ID"""
        pass

    @abstractmethod
    async def list_by_owner(self, owner_id: UUID) -> List[Project]:
        """Lista todos os projetos de um proprietário"""
        pass

    @abstractmethod
    async def delete(self, project_id: UUID) -> None:
        """Remove um projeto do repositório"""
        pass

    @abstractmethod
    async def update(self, project: Project) -> Project:
        """Atualiza um projeto existente"""
        pass
