<script lang="ts">
import { Menubar, Separator, Tabs } from 'bits-ui';
import Folder from 'phosphor-svelte/lib/Folder';
import Gear from 'phosphor-svelte/lib/Gear';
import Plus from 'phosphor-svelte/lib/Plus';
import Sidebar from 'phosphor-svelte/lib/Sidebar';
import SquaresFour from 'phosphor-svelte/lib/SquaresFour';

interface Props {
	projectName?: string;
	viewMode?: string;
	onViewChange?: (mode: string) => void;
	onSettingsClick?: () => void;
	onSidebarToggle?: () => void;
}

const {
	projectName = 'vibe-kanban',
	viewMode = 'hub-view',
	onViewChange,
	onSettingsClick,
	onSidebarToggle,
}: Props = $props();
</script>

<header
	class="h-[var(--header-height)] border-b border-[var(--border-default)] bg-[var(--bg-elevated)] flex items-center justify-between px-4"
>
	<!-- Left: Logo & Breadcrumb -->
	<div class="flex items-center gap-4">
		<div class="flex items-center gap-2">
			<SquaresFour class="size-5 text-[var(--accent-primary)]" weight="fill" />
			<span class="font-semibold text-uppercase-tracking text-xs">Knowledge Orchestrator</span>
		</div>

		<Separator.Root class="h-4 w-px bg-[var(--border-default)]" orientation="vertical" />

		<nav class="flex items-center gap-2 text-[var(--text-secondary)] text-xs">
			<span>{projectName}</span>
			<span class="text-[var(--text-muted)]">/</span>
			<span class="text-[var(--text-primary)]">{viewMode}</span>
		</nav>
	</div>

	<!-- Center: View Toggle -->
	<Tabs.Root
		value={viewMode}
		onValueChange={(v) => onViewChange?.(v)}
		class="hidden md:block"
	>
		<Tabs.List
			class="flex items-center gap-1 rounded-md bg-[var(--bg-surface)] p-1 border border-[var(--border-muted)]"
		>
			<Tabs.Trigger
				value="hub-view"
				class="px-3 py-1.5 text-xs rounded transition-colors data-[state=active]:bg-[var(--bg-hover)] data-[state=active]:text-[var(--text-primary)] text-[var(--text-muted)] hover:text-[var(--text-secondary)]"
			>
				Hub View
			</Tabs.Trigger>
			<Tabs.Trigger
				value="board-view"
				class="px-3 py-1.5 text-xs rounded transition-colors data-[state=active]:bg-[var(--bg-hover)] data-[state=active]:text-[var(--text-primary)] text-[var(--text-muted)] hover:text-[var(--text-secondary)]"
			>
				Board View
			</Tabs.Trigger>
		</Tabs.List>
	</Tabs.Root>

	<!-- Right: Actions -->
	<div class="flex items-center gap-2">
		<Menubar.Root class="flex items-center gap-1">
			<Menubar.Menu>
				<Menubar.Trigger
					class="flex items-center gap-2 px-3 py-1.5 text-xs rounded border border-[var(--border-default)] hover:bg-[var(--bg-hover)] transition-colors"
				>
					<Folder class="size-4" />
					<span class="hidden sm:inline">Project</span>
				</Menubar.Trigger>
				<Menubar.Portal>
					<Menubar.Content
						class="z-50 min-w-[180px] rounded-md border border-[var(--border-default)] bg-[var(--bg-elevated)] p-1 shadow-lg animate-fade-in"
						align="end"
						sideOffset={4}
					>
						<Menubar.Item
							class="flex items-center gap-2 px-3 py-2 text-xs rounded cursor-pointer hover:bg-[var(--bg-hover)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors"
						>
							Open Recent
						</Menubar.Item>
						<Menubar.Item
							class="flex items-center gap-2 px-3 py-2 text-xs rounded cursor-pointer hover:bg-[var(--bg-hover)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors"
						>
							New Project
						</Menubar.Item>
						<Menubar.Separator class="my-1 h-px bg-[var(--border-muted)]" />
						<Menubar.Item
							class="flex items-center gap-2 px-3 py-2 text-xs rounded cursor-pointer hover:bg-[var(--bg-hover)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors"
						>
							Import
						</Menubar.Item>
					</Menubar.Content>
				</Menubar.Portal>
			</Menubar.Menu>
		</Menubar.Root>

		<button
			type="button"
			onclick={() => onSidebarToggle?.()}
			class="size-9 flex items-center justify-center rounded border border-[var(--border-default)] hover:bg-[var(--bg-hover)] transition-colors focus-ring"
			aria-label="Toggle sidebar"
		>
			<Sidebar class="size-4" />
		</button>

		<button
			type="button"
			class="size-9 flex items-center justify-center rounded border border-[var(--border-default)] hover:bg-[var(--bg-hover)] transition-colors focus-ring"
			aria-label="Add new task"
		>
			<Plus class="size-4" />
		</button>

		<button
			type="button"
			onclick={() => onSettingsClick?.()}
			class="size-9 flex items-center justify-center rounded border border-[var(--border-default)] hover:bg-[var(--bg-hover)] transition-colors focus-ring"
			aria-label="Settings"
		>
			<Gear class="size-4" />
		</button>

		<!-- User Avatar Placeholder -->
		<div
			class="size-9 rounded bg-[var(--accent-primary)] flex items-center justify-center text-xs font-bold text-[var(--text-inverse)]"
		>
			DW
		</div>
	</div>
</header>
