/**
 * Schema API service with memory caching.
 * Fetches field definitions for dynamic form rendering.
 */

import type { EntitySchema, EnumsResponse } from '$lib/types/schema';
import { request } from './api';

// Memory cache for schemas (avoids repeated fetches)
let taskSchemaCache: EntitySchema | null = null;
let projectSchemaCache: EntitySchema | null = null;
let enumsCache: EnumsResponse | null = null;

/** Fetch task schema (cached) */
export async function fetchTaskSchema(): Promise<EntitySchema> {
	if (taskSchemaCache) return taskSchemaCache;
	taskSchemaCache = await request<EntitySchema>('/api/schema/task');
	return taskSchemaCache;
}

/** Fetch project schema (cached) */
export async function fetchProjectSchema(): Promise<EntitySchema> {
	if (projectSchemaCache) return projectSchemaCache;
	projectSchemaCache = await request<EntitySchema>('/api/schema/project');
	return projectSchemaCache;
}

/** Fetch all enums with metadata (cached) */
export async function fetchEnums(): Promise<EnumsResponse> {
	if (enumsCache) return enumsCache;
	enumsCache = await request<EnumsResponse>('/api/schema/enums');
	return enumsCache;
}

/** Clear all caches (for testing/hot-reload) */
export function clearSchemaCache(): void {
	taskSchemaCache = null;
	projectSchemaCache = null;
	enumsCache = null;
}

// ─────────────────────────────────────────────────────────────
// Enum Lookup Helpers
// ─────────────────────────────────────────────────────────────

/** Get label for a task status value */
export function getTaskStatusLabel(
	enums: EnumsResponse,
	value: string,
): string {
	const option = enums.task_status.find((o) => o.value === value);
	return option?.label ?? value;
}

/** Get label for a task type value */
export function getTaskTypeLabel(enums: EnumsResponse, value: string): string {
	const option = enums.task_type.find((o) => o.value === value);
	return option?.label ?? value;
}

/** Get icon name for a task type value */
export function getTaskTypeIcon(
	enums: EnumsResponse,
	value: string,
): string | undefined {
	const option = enums.task_type.find((o) => o.value === value);
	return option?.icon;
}

/** Get prefix for a task type value (e.g., "RES" for research) */
export function getTaskTypePrefix(
	enums: EnumsResponse,
	value: string,
): string | undefined {
	const option = enums.task_type.find((o) => o.value === value);
	return option?.prefix;
}

/** Get label for an agent run status value */
export function getAgentRunStatusLabel(
	enums: EnumsResponse,
	value: string,
): string {
	const option = enums.agent_run_status.find((o) => o.value === value);
	return option?.label ?? value;
}
