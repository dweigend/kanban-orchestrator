<script lang="ts">
import { Accordion } from 'bits-ui';
import Bell from 'phosphor-svelte/lib/Bell';
import Code from 'phosphor-svelte/lib/Code';
import GitBranch from 'phosphor-svelte/lib/GitBranch';
import Robot from 'phosphor-svelte/lib/Robot';
import ShieldCheck from 'phosphor-svelte/lib/ShieldCheck';
import { showError, showSuccess } from '$lib/services/toast';
import {
	agentModelOptions,
	applySettings,
	fontOptions,
	getSettings,
	saveBackendSettings,
	saveSettings,
	setAgentMaxTurns,
	setAgentModel,
	setAnalytics,
	setFontFamily,
	setFontSize,
	setGitAutoCheckpoint,
	setNotifications,
} from '$lib/stores/settings.svelte';
import SettingSelect from './SettingSelect.svelte';
import SettingSlider from './SettingSlider.svelte';
import SettingsAccordionItem from './SettingsAccordionItem.svelte';
import SettingToggle from './SettingToggle.svelte';

// Reactive settings
const settings = $derived(getSettings());

// Handlers with side effects
function handleFontFamilyChange(value: string) {
	setFontFamily(value);
	applySettings();
}

function handleFontSizeChange(value: number) {
	setFontSize(value);
	applySettings();
}

async function handleSave() {
	try {
		saveSettings();
		await saveBackendSettings();
		showSuccess('Settings saved');
	} catch {
		showError('Failed to save backend settings');
	}
}
</script>

<div class="p-4">
	<!-- Header -->
	<div class="flex items-center justify-between mb-4">
		<h2 class="text-sm font-semibold text-uppercase-tracking">Settings</h2>
		<button
			type="button"
			onclick={handleSave}
			class="px-3 py-1.5 text-xs bg-[var(--accent-primary)] text-[var(--text-inverse)] rounded hover:bg-[var(--accent-hover)] transition-colors font-medium"
		>
			SAVE
		</button>
	</div>

	<Accordion.Root type="multiple" value={['editor']}>
		<!-- Editor Config -->
		<SettingsAccordionItem value="editor" title="Editor Config" icon={Code}>
			<div class="space-y-5">
				<SettingSelect
					label="Font Family"
					value={settings.fontFamily}
					onValueChange={handleFontFamilyChange}
					options={fontOptions}
				/>
				<SettingSlider
					label="Font Size"
					value={settings.fontSize}
					onValueChange={handleFontSizeChange}
					min={10}
					max={24}
					unit="px"
				/>
			</div>
		</SettingsAccordionItem>

		<!-- Git & Versioning -->
		<SettingsAccordionItem value="git" title="Git & Versioning" icon={GitBranch}>
			<SettingToggle
				title="Auto Checkpoint"
				description="Create git commits before agent runs"
				checked={settings.gitAutoCheckpoint}
				onCheckedChange={setGitAutoCheckpoint}
			/>
		</SettingsAccordionItem>

		<!-- Agent Config -->
		<SettingsAccordionItem value="agent" title="Agent Config" icon={Robot}>
			<div class="space-y-5">
				<SettingSelect
					label="Agent Model"
					value={settings.agentModel}
					onValueChange={setAgentModel}
					options={agentModelOptions}
				/>
				<SettingSlider
					label="Max Agent Turns"
					value={settings.agentMaxTurns}
					onValueChange={setAgentMaxTurns}
					min={1}
					max={50}
				/>
			</div>
		</SettingsAccordionItem>

		<!-- Notifications -->
		<SettingsAccordionItem value="notifications" title="Notifications" icon={Bell}>
			<SettingToggle
				title="Enable Notifications"
				description="Receive task updates"
				checked={settings.notifications}
				onCheckedChange={setNotifications}
			/>
		</SettingsAccordionItem>

		<!-- Privacy -->
		<SettingsAccordionItem value="privacy" title="Privacy" icon={ShieldCheck} isLast>
			<SettingToggle
				title="Analytics"
				description="Help improve the app"
				checked={settings.analytics}
				onCheckedChange={setAnalytics}
			/>
		</SettingsAccordionItem>
	</Accordion.Root>
</div>
