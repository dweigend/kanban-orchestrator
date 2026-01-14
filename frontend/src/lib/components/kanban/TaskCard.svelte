<script lang="ts">
import { DropdownMenu } from 'bits-ui';
import ArrowSquareOut from 'phosphor-svelte/lib/ArrowSquareOut';
import Chat from 'phosphor-svelte/lib/Chat';
import Code from 'phosphor-svelte/lib/Code';
import DotsThree from 'phosphor-svelte/lib/DotsThree';
import MagnifyingGlass from 'phosphor-svelte/lib/MagnifyingGlass';
import Note from 'phosphor-svelte/lib/Note';
import type { Task, TaskType } from '$lib/types/task';
import { TASK_TYPE_COLORS } from '$lib/types/task';

interface Props {
	task: Task;
	onEdit?: (task: Task) => void;
	onDelete?: (task: Task) => void;
}

const { task, onEdit, onDelete }: Props = $props();

const typeIcons: Record<TaskType, typeof MagnifyingGlass> = {
	research: MagnifyingGlass,
	dev: Code,
	notes: Note,
	neutral: Chat,
};

const TypeIcon = $derived(typeIcons[task.type]);

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
	// Don't trigger edit if clicking on the dropdown trigger
	const target = e.target as HTMLElement;
	if (target.closest('[data-dropdown-trigger]')) return;
	onEdit?.(task);
}

function getShortId(id: string): string {
	const prefix =
		task.type === 'research' ? 'RES' : task.type === 'dev' ? 'DEV' : 'NOTE';
	return `#${prefix}-${id.slice(0, 2).toUpperCase()}`;
}
</script>

<article
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

		<DropdownMenu.Root>
			<DropdownMenu.Trigger
				class="size-6 flex items-center justify-center rounded opacity-0 group-hover:opacity-100 hover:bg-[var(--bg-hover)] transition-all focus-ring"
				aria-label="Task actions"
				data-dropdown-trigger
			>
				<DotsThree class="size-4" weight="bold" />
			</DropdownMenu.Trigger>
			<DropdownMenu.Portal>
				<DropdownMenu.Content
					class="z-50 min-w-[140px] rounded-md border border-[var(--border-default)] bg-[var(--bg-elevated)] p-1 shadow-lg animate-fade-in"
					sideOffset={4}
				>
					<DropdownMenu.Item
						class="flex items-center gap-2 px-3 py-2 text-xs rounded cursor-pointer hover:bg-[var(--bg-hover)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors"
						onclick={() => onEdit?.(task)}
					>
						Edit
					</DropdownMenu.Item>
					<DropdownMenu.Item
						class="flex items-center gap-2 px-3 py-2 text-xs rounded cursor-pointer hover:bg-[var(--bg-hover)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors"
					>
						<ArrowSquareOut class="size-3" />
						Open
					</DropdownMenu.Item>
					<DropdownMenu.Separator class="my-1 h-px bg-[var(--border-muted)]" />
					<DropdownMenu.Item
						class="flex items-center gap-2 px-3 py-2 text-xs rounded cursor-pointer hover:bg-red-500/10 text-red-400 transition-colors"
						onclick={() => onDelete?.(task)}
					>
						Delete
					</DropdownMenu.Item>
				</DropdownMenu.Content>
			</DropdownMenu.Portal>
		</DropdownMenu.Root>
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
		class="flex items-center justify-end gap-2 px-3 py-2 border-t border-[var(--border-muted)] bg-[var(--bg-elevated)]"
	>
		<TypeIcon class="size-4 text-[var(--text-muted)]" />
	</div>
</article>
