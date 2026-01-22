<script lang="ts">
import { Separator } from 'bits-ui';
import { getTaskStatuses } from '$lib/stores/schema.svelte';
import type { Task, TaskStatus } from '$lib/types/task';
import { type BackendTaskStatus, STATUS_FROM_BACKEND } from '$lib/types/task';
import Column from './Column.svelte';

interface Props {
	tasks: Task[];
	onAddTask?: (status: TaskStatus) => void;
	onEditTask?: (task: Task) => void;
	onDeleteTask?: (task: Task) => void;
	onTaskDrop?: (taskId: string, newStatus: TaskStatus) => void;
	onRunAgent?: (task: Task) => void;
	runningAgentTaskId?: string | null;
}

const {
	tasks,
	onAddTask,
	onEditTask,
	onDeleteTask,
	onTaskDrop,
	onRunAgent,
	runningAgentTaskId,
}: Props = $props();

// Default columns (fallback if schema not loaded)
const defaultColumns: TaskStatus[] = [
	'TODO',
	'IN_PROGRESS',
	'NEEDS_REVIEW',
	'DONE',
];

// Reactive columns from schema (re-evaluates when schema loads)
// Schema returns lowercase ('todo'), frontend uses UPPERCASE ('TODO')
const columns = $derived.by(() => {
	const statuses = getTaskStatuses();
	if (statuses.length === 0) return defaultColumns;
	// Map lowercase schema values to UPPERCASE frontend format
	return statuses.map((s) => STATUS_FROM_BACKEND[s as BackendTaskStatus]);
});

function getTasksByStatus(status: TaskStatus): Task[] {
	return tasks.filter((t) => t.status === status);
}
</script>

<div class="flex-1 flex overflow-hidden bg-[var(--bg-base)]">
	{#each columns as status, i}
		{#if i > 0}
			<Separator.Root
				class="w-px bg-[var(--border-default)] self-stretch"
				orientation="vertical"
			/>
		{/if}
		<Column
			{status}
			tasks={getTasksByStatus(status)}
			onAddTask={() => onAddTask?.(status)}
			{onEditTask}
			{onDeleteTask}
			{onTaskDrop}
			{onRunAgent}
			{runningAgentTaskId}
		/>
	{/each}
</div>
