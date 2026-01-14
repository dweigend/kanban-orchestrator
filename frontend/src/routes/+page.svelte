<script lang="ts">
import Board from '$lib/components/kanban/Board.svelte';
import Header, { type SidebarTab } from '$lib/components/layout/Header.svelte';
import FunctionPanel from '$lib/components/panel/FunctionPanel.svelte';
import { subscribeToEvents } from '$lib/services/events';
import * as taskApi from '$lib/services/tasks';
import { showError, showSuccess } from '$lib/services/toast';
import type { Agent } from '$lib/types/agent';
import type { Task, TaskStatus } from '$lib/types/task';

// UI State
let viewMode = $state('hub-view');
let sidebarVisible = $state(true);
let activeTab = $state<SidebarTab>('overview');
let editingTask = $state<Task | null>(null);

// Data State
let tasks = $state<Task[]>([]);
let loading = $state(true);

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
	try {
		if (!task.id || task.id === '') {
			await taskApi.createTask(task);
			showSuccess('Task created');
		} else {
			const updated = await taskApi.updateTask(task.id, task);
			tasks = tasks.map((t) =>
				t.id === updated.id
					? { ...updated, type: task.type, description: task.description }
					: t,
			);
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
		tasks = tasks.map((t) =>
			t.id === taskId
				? { ...updated, type: task.type, description: task.description }
				: t,
		);
		showSuccess('Task moved');
	} catch (e) {
		showError(e instanceof Error ? e.message : 'Failed to move task');
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
		{:else}
			<Board
				{tasks}
				onEditTask={handleEditTask}
				onDeleteTask={handleDeleteTaskFromBoard}
				onTaskDrop={handleTaskDrop}
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
			/>
		{/if}
	</main>
</div>
