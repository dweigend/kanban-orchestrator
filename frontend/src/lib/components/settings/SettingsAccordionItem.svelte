<script lang="ts">
import { Accordion } from 'bits-ui';
import CaretDown from 'phosphor-svelte/lib/CaretDown';
import type { Component, Snippet } from 'svelte';

interface Props {
	value: string;
	title: string;
	// biome-ignore lint/suspicious/noExplicitAny: phosphor-svelte icons have varying prop types
	icon: Component<any>;
	isLast?: boolean;
	children: Snippet;
}

const { value, title, icon: Icon, isLast = false, children }: Props = $props();
</script>

<Accordion.Item {value} class="border border-[var(--border-muted)] rounded {isLast ? '' : 'mb-2'}">
	<Accordion.Header>
		<Accordion.Trigger
			class="flex items-center justify-between w-full px-4 py-3 hover:bg-[var(--bg-hover)] transition-colors group"
		>
			<div class="flex items-center gap-3">
				<Icon class="size-5 text-[var(--text-muted)]" />
				<span class="text-sm font-medium text-uppercase-tracking">{title}</span>
			</div>
			<CaretDown
				class="size-4 text-[var(--text-muted)] transition-transform group-data-[state=open]:rotate-180"
			/>
		</Accordion.Trigger>
	</Accordion.Header>
	<Accordion.Content class="border-t border-[var(--border-muted)] bg-[var(--bg-surface)]">
		<div class="p-4">
			{@render children()}
		</div>
	</Accordion.Content>
</Accordion.Item>
