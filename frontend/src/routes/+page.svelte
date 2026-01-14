<script lang="ts">
import Board from '$lib/components/kanban/Board.svelte';
import Header, { type SidebarTab } from '$lib/components/layout/Header.svelte';
import FunctionPanel from '$lib/components/panel/FunctionPanel.svelte';
import { subscribeToEvents } from '$lib/services/events';
import * as taskApi from '$lib/services/tasks';
import type { Agent } from '$lib/types/agent';
import type { Task } from '$lib/types/task';

// UI State
let viewMode = $state('hub-view');
let sidebarVisible = $state(true);
let activeTab = $state<SidebarTab>('overview');
let editingTask = $state<Task | null>(null);

// Data State
let tasks = $state<Task[]>([]);
let loading = $state(true);
let error = $state<string | null>(null);

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
	error = null;
	try {
		tasks = await taskApi.fetchTasks();
	} catch (e) {
		error = e instanceof Error ? e.message : 'Failed to load tasks';
		console.error('Failed to load tasks:', e);
	} finally {
		loading = false;
	}
}

// Initial load
$effect(() => {
	loadTasks();
});

// SSE subscription for real-time updates
$effect(() => {
	const unsubscribe = subscribeToEvents((event) => {
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
					tasks = tasks.map((t) =>
						t.id === event.task!.id
							? { ...event.task!, type: t.type, description: t.description }
							: t,
					);
				}
				break;
			case 'task_deleted':
				if (event.taskId) {
					tasks = tasks.filter((t) => t.id !== event.taskId);
				}
				break;
		}
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
	error = null;
	try {
		if (!task.id || task.id === '') {
			// Create new task - SSE will add it to the list (avoid duplicate)
			await taskApi.createTask(task);
		} else {
			// Update existing task
			const updated = await taskApi.updateTask(task.id, task);
			// Preserve local-only fields
			tasks = tasks.map((t) =>
				t.id === updated.id
					? { ...updated, type: task.type, description: task.description }
					: t,
			);
		}
		// Reset UI state after successful save
		activeTab = 'overview';
		editingTask = null;
	} catch (e) {
		error = e instanceof Error ? e.message : 'Failed to save task';
		console.error('Failed to save task:', e);
	}
}

async function handleTaskDelete(taskId: string) {
	error = null;
	try {
		await taskApi.deleteTask(taskId);
		// SSE will remove from list, but also update locally for immediate feedback
		tasks = tasks.filter((t) => t.id !== taskId);
		editingTask = null;
		activeTab = 'overview';
	} catch (e) {
		error = e instanceof Error ? e.message : 'Failed to delete task';
		console.error('Failed to delete task:', e);
	}
}

function handleSearch(query: string) {
	console.log('Search:', query);
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
		{:else if error}
			<div class="flex-1 flex flex-col items-center justify-center gap-4">
				<p class="text-red-400">{error}</p>
				<button
					type="button"
					onclick={loadTasks}
					class="px-4 py-2 text-sm border border-[var(--border-default)] rounded hover:bg-[var(--bg-hover)] transition-colors"
				>
					Retry
				</button>
			</div>
		{:else}
			<Board {tasks} />
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
			/>
		{/if}
	</main>
</div>
