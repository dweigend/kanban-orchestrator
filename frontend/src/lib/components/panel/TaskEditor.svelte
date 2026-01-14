<script lang="ts">
import { Select, Separator } from 'bits-ui';
import CaretDown from 'phosphor-svelte/lib/CaretDown';
import Check from 'phosphor-svelte/lib/Check';
import FloppyDisk from 'phosphor-svelte/lib/FloppyDisk';
import Trash from 'phosphor-svelte/lib/Trash';
import type { Task, TaskStatus, TaskType } from '$lib/types/task';
import { TASK_STATUS_LABELS, TASK_TYPE_LABELS } from '$lib/types/task';

interface Props {
	task?: Task | null;
	onSave?: (task: Task) => void;
	onDelete?: (taskId: string) => void;
}

const { task = null, onSave, onDelete }: Props = $props();

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

// Form state - initialized and reset via effect when task changes
let title = $state('');
let description = $state('');
let status = $state<TaskStatus>('TODO');
let type = $state<TaskType>('neutral');
let errors = $state<{ title?: string }>({});

// Reset form when task prop changes
$effect(() => {
	title = currentTask.title;
	description = currentTask.description ?? '';
	status = currentTask.status;
	type = currentTask.type;
	errors = {};
});

const isNewTask = $derived(!currentTask.id || currentTask.id === '');

const typeOptions = Object.entries(TASK_TYPE_LABELS).map(([value, label]) => ({
	value: value as TaskType,
	label,
}));

const statusOptions = Object.entries(TASK_STATUS_LABELS).map(
	([value, label]) => ({
		value: value as TaskStatus,
		label,
	}),
);

const selectedTypeLabel = $derived(TASK_TYPE_LABELS[type]);
const selectedStatusLabel = $derived(TASK_STATUS_LABELS[status]);

/**
 * Validate form before submission
 */
function validateForm(): boolean {
	errors = {};
	const trimmedTitle = title.trim();

	if (!trimmedTitle) {
		errors = { ...errors, title: 'Title is required' };
	} else if (trimmedTitle.length > 100) {
		errors = { ...errors, title: 'Title must be 100 characters or less' };
	}

	return Object.keys(errors).length === 0;
}

function handleSave() {
	if (!validateForm()) return;

	const updatedTask: Task = {
		...currentTask,
		title: title.trim(),
		description: description.trim() || undefined,
		status,
		type,
		updated_at: new Date().toISOString(),
	};
	onSave?.(updatedTask);
}

function handleDelete() {
	if (currentTask.id) {
		onDelete?.(currentTask.id);
	}
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
	<div class="flex-1 space-y-4 overflow-y-auto">
		<!-- Title -->
		<div class="space-y-2">
			<label for="task-title" class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
				Title *
			</label>
			<input
				id="task-title"
				type="text"
				bind:value={title}
				placeholder="Enter task title..."
				class="w-full px-3 py-2 text-sm border rounded bg-[var(--bg-surface)] transition-colors
					{errors.title
					? 'border-red-500 focus:border-red-500'
					: 'border-[var(--border-default)] focus:border-[var(--border-focus)]'}
					placeholder:text-[var(--text-muted)] focus:outline-none"
			/>
			{#if errors.title}
				<p class="text-xs text-red-400">{errors.title}</p>
			{/if}
		</div>

		<!-- Description -->
		<div class="space-y-2">
			<label
				for="task-description"
				class="text-xs text-uppercase-tracking text-[var(--text-muted)]"
			>
				Description
			</label>
			<textarea
				id="task-description"
				bind:value={description}
				placeholder="Add a description..."
				rows="4"
				class="w-full px-3 py-2 text-sm border border-[var(--border-default)] rounded bg-[var(--bg-surface)] focus:border-[var(--border-focus)] focus:outline-none placeholder:text-[var(--text-muted)] resize-none transition-colors"
			></textarea>
		</div>

		<Separator.Root class="h-px bg-[var(--border-muted)]" />

		<!-- Type Select -->
		<div class="space-y-2">
			<span class="text-xs text-uppercase-tracking text-[var(--text-muted)]">Type</span>
			<Select.Root type="single" bind:value={type} items={typeOptions}>
				<Select.Trigger
					class="flex items-center justify-between w-full px-3 py-2 border border-[var(--border-default)] rounded bg-[var(--bg-surface)] hover:border-[var(--border-focus)] transition-colors"
				>
					<span class="text-sm">{selectedTypeLabel}</span>
					<CaretDown class="size-4 text-[var(--text-muted)]" />
				</Select.Trigger>
				<Select.Portal>
					<Select.Content
						class="z-[60] border border-[var(--border-default)] bg-[var(--bg-elevated)] rounded shadow-lg p-1 animate-fade-in"
						sideOffset={4}
					>
						<Select.Viewport>
							{#each typeOptions as option}
								<Select.Item
									value={option.value}
									label={option.label}
									class="flex items-center justify-between px-3 py-2 text-sm rounded cursor-pointer hover:bg-[var(--bg-hover)] transition-colors"
								>
									{#snippet children({ selected })}
										{option.label}
										{#if selected}
											<Check class="size-4 text-[var(--accent-primary)]" />
										{/if}
									{/snippet}
								</Select.Item>
							{/each}
						</Select.Viewport>
					</Select.Content>
				</Select.Portal>
			</Select.Root>
		</div>

		<!-- Status Select (only for existing tasks) -->
		{#if !isNewTask}
			<div class="space-y-2">
				<span class="text-xs text-uppercase-tracking text-[var(--text-muted)]">Status</span>
				<Select.Root type="single" bind:value={status} items={statusOptions}>
					<Select.Trigger
						class="flex items-center justify-between w-full px-3 py-2 border border-[var(--border-default)] rounded bg-[var(--bg-surface)] hover:border-[var(--border-focus)] transition-colors"
					>
						<span class="text-sm">{selectedStatusLabel}</span>
						<CaretDown class="size-4 text-[var(--text-muted)]" />
					</Select.Trigger>
					<Select.Portal>
						<Select.Content
							class="z-[60] border border-[var(--border-default)] bg-[var(--bg-elevated)] rounded shadow-lg p-1 animate-fade-in"
							sideOffset={4}
						>
							<Select.Viewport>
								{#each statusOptions as option}
									<Select.Item
										value={option.value}
										label={option.label}
										class="flex items-center justify-between px-3 py-2 text-sm rounded cursor-pointer hover:bg-[var(--bg-hover)] transition-colors"
									>
										{#snippet children({ selected })}
											{option.label}
											{#if selected}
												<Check class="size-4 text-[var(--accent-primary)]" />
											{/if}
										{/snippet}
									</Select.Item>
								{/each}
							</Select.Viewport>
						</Select.Content>
					</Select.Portal>
				</Select.Root>
			</div>
		{/if}
	</div>

	<!-- Save Button -->
	<div class="pt-4 border-t border-[var(--border-muted)] mt-4">
		<button
			type="button"
			onclick={handleSave}
			class="flex items-center justify-center gap-2 w-full px-4 py-2.5 text-sm font-medium bg-[var(--accent-primary)] text-[var(--text-inverse)] rounded hover:bg-[var(--accent-hover)] transition-colors"
		>
			<FloppyDisk class="size-4" />
			{isNewTask ? 'CREATE TASK' : 'SAVE CHANGES'}
		</button>
	</div>
</div>
