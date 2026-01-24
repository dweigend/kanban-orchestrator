/**
 * Settings Store
 * Zentrale Verwaltung aller App-Settings
 * - UI Settings: localStorage (fontFamily, fontSize, notifications, analytics)
 * - Backend Settings: API (git, agent config)
 */

import {
	type BackendSettings,
	fetchBackendSettings,
	saveBackendSettings as saveBackendSettingsApi,
} from '$lib/services/settings';

const SETTINGS_KEY = 'kanban-settings';

// Font Mapping
const FONT_MAP: Record<string, string> = {
	'jetbrains-mono': "'JetBrains Mono', ui-monospace, monospace",
	'fira-code': "'Fira Code', ui-monospace, monospace",
	'source-code-pro': "'Source Code Pro', ui-monospace, monospace",
	'cascadia-code': "'Cascadia Code', ui-monospace, monospace",
};

export const fontOptions = [
	{ value: 'jetbrains-mono', label: 'JetBrains Mono' },
	{ value: 'fira-code', label: 'Fira Code' },
	{ value: 'source-code-pro', label: 'Source Code Pro' },
	{ value: 'cascadia-code', label: 'Cascadia Code' },
];

// UI Settings State (localStorage)
let fontFamily = $state('jetbrains-mono');
let fontSize = $state(14);
let notifications = $state(true);
let analytics = $state(false);

// Backend Settings State (API)
let gitAutoCheckpoint = $state(true);
let gitCheckpointPrefix = $state('checkpoint:');
let agentMaxTurns = $state(10);
let agentModel = $state('claude-sonnet-4-20250514');

// Agent model options
export const agentModelOptions = [
	{ value: 'claude-sonnet-4-20250514', label: 'Claude Sonnet 4' },
	{ value: 'claude-opus-4-20250514', label: 'Claude Opus 4' },
];

// Derived: CSS-ready font family string
export function getFontFamily(): string {
	return FONT_MAP[fontFamily] ?? FONT_MAP['jetbrains-mono'];
}

// Derived: Font size in pixels
export function getFontSize(): number {
	return fontSize;
}

// Getters for reactive access
export function getSettings() {
	return {
		// UI Settings
		fontFamily,
		fontSize,
		notifications,
		analytics,
		// Backend Settings
		gitAutoCheckpoint,
		gitCheckpointPrefix,
		agentMaxTurns,
		agentModel,
	};
}

// Setters
export function setFontFamily(value: string) {
	fontFamily = value;
}

export function setFontSize(value: number) {
	fontSize = value;
}

export function setGitAutoCheckpoint(value: boolean) {
	gitAutoCheckpoint = value;
}

export function setGitCheckpointPrefix(value: string) {
	gitCheckpointPrefix = value;
}

export function setAgentMaxTurns(value: number) {
	agentMaxTurns = value;
}

export function setAgentModel(value: string) {
	agentModel = value;
}

export function setNotifications(value: boolean) {
	notifications = value;
}

export function setAnalytics(value: boolean) {
	analytics = value;
}

// Load UI settings from localStorage
export function loadSettings() {
	if (typeof window === 'undefined') return;

	const saved = localStorage.getItem(SETTINGS_KEY);
	if (!saved) return;

	try {
		const settings = JSON.parse(saved);
		fontFamily = settings.fontFamily ?? fontFamily;
		fontSize = settings.fontSize ?? fontSize;
		notifications = settings.notifications ?? notifications;
		analytics = settings.analytics ?? analytics;
	} catch (e) {
		console.error('Failed to parse settings:', e);
	}
}

// Load backend settings from API
export async function loadBackendSettings(): Promise<void> {
	try {
		const settings = await fetchBackendSettings();
		gitAutoCheckpoint = settings.git.auto_checkpoint;
		gitCheckpointPrefix = settings.git.checkpoint_prefix;
		agentMaxTurns = settings.agent.max_turns;
		agentModel = settings.agent.model;
	} catch (e) {
		console.error('Failed to load backend settings:', e);
	}
}

// Save UI settings to localStorage
export function saveSettings() {
	if (typeof window === 'undefined') return;

	const settings = {
		fontFamily,
		fontSize,
		notifications,
		analytics,
	};
	localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

// Save backend settings to API
export async function saveBackendSettings(): Promise<void> {
	const settings: BackendSettings = {
		git: {
			auto_checkpoint: gitAutoCheckpoint,
			checkpoint_prefix: gitCheckpointPrefix,
		},
		agent: {
			max_turns: agentMaxTurns,
			model: agentModel,
		},
	};
	await saveBackendSettingsApi(settings);
}

// Apply settings to CSS custom properties
export function applySettings() {
	if (typeof document === 'undefined') return;

	const fontValue = getFontFamily();
	// Set both CSS custom property and Tailwind theme variable
	document.documentElement.style.setProperty('--font-mono', fontValue);
	document.documentElement.style.setProperty('--font-family-mono', fontValue);
	document.documentElement.style.setProperty('--font-size-sm', `${fontSize}px`);
}
