<script lang="ts">
import { ScrollArea } from 'bits-ui';

interface LogEntry {
	id: string;
	timestamp: string;
	level: 'info' | 'warn' | 'error' | 'success';
	message: string;
	source?: string;
}

interface Props {
	logs: LogEntry[];
}

const { logs }: Props = $props();

const levelColors: Record<LogEntry['level'], string> = {
	info: 'text-blue-400',
	warn: 'text-yellow-400',
	error: 'text-red-400',
	success: 'text-green-400',
};

const levelLabels: Record<LogEntry['level'], string> = {
	info: 'INFO',
	warn: 'WARN',
	error: 'ERR',
	success: '✓',
};

function formatTime(timestamp: string): string {
	const date = new Date(timestamp);
	return date.toLocaleTimeString('de-DE', {
		hour: '2-digit',
		minute: '2-digit',
		second: '2-digit',
	});
}
</script>

<section class="flex flex-col">
	<header class="flex items-center justify-between px-3 py-2">
		<div class="flex items-center gap-2">
			<span class="text-xs text-[var(--text-muted)]">▤</span>
			<span class="text-xs text-uppercase-tracking text-[var(--text-secondary)]">System Log</span>
		</div>
		<button
			type="button"
			class="text-xs text-[var(--text-muted)] hover:text-[var(--text-secondary)] transition-colors"
		>
			View All
		</button>
	</header>

	<ScrollArea.Root class="flex-1 max-h-[180px]">
		<ScrollArea.Viewport class="px-3">
			<div
				class="font-mono text-xs leading-relaxed bg-[var(--bg-base)] border border-[var(--border-muted)] rounded p-3 space-y-1"
			>
				{#each logs as log (log.id)}
					<div class="flex items-start gap-2">
						<span class="text-[var(--text-muted)] shrink-0">{formatTime(log.timestamp)}</span>
						<span class="{levelColors[log.level]} shrink-0 w-12">{levelLabels[log.level]}</span>
						<span class="text-[var(--text-secondary)]">{log.message}</span>
						{#if log.source}
							<span class="text-green-400 ml-auto shrink-0">{log.source}</span>
						{/if}
					</div>
				{/each}

				{#if logs.length === 0}
					<div class="text-[var(--text-muted)] text-center py-4">No log entries</div>
				{/if}

				<!-- Cursor blink effect -->
				<div class="flex items-center gap-1 pt-1">
					<span class="text-[var(--text-muted)]">Waiting for changes...</span>
					<span class="animate-pulse-subtle">▊</span>
				</div>
			</div>
		</ScrollArea.Viewport>
		<ScrollArea.Scrollbar orientation="vertical" class="w-1.5 touch-none select-none p-px">
			<ScrollArea.Thumb class="bg-[var(--border-default)] rounded-full" />
		</ScrollArea.Scrollbar>
	</ScrollArea.Root>
</section>
