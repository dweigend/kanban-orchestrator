<script lang="ts">
import { Separator } from 'bits-ui';
import CheckSquare from 'phosphor-svelte/lib/CheckSquare';
import FloppyDisk from 'phosphor-svelte/lib/FloppyDisk';
import FolderOpen from 'phosphor-svelte/lib/FolderOpen';
import Play from 'phosphor-svelte/lib/Play';
import Square from 'phosphor-svelte/lib/Square';
import Trash from 'phosphor-svelte/lib/Trash';
import { FieldRenderer } from '$lib/components/form';
import { fetchTaskSchema } from '$lib/services/schema';
import { getEnums } from '$lib/stores/schema.svelte';
import type { EntitySchema, SchemaField } from '$lib/types/schema';
import type { Step, Task, TaskType } from '$lib/types/task';
import { STATUS_FROM_BACKEND, STATUS_TO_BACKEND } from '$lib/types/task';

interface Props {
	task?: Task | null;
	subtasks?: Task[];
	onSave?: (task: Task) => void;
	onDelete?: (taskId: string) => void;
	onStepToggle?: (taskId: string, stepIndex: number, done: boolean) => void;
	onExecute?: (taskId: string) => void;
}

const {
	task = null,
	subtasks = [],
	onSave,
	onDelete,
	onStepToggle,
	onExecute,
}: Props = $props();

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
const isNeedsReview = $derived(currentTask.status === 'NEEDS_REVIEW');
const hasSubtasks = $derived(subtasks.length > 0);
const hasSteps = $derived(currentTask.steps && currentTask.steps.length > 0);

// Label mappings for select fields from schema store
const selectLabels = $derived.by((): Record<string, Record<string, string>> => {
	const enums = getEnums();
	if (!enums) {
		// Fallback if schema not loaded yet
		return { status: {}, type: {} };
	}
	return {
		status: Object.fromEntries(
			enums.task_status.map((o) => [o.value, o.label]),
		),
		type: Object.fromEntries(enums.task_type.map((o) => [o.value, o.label])),
	};
});

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

function handleStepClick(index: number, step: Step) {
	onStepToggle?.(currentTask.id, index, !step.done);
}

function handleExecute() {
	onExecute?.(currentTask.id);
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

			<!-- Steps (for subtasks with steps) -->
			{#if hasSteps}
				<Separator.Root class="h-px bg-[var(--border-muted)]" />
				<div class="space-y-2">
					<div class="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">
						Steps
					</div>
					<div class="space-y-1">
						{#each currentTask.steps as step, index (index)}
							<button
								type="button"
								onclick={() => handleStepClick(index, step)}
								class="flex items-center gap-2 w-full px-2 py-1.5 rounded text-left hover:bg-[var(--bg-hover)] transition-colors"
							>
								{#if step.done}
									<CheckSquare
										class="size-4 text-green-400 shrink-0"
										weight="fill"
									/>
									<span class="text-sm text-[var(--text-muted)] line-through">
										{step.text}
									</span>
								{:else}
									<Square class="size-4 text-[var(--text-muted)] shrink-0" />
									<span class="text-sm text-[var(--text-primary)]">
										{step.text}
									</span>
								{/if}
							</button>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Subtasks Overview (for parent tasks) -->
			{#if hasSubtasks}
				<Separator.Root class="h-px bg-[var(--border-muted)]" />
				<div class="space-y-2">
					<div class="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">
						Subtasks ({subtasks.length})
					</div>
					<div class="space-y-1">
						{#each subtasks as subtask (subtask.id)}
							<div
								class="flex items-center gap-2 px-2 py-1.5 rounded bg-[var(--bg-elevated)]"
							>
								{#if subtask.status === 'DONE'}
									<CheckSquare
										class="size-4 text-green-400 shrink-0"
										weight="fill"
									/>
								{:else}
									<Square class="size-4 text-[var(--text-muted)] shrink-0" />
								{/if}
								<span
									class="text-sm flex-1 truncate"
									class:text-[var(--text-muted)]={subtask.status === 'DONE'}
									class:line-through={subtask.status === 'DONE'}
									class:text-[var(--text-primary)]={subtask.status !== 'DONE'}
								>
									{subtask.title}
								</span>
								{#if subtask.steps && subtask.steps.length > 0}
									{@const done = subtask.steps.filter((s) => s.done).length}
									<span class="text-xs text-[var(--text-muted)]">
										{done}/{subtask.steps.length}
									</span>
								{/if}
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Result (readonly, only if exists) -->
			{#if currentTask.result}
				{@const resultField = getField('result')}
				{#if resultField}
					<Separator.Root class="h-px bg-[var(--border-muted)]" />
					<FieldRenderer field={resultField} value={currentTask.result} />
				{/if}
			{/if}

			<!-- Delegation Info (Phase 11B) -->
			{#if !isNewTask && currentTask.sandbox_dir}
				<Separator.Root class="h-px bg-[var(--border-muted)]" />
				<div class="space-y-3">
					<div class="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">
						Task Info
					</div>

					<!-- Source Badge -->
					<div class="flex items-center gap-2">
						<span class="text-xs text-[var(--text-muted)]">Source:</span>
						<span class="px-2 py-0.5 text-xs font-medium rounded-full
							{currentTask.source === 'mcp' ? 'bg-blue-500/20 text-blue-400' :
							 currentTask.source === 'api' ? 'bg-green-500/20 text-green-400' :
							 'bg-[var(--bg-elevated)] text-[var(--text-muted)]'}">
							{currentTask.source?.toUpperCase() ?? 'UI'}
						</span>
					</div>

					<!-- Sandbox Directory -->
					<div class="space-y-1">
						<span class="text-xs text-[var(--text-muted)]">Sandbox:</span>
						<div class="flex items-center gap-2 px-2 py-1.5 rounded bg-[var(--bg-elevated)] text-xs font-mono text-[var(--text-secondary)]">
							<FolderOpen class="size-3.5 shrink-0 text-[var(--text-muted)]" />
							<span class="truncate">{currentTask.sandbox_dir}</span>
						</div>
					</div>

					<!-- Target Path (if set) -->
					{#if currentTask.target_path}
						<div class="space-y-1">
							<span class="text-xs text-[var(--text-muted)]">Target:</span>
							<div class="flex items-center gap-2 px-2 py-1.5 rounded bg-[var(--bg-elevated)] text-xs font-mono text-[var(--text-secondary)]">
								<FolderOpen class="size-3.5 shrink-0 text-green-400" />
								<span class="truncate">{currentTask.target_path}</span>
							</div>
						</div>
					{/if}
				</div>
			{/if}
		</div>
	{/if}

	<!-- Action Buttons -->
	<div class="pt-4 border-t border-[var(--border-muted)] mt-4 space-y-2">
		<!-- Approve & Execute (only for NEEDS_REVIEW with subtasks) -->
		{#if isNeedsReview && hasSubtasks}
			<button
				type="button"
				onclick={handleExecute}
				disabled={schemaLoading}
				class="flex items-center justify-center gap-2 w-full px-4 py-2.5 text-sm font-medium
					bg-green-600 text-white rounded
					hover:bg-green-500 transition-colors disabled:opacity-50"
			>
				<Play class="size-4" weight="fill" />
				APPROVE & EXECUTE
			</button>
		{/if}

		<!-- Save Button -->
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
