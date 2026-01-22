<script lang="ts">
import { Separator } from 'bits-ui';
import type { Agent, AgentLogEntry, AgentRun } from '$lib/types/agent';
import type { Task } from '$lib/types/task';
import AgentLog from './AgentLog.svelte';
import ProjectOverview from './ProjectOverview.svelte';
import SearchBar from './SearchBar.svelte';
import SettingsPanel from './SettingsPanel.svelte';
import SystemLog from './SystemLog.svelte';
import TaskEditor from './TaskEditor.svelte';

interface LogEntry {
	id: string;
	timestamp: string;
	level: 'info' | 'warn' | 'error' | 'success';
	message: string;
	source?: string;
}

export type SidebarTab = 'overview' | 'agents' | 'settings' | 'new-task';

interface Props {
	projectName?: string;
	projectStatus?: string;
	projectTarget?: string;
	projectTags?: string[];
	agents?: Agent[];
	logs?: LogEntry[];
	activeTab?: SidebarTab;
	editingTask?: Task | null;
	onSearch?: (query: string) => void;
	onTaskSave?: (task: Task) => void;
	onTaskDelete?: (taskId: string) => void;
	agentLogs?: AgentLogEntry[];
	agentRuns?: AgentRun[];
	tasks?: Task[];
	agentTaskTitle?: string;
	isAgentRunning?: boolean;
}

const {
	projectName = 'vibe-kanban',
	projectStatus = 'V3 Redesign',
	projectTarget = 'High Contrast',
	projectTags = ['React', 'Tailwind', 'MCP'],
	agents = [],
	logs = [],
	activeTab = 'overview',
	editingTask = null,
	onSearch,
	onTaskSave,
	onTaskDelete,
	agentLogs = [],
	agentRuns = [],
	tasks = [],
	agentTaskTitle = '',
	isAgentRunning = false,
}: Props = $props();

// Resize state
let sidebarWidth = $state(320);
let isResizing = $state(false);

function handleMouseDown(e: MouseEvent) {
	isResizing = true;
	e.preventDefault();
}

function handleMouseMove(e: MouseEvent) {
	if (!isResizing) return;
	const newWidth = window.innerWidth - e.clientX;
	sidebarWidth = Math.max(280, Math.min(600, newWidth));
}

function handleMouseUp() {
	isResizing = false;
}

function handleKeyDown(e: KeyboardEvent) {
	const step = e.shiftKey ? 50 : 10;
	if (e.key === 'ArrowLeft') {
		sidebarWidth = Math.min(600, sidebarWidth + step);
		e.preventDefault();
	} else if (e.key === 'ArrowRight') {
		sidebarWidth = Math.max(280, sidebarWidth - step);
		e.preventDefault();
	}
}
</script>

<svelte:window onmousemove={handleMouseMove} onmouseup={handleMouseUp} />

<aside
	class="border-l border-[var(--border-default)] bg-[var(--bg-elevated)] flex flex-col overflow-hidden relative"
	style="width: {sidebarWidth}px"
>
	<!-- Resize Handle -->
	<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<div
		class="absolute left-0 top-0 bottom-0 w-1 cursor-ew-resize hover:bg-[var(--accent-primary)] transition-colors z-10"
		class:bg-[var(--accent-primary)]={isResizing}
		onmousedown={handleMouseDown}
		onkeydown={handleKeyDown}
		role="separator"
		aria-orientation="vertical"
		aria-valuenow={sidebarWidth}
		aria-valuemin={280}
		aria-valuemax={600}
		aria-label="Resize sidebar"
		tabindex="0"
	></div>

	<!-- Content based on activeTab -->
	{#if activeTab === 'overview'}
		<div class="flex-1 flex flex-col min-h-0 overflow-hidden">
			<div class="py-3">
				<SearchBar {onSearch} />
			</div>
			<Separator.Root class="h-px bg-[var(--border-muted)]" />
			<div class="py-3">
				<ProjectOverview
					name={projectName}
					status={projectStatus}
					target={projectTarget}
					tags={projectTags}
				/>
			</div>
			<Separator.Root class="h-px bg-[var(--border-muted)]" />
			<div class="py-3 flex-1 min-h-0">
				<SystemLog {logs} />
			</div>
		</div>
	{:else if activeTab === 'agents'}
		<div class="flex-1 flex flex-col min-h-0">
			<AgentLog
				logs={agentLogs}
				runs={agentRuns}
				{tasks}
				taskTitle={agentTaskTitle}
				isRunning={isAgentRunning}
			/>
		</div>
	{:else if activeTab === 'settings'}
		<div class="flex-1 min-h-0 overflow-y-auto">
			<SettingsPanel />
		</div>
	{:else if activeTab === 'new-task'}
		<div class="flex-1 min-h-0 overflow-y-auto">
			<TaskEditor task={editingTask} onSave={onTaskSave} onDelete={onTaskDelete} />
		</div>
	{/if}
</aside>
