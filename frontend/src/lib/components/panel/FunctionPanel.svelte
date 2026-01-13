<script lang="ts">
import { Separator, Tabs } from 'bits-ui';
import Gauge from 'phosphor-svelte/lib/Gauge';
import Gear from 'phosphor-svelte/lib/Gear';
import PencilSimple from 'phosphor-svelte/lib/PencilSimple';
import Robot from 'phosphor-svelte/lib/Robot';
import type { Agent } from '$lib/types/agent';
import type { Task } from '$lib/types/task';
import AgentList from './AgentList.svelte';
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

interface Props {
	projectName?: string;
	projectStatus?: string;
	projectTarget?: string;
	projectTags?: string[];
	agents?: Agent[];
	logs?: LogEntry[];
	editingTask?: Task | null;
	onSearch?: (query: string) => void;
	onTaskSave?: (task: Task) => void;
	onTaskCancel?: () => void;
}

const {
	projectName = 'vibe-kanban',
	projectStatus = 'V3 Redesign',
	projectTarget = 'High Contrast',
	projectTags = ['React', 'Tailwind', 'MCP'],
	agents = [],
	logs = [],
	editingTask = null,
	onSearch,
	onTaskSave,
	onTaskCancel,
}: Props = $props();

// Active tab - switches to 'editor' when editingTask is set
const activeTab = $derived(editingTask ? 'editor' : 'overview');
</script>

<aside
	class="w-[var(--sidebar-width)] border-l border-[var(--border-default)] bg-[var(--bg-elevated)] flex flex-col overflow-hidden"
>
	<Tabs.Root value={activeTab} class="flex flex-col h-full">
		<!-- Tab List -->
		<Tabs.List
			class="flex border-b border-[var(--border-muted)] bg-[var(--bg-surface)] shrink-0"
		>
			<Tabs.Trigger
				value="overview"
				class="flex items-center gap-1.5 px-3 py-2 text-xs text-uppercase-tracking text-[var(--text-muted)] hover:text-[var(--text-primary)] border-b-2 border-transparent data-[state=active]:border-[var(--accent-primary)] data-[state=active]:text-[var(--text-primary)] transition-colors"
			>
				<Gauge class="size-4" />
				Overview
			</Tabs.Trigger>
			<Tabs.Trigger
				value="agents"
				class="flex items-center gap-1.5 px-3 py-2 text-xs text-uppercase-tracking text-[var(--text-muted)] hover:text-[var(--text-primary)] border-b-2 border-transparent data-[state=active]:border-[var(--accent-primary)] data-[state=active]:text-[var(--text-primary)] transition-colors"
			>
				<Robot class="size-4" />
				Agents
			</Tabs.Trigger>
			<Tabs.Trigger
				value="settings"
				class="flex items-center gap-1.5 px-3 py-2 text-xs text-uppercase-tracking text-[var(--text-muted)] hover:text-[var(--text-primary)] border-b-2 border-transparent data-[state=active]:border-[var(--accent-primary)] data-[state=active]:text-[var(--text-primary)] transition-colors"
			>
				<Gear class="size-4" />
				Settings
			</Tabs.Trigger>
			{#if editingTask}
				<Tabs.Trigger
					value="editor"
					class="flex items-center gap-1.5 px-3 py-2 text-xs text-uppercase-tracking text-[var(--accent-primary)] border-b-2 border-transparent data-[state=active]:border-[var(--accent-primary)] transition-colors"
				>
					<PencilSimple class="size-4" />
					Edit Task
				</Tabs.Trigger>
			{/if}
		</Tabs.List>

		<!-- Overview Tab -->
		<Tabs.Content value="overview" class="flex-1 flex flex-col min-h-0 overflow-hidden">
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
		</Tabs.Content>

		<!-- Agents Tab -->
		<Tabs.Content value="agents" class="flex-1 flex flex-col min-h-0 overflow-y-auto p-3">
			<AgentList {agents} />
		</Tabs.Content>

		<!-- Settings Tab -->
		<Tabs.Content value="settings" class="flex-1 min-h-0 overflow-y-auto">
			<SettingsPanel />
		</Tabs.Content>

		<!-- Task Editor Tab (contextual) -->
		{#if editingTask}
			<Tabs.Content value="editor" class="flex-1 min-h-0 overflow-y-auto">
				<TaskEditor
					task={editingTask}
					onSave={onTaskSave}
					onCancel={onTaskCancel}
				/>
			</Tabs.Content>
		{/if}
	</Tabs.Root>
</aside>
