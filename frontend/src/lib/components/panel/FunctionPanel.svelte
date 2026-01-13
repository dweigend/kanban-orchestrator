<script lang="ts">
import { Separator } from 'bits-ui';
import type { Agent } from '$lib/types/agent';
import AgentList from './AgentList.svelte';
import ProjectOverview from './ProjectOverview.svelte';
import SearchBar from './SearchBar.svelte';
import SystemLog from './SystemLog.svelte';

interface LogEntry {
	id: string;
	timestamp: string;
	level: 'info' | 'warn' | 'error' | 'success';
	message: string;
	source?: string;
}

interface Props {
	projectName?: string;
	projectStatus?: string;
	projectTarget?: string;
	projectTags?: string[];
	agents?: Agent[];
	logs?: LogEntry[];
	onSearch?: (query: string) => void;
}

const {
	projectName = 'vibe-kanban',
	projectStatus = 'V3 Redesign',
	projectTarget = 'High Contrast',
	projectTags = ['React', 'Tailwind', 'MCP'],
	agents = [],
	logs = [],
	onSearch,
}: Props = $props();
</script>

<aside
	class="w-[var(--sidebar-width)] border-l border-[var(--border-default)] bg-[var(--bg-elevated)] flex flex-col overflow-hidden"
>
	<!-- Search -->
	<div class="py-3">
		<SearchBar {onSearch} />
	</div>

	<Separator.Root class="h-px bg-[var(--border-muted)]" />

	<!-- Overview -->
	<div class="py-3">
		<ProjectOverview
			name={projectName}
			status={projectStatus}
			target={projectTarget}
			tags={projectTags}
		/>
	</div>

	<Separator.Root class="h-px bg-[var(--border-muted)]" />

	<!-- Agents -->
	<div class="py-3">
		<AgentList {agents} />
	</div>

	<Separator.Root class="h-px bg-[var(--border-muted)]" />

	<!-- System Log -->
	<div class="py-3 flex-1 min-h-0">
		<SystemLog {logs} />
	</div>
</aside>
