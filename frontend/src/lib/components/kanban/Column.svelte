<script lang="ts">
import { Button } from 'bits-ui';
import Plus from 'phosphor-svelte/lib/Plus';
import type { Snippet } from 'svelte';
import type { Task, TaskStatus } from '$lib/types/task';
import { TASK_STATUS_LABELS } from '$lib/types/task';
import TaskCard from './TaskCard.svelte';

interface Props {
	status: TaskStatus;
	tasks: Task[];
	onAddTask?: () => void;
	onEditTask?: (task: Task) => void;
	onDeleteTask?: (task: Task) => void;
	children?: Snippet;
}

const { status, tasks, onAddTask, onEditTask, onDeleteTask }: Props = $props();

const taskCount = $derived(tasks.length);
</script>

<section class="flex flex-col min-w-[280px] max-w-[320px] flex-1">
	<!-- Column Header -->
	<header
		class="flex items-center justify-between px-3 py-2 border-b border-[var(--border-default)]"
	>
		<div class="flex items-center gap-2">
			<span class="text-xs text-uppercase-tracking text-[var(--text-secondary)]">
				{TASK_STATUS_LABELS[status]}
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
			aria-label="Add task to {TASK_STATUS_LABELS[status]}"
		>
			<Plus class="size-4" />
		</Button.Root>
	</header>

	<!-- Tasks List -->
	<div class="flex-1 overflow-y-auto p-2 space-y-2 scrollbar-thin">
		{#each tasks as task (task.id)}
			<TaskCard {task} onEdit={onEditTask} onDelete={onDeleteTask} />
		{/each}

		{#if tasks.length === 0}
			<div
				class="flex items-center justify-center h-24 border border-dashed border-[var(--border-muted)] rounded text-xs text-[var(--text-muted)]"
			>
				No tasks
			</div>
		{/if}
	</div>
</section>
