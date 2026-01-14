/**
 * Task API service - CRUD operations
 */

import type { BackendTask, Task } from '$lib/types/task';
import {
	mapBackendToTask,
	mapTaskToCreatePayload,
	mapTaskToUpdatePayload,
} from '$lib/types/task';
import { request } from './api';

/**
 * Fetch all tasks from backend
 */
export async function fetchTasks(): Promise<Task[]> {
	const backendTasks = await request<BackendTask[]>('/api/tasks');
	return backendTasks.map(mapBackendToTask);
}

/**
 * Fetch a single task by ID
 */
export async function fetchTask(id: string): Promise<Task> {
	const backendTask = await request<BackendTask>(`/api/tasks/${id}`);
	return mapBackendToTask(backendTask);
}

/**
 * Create a new task
 */
export async function createTask(task: Partial<Task>): Promise<Task> {
	const payload = mapTaskToCreatePayload(task);
	const backendTask = await request<BackendTask>('/api/tasks', {
		method: 'POST',
		body: JSON.stringify(payload),
	});
	return mapBackendToTask(backendTask);
}

/**
 * Update an existing task
 */
export async function updateTask(
	id: string,
	task: Partial<Task>,
): Promise<Task> {
	const payload = mapTaskToUpdatePayload(task);
	const backendTask = await request<BackendTask>(`/api/tasks/${id}`, {
		method: 'PUT',
		body: JSON.stringify(payload),
	});
	return mapBackendToTask(backendTask);
}

/**
 * Delete a task
 */
export async function deleteTask(id: string): Promise<void> {
	await request<void>(`/api/tasks/${id}`, { method: 'DELETE' });
}
