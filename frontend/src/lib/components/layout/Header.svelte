<script lang="ts">
import { Menubar, Separator } from 'bits-ui';
import Folder from 'phosphor-svelte/lib/Folder';
import Gauge from 'phosphor-svelte/lib/Gauge';
import Gear from 'phosphor-svelte/lib/Gear';
import Plus from 'phosphor-svelte/lib/Plus';
import Robot from 'phosphor-svelte/lib/Robot';
import SidebarSimple from 'phosphor-svelte/lib/SidebarSimple';
import SquaresFour from 'phosphor-svelte/lib/SquaresFour';

export type SidebarTab = 'overview' | 'agents' | 'settings' | 'new-task';

interface Props {
	activeTab?: SidebarTab;
	sidebarVisible?: boolean;
	onTabChange?: (tab: SidebarTab) => void;
	onSidebarToggle?: () => void;
}

const {
	activeTab = 'overview',
	sidebarVisible = true,
	onTabChange,
	onSidebarToggle,
}: Props = $props();

function handleTabClick(tab: SidebarTab) {
	onTabChange?.(tab);
}
</script>

<header
	class="h-[var(--header-height)] border-b border-[var(--border-default)] bg-[var(--bg-elevated)] flex items-center justify-between px-4"
>
	<!-- Left: Logo -->
	<div class="flex items-center gap-2">
		<SquaresFour class="size-5 text-[var(--accent-primary)]" weight="fill" />
		<span class="font-semibold text-uppercase-tracking text-xs hidden md:inline">Knowledge Orchestrator</span>
	</div>

	<!-- Right: Sidebar Controls + Actions -->
	<div class="flex items-center gap-1">
		<!-- Sidebar Tab Buttons -->
		<div class="flex items-center gap-1 mr-2">
			<button
				type="button"
				onclick={() => handleTabClick('overview')}
				class="size-9 flex items-center justify-center rounded transition-colors focus-ring
					{activeTab === 'overview' && sidebarVisible
					? 'bg-[var(--accent-primary)] text-[var(--text-inverse)]'
					: 'border border-[var(--border-default)] hover:bg-[var(--bg-hover)] text-[var(--text-muted)] hover:text-[var(--text-primary)]'}"
				title="Overview"
			>
				<Gauge class="size-4" />
			</button>
			<button
				type="button"
				onclick={() => handleTabClick('agents')}
				class="size-9 flex items-center justify-center rounded transition-colors focus-ring
					{activeTab === 'agents' && sidebarVisible
					? 'bg-[var(--accent-primary)] text-[var(--text-inverse)]'
					: 'border border-[var(--border-default)] hover:bg-[var(--bg-hover)] text-[var(--text-muted)] hover:text-[var(--text-primary)]'}"
				title="Agents"
			>
				<Robot class="size-4" />
			</button>
			<button
				type="button"
				onclick={() => handleTabClick('settings')}
				class="size-9 flex items-center justify-center rounded transition-colors focus-ring
					{activeTab === 'settings' && sidebarVisible
					? 'bg-[var(--accent-primary)] text-[var(--text-inverse)]'
					: 'border border-[var(--border-default)] hover:bg-[var(--bg-hover)] text-[var(--text-muted)] hover:text-[var(--text-primary)]'}"
				title="Settings"
			>
				<Gear class="size-4" />
			</button>
			<button
				type="button"
				onclick={() => handleTabClick('new-task')}
				class="size-9 flex items-center justify-center rounded transition-colors focus-ring
					{activeTab === 'new-task' && sidebarVisible
					? 'bg-[var(--accent-primary)] text-[var(--text-inverse)]'
					: 'border border-[var(--border-default)] hover:bg-[var(--bg-hover)] text-[var(--accent-primary)]'}"
				title="New Task"
			>
				<Plus class="size-4" />
			</button>
		</div>

		<Separator.Root class="h-6 w-px bg-[var(--border-default)]" orientation="vertical" />

		<!-- Sidebar Toggle -->
		<button
			type="button"
			onclick={() => onSidebarToggle?.()}
			class="size-9 flex items-center justify-center rounded border border-[var(--border-default)] hover:bg-[var(--bg-hover)] transition-colors focus-ring ml-2
				{sidebarVisible ? 'text-[var(--accent-primary)]' : 'text-[var(--text-muted)]'}"
			title={sidebarVisible ? 'Hide Sidebar' : 'Show Sidebar'}
		>
			<SidebarSimple class="size-4" weight={sidebarVisible ? 'fill' : 'regular'} />
		</button>

		<Separator.Root class="h-6 w-px bg-[var(--border-default)] ml-2" orientation="vertical" />

		<!-- Project Menu -->
		<Menubar.Root class="flex items-center gap-1 ml-2">
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

		<!-- User Avatar -->
		<div
			class="size-9 rounded bg-[var(--accent-primary)] flex items-center justify-center text-xs font-bold text-[var(--text-inverse)] ml-1"
		>
			DW
		</div>
	</div>
</header>
