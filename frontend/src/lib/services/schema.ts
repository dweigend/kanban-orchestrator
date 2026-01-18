/**
 * Schema API service with memory caching.
 * Fetches field definitions for dynamic form rendering.
 */

import type { EntitySchema, SchemaEnums } from '$lib/types/schema';
import { request } from './api';

// Memory cache for schemas (avoids repeated fetches)
let taskSchemaCache: EntitySchema | null = null;
let projectSchemaCache: EntitySchema | null = null;
let enumsCache: SchemaEnums | null = null;

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

/** Fetch all enums (cached) */
export async function fetchEnums(): Promise<SchemaEnums> {
	if (enumsCache) return enumsCache;
	enumsCache = await request<SchemaEnums>('/api/schema/enums');
	return enumsCache;
}

/** Clear all caches (for testing/hot-reload) */
export function clearSchemaCache(): void {
	taskSchemaCache = null;
	projectSchemaCache = null;
	enumsCache = null;
}
