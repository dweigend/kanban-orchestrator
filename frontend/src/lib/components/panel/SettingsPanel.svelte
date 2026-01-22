<script lang="ts">
import { Accordion, Select, Separator, Slider, Switch } from 'bits-ui';
import Bell from 'phosphor-svelte/lib/Bell';
import CaretDown from 'phosphor-svelte/lib/CaretDown';
import Check from 'phosphor-svelte/lib/Check';
import Code from 'phosphor-svelte/lib/Code';
import GitBranch from 'phosphor-svelte/lib/GitBranch';
import Palette from 'phosphor-svelte/lib/Palette';
import ShieldCheck from 'phosphor-svelte/lib/ShieldCheck';
import { showSuccess } from '$lib/services/toast';

const SETTINGS_KEY = 'kanban-settings';

// Settings State (with defaults)
let fontFamily = $state('jetbrains-mono');
let fontSize = $state(14);
let lineNumbers = $state(true);
let wordWrap = $state(false);
let autoCommit = $state(false);
let notifications = $state(true);
let analytics = $state(false);

// Load settings from localStorage on mount
$effect(() => {
	const saved = localStorage.getItem(SETTINGS_KEY);
	if (saved) {
		try {
			const settings = JSON.parse(saved);
			fontFamily = settings.fontFamily ?? fontFamily;
			fontSize = settings.fontSize ?? fontSize;
			lineNumbers = settings.lineNumbers ?? lineNumbers;
			wordWrap = settings.wordWrap ?? wordWrap;
			autoCommit = settings.autoCommit ?? autoCommit;
			notifications = settings.notifications ?? notifications;
			analytics = settings.analytics ?? analytics;
		} catch (e) {
			console.error('Failed to parse settings:', e);
		}
	}
});

const fontOptions = [
	{ value: 'jetbrains-mono', label: 'JetBrains Mono' },
	{ value: 'fira-code', label: 'Fira Code' },
	{ value: 'source-code-pro', label: 'Source Code Pro' },
	{ value: 'cascadia-code', label: 'Cascadia Code' },
];

const selectedFontLabel = $derived(
	fontOptions.find((f) => f.value === fontFamily)?.label ?? 'Select font',
);

function handleSave() {
	const settings = {
		fontFamily,
		fontSize,
		lineNumbers,
		wordWrap,
		autoCommit,
		notifications,
		analytics,
	};
	localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
	showSuccess('Settings saved');
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
		<!-- Appearance -->
		<Accordion.Item value="appearance" class="border border-[var(--border-muted)] rounded mb-2">
			<Accordion.Header>
				<Accordion.Trigger
					class="flex items-center justify-between w-full px-4 py-3 hover:bg-[var(--bg-hover)] transition-colors group"
				>
					<div class="flex items-center gap-3">
						<Palette class="size-5 text-[var(--text-muted)]" />
						<span class="text-sm font-medium text-uppercase-tracking">Appearance</span>
					</div>
					<CaretDown
						class="size-4 text-[var(--text-muted)] transition-transform group-data-[state=open]:rotate-180"
					/>
				</Accordion.Trigger>
			</Accordion.Header>
			<Accordion.Content class="border-t border-[var(--border-muted)] bg-[var(--bg-surface)]">
				<div class="p-4 text-sm text-[var(--text-muted)]">
					Theme and visual settings coming soon...
				</div>
			</Accordion.Content>
		</Accordion.Item>

		<!-- Editor Config -->
		<Accordion.Item value="editor" class="border border-[var(--border-muted)] rounded mb-2">
			<Accordion.Header>
				<Accordion.Trigger
					class="flex items-center justify-between w-full px-4 py-3 hover:bg-[var(--bg-hover)] transition-colors group"
				>
					<div class="flex items-center gap-3">
						<Code class="size-5 text-[var(--text-muted)]" />
						<span class="text-sm font-medium text-uppercase-tracking">Editor Config</span>
					</div>
					<CaretDown
						class="size-4 text-[var(--text-muted)] transition-transform group-data-[state=open]:rotate-180"
					/>
				</Accordion.Trigger>
			</Accordion.Header>
			<Accordion.Content class="border-t border-[var(--border-muted)] bg-[var(--bg-surface)]">
				<div class="p-4 space-y-5">
					<!-- Font Family -->
					<div class="space-y-2">
						<span class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
							Font Family
						</span>
						<Select.Root type="single" bind:value={fontFamily} items={fontOptions}>
							<Select.Trigger
								class="flex items-center justify-between w-full px-3 py-2 border border-[var(--border-default)] rounded bg-[var(--bg-elevated)] hover:border-[var(--border-focus)] transition-colors"
							>
								<span class="text-sm">{selectedFontLabel}</span>
								<CaretDown class="size-4 text-[var(--text-muted)]" />
							</Select.Trigger>
							<Select.Portal>
								<Select.Content
									class="z-[60] border border-[var(--border-default)] bg-[var(--bg-elevated)] rounded shadow-lg p-1 animate-fade-in"
									sideOffset={4}
								>
									<Select.Viewport>
										{#each fontOptions as font}
											<Select.Item
												value={font.value}
												label={font.label}
												class="flex items-center justify-between px-3 py-2 text-sm rounded cursor-pointer hover:bg-[var(--bg-hover)] transition-colors"
											>
												{#snippet children({ selected })}
													{font.label}
													{#if selected}
														<Check class="size-4 text-[var(--accent-primary)]" />
													{/if}
												{/snippet}
											</Select.Item>
										{/each}
									</Select.Viewport>
								</Select.Content>
							</Select.Portal>
						</Select.Root>
					</div>

					<!-- Font Size -->
					<div class="space-y-2">
						<div class="flex items-center justify-between">
							<span class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
								Font Size
							</span>
							<span
								class="px-2 py-1 text-xs border border-[var(--border-default)] rounded bg-[var(--bg-elevated)]"
							>
								{fontSize}px
							</span>
						</div>
						<Slider.Root
							type="single"
							bind:value={fontSize}
							min={10}
							max={24}
							step={1}
							class="relative flex items-center w-full h-5 touch-none select-none"
						>
							<Slider.Range class="absolute h-1 rounded-full bg-[var(--accent-primary)]" />
							<Slider.Thumb
								index={0}
								class="block size-4 rounded-full bg-[var(--accent-primary)] border-2 border-[var(--bg-elevated)] shadow-md focus-ring cursor-pointer"
							/>
						</Slider.Root>
					</div>

					<Separator.Root class="h-px bg-[var(--border-muted)]" />

					<!-- Line Numbers -->
					<div class="flex items-center justify-between">
						<div>
							<p class="text-sm font-medium">Line Numbers</p>
							<p class="text-xs text-[var(--text-muted)]">Show gutter</p>
						</div>
						<Switch.Root
							bind:checked={lineNumbers}
							class="w-11 h-6 rounded-full bg-[var(--bg-surface)] border border-[var(--border-default)] data-[state=checked]:bg-[var(--accent-primary)] transition-colors"
						>
							<Switch.Thumb
								class="block size-5 rounded-full bg-white shadow-md transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0.5"
							/>
						</Switch.Root>
					</div>

					<!-- Word Wrap -->
					<div class="flex items-center justify-between">
						<div>
							<p class="text-sm font-medium">Word Wrap</p>
							<p class="text-xs text-[var(--text-muted)]">Soft wrap lines</p>
						</div>
						<Switch.Root
							bind:checked={wordWrap}
							class="w-11 h-6 rounded-full bg-[var(--bg-surface)] border border-[var(--border-default)] data-[state=checked]:bg-[var(--accent-primary)] transition-colors"
						>
							<Switch.Thumb
								class="block size-5 rounded-full bg-white shadow-md transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0.5"
							/>
						</Switch.Root>
					</div>
				</div>
			</Accordion.Content>
		</Accordion.Item>

		<!-- Git & Versioning -->
		<Accordion.Item value="git" class="border border-[var(--border-muted)] rounded mb-2">
			<Accordion.Header>
				<Accordion.Trigger
					class="flex items-center justify-between w-full px-4 py-3 hover:bg-[var(--bg-hover)] transition-colors group"
				>
					<div class="flex items-center gap-3">
						<GitBranch class="size-5 text-[var(--text-muted)]" />
						<span class="text-sm font-medium text-uppercase-tracking">Git & Versioning</span>
					</div>
					<CaretDown
						class="size-4 text-[var(--text-muted)] transition-transform group-data-[state=open]:rotate-180"
					/>
				</Accordion.Trigger>
			</Accordion.Header>
			<Accordion.Content class="border-t border-[var(--border-muted)] bg-[var(--bg-surface)]">
				<div class="p-4">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-sm font-medium">Auto Commit</p>
							<p class="text-xs text-[var(--text-muted)]">Commit changes automatically</p>
						</div>
						<Switch.Root
							bind:checked={autoCommit}
							class="w-11 h-6 rounded-full bg-[var(--bg-surface)] border border-[var(--border-default)] data-[state=checked]:bg-[var(--accent-primary)] transition-colors"
						>
							<Switch.Thumb
								class="block size-5 rounded-full bg-white shadow-md transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0.5"
							/>
						</Switch.Root>
					</div>
				</div>
			</Accordion.Content>
		</Accordion.Item>

		<!-- Notifications -->
		<Accordion.Item value="notifications" class="border border-[var(--border-muted)] rounded mb-2">
			<Accordion.Header>
				<Accordion.Trigger
					class="flex items-center justify-between w-full px-4 py-3 hover:bg-[var(--bg-hover)] transition-colors group"
				>
					<div class="flex items-center gap-3">
						<Bell class="size-5 text-[var(--text-muted)]" />
						<span class="text-sm font-medium text-uppercase-tracking">Notifications</span>
					</div>
					<CaretDown
						class="size-4 text-[var(--text-muted)] transition-transform group-data-[state=open]:rotate-180"
					/>
				</Accordion.Trigger>
			</Accordion.Header>
			<Accordion.Content class="border-t border-[var(--border-muted)] bg-[var(--bg-surface)]">
				<div class="p-4">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-sm font-medium">Enable Notifications</p>
							<p class="text-xs text-[var(--text-muted)]">Receive task updates</p>
						</div>
						<Switch.Root
							bind:checked={notifications}
							class="w-11 h-6 rounded-full bg-[var(--bg-surface)] border border-[var(--border-default)] data-[state=checked]:bg-[var(--accent-primary)] transition-colors"
						>
							<Switch.Thumb
								class="block size-5 rounded-full bg-white shadow-md transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0.5"
							/>
						</Switch.Root>
					</div>
				</div>
			</Accordion.Content>
		</Accordion.Item>

		<!-- Privacy -->
		<Accordion.Item value="privacy" class="border border-[var(--border-muted)] rounded">
			<Accordion.Header>
				<Accordion.Trigger
					class="flex items-center justify-between w-full px-4 py-3 hover:bg-[var(--bg-hover)] transition-colors group"
				>
					<div class="flex items-center gap-3">
						<ShieldCheck class="size-5 text-[var(--text-muted)]" />
						<span class="text-sm font-medium text-uppercase-tracking">Privacy</span>
					</div>
					<CaretDown
						class="size-4 text-[var(--text-muted)] transition-transform group-data-[state=open]:rotate-180"
					/>
				</Accordion.Trigger>
			</Accordion.Header>
			<Accordion.Content class="border-t border-[var(--border-muted)] bg-[var(--bg-surface)]">
				<div class="p-4">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-sm font-medium">Analytics</p>
							<p class="text-xs text-[var(--text-muted)]">Help improve the app</p>
						</div>
						<Switch.Root
							bind:checked={analytics}
							class="w-11 h-6 rounded-full bg-[var(--bg-surface)] border border-[var(--border-default)] data-[state=checked]:bg-[var(--accent-primary)] transition-colors"
						>
							<Switch.Thumb
								class="block size-5 rounded-full bg-white shadow-md transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0.5"
							/>
						</Switch.Root>
					</div>
				</div>
			</Accordion.Content>
		</Accordion.Item>
	</Accordion.Root>
</div>
