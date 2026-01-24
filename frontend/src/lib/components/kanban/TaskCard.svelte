<script lang="ts">
import CaretDown from 'phosphor-svelte/lib/CaretDown';
import CaretRight from 'phosphor-svelte/lib/CaretRight';
import Chat from 'phosphor-svelte/lib/Chat';
import CircleNotch from 'phosphor-svelte/lib/CircleNotch';
import Code from 'phosphor-svelte/lib/Code';
import ListChecks from 'phosphor-svelte/lib/ListChecks';
import MagnifyingGlass from 'phosphor-svelte/lib/MagnifyingGlass';
import Note from 'phosphor-svelte/lib/Note';
import Play from 'phosphor-svelte/lib/Play';
import Trash from 'phosphor-svelte/lib/Trash';
import { getTypeIcon, getTypePrefix } from '$lib/stores/schema.svelte';
import type { Task } from '$lib/types/task';
import { TASK_TYPE_COLORS } from '$lib/types/task';
import SubtaskTree from './SubtaskTree.svelte';

interface Props {
	task: Task;
	subtasks?: Task[];
	isExpanded?: boolean;
	onEdit?: (task: Task) => void;
	onDelete?: (task: Task) => void;
	onRunAgent?: (task: Task) => void;
	onPlanTask?: (task: Task) => void;
	onToggleExpand?: (taskId: string) => void;
	isAgentRunning?: boolean;
	isPlanning?: boolean;
}

const {
	task,
	subtasks = [],
	isExpanded = false,
	onEdit,
	onDelete,
	onRunAgent,
	onPlanTask,
	onToggleExpand,
	isAgentRunning = false,
	isPlanning = false,
}: Props = $props();

// Icon mapping (icon names from schema → Phosphor components)
const iconComponents: Record<string, typeof MagnifyingGlass> = {
	MagnifyingGlass: MagnifyingGlass,
	Code: Code,
	Note: Note,
	Chat: Chat,
};

// Get icon component from schema with fallback
const TypeIcon = $derived.by(() => {
	const iconName = getTypeIcon(task.type);
	return iconName ? (iconComponents[iconName] ?? Chat) : Chat;
});

// Progress calculation
const progress = $derived.by(() => {
	if (subtasks.length === 0) return null;
	let total = 0;
	let completed = 0;
	for (const st of subtasks) {
		if (st.steps) {
			for (const step of st.steps) {
				total++;
				if (step.done) completed++;
			}
		}
	}
	return total > 0 ? { completed, total } : null;
});

// Show plan button: TODO tasks without subtasks
const showPlanButton = $derived(
	task.status === 'TODO' && subtasks.length === 0 && !task.parent_id,
);

// Has expandable content
const hasSubtasks = $derived(subtasks.length > 0);

let isDragging = $state(false);

function handleDragStart(e: DragEvent) {
	isDragging = true;
	if (e.dataTransfer) {
		e.dataTransfer.setData('text/plain', task.id);
		e.dataTransfer.effectAllowed = 'move';
	}
}

function handleDragEnd() {
	isDragging = false;
}

function handleClick(e: MouseEvent) {
	// Don't trigger edit if clicking on action buttons
	const target = e.target as HTMLElement;
	if (target.closest('[data-action-btn]')) return;
	onEdit?.(task);
}

function getShortId(id: string): string {
	const prefix = getTypePrefix(task.type);
	return `#${prefix}-${id.slice(0, 2).toUpperCase()}`;
}
</script>

<div
	class="group relative border border-[var(--border-default)] bg-[var(--bg-surface)] rounded-sm overflow-hidden hover:border-[var(--border-focus)] transition-colors"
	class:opacity-50={isDragging}
	style="border-left: 4px solid {TASK_TYPE_COLORS[task.type]}"
>
	<!-- Main Card (draggable, clickable) -->
	<div
		class="cursor-pointer"
		draggable="true"
		ondragstart={handleDragStart}
		ondragend={handleDragEnd}
		onclick={handleClick}
		onkeydown={(e) => e.key === 'Enter' && onEdit?.(task)}
		role="button"
		tabindex="0"
	>
		<!-- Header -->
		<div class="flex items-center justify-between px-3 pt-3">
			<div class="flex items-center gap-1">
				<!-- Expand/Collapse toggle -->
				{#if hasSubtasks}
					<button
						type="button"
						onclick={(e) => {
							e.stopPropagation();
							onToggleExpand?.(task.id);
						}}
						data-action-btn
						class="size-5 flex items-center justify-center rounded hover:bg-[var(--bg-hover)] transition-all text-[var(--text-muted)]"
						title={isExpanded ? 'Collapse' : 'Expand'}
					>
						{#if isExpanded}
							<CaretDown class="size-3" weight="bold" />
						{:else}
							<CaretRight class="size-3" weight="bold" />
						{/if}
					</button>
				{/if}
				<span class="text-xs text-[var(--text-muted)] font-mono">{getShortId(task.id)}</span>
			</div>

			<div class="flex items-center gap-1">
				<!-- Plan Task (only for TODO without subtasks) -->
				{#if showPlanButton}
					<button
						type="button"
						onclick={(e) => {
							e.stopPropagation();
							onPlanTask?.(task);
						}}
						disabled={isPlanning}
						data-action-btn
						class="size-6 flex items-center justify-center rounded opacity-0 group-hover:opacity-100 hover:bg-[var(--bg-hover)] transition-all focus-ring disabled:opacity-50 text-[var(--text-muted)] hover:text-blue-400"
						title={isPlanning ? 'Planning...' : 'Plan Task'}
					>
						{#if isPlanning}
							<CircleNotch class="size-4 animate-spin text-blue-400" />
						{:else}
							<ListChecks class="size-4" weight="bold" />
						{/if}
					</button>
				{/if}

				<!-- Run Agent -->
				<button
					type="button"
					onclick={(e) => {
						e.stopPropagation();
						onRunAgent?.(task);
					}}
					disabled={isAgentRunning}
					data-action-btn
					class="size-6 flex items-center justify-center rounded opacity-0 group-hover:opacity-100 hover:bg-[var(--bg-hover)] transition-all focus-ring disabled:opacity-50 disabled:cursor-not-allowed text-[var(--text-muted)] hover:text-[var(--accent-primary)]"
					title={isAgentRunning ? 'Agent running...' : 'Run Agent'}
				>
					{#if isAgentRunning}
						<CircleNotch class="size-4 animate-spin text-orange-400" />
					{:else}
						<Play class="size-4" weight="fill" />
					{/if}
				</button>

				<!-- Delete -->
				<button
					type="button"
					onclick={(e) => {
						e.stopPropagation();
						onDelete?.(task);
					}}
					data-action-btn
					class="size-6 flex items-center justify-center rounded opacity-0 group-hover:opacity-100 hover:bg-red-500/10 transition-all focus-ring text-[var(--text-muted)] hover:text-red-400"
					title="Delete"
				>
					<Trash class="size-4" weight="bold" />
				</button>
			</div>
		</div>

		<!-- Content -->
		<div class="px-3 pb-3 pt-2">
			<h3 class="text-sm font-medium text-[var(--text-primary)] leading-snug">{task.title}</h3>

			{#if task.description}
				<p class="mt-1 text-xs text-[var(--text-muted)] line-clamp-2">{task.description}</p>
			{/if}
		</div>

		<!-- Footer with progress and type icon -->
		<div
			class="flex items-center justify-between gap-2 px-3 py-2 border-t border-[var(--border-muted)] bg-[var(--bg-elevated)]"
		>
			{#if isAgentRunning}
				<div class="flex items-center gap-1 text-xs text-orange-400">
					<CircleNotch class="size-3 animate-spin" />
					<span>Agent</span>
				</div>
			{:else if isPlanning}
				<div class="flex items-center gap-1 text-xs text-blue-400">
					<CircleNotch class="size-3 animate-spin" />
					<span>Planning</span>
				</div>
			{:else if progress}
				<div class="flex items-center gap-1 text-xs text-[var(--text-muted)]">
					<span>{progress.completed}/{progress.total} steps</span>
				</div>
			{:else if hasSubtasks}
				<div class="flex items-center gap-1 text-xs text-[var(--text-muted)]">
					<span>{subtasks.length} subtasks</span>
				</div>
			{:else}
				<span></span>
			{/if}
			<TypeIcon class="size-4 text-[var(--text-muted)]" />
		</div>
	</div>

	<!-- Expanded Subtasks List with Tree Structure -->
	{#if isExpanded && hasSubtasks}
		<SubtaskTree {subtasks} {onEdit} />
	{/if}
</div>
