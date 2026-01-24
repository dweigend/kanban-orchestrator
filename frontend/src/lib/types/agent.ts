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

// ─────────────────────────────────────────────────────────────
// Agent Run Types (for task execution)
// ─────────────────────────────────────────────────────────────

/**
 * Agent run status
 */
export type AgentRunStatus =
	| 'pending'
	| 'running'
	| 'needs_review'
	| 'completed'
	| 'failed'
	| 'cancelled';

/**
 * Agent run record
 */
export interface AgentRun {
	id: string;
	task_id: string;
	created_at: string;
	status: AgentRunStatus;
	logs?: string;
	error_message?: string;
	started_at: string | null;
	completed_at?: string;
}

/**
 * Agent log entry from SSE stream
 */
export interface AgentLogEntry {
	timestamp: string;
	type: string;
	content: string;
}

/**
 * SSE event for agent log
 */
export interface AgentLogEvent {
	task_id: string;
	agent_run_id: string;
	log: AgentLogEntry;
}
