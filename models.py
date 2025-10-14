from pydantic import BaseModel
from typing import Optional

class Server(BaseModel):
    id: int
    name: str
    owner: str
    description: Optional[str] = None
    files: list[str] = []

class Project(BaseModel):
    id: int
    name: str
    files: list[str] = []
    server_id: int
