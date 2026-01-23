<script lang="ts">
import { Button } from 'bits-ui';
import Plus from 'phosphor-svelte/lib/Plus';
import type { Snippet } from 'svelte';
import { getStatusLabel } from '$lib/stores/schema.svelte';
import type { Task, TaskStatus } from '$lib/types/task';
import TaskCard from './TaskCard.svelte';

interface Props {
	status: TaskStatus;
	tasks: Task[];
	onAddTask?: () => void;
	onEditTask?: (task: Task) => void;
	onDeleteTask?: (task: Task) => void;
	onTaskDrop?: (taskId: string, newStatus: TaskStatus) => void;
	onRunAgent?: (task: Task) => void;
	runningAgentTaskId?: string | null;
	children?: Snippet;
}

const {
	status,
	tasks,
	onAddTask,
	onEditTask,
	onDeleteTask,
	onTaskDrop,
	onRunAgent,
	runningAgentTaskId,
}: Props = $props();

let isDragOver = $state(false);

function handleDragOver(e: DragEvent) {
	e.preventDefault();
	if (e.dataTransfer) {
		e.dataTransfer.dropEffect = 'move';
	}
	isDragOver = true;
}

function handleDragLeave() {
	isDragOver = false;
}

function handleDrop(e: DragEvent) {
	e.preventDefault();
	isDragOver = false;
	const taskId = e.dataTransfer?.getData('text/plain');
	if (taskId) {
		onTaskDrop?.(taskId, status);
	}
}

const taskCount = $derived(tasks.length);
</script>

<section class="flex flex-col min-w-[280px] max-w-[320px] flex-1">
	<!-- Column Header -->
	<header
		class="flex items-center justify-between px-3 py-2 border-b border-[var(--border-default)]"
	>
		<div class="flex items-center gap-2">
			<span class="text-xs text-uppercase-tracking text-[var(--text-secondary)]">
				{getStatusLabel(status.toLowerCase())}
			</span>
			<span
				class="size-5 flex items-center justify-center rounded bg-[var(--bg-surface)] text-xs text-[var(--text-muted)]"
			>
				{taskCount}
			</span>
		</div>

		<Button.Root
			class="size-6 flex items-center justify-center rounded hover:bg-[var(--bg-hover)] text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors focus-ring"
			onclick={() => onAddTask?.()}
			aria-label="Add task to {getStatusLabel(status.toLowerCase())}"
		>
			<Plus class="size-4" />
		</Button.Root>
	</header>

	<!-- Tasks List (Drop Target) -->
	<div
		class="flex-1 overflow-y-auto p-2 space-y-2 scrollbar-thin transition-colors"
		class:bg-[var(--bg-hover)]={isDragOver}
		ondragover={handleDragOver}
		ondragleave={handleDragLeave}
		ondrop={handleDrop}
		role="list"
	>
		{#each tasks as task (task.id)}
			<TaskCard
				{task}
				onEdit={onEditTask}
				onDelete={onDeleteTask}
				{onRunAgent}
				isAgentRunning={runningAgentTaskId === task.id}
			/>
		{/each}

		{#if tasks.length === 0}
			<div
				class="flex items-center justify-center h-24 border border-dashed border-[var(--border-muted)] rounded text-xs text-[var(--text-muted)]"
				class:border-[var(--accent-primary)]={isDragOver}
			>
				{isDragOver ? 'Drop here' : 'No tasks'}
			</div>
		{/if}
	</div>
</section>
