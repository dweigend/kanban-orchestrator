/**
 * Agent API service for running tasks with Claude Agent SDK
 */

import type { AgentRun } from '$lib/types/agent';
import { request } from './api';

/**
 * Start an agent run for a task
 */
export async function startAgentRun(taskId: string): Promise<AgentRun> {
	return request<AgentRun>('/api/agent/run', {
		method: 'POST',
		body: JSON.stringify({ task_id: taskId }),
	});
}

/**
 * Stop a running agent
 */
export async function stopAgentRun(
	runId: string,
): Promise<{ success: boolean; status: string }> {
	return request<{ success: boolean; status: string }>(
		`/api/agent/stop/${runId}`,
		{
			method: 'POST',
		},
	);
}

/**
 * Get agent runs for a task
 */
export async function getAgentRuns(taskId?: string): Promise<AgentRun[]> {
	const params = taskId ? { task_id: taskId } : undefined;
	return request<AgentRun[]>('/api/agent/runs', { params });
}

/**
 * Get a specific agent run
 */
export async function getAgentRun(runId: string): Promise<AgentRun> {
	return request<AgentRun>(`/api/agent/runs/${runId}`);
}
