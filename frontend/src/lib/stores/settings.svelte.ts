/**
 * Settings Store
 * Zentrale Verwaltung aller App-Settings mit localStorage-Persistenz
 */

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

// Settings State
let fontFamily = $state('jetbrains-mono');
let fontSize = $state(14);
let autoCommit = $state(false);
let notifications = $state(true);
let analytics = $state(false);

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
		fontFamily,
		fontSize,
		autoCommit,
		notifications,
		analytics,
	};
}

// Setters
export function setFontFamily(value: string) {
	fontFamily = value;
}

export function setFontSize(value: number) {
	fontSize = value;
}

export function setAutoCommit(value: boolean) {
	autoCommit = value;
}

export function setNotifications(value: boolean) {
	notifications = value;
}

export function setAnalytics(value: boolean) {
	analytics = value;
}

// Load from localStorage
export function loadSettings() {
	if (typeof window === 'undefined') return;

	const saved = localStorage.getItem(SETTINGS_KEY);
	if (!saved) return;

	try {
		const settings = JSON.parse(saved);
		fontFamily = settings.fontFamily ?? fontFamily;
		fontSize = settings.fontSize ?? fontSize;
		autoCommit = settings.autoCommit ?? autoCommit;
		notifications = settings.notifications ?? notifications;
		analytics = settings.analytics ?? analytics;
	} catch (e) {
		console.error('Failed to parse settings:', e);
	}
}

// Save to localStorage
export function saveSettings() {
	if (typeof window === 'undefined') return;

	const settings = {
		fontFamily,
		fontSize,
		autoCommit,
		notifications,
		analytics,
	};
	localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

// Apply settings to CSS custom properties
export function applySettings() {
	if (typeof document === 'undefined') return;

	document.documentElement.style.setProperty('--font-mono', getFontFamily());
	document.documentElement.style.setProperty('--font-size-sm', `${fontSize}px`);
}
