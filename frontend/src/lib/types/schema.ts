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

/** Enum response from /api/schema/enums */
export interface SchemaEnums {
	task_status: string[];
	task_type: string[];
	agent_run_status: string[];
}
