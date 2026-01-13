<script lang="ts">
import { ScrollArea, Tooltip } from 'bits-ui';
import Blueprint from 'phosphor-svelte/lib/Blueprint';
import Code from 'phosphor-svelte/lib/Code';
import GitBranch from 'phosphor-svelte/lib/GitBranch';
import MagnifyingGlass from 'phosphor-svelte/lib/MagnifyingGlass';
import type { Agent, AgentType } from '$lib/types/agent';
import { AGENT_STATUS_COLORS } from '$lib/types/agent';

interface Props {
	agents: Agent[];
}

const { agents }: Props = $props();

const typeIcons: Record<AgentType, typeof GitBranch> = {
	orchestrator: GitBranch,
	coder: Code,
	researcher: MagnifyingGlass,
	architect: Blueprint,
};

function getStatusLabel(status: Agent['status']): string {
	return status.charAt(0).toUpperCase() + status.slice(1);
}
</script>

<section class="space-y-2">
	<header class="flex items-center gap-2 px-3">
		<span class="text-xs text-[var(--text-muted)]">✦</span>
		<span class="text-xs text-uppercase-tracking text-[var(--text-secondary)]">Active Agents</span>
	</header>

	<ScrollArea.Root class="max-h-[200px]">
		<ScrollArea.Viewport class="px-3 space-y-1">
			{#each agents as agent (agent.id)}
				{@const Icon = typeIcons[agent.type]}
				<Tooltip.Root delayDuration={300}>
					<Tooltip.Trigger
						class="w-full text-left"
					>
						<div
							class="flex items-center gap-3 px-3 py-2 rounded border border-[var(--border-muted)] bg-[var(--bg-surface)] hover:border-[var(--border-default)] transition-colors cursor-default"
							class:border-l-2={agent.status === 'busy'}
							style={agent.status === 'busy' ? `border-left-color: ${AGENT_STATUS_COLORS.busy}` : ''}
						>
							<div
								class="size-8 flex items-center justify-center rounded bg-[var(--bg-elevated)]"
								style="color: {AGENT_STATUS_COLORS[agent.status]}"
							>
								<Icon class="size-4" weight={agent.status === 'busy' ? 'fill' : 'regular'} />
							</div>

							<div class="flex-1 min-w-0">
								<div class="flex items-center gap-2">
									<span class="text-sm text-[var(--text-primary)] truncate">{agent.name}</span>
									{#if agent.status === 'busy'}
										<span
											class="px-1.5 py-0.5 text-[10px] rounded bg-orange-500/20 text-orange-400 font-medium"
										>
											BUSY
										</span>
									{/if}
								</div>
								{#if agent.current_task}
									<p class="text-xs text-[var(--text-muted)] truncate">
										› {agent.current_task}
									</p>
								{/if}
							</div>
						</div>
					</Tooltip.Trigger>
					<Tooltip.Portal>
						<Tooltip.Content
							class="z-50 max-w-[240px] rounded border border-[var(--border-default)] bg-[var(--bg-elevated)] px-3 py-2 text-xs shadow-lg animate-fade-in"
							sideOffset={4}
						>
							<p class="font-medium text-[var(--text-primary)]">{agent.name}</p>
							<p class="text-[var(--text-muted)] mt-1">
								Status: {getStatusLabel(agent.status)}
							</p>
							{#if agent.description}
								<p class="text-[var(--text-secondary)] mt-1">{agent.description}</p>
							{/if}
							<Tooltip.Arrow class="fill-[var(--bg-elevated)] stroke-[var(--border-default)]" />
						</Tooltip.Content>
					</Tooltip.Portal>
				</Tooltip.Root>
			{/each}
		</ScrollArea.Viewport>
		<ScrollArea.Scrollbar
			orientation="vertical"
			class="w-1.5 touch-none select-none p-px"
		>
			<ScrollArea.Thumb class="bg-[var(--border-default)] rounded-full" />
		</ScrollArea.Scrollbar>
	</ScrollArea.Root>
</section>
