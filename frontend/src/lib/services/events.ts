/**
 * SSE Event subscription for real-time updates
 */

import type { AgentLogEvent } from '$lib/types/agent';
import type { BackendTask, Task } from '$lib/types/task';
import { mapBackendToTask } from '$lib/types/task';

const API_BASE = 'http://localhost:8000';

export type EventType =
	| 'task_created'
	| 'task_updated'
	| 'task_deleted'
	| 'agent_log'
	| 'heartbeat';

export interface TaskEvent {
	type: EventType;
	task?: Task;
	taskId?: string;
	agentLog?: AgentLogEvent;
}

export type EventCallback = (event: TaskEvent) => void;

/**
 * Subscribe to real-time task events via SSE
 * Returns cleanup function to close connection
 */
export function subscribeToEvents(callback: EventCallback): () => void {
	const eventSource = new EventSource(`${API_BASE}/api/events`);

	eventSource.addEventListener('task_created', (e: MessageEvent) => {
		const data = JSON.parse(e.data) as BackendTask;
		callback({ type: 'task_created', task: mapBackendToTask(data) });
	});

	eventSource.addEventListener('task_updated', (e: MessageEvent) => {
		const data = JSON.parse(e.data) as BackendTask;
		callback({ type: 'task_updated', task: mapBackendToTask(data) });
	});

	eventSource.addEventListener('task_deleted', (e: MessageEvent) => {
		const data = JSON.parse(e.data) as { id: string };
		callback({ type: 'task_deleted', taskId: data.id });
	});

	eventSource.addEventListener('agent_log', (e: MessageEvent) => {
		const data = JSON.parse(e.data) as AgentLogEvent;
		callback({ type: 'agent_log', agentLog: data });
	});

	eventSource.addEventListener('heartbeat', () => {
		callback({ type: 'heartbeat' });
	});

	eventSource.onerror = () => {
		console.error('SSE connection error, will auto-reconnect...');
	};

	return () => eventSource.close();
}
