<script lang="ts">
import Board from '$lib/components/kanban/Board.svelte';
import Header from '$lib/components/layout/Header.svelte';
import FunctionPanel from '$lib/components/panel/FunctionPanel.svelte';
import type { Agent } from '$lib/types/agent';
import type { Task } from '$lib/types/task';

// State
let viewMode = $state('hub-view');
let sidebarVisible = $state(true);
let editingTask = $state<Task | null>(null);

// Mock data for demonstration
const tasks: Task[] = $state([
	{
		id: '04',
		title: 'Marktanalyse KI-Tools 2026',
		description: 'Comprehensive market analysis of AI tools in 2026',
		status: 'TODO',
		type: 'research',
		created_at: new Date().toISOString(),
	},
	{
		id: '22',
		title: 'Refactor Sidebar Component',
		description: 'Improve sidebar component structure and performance',
		status: 'TODO',
		type: 'dev',
		created_at: new Date().toISOString(),
	},
	{
		id: '15',
		title: 'Meeting Notizen: UX Sync',
		description: 'Notes from the weekly UX sync meeting',
		status: 'TODO',
		type: 'notes',
		created_at: new Date().toISOString(),
	},
	{
		id: '18',
		title: 'Baumarten Recherche',
		description: 'Research on different tree species for the project',
		status: 'IN_PROGRESS',
		type: 'research',
		created_at: new Date().toISOString(),
	},
	{
		id: '07',
		title: 'Dateistruktur Setup',
		description: 'Set up the file structure for the new module',
		status: 'DONE',
		type: 'dev',
		created_at: new Date().toISOString(),
	},
]);

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

// Handlers
function handleViewChange(mode: string) {
	viewMode = mode;
}

function handleSidebarToggle() {
	sidebarVisible = !sidebarVisible;
}

function handleAddTask() {
	// Create a new empty task for the editor
	const newTask: Task = {
		id: '', // Empty id = new task
		title: '',
		description: '',
		status: 'TODO',
		type: 'neutral',
		created_at: new Date().toISOString(),
	};
	editingTask = newTask;
	sidebarVisible = true; // Ensure sidebar is visible
}

function handleTaskSave(task: Task) {
	if (task.id === '') {
		// Create new task with generated ID
		const createdTask: Task = {
			...task,
			id: String(Date.now()), // Simple ID generation for now
		};
		tasks.push(createdTask);
	} else {
		// Update existing task
		const index = tasks.findIndex((t) => t.id === task.id);
		if (index !== -1) {
			tasks[index] = task;
		}
	}
	editingTask = null;
}

function handleTaskCancel() {
	editingTask = null;
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
		onViewChange={handleViewChange}
		onSidebarToggle={handleSidebarToggle}
		onAddTask={handleAddTask}
	/>

	<main class="flex-1 flex overflow-hidden">
		<Board {tasks} />

		{#if sidebarVisible}
			<FunctionPanel
				{agents}
				{logs}
				{editingTask}
				onSearch={handleSearch}
				onTaskSave={handleTaskSave}
				onTaskCancel={handleTaskCancel}
			/>
		{/if}
	</main>
</div>
