/**
 * Task type categories with associated colors
 */
export type TaskType = 'research' | 'dev' | 'notes' | 'neutral';

/**
 * Task status for Kanban columns (frontend uses uppercase)
 */
export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'NEEDS_REVIEW' | 'DONE';

/**
 * Backend status format (lowercase)
 */
export type BackendTaskStatus =
	| 'todo'
	| 'in_progress'
	| 'needs_review'
	| 'done';

/**
 * Map frontend status to backend format
 */
export const STATUS_TO_BACKEND: Record<TaskStatus, BackendTaskStatus> = {
	TODO: 'todo',
	IN_PROGRESS: 'in_progress',
	NEEDS_REVIEW: 'needs_review',
	DONE: 'done',
};

/**
 * Map backend status to frontend format
 */
export const STATUS_FROM_BACKEND: Record<BackendTaskStatus, TaskStatus> = {
	todo: 'TODO',
	in_progress: 'IN_PROGRESS',
	needs_review: 'NEEDS_REVIEW',
	done: 'DONE',
};

/**
 * Task model matching backend schema
 */
export interface Task {
	id: string;
	title: string;
	description?: string;
	status: TaskStatus;
	type: TaskType;
	created_at: string;
	updated_at?: string;
}

/**
 * Payload for creating a new task
 */
export interface TaskCreate {
	title: string;
	description?: string;
	type?: TaskType;
}

/**
 * Payload for updating an existing task
 */
export interface TaskUpdate {
	title?: string;
	description?: string;
	status?: TaskStatus;
	type?: TaskType;
}

/**
 * Color mapping for task types
 */
export const TASK_TYPE_COLORS: Record<TaskType, string> = {
	research: 'var(--task-research)',
	dev: 'var(--task-dev)',
	notes: 'var(--task-notes)',
	neutral: 'var(--task-neutral)',
};

/**
 * Labels for task types
 */
export const TASK_TYPE_LABELS: Record<TaskType, string> = {
	research: 'Research',
	dev: 'Development',
	notes: 'Notes',
	neutral: 'General',
};

/**
 * Labels for task status columns
 */
export const TASK_STATUS_LABELS: Record<TaskStatus, string> = {
	TODO: 'To Do',
	IN_PROGRESS: 'Running',
	NEEDS_REVIEW: 'Review',
	DONE: 'Done',
};

// ─────────────────────────────────────────────────────────────
// Backend API Types
// ─────────────────────────────────────────────────────────────

/**
 * Task as returned by backend API
 */
export interface BackendTask {
	id: string;
	title: string;
	status: BackendTaskStatus;
	created_at: string;
}

/**
 * Payload for creating a task via API
 */
export interface TaskCreatePayload {
	title: string;
	status?: BackendTaskStatus;
}

/**
 * Payload for updating a task via API
 */
export interface TaskUpdatePayload {
	title?: string;
	status?: BackendTaskStatus;
}

// ─────────────────────────────────────────────────────────────
// Mapping Functions
// ─────────────────────────────────────────────────────────────

/**
 * Convert backend task to frontend format
 */
export function mapBackendToTask(backend: BackendTask): Task {
	return {
		id: backend.id,
		title: backend.title,
		status: STATUS_FROM_BACKEND[backend.status],
		type: 'neutral', // Default for backend tasks (not stored in backend)
		created_at: backend.created_at,
	};
}

/**
 * Convert frontend task to create payload
 */
export function mapTaskToCreatePayload(task: Partial<Task>): TaskCreatePayload {
	return {
		title: task.title ?? '',
		status: task.status ? STATUS_TO_BACKEND[task.status] : undefined,
	};
}

/**
 * Convert frontend task to update payload
 */
export function mapTaskToUpdatePayload(task: Partial<Task>): TaskUpdatePayload {
	const payload: TaskUpdatePayload = {};
	if (task.title !== undefined) payload.title = task.title;
	if (task.status !== undefined)
		payload.status = STATUS_TO_BACKEND[task.status];
	return payload;
}
