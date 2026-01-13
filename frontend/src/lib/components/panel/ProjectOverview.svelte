<script lang="ts">
import { Accordion } from 'bits-ui';
import CaretDown from 'phosphor-svelte/lib/CaretDown';

interface Props {
	name: string;
	status?: string;
	target?: string;
	tags?: string[];
}

const {
	name,
	status = 'Active',
	target = 'High Contrast',
	tags = [],
}: Props = $props();
</script>

<section class="space-y-2">
	<header class="flex items-center gap-2 px-3">
		<span class="text-xs text-[var(--text-muted)]">◉</span>
		<span class="text-xs text-uppercase-tracking text-[var(--text-secondary)]">Overview</span>
	</header>

	<Accordion.Root type="single" class="px-3">
		<Accordion.Item
			value="project-details"
			class="border border-[var(--border-muted)] rounded overflow-hidden"
		>
			<Accordion.Header>
				<Accordion.Trigger
					class="flex items-center justify-between w-full px-3 py-3 bg-[var(--bg-surface)] hover:bg-[var(--bg-hover)] transition-colors group"
				>
					<span class="text-sm font-medium text-[var(--text-primary)]">{name}</span>
					<CaretDown
						class="size-4 text-[var(--text-muted)] transition-transform group-data-[state=open]:rotate-180"
					/>
				</Accordion.Trigger>
			</Accordion.Header>
			<Accordion.Content
				class="bg-[var(--bg-elevated)] data-[state=open]:animate-slide-in overflow-hidden"
			>
				<div class="px-3 py-3 space-y-2 text-xs">
					<div class="flex items-center gap-2">
						<span class="text-[var(--text-muted)]">//</span>
						<span class="text-[var(--text-secondary)]">Status:</span>
						<span class="text-[var(--text-primary)]">{status}</span>
					</div>
					<div class="flex items-center gap-2">
						<span class="text-[var(--text-muted)]">//</span>
						<span class="text-[var(--text-secondary)]">Target:</span>
						<span class="text-[var(--text-primary)]">{target}</span>
					</div>

					{#if tags.length > 0}
						<div class="flex items-center gap-2 pt-2">
							{#each tags as tag}
								<span
									class="px-2 py-1 rounded border border-[var(--border-muted)] text-[var(--text-muted)]"
								>
									{tag}
								</span>
							{/each}
						</div>
					{/if}
				</div>
			</Accordion.Content>
		</Accordion.Item>
	</Accordion.Root>
</section>
