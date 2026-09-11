from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project, Technology
from app.schemas import TechnologyCreate, TechnologyOut, TechnologyUpdate

router = APIRouter(prefix="/projects", tags=["technologies"])

PROJECT_NOT_FOUND = "Project not found"
TECH_NOT_FOUND = "Technology not found"


@router.post(
    "/{project_id}/technologies",
    response_model=TechnologyOut,
    status_code=status.HTTP_201_CREATED,
)
def create_technology(
    project_id: int, payload: TechnologyCreate, db: Session = Depends(get_db)
) -> Technology:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND)
    technology = Technology(project_id=project_id, name=payload.name)
    db.add(technology)
    db.commit()
    db.refresh(technology)
    return technology


@router.patch("/{project_id}/technologies/{technology_id}", response_model=TechnologyOut)
def update_technology(
    project_id: int,
    technology_id: int,
    payload: TechnologyUpdate,
    db: Session = Depends(get_db),
) -> Technology:
    technology = db.scalar(
        select(Technology).where(
            Technology.id == technology_id, Technology.project_id == project_id
        )
    )
    if technology is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TECH_NOT_FOUND)
    technology.name = payload.name
    db.commit()
    db.refresh(technology)
    return technology


@router.delete("/{project_id}/technologies/{technology_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technology(
    project_id: int, technology_id: int, db: Session = Depends(get_db)
) -> None:
    technology = db.scalar(
        select(Technology).where(
            Technology.id == technology_id, Technology.project_id == project_id
        )
    )
    if technology is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TECH_NOT_FOUND)
    db.delete(technology)
    db.commit()