"""Project CRUD operations with async SQLAlchemy.

This module provides database operations for projects.
Projects serve as workspaces that group related tasks together.

Functions:
    create_project: Create new project
    get_project: Retrieve single project by ID
    get_all_projects: List all projects
    update_project: Update project fields
    delete_project: Remove project (cascades to associated tasks)
"""

from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ProjectCreate, ProjectUpdate
from src.models.project import Project


async def create_project(db: AsyncSession, project_data: ProjectCreate) -> Project:
    """Create a new project."""
    project = Project(
        id=str(uuid4()),
        name=project_data.name,
        workspace_path=project_data.workspace_path,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def get_project(db: AsyncSession, project_id: str) -> Project | None:
    """Get a single project by ID."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()


async def get_all_projects(db: AsyncSession) -> list[Project]:
    """Get all projects ordered by creation date."""
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    return list(result.scalars().all())


async def update_project(
    db: AsyncSession,
    project_id: str,
    project_data: ProjectUpdate,
) -> Project | None:
    """Update an existing project. Returns None if not found."""
    project = await get_project(db, project_id)
    if not project:
        return None

    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: str) -> bool:
    """Delete a project by ID.

    Uses SQLAlchemy 2.0 delete statement pattern.
    Note: Associated tasks are cascade-deleted via FK relationship.

    Returns:
        True if deleted, False if project not found.
    """
    project = await get_project(db, project_id)
    if not project:
        return False

    # Delete using statement (SQLAlchemy 2.0 pattern)
    await db.execute(delete(Project).where(Project.id == project_id))
    await db.commit()
    return True
