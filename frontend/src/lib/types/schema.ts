/**
 * Schema types for dynamic form rendering.
 * Matches backend: backend/src/api/schemas.py
 */

/** Field types matching backend FieldType enum */
export type FieldType =
	| 'text'
	| 'textarea'
	| 'select'
	| 'readonly'
	| 'datetime';

/** Schema field definition from backend */
export interface SchemaField {
	name: string;
	type: FieldType;
	required: boolean;
	description: string;
	options?: string[];
}

/** Entity schema response */
export interface EntitySchema {
	fields: SchemaField[];
}

// ─────────────────────────────────────────────────────────────
// Enum Option Types (for schema-driven UI)
// ─────────────────────────────────────────────────────────────

/** Base enum option with value and label */
export interface EnumOption {
	value: string;
	label: string;
}

/** Task status option with description for tooltips */
export interface TaskStatusOption extends EnumOption {
	description: string;
}

/** Task type option with icon and prefix for UI rendering */
export interface TaskTypeOption extends EnumOption {
	icon: string;
	prefix: string;
}

/** Agent run status option */
export interface AgentRunStatusOption extends EnumOption {}

/** Enum response from /api/schema/enums (new format with metadata) */
export interface EnumsResponse {
	task_status: TaskStatusOption[];
	task_type: TaskTypeOption[];
	agent_run_status: AgentRunStatusOption[];
}

/**
 * @deprecated Use EnumsResponse instead
 * Legacy enum response (flat string arrays)
 */
export interface SchemaEnums {
	task_status: string[];
	task_type: string[];
	agent_run_status: string[];
}
