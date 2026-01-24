<script lang="ts">
import CheckCircle from 'phosphor-svelte/lib/CheckCircle';
import Circle from 'phosphor-svelte/lib/Circle';
import CircleNotch from 'phosphor-svelte/lib/CircleNotch';
import type { Task } from '$lib/types/task';

interface Props {
	subtasks: Task[];
	onEdit?: (task: Task) => void;
}

const { subtasks, onEdit }: Props = $props();
</script>

<div class="border-t border-[var(--border-muted)] bg-[var(--bg-elevated)]">
	{#each subtasks as subtask, i (subtask.id)}
		{@const isLast = i === subtasks.length - 1}
		<div
			class="flex items-stretch hover:bg-[var(--bg-hover)] cursor-pointer"
			onclick={() => onEdit?.(subtask)}
			onkeydown={(e) => e.key === 'Enter' && onEdit?.(subtask)}
			role="button"
			tabindex="0"
		>
			<!-- Tree Structure -->
			<div class="flex items-center pl-3 text-[var(--border-default)]">
				<!-- Vertical line + branch -->
				<div class="flex items-center h-full">
					<div class="relative w-4 h-full flex items-center justify-center">
						<!-- Vertical line (full height except last item) -->
						<div
							class="absolute left-1/2 -translate-x-1/2 w-px bg-[var(--border-default)] {isLast
								? 'top-0 h-1/2'
								: 'top-0 bottom-0'}"
						></div>
					</div>
					<!-- Horizontal branch -->
					<div class="w-2 h-px bg-[var(--border-default)]"></div>
				</div>
			</div>

			<!-- Subtask Content -->
			<div class="flex-1 flex items-center gap-2 py-2 pr-3">
				{#if subtask.status === 'DONE'}
					<CheckCircle class="size-3.5 text-green-400 shrink-0" weight="fill" />
				{:else if subtask.status === 'IN_PROGRESS'}
					<CircleNotch class="size-3.5 text-orange-400 animate-spin shrink-0" />
				{:else}
					<Circle class="size-3.5 text-[var(--text-muted)] shrink-0" />
				{/if}

				<span class="text-xs text-[var(--text-secondary)] truncate flex-1">
					{subtask.title}
				</span>

				{#if subtask.steps && subtask.steps.length > 0}
					{@const done = subtask.steps.filter((s) => s.done).length}
					<span class="text-[10px] text-[var(--text-muted)] tabular-nums shrink-0">
						{done}/{subtask.steps.length}
					</span>
				{/if}
			</div>
		</div>
	{/each}
</div>
