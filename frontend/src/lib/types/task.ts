/**
 * Task type definitions and mapping utilities.
 *
 * This module defines:
 * - TaskType: Visual category (research/dev/notes/neutral)
 * - TaskStatus: Kanban column state (TODO/IN_PROGRESS/NEEDS_REVIEW/DONE)
 * - Task: Full task interface matching backend schema
 * - Mapping functions for backend ↔ frontend conversion
 *
 * IMPORTANT: Keep in sync with backend:
 * - Pydantic schemas: backend/src/api/schemas.py
 * - SQLAlchemy models: backend/src/models/task.py
 */

// ─────────────────────────────────────────────────────────────
// Type Definitions
// ─────────────────────────────────────────────────────────────

/**
 * A single step within a subtask (checkbox item).
 * Used for granular progress tracking.
 */
export interface Step {
	text: string;
	done: boolean;
}

/**
 * Task type categories with associated colors.
 * Matches backend TaskType enum (lowercase).
 */
export type TaskType = 'research' | 'dev' | 'notes' | 'neutral';

/**
 * Task status for Kanban columns.
 * Frontend uses UPPERCASE for display constants.
 */
export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'NEEDS_REVIEW' | 'DONE';

/**
 * Backend status format (lowercase, matches Python StrEnum).
 */
export type BackendTaskStatus =
	| 'todo'
	| 'in_progress'
	| 'needs_review'
	| 'done';

// ─────────────────────────────────────────────────────────────
// Status Mapping
// ─────────────────────────────────────────────────────────────

/**
 * Map frontend status to backend format.
 */
export const STATUS_TO_BACKEND: Record<TaskStatus, BackendTaskStatus> = {
	TODO: 'todo',
	IN_PROGRESS: 'in_progress',
	NEEDS_REVIEW: 'needs_review',
	DONE: 'done',
};

/**
 * Map backend status to frontend format.
 */
export const STATUS_FROM_BACKEND: Record<BackendTaskStatus, TaskStatus> = {
	todo: 'TODO',
	in_progress: 'IN_PROGRESS',
	needs_review: 'NEEDS_REVIEW',
	done: 'DONE',
};

// ─────────────────────────────────────────────────────────────
// Task Interfaces
// ─────────────────────────────────────────────────────────────

/**
 * Full task model used in frontend components.
 * Status uses UPPERCASE for display.
 */
export interface Task {
	id: string;
	title: string;
	description?: string;
	result?: string; // Agent result (temporary until Schema-Driven UI)
	status: TaskStatus;
	type: TaskType;
	project_id?: string;
	parent_id?: string;
	steps?: Step[]; // Granular steps for subtasks
	created_at: string;
}

/**
 * Task as returned by backend API.
 * Status uses lowercase (Python enum format).
 */
export interface BackendTask {
	id: string;
	title: string;
	description: string | null;
	result: string | null; // Agent result
	status: BackendTaskStatus;
	type: TaskType; // Backend now stores type
	project_id: string | null;
	parent_id: string | null;
	steps: Step[] | null; // Granular steps for subtasks
	created_at: string;
}

/**
 * Payload for creating a new task.
 */
export interface TaskCreate {
	title: string;
	description?: string;
	type?: TaskType;
	status?: BackendTaskStatus;
}

/**
 * Payload for updating an existing task.
 */
export interface TaskUpdate {
	title?: string;
	description?: string;
	status?: BackendTaskStatus;
	type?: TaskType;
}

// ─────────────────────────────────────────────────────────────
// Display Constants
// ─────────────────────────────────────────────────────────────

/**
 * Color mapping for task types (CSS custom properties).
 */
export const TASK_TYPE_COLORS: Record<TaskType, string> = {
	research: 'var(--task-research)',
	dev: 'var(--task-dev)',
	notes: 'var(--task-notes)',
	neutral: 'var(--task-neutral)',
};

// ─────────────────────────────────────────────────────────────
// Mapping Functions
// ─────────────────────────────────────────────────────────────

/**
 * Convert backend task to frontend format.
 * Transforms status from lowercase to UPPERCASE.
 */
export function mapBackendToTask(backend: BackendTask): Task {
	return {
		id: backend.id,
		title: backend.title,
		description: backend.description ?? undefined,
		result: backend.result ?? undefined,
		status: STATUS_FROM_BACKEND[backend.status],
		type: backend.type, // Now persisted in backend
		project_id: backend.project_id ?? undefined,
		parent_id: backend.parent_id ?? undefined,
		steps: backend.steps ?? undefined,
		created_at: backend.created_at,
	};
}

/**
 * Convert frontend task to create payload.
 */
export function mapTaskToCreatePayload(task: Partial<Task>): TaskCreate {
	return {
		title: task.title ?? '',
		description: task.description,
		type: task.type,
		status: task.status ? STATUS_TO_BACKEND[task.status] : undefined,
	};
}

/**
 * Convert frontend task to update payload.
 */
export function mapTaskToUpdatePayload(task: Partial<Task>): TaskUpdate {
	const payload: TaskUpdate = {};
	if (task.title !== undefined) payload.title = task.title;
	if (task.description !== undefined) payload.description = task.description;
	if (task.status !== undefined)
		payload.status = STATUS_TO_BACKEND[task.status];
	if (task.type !== undefined) payload.type = task.type;
	return payload;
}
