<script lang="ts">
import type { Snippet } from 'svelte';
import { getStatusLabel } from '$lib/stores/schema.svelte';
import type { Task, TaskStatus } from '$lib/types/task';
import TaskCard from './TaskCard.svelte';

interface Props {
	status: TaskStatus;
	tasks: Task[];
	onEditTask?: (task: Task) => void;
	onDeleteTask?: (task: Task) => void;
	onTaskDrop?: (taskId: string, newStatus: TaskStatus) => void;
	onRunAgent?: (task: Task) => void;
	onPlanTask?: (task: Task) => void;
	onToggleExpand?: (taskId: string) => void;
	runningAgentTaskId?: string | null;
	planningTaskId?: string | null;
	expandedTasks?: Set<string>;
	getSubtasksFor?: (parentId: string) => Task[];
	children?: Snippet;
}

const {
	status,
	tasks,
	onEditTask,
	onDeleteTask,
	onTaskDrop,
	onRunAgent,
	onPlanTask,
	onToggleExpand,
	runningAgentTaskId,
	planningTaskId,
	expandedTasks = new Set(),
	getSubtasksFor = () => [],
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
				subtasks={getSubtasksFor(task.id)}
				isExpanded={expandedTasks.has(task.id)}
				onEdit={onEditTask}
				onDelete={onDeleteTask}
				{onRunAgent}
				{onPlanTask}
				{onToggleExpand}
				isAgentRunning={runningAgentTaskId === task.id}
				isPlanning={planningTaskId === task.id}
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
