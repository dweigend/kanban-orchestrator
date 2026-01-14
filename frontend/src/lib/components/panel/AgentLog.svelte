<script lang="ts">
import { ScrollArea } from 'bits-ui';
import type { AgentLogEntry } from '$lib/types/agent';

interface Props {
	logs: AgentLogEntry[];
	taskTitle?: string;
	isRunning?: boolean;
}

const { logs, taskTitle = 'Task', isRunning = false }: Props = $props();

const typeColors: Record<string, string> = {
	user: 'text-blue-400',
	assistant: 'text-green-400',
	system: 'text-yellow-400',
	result: 'text-purple-400',
	error: 'text-red-400',
	unknown: 'text-[var(--text-muted)]',
};

function formatTime(timestamp: string): string {
	const date = new Date(timestamp);
	return date.toLocaleTimeString('de-DE', {
		hour: '2-digit',
		minute: '2-digit',
		second: '2-digit',
	});
}

function getTypeColor(type: string): string {
	return typeColors[type] || typeColors.unknown;
}

function truncateContent(content: string, maxLength = 200): string {
	if (content.length <= maxLength) return content;
	return `${content.slice(0, maxLength)}...`;
}
</script>

<section class="flex flex-col h-full">
	<header class="flex items-center justify-between px-3 py-2 border-b border-[var(--border-muted)]">
		<div class="flex items-center gap-2">
			{#if isRunning}
				<span class="animate-spin text-xs">⟳</span>
			{:else}
				<span class="text-xs text-[var(--text-muted)]">⚙</span>
			{/if}
			<span class="text-xs text-uppercase-tracking text-[var(--text-secondary)]">Agent Log</span>
		</div>
		<span class="text-xs text-[var(--text-muted)] truncate max-w-[150px]">{taskTitle}</span>
	</header>

	<ScrollArea.Root class="flex-1">
		<ScrollArea.Viewport class="h-full p-3">
			<div
				class="font-mono text-xs leading-relaxed bg-[var(--bg-base)] border border-[var(--border-muted)] rounded p-3 space-y-2 min-h-[200px]"
			>
				{#each logs as log, i (i)}
					<div class="flex flex-col gap-0.5">
						<div class="flex items-center gap-2">
							<span class="text-[var(--text-muted)] shrink-0">{formatTime(log.timestamp)}</span>
							<span class="{getTypeColor(log.type)} shrink-0 uppercase text-[10px]">{log.type}</span>
						</div>
						<div class="text-[var(--text-secondary)] pl-4 whitespace-pre-wrap break-words">
							{truncateContent(log.content)}
						</div>
					</div>
				{/each}

				{#if logs.length === 0}
					<div class="text-[var(--text-muted)] text-center py-8">
						{#if isRunning}
							<span class="animate-pulse">Starting agent...</span>
						{:else}
							No agent activity
						{/if}
					</div>
				{/if}

				{#if isRunning}
					<div class="flex items-center gap-1 pt-2 border-t border-[var(--border-muted)]">
						<span class="text-[var(--text-muted)]">Agent working...</span>
						<span class="animate-pulse">▊</span>
					</div>
				{/if}
			</div>
		</ScrollArea.Viewport>
		<ScrollArea.Scrollbar orientation="vertical" class="w-1.5 touch-none select-none p-px">
			<ScrollArea.Thumb class="bg-[var(--border-default)] rounded-full" />
		</ScrollArea.Scrollbar>
	</ScrollArea.Root>
</section>
