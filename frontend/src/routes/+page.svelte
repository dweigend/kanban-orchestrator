<script lang="ts">
import Board from '$lib/components/kanban/Board.svelte';
import Header, { type SidebarTab } from '$lib/components/layout/Header.svelte';
import FunctionPanel from '$lib/components/panel/FunctionPanel.svelte';
import * as agentApi from '$lib/services/agent';
import { type ConnectionState, subscribeToEvents } from '$lib/services/events';
import * as taskApi from '$lib/services/tasks';
import { showError, showSuccess } from '$lib/services/toast';
import { isSchemaReady } from '$lib/stores/schema.svelte';
import type { Agent, AgentLogEntry, AgentRun } from '$lib/types/agent';
import type { Task, TaskStatus } from '$lib/types/task';

// UI State
let viewMode = $state('hub-view');
let sidebarVisible = $state(true);
let activeTab = $state<SidebarTab>('overview');
let editingTask = $state<Task | null>(null);

// Data State
let tasks = $state<Task[]>([]);
let loading = $state(true);

// Agent State
let runningAgentTaskId = $state<string | null>(null);
let agentLogs = $state<AgentLogEntry[]>([]);
let currentAgentTaskTitle = $state<string>('');
let agentRuns = $state<AgentRun[]>([]);

// Connection State
let connectionState = $state<ConnectionState>('connecting');

// Mock agents (will be connected to backend later)
const agents: Agent[] = $state([
	{
		id: '1',
		name: 'Architect',
		type: 'architect',
		status: 'idle',
		description: 'System architecture and design patterns',
	},
	{
		id: '2',
		name: 'Coder',
		type: 'coder',
		status: 'busy',
		current_task: 'refactoring sidebar_component.tsx',
		description: 'Code implementation and refactoring',
	},
	{
		id: '3',
		name: 'Researcher',
		type: 'researcher',
		status: 'idle',
		description: 'Research and documentation',
	},
]);

// Mock logs (will be connected to backend later)
const logs = $state([
	{
		id: '1',
		timestamp: new Date(Date.now() - 60000).toISOString(),
		level: 'success' as const,
		message: 'Python Interpreter connected successfully',
	},
	{
		id: '2',
		timestamp: new Date(Date.now() - 30000).toISOString(),
		level: 'info' as const,
		message: 'Web Search: "Tailwind CSS high contrast"',
		source: 'Researcher',
	},
	{
		id: '3',
		timestamp: new Date().toISOString(),
		level: 'error' as const,
		message: 'PostgreSQL: Connection timeout (5432)',
	},
]);

// Load tasks on mount
async function loadTasks() {
	loading = true;
	try {
		tasks = await taskApi.fetchTasks();
	} catch (e) {
		showError(e instanceof Error ? e.message : 'Failed to load tasks');
	} finally {
		loading = false;
	}
}

// Load agent runs history
async function loadAgentRuns() {
	try {
		agentRuns = await agentApi.getAgentRuns();
	} catch (e) {
		console.error('Failed to load agent runs:', e);
	}
}

// Initial load (wait for schema to be ready)
$effect(() => {
	if (isSchemaReady()) {
		loadTasks();
		loadAgentRuns();
	}
});

// SSE subscription for real-time updates
$effect(() => {
	const unsubscribe = subscribeToEvents({
		onEvent: (event) => {
			switch (event.type) {
				case 'task_created':
					if (event.task) {
						// Only add if not already present (avoid duplicates from own actions)
						if (!tasks.find((t) => t.id === event.task!.id)) {
							tasks = [...tasks, event.task];
						}
					}
					break;
				case 'task_updated':
					if (event.task) {
						// Backend now includes type, so use it directly
						tasks = tasks.map((t) =>
							t.id === event.task!.id ? event.task! : t,
						);
					}
					break;
				case 'task_deleted':
					if (event.taskId) {
						tasks = tasks.filter((t) => t.id !== event.taskId);
					}
					break;
				case 'agent_log':
					if (event.agentLog) {
						const { task_id, log } = event.agentLog;
						// Only collect logs for currently running task
						if (task_id === runningAgentTaskId) {
							agentLogs = [...agentLogs, log];
						}
						// Agent finished?
						if (log.type === 'result' || log.type === 'error') {
							runningAgentTaskId = null;
						}
					}
					break;
			}
		},
		onConnectionChange: (state) => {
			connectionState = state;
			if (state === 'disconnected') {
				showError('Connection lost. Reconnecting...');
			} else if (state === 'connected') {
				// Reload tasks after reconnection to ensure consistency
				loadTasks();
			}
		},
	});

	return unsubscribe;
});

// Handlers
function handleViewChange(mode: string) {
	viewMode = mode;
}

function handleTabChange(tab: SidebarTab) {
	activeTab = tab;
	if (!sidebarVisible) {
		sidebarVisible = true;
	}
	if (tab !== 'new-task') {
		editingTask = null;
	}
}

function handleSidebarToggle() {
	sidebarVisible = !sidebarVisible;
}

async function handleTaskSave(task: Task) {
	try {
		if (!task.id || task.id === '') {
			await taskApi.createTask(task);
			showSuccess('Task created');
		} else {
			const updated = await taskApi.updateTask(task.id, task);
			// Backend now stores type and description, use response directly
			tasks = tasks.map((t) => (t.id === updated.id ? updated : t));
			showSuccess('Task updated');
		}
		activeTab = 'overview';
		editingTask = null;
	} catch (e) {
		showError(e instanceof Error ? e.message : 'Failed to save task');
	}
}

async function handleTaskDelete(taskId: string) {
	try {
		await taskApi.deleteTask(taskId);
		tasks = tasks.filter((t) => t.id !== taskId);
		editingTask = null;
		activeTab = 'overview';
		showSuccess('Task deleted');
	} catch (e) {
		showError(e instanceof Error ? e.message : 'Failed to delete task');
	}
}

function handleAddTask(status: TaskStatus) {
	// Create empty task with pre-selected status for the column
	editingTask = {
		id: '',
		title: '',
		description: '',
		status: status,
		type: 'neutral',
		created_at: new Date().toISOString(),
	};
	activeTab = 'new-task';
	if (!sidebarVisible) {
		sidebarVisible = true;
	}
}

function handleEditTask(task: Task) {
	editingTask = task;
	activeTab = 'new-task';
	if (!sidebarVisible) {
		sidebarVisible = true;
	}
}

function handleDeleteTaskFromBoard(task: Task) {
	handleTaskDelete(task.id);
}

async function handleTaskDrop(taskId: string, newStatus: TaskStatus) {
	const task = tasks.find((t) => t.id === taskId);
	if (!task || task.status === newStatus) return;

	try {
		const updated = await taskApi.updateTask(taskId, { status: newStatus });
		// Backend returns full task with type and description
		tasks = tasks.map((t) => (t.id === taskId ? updated : t));
		showSuccess('Task moved');
	} catch (e) {
		showError(e instanceof Error ? e.message : 'Failed to move task');
	}
}

function handleSearch(query: string) {
	console.log('Search:', query);
}

async function handleRunAgent(task: Task) {
	if (runningAgentTaskId) {
		showError('Agent is already running');
		return;
	}

	try {
		// Reset logs & set running state
		agentLogs = [];
		runningAgentTaskId = task.id;
		currentAgentTaskTitle = task.title;

		// Switch to agents tab
		activeTab = 'agents';
		if (!sidebarVisible) {
			sidebarVisible = true;
		}

		// Start agent
		const run = await agentApi.startAgentRun(task.id);
		showSuccess(`Agent started: ${run.id.slice(0, 8)}`);
	} catch (e) {
		runningAgentTaskId = null;
		showError(e instanceof Error ? e.message : 'Failed to start agent');
	}
}
</script>

<svelte:head>
	<title>Knowledge Orchestrator</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<div class="h-screen flex flex-col overflow-hidden">
	<Header
		projectName="vibe-kanban"
		{viewMode}
		{activeTab}
		{sidebarVisible}
		onViewChange={handleViewChange}
		onTabChange={handleTabChange}
		onSidebarToggle={handleSidebarToggle}
	/>

	<main class="flex-1 flex overflow-hidden">
		{#if loading}
			<div class="flex-1 flex items-center justify-center text-[var(--text-muted)]">
				Loading tasks...
			</div>
		{:else}
			<Board
				{tasks}
				onAddTask={handleAddTask}
				onEditTask={handleEditTask}
				onDeleteTask={handleDeleteTaskFromBoard}
				onTaskDrop={handleTaskDrop}
				onRunAgent={handleRunAgent}
				{runningAgentTaskId}
			/>
		{/if}

		{#if sidebarVisible}
			<FunctionPanel
				{agents}
				{logs}
				{activeTab}
				{editingTask}
				onSearch={handleSearch}
				onTaskSave={handleTaskSave}
				onTaskDelete={handleTaskDelete}
				{agentLogs}
				{agentRuns}
				{tasks}
				agentTaskTitle={currentAgentTaskTitle}
				isAgentRunning={runningAgentTaskId !== null}
			/>
		{/if}
	</main>
</div>
