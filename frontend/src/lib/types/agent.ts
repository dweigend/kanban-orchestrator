/**
 * Agent status indicators
 */
export type AgentStatus = 'active' | 'idle' | 'busy' | 'error';

/**
 * Agent type identifiers
 */
export type AgentType = 'orchestrator' | 'coder' | 'researcher' | 'architect';

/**
 * Agent model
 */
export interface Agent {
	id: string;
	name: string;
	type: AgentType;
	status: AgentStatus;
	current_task?: string;
	description?: string;
}

/**
 * Status color mapping
 */
export const AGENT_STATUS_COLORS: Record<AgentStatus, string> = {
	active: 'var(--status-active)',
	idle: 'var(--status-idle)',
	busy: 'var(--status-busy)',
	error: 'var(--status-error)',
};

/**
 * Agent icon mapping (Phosphor icon names)
 */
export const AGENT_TYPE_ICONS: Record<AgentType, string> = {
	orchestrator: 'GitBranch',
	coder: 'Code',
	researcher: 'MagnifyingGlass',
	architect: 'Blueprint',
};
