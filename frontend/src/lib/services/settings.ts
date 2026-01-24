/**
 * Settings API service for backend configuration
 */

import { request } from './api';

export interface GitSettings {
	auto_checkpoint: boolean;
	checkpoint_prefix: string;
}

export interface AgentSettings {
	max_turns: number;
	model: string;
}

export interface BackendSettings {
	git: GitSettings;
	agent: AgentSettings;
}

/**
 * Fetch current backend settings
 */
export async function fetchBackendSettings(): Promise<BackendSettings> {
	return request<BackendSettings>('/api/settings');
}

/**
 * Save backend settings
 */
export async function saveBackendSettings(
	settings: BackendSettings,
): Promise<BackendSettings> {
	return request<BackendSettings>('/api/settings', {
		method: 'POST',
		body: JSON.stringify(settings),
	});
}
