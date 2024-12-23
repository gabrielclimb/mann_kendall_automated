from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Project:
    """Entidade Project do domínio"""

    name: str
    description: Optional[str]
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    id: UUID = uuid4()

    def update_description(self, new_description: str) -> None:
        """Atualiza a descrição do projeto"""
        self.description = new_description
        self.updated_at = datetime.utcnow()

    @classmethod
    def create(cls, name: str, description: str, owner_id: UUID) -> "Project":
        """Factory method para criar um novo projeto"""
        now = datetime.utcnow()
        return cls(
            name=name,
            description=description,
            owner_id=owner_id,
            created_at=now,
            updated_at=now,
        )
