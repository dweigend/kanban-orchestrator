<script lang="ts">
import { Separator } from 'bits-ui';
import FloppyDisk from 'phosphor-svelte/lib/FloppyDisk';
import Trash from 'phosphor-svelte/lib/Trash';
import { FieldRenderer } from '$lib/components/form';
import { fetchTaskSchema } from '$lib/services/schema';
import type { EntitySchema, SchemaField } from '$lib/types/schema';
import type { Task, TaskStatus, TaskType } from '$lib/types/task';
import {
	STATUS_FROM_BACKEND,
	STATUS_TO_BACKEND,
	TASK_STATUS_LABELS,
	TASK_TYPE_LABELS,
} from '$lib/types/task';

interface Props {
	task?: Task | null;
	onSave?: (task: Task) => void;
	onDelete?: (taskId: string) => void;
}

const { task = null, onSave, onDelete }: Props = $props();

// Schema state
let schema = $state<EntitySchema | null>(null);
let schemaLoading = $state(true);

// Load schema on mount
$effect(() => {
	fetchTaskSchema()
		.then((s) => {
			schema = s;
		})
		.finally(() => {
			schemaLoading = false;
		});
});

// Default empty task for new tasks
const defaultTask: Task = {
	id: '',
	title: '',
	description: '',
	status: 'TODO',
	type: 'neutral',
	created_at: new Date().toISOString(),
};

// Use provided task or default
const currentTask = $derived(task ?? defaultTask);

// Form state as record (schema-driven)
let formData = $state<Record<string, string>>({});
let errors = $state<Record<string, string>>({});

// Reset form when task prop changes
$effect(() => {
	formData = {
		title: currentTask.title,
		description: currentTask.description ?? '',
		// Convert status to lowercase for form (matches backend schema options)
		status: STATUS_TO_BACKEND[currentTask.status],
		type: currentTask.type,
		result: currentTask.result ?? '',
		created_at: currentTask.created_at,
	};
	errors = {};
});

const isNewTask = $derived(!currentTask.id || currentTask.id === '');

// Label mappings for select fields (lowercase keys match backend schema)
const selectLabels: Record<string, Record<string, string>> = {
	status: Object.fromEntries(
		Object.entries(TASK_STATUS_LABELS).map(([k, v]) => [
			STATUS_TO_BACKEND[k as TaskStatus],
			v,
		]),
	),
	type: TASK_TYPE_LABELS,
};

// Filter fields for display based on schema
const editableFields = $derived(
	schema?.fields.filter(
		(f) =>
			// Show editable fields (text, textarea, select)
			f.type !== 'readonly' &&
			f.type !== 'datetime' &&
			// Hide status for new tasks
			(f.name !== 'status' || !isNewTask),
	) ?? [],
);

function handleFieldChange(name: string, value: string) {
	formData = { ...formData, [name]: value };
	// Clear error on change
	if (errors[name]) {
		const { [name]: _, ...rest } = errors;
		errors = rest;
	}
}

function validateForm(): boolean {
	errors = {};

	// Validate required fields from schema
	for (const field of schema?.fields ?? []) {
		if (field.required && !formData[field.name]?.trim()) {
			errors = { ...errors, [field.name]: `${field.name} is required` };
		}
	}

	// Title length validation
	if (formData.title && formData.title.length > 100) {
		errors = { ...errors, title: 'Title must be 100 characters or less' };
	}

	return Object.keys(errors).length === 0;
}

function handleSave() {
	if (!validateForm()) return;

	const updatedTask: Task = {
		...currentTask,
		title: formData.title.trim(),
		description: formData.description?.trim() || undefined,
		// Convert status back to UPPERCASE for frontend Task type
		status:
			STATUS_FROM_BACKEND[formData.status as keyof typeof STATUS_FROM_BACKEND],
		type: formData.type as TaskType,
	};
	onSave?.(updatedTask);
}

function handleDelete() {
	if (currentTask.id) {
		onDelete?.(currentTask.id);
	}
}

// Get field by name helper
function getField(name: string): SchemaField | undefined {
	return schema?.fields.find((f) => f.name === name);
}
</script>

<div class="p-4 flex flex-col h-full">
	<!-- Header -->
	<div class="flex items-center justify-between mb-4">
		<h2 class="text-sm font-semibold text-uppercase-tracking">
			{isNewTask ? 'New Task' : 'Edit Task'}
		</h2>
		{#if !isNewTask}
			<button
				type="button"
				onclick={handleDelete}
				class="p-1.5 rounded hover:bg-red-500/20 text-[var(--text-muted)] hover:text-red-400 transition-colors"
				title="Delete task"
			>
				<Trash class="size-4" />
			</button>
		{/if}
	</div>

	<!-- Form -->
	{#if schemaLoading}
		<div class="flex-1 flex items-center justify-center text-[var(--text-muted)]">
			Loading...
		</div>
	{:else if schema}
		<div class="flex-1 space-y-4 overflow-y-auto">
			<!-- Dynamic editable fields -->
			{#each editableFields as field (field.name)}
				<FieldRenderer
					{field}
					value={formData[field.name]}
					error={errors[field.name]}
					displayLabels={selectLabels[field.name]}
					onchange={(v) => handleFieldChange(field.name, v)}
				/>
			{/each}

			<!-- Result (readonly, only if exists) -->
			{#if currentTask.result}
				{@const resultField = getField('result')}
				{#if resultField}
					<Separator.Root class="h-px bg-[var(--border-muted)]" />
					<FieldRenderer field={resultField} value={currentTask.result} />
				{/if}
			{/if}
		</div>
	{/if}

	<!-- Save Button -->
	<div class="pt-4 border-t border-[var(--border-muted)] mt-4">
		<button
			type="button"
			onclick={handleSave}
			disabled={schemaLoading}
			class="flex items-center justify-center gap-2 w-full px-4 py-2.5 text-sm font-medium
				bg-[var(--accent-primary)] text-[var(--text-inverse)] rounded
				hover:bg-[var(--accent-hover)] transition-colors disabled:opacity-50"
		>
			<FloppyDisk class="size-4" />
			{isNewTask ? 'CREATE TASK' : 'SAVE CHANGES'}
		</button>
	</div>
</div>
