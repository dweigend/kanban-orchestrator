/**
 * SSE Event subscription for real-time updates
 * Includes exponential backoff reconnection logic
 */

import type { AgentLogEvent } from '$lib/types/agent';
import type { BackendTask, Task } from '$lib/types/task';
import { mapBackendToTask } from '$lib/types/task';

const API_BASE = 'http://localhost:8000';

// Reconnection config
const INITIAL_RETRY_DELAY = 1000; // 1 second
const MAX_RETRY_DELAY = 30000; // 30 seconds
const BACKOFF_MULTIPLIER = 2;

export type EventType =
	| 'task_created'
	| 'task_updated'
	| 'task_deleted'
	| 'agent_log'
	| 'heartbeat';

export type ConnectionState = 'connected' | 'connecting' | 'disconnected';

export interface TaskEvent {
	type: EventType;
	task?: Task;
	taskId?: string;
	agentLog?: AgentLogEvent;
}

export type EventCallback = (event: TaskEvent) => void;
export type ConnectionCallback = (state: ConnectionState) => void;

interface SubscribeOptions {
	onEvent: EventCallback;
	onConnectionChange?: ConnectionCallback;
}

/**
 * Subscribe to real-time task events via SSE
 * Returns cleanup function to close connection
 *
 * Features:
 * - Exponential backoff reconnection (1s → 2s → 4s → ... → 30s max)
 * - Connection state callbacks for UI feedback
 * - Automatic retry on disconnect
 */
export function subscribeToEvents(options: SubscribeOptions): () => void {
	const { onEvent, onConnectionChange } = options;

	let eventSource: EventSource | null = null;
	let retryDelay = INITIAL_RETRY_DELAY;
	let retryTimeout: ReturnType<typeof setTimeout> | null = null;
	let isCleanedUp = false;

	function setConnectionState(state: ConnectionState): void {
		onConnectionChange?.(state);
	}

	function setupEventSource(): void {
		if (isCleanedUp) return;

		setConnectionState('connecting');
		eventSource = new EventSource(`${API_BASE}/api/events`);

		eventSource.onopen = () => {
			setConnectionState('connected');
			retryDelay = INITIAL_RETRY_DELAY; // Reset backoff on successful connection
		};

		eventSource.addEventListener('task_created', (e: MessageEvent) => {
			const data = JSON.parse(e.data) as BackendTask;
			onEvent({ type: 'task_created', task: mapBackendToTask(data) });
		});

		eventSource.addEventListener('task_updated', (e: MessageEvent) => {
			const data = JSON.parse(e.data) as BackendTask;
			onEvent({ type: 'task_updated', task: mapBackendToTask(data) });
		});

		eventSource.addEventListener('task_deleted', (e: MessageEvent) => {
			const data = JSON.parse(e.data) as { id: string };
			onEvent({ type: 'task_deleted', taskId: data.id });
		});

		eventSource.addEventListener('agent_log', (e: MessageEvent) => {
			const data = JSON.parse(e.data) as AgentLogEvent;
			onEvent({ type: 'agent_log', agentLog: data });
		});

		eventSource.addEventListener('heartbeat', () => {
			onEvent({ type: 'heartbeat' });
		});

		eventSource.onerror = () => {
			if (isCleanedUp) return;

			setConnectionState('disconnected');
			eventSource?.close();
			eventSource = null;

			// Schedule reconnect with exponential backoff
			console.warn(`SSE disconnected, retrying in ${retryDelay / 1000}s...`);
			retryTimeout = setTimeout(() => {
				retryDelay = Math.min(retryDelay * BACKOFF_MULTIPLIER, MAX_RETRY_DELAY);
				setupEventSource();
			}, retryDelay);
		};
	}

	// Initial connection
	setupEventSource();

	// Return cleanup function
	return () => {
		isCleanedUp = true;
		if (retryTimeout) {
			clearTimeout(retryTimeout);
			retryTimeout = null;
		}
		if (eventSource) {
			eventSource.close();
			eventSource = null;
		}
		setConnectionState('disconnected');
	};
}

/**
 * Legacy API - simple subscription without connection state callbacks
 * @deprecated Use subscribeToEvents({ onEvent, onConnectionChange }) instead
 */
export function subscribeToEventsSimple(callback: EventCallback): () => void {
	return subscribeToEvents({ onEvent: callback });
}
