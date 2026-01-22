<script lang="ts">
import Chat from 'phosphor-svelte/lib/Chat';
import CircleNotch from 'phosphor-svelte/lib/CircleNotch';
import Code from 'phosphor-svelte/lib/Code';
import MagnifyingGlass from 'phosphor-svelte/lib/MagnifyingGlass';
import Note from 'phosphor-svelte/lib/Note';
import Play from 'phosphor-svelte/lib/Play';
import Trash from 'phosphor-svelte/lib/Trash';
import { getTypeIcon, getTypePrefix } from '$lib/stores/schema.svelte';
import type { Task } from '$lib/types/task';
import { TASK_TYPE_COLORS } from '$lib/types/task';

interface Props {
	task: Task;
	onEdit?: (task: Task) => void;
	onDelete?: (task: Task) => void;
	onRunAgent?: (task: Task) => void;
	isAgentRunning?: boolean;
}

const {
	task,
	onEdit,
	onDelete,
	onRunAgent,
	isAgentRunning = false,
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
	class="group relative border border-[var(--border-default)] bg-[var(--bg-surface)] rounded-sm overflow-hidden hover:border-[var(--border-focus)] transition-colors cursor-pointer"
	class:opacity-50={isDragging}
	style="border-left: 4px solid {TASK_TYPE_COLORS[task.type]}"
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
		<span class="text-xs text-[var(--text-muted)] font-mono">{getShortId(task.id)}</span>

		<div class="flex items-center gap-1">
			<!-- Run Agent -->
			<button
				type="button"
				onclick={() => onRunAgent?.(task)}
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
				onclick={() => onDelete?.(task)}
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

	<!-- Footer with type icon -->
	<div
		class="flex items-center justify-between gap-2 px-3 py-2 border-t border-[var(--border-muted)] bg-[var(--bg-elevated)]"
	>
		{#if isAgentRunning}
			<div class="flex items-center gap-1 text-xs text-orange-400">
				<CircleNotch class="size-3 animate-spin" />
				<span>Agent</span>
			</div>
		{:else}
			<span></span>
		{/if}
		<TypeIcon class="size-4 text-[var(--text-muted)]" />
	</div>
</div>
