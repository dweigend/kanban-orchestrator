"""Project CRUD API endpoints."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import project_service
from src.api.schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from src.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Create a new project."""
    project = await project_service.create_project(db, project_data)
    return ProjectResponse.model_validate(project)


@router.get("", response_model=list[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)) -> list[ProjectResponse]:
    """Get all projects."""
    projects = await project_service.get_all_projects(db)
    return [ProjectResponse.model_validate(p) for p in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Get a single project by ID."""
    project = await project_service.get_project(db, project_id)
    if not project:
        logger.warning("Project not found: %s", project_id)
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse.model_validate(project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Update an existing project."""
    project = await project_service.update_project(db, project_id, project_data)
    if not project:
        logger.warning("Project not found for update: %s", project_id)
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a project."""
    deleted = await project_service.delete_project(db, project_id)
    if not deleted:
        logger.warning("Project not found for deletion: %s", project_id)
        raise HTTPException(status_code=404, detail="Project not found")
