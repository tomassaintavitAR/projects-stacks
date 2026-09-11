from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class ProjectUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime


class TechnologyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class TechnologyUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class TechnologyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    created_at: datetime


class ProjectDetail(ProjectOut):
    technologies: list[TechnologyOut] = []