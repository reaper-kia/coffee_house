from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AuthUserReadModel:
    id: UUID
    email: str
    password_hash: str