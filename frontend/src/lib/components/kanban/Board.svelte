<script lang="ts">
import { Separator } from 'bits-ui';
import type { Task, TaskStatus } from '$lib/types/task';
import Column from './Column.svelte';

interface Props {
	tasks: Task[];
	onAddTask?: (status: TaskStatus) => void;
	onEditTask?: (task: Task) => void;
	onDeleteTask?: (task: Task) => void;
}

const { tasks, onAddTask, onEditTask, onDeleteTask }: Props = $props();

const columns: TaskStatus[] = ['TODO', 'IN_PROGRESS', 'DONE'];

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
		/>
	{/each}
</div>
