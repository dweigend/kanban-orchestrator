/**
 * Schema store for enum metadata.
 * Loads once on app init and provides reactive access.
 */

import { fetchEnums } from '$lib/services/schema';
import type { EnumsResponse } from '$lib/types/schema';

// Reactive state
let enums = $state<EnumsResponse | null>(null);
let loading = $state(false);
let error = $state<string | null>(null);

/** Initialize schema store (call once on app startup) */
export async function initSchemaStore(): Promise<void> {
	if (enums || loading) return;

	loading = true;
	error = null;

	try {
		enums = await fetchEnums();
	} catch (e) {
		error = e instanceof Error ? e.message : 'Failed to load schema';
		console.error('Schema store init failed:', e);
	} finally {
		loading = false;
	}
}

/** Get current enums (null if not loaded) */
export function getEnums(): EnumsResponse | null {
	return enums;
}

/** Check if schema is loading */
export function isLoading(): boolean {
	return loading;
}

/** Get error message if any */
export function getError(): string | null {
	return error;
}

// ─────────────────────────────────────────────────────────────
// Convenience getters with fallbacks
// ─────────────────────────────────────────────────────────────

/** Get task status label with fallback */
export function getStatusLabel(value: string): string {
	const option = enums?.task_status.find((o) => o.value === value);
	return option?.label ?? value;
}

/** Get task type label with fallback */
export function getTypeLabel(value: string): string {
	const option = enums?.task_type.find((o) => o.value === value);
	return option?.label ?? value;
}

/** Get task type icon name */
export function getTypeIcon(value: string): string | undefined {
	const option = enums?.task_type.find((o) => o.value === value);
	return option?.icon;
}

/** Get task type prefix for short IDs */
export function getTypePrefix(value: string): string {
	const option = enums?.task_type.find((o) => o.value === value);
	return option?.prefix ?? value.toUpperCase().slice(0, 3);
}

/** Get agent run status label */
export function getAgentStatusLabel(value: string): string {
	const option = enums?.agent_run_status.find((o) => o.value === value);
	return option?.label ?? value;
}

/** Get all task status values (for column rendering) */
export function getTaskStatuses(): string[] {
	return enums?.task_status.map((o) => o.value) ?? [];
}

/** Check if schema is ready (loaded and not loading) */
export function isSchemaReady(): boolean {
	return enums !== null && !loading;
}
