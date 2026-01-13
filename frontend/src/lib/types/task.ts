/**
 * Task type categories with associated colors
 */
export type TaskType = 'research' | 'dev' | 'notes' | 'neutral';

/**
 * Task status for Kanban columns
 */
export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE';

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
	IN_PROGRESS: 'In Progress',
	DONE: 'Done',
};
