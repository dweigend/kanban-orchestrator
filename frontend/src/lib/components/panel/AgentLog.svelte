<script lang="ts">
import { ScrollArea } from 'bits-ui';
import { getAgentStatusLabel } from '$lib/stores/schema.svelte';
import type { AgentLogEntry, AgentRun } from '$lib/types/agent';
import type { Task } from '$lib/types/task';

interface Props {
	logs: AgentLogEntry[];
	runs?: AgentRun[];
	tasks?: Task[];
	taskTitle?: string;
	isRunning?: boolean;
}

const {
	logs,
	runs = [],
	tasks = [],
	taskTitle = 'Task',
	isRunning = false,
}: Props = $props();

const typeColors: Record<string, string> = {
	user: 'text-blue-400',
	assistant: 'text-green-400',
	system: 'text-yellow-400',
	result: 'text-purple-400',
	error: 'text-red-400',
	unknown: 'text-[var(--text-muted)]',
};

const statusColors: Record<string, string> = {
	pending: 'text-yellow-400',
	running: 'text-blue-400',
	needs_review: 'text-orange-400',
	completed: 'text-green-400',
	failed: 'text-red-400',
	cancelled: 'text-[var(--text-muted)]',
};

function formatTime(timestamp: string): string {
	const date = new Date(timestamp);
	return date.toLocaleTimeString('de-DE', {
		hour: '2-digit',
		minute: '2-digit',
		second: '2-digit',
	});
}

function formatDate(timestamp: string): string {
	const date = new Date(timestamp);
	return date.toLocaleDateString('de-DE', {
		day: '2-digit',
		month: '2-digit',
		hour: '2-digit',
		minute: '2-digit',
	});
}

function getTypeColor(type: string): string {
	return typeColors[type] || typeColors.unknown;
}

function getStatusColor(status: string): string {
	return statusColors[status] || statusColors.pending;
}

function truncateContent(content: string, maxLength = 200): string {
	if (content.length <= maxLength) return content;
	return `${content.slice(0, maxLength)}...`;
}

function getTaskTitle(taskId: string): string {
	const task = tasks.find((t) => t.id === taskId);
	return task?.title ?? 'Unknown Task';
}

// Sort runs by date, newest first (fallback to created_at if started_at is null)
const sortedRuns = $derived(
	[...runs].sort((a, b) => {
		const dateA = a.started_at ?? a.created_at;
		const dateB = b.started_at ?? b.created_at;
		return new Date(dateB).getTime() - new Date(dateA).getTime();
	}),
);
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
			<!-- Live Logs (when agent is running or has logs) -->
			{#if logs.length > 0 || isRunning}
				<div
					class="font-mono text-xs leading-relaxed bg-[var(--bg-base)] border border-[var(--border-muted)] rounded p-3 space-y-2 min-h-[200px]"
				>
					{#each logs as log, i (i)}
						<div class="flex flex-col gap-0.5">
							<div class="flex items-center gap-2">
								<span class="text-[var(--text-muted)] shrink-0">{formatTime(log.timestamp)}</span>
								<span class="{getTypeColor(log.type)} shrink-0 uppercase text-[10px]"
									>{log.type}</span
								>
							</div>
							<div class="text-[var(--text-secondary)] pl-4 whitespace-pre-wrap break-words">
								{truncateContent(log.content)}
							</div>
						</div>
					{/each}

					{#if logs.length === 0 && isRunning}
						<div class="text-[var(--text-muted)] text-center py-8">
							<span class="animate-pulse">Starting agent...</span>
						</div>
					{/if}

					{#if isRunning}
						<div class="flex items-center gap-1 pt-2 border-t border-[var(--border-muted)]">
							<span class="text-[var(--text-muted)]">Agent working...</span>
							<span class="animate-pulse">▊</span>
						</div>
					{/if}
				</div>
			{:else}
				<!-- Historical Runs (when no live logs) -->
				<div class="space-y-3">
					{#if sortedRuns.length > 0}
						<div class="text-xs text-uppercase-tracking text-[var(--text-muted)] mb-2">
							Recent Agent Runs
						</div>
						{#each sortedRuns as run (run.id)}
							<div
								class="bg-[var(--bg-base)] border border-[var(--border-muted)] rounded p-3 space-y-2"
							>
								<div class="flex items-center justify-between">
									<span class="text-xs font-medium text-[var(--text-primary)] truncate max-w-[180px]">
										{getTaskTitle(run.task_id)}
									</span>
									<span class="text-[10px] {getStatusColor(run.status)} uppercase">
										{getAgentStatusLabel(run.status)}
									</span>
								</div>
								<div class="flex items-center gap-2 text-[10px] text-[var(--text-muted)]">
									<span>{formatDate(run.started_at ?? run.created_at)}</span>
									{#if run.completed_at}
										<span>→</span>
										<span>{formatTime(run.completed_at)}</span>
									{/if}
								</div>
								{#if run.error_message}
									<div class="text-xs text-red-400 truncate">
										{run.error_message}
									</div>
								{/if}
							</div>
						{/each}
					{:else}
						<div
							class="font-mono text-xs bg-[var(--bg-base)] border border-[var(--border-muted)] rounded p-3 min-h-[200px] flex items-center justify-center"
						>
							<span class="text-[var(--text-muted)]">No agent activity yet</span>
						</div>
					{/if}
				</div>
			{/if}
		</ScrollArea.Viewport>
		<ScrollArea.Scrollbar orientation="vertical" class="w-1.5 touch-none select-none p-px">
			<ScrollArea.Thumb class="bg-[var(--border-default)] rounded-full" />
		</ScrollArea.Scrollbar>
	</ScrollArea.Root>
</section>
