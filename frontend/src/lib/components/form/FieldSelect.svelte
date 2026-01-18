<script lang="ts">
import { Select } from 'bits-ui';
import CaretDown from 'phosphor-svelte/lib/CaretDown';
import Check from 'phosphor-svelte/lib/Check';
import type { SchemaField } from '$lib/types/schema';

interface Props {
	field: SchemaField;
	value: string;
	displayLabels?: Record<string, string>;
	onchange: (value: string) => void;
}

const { field, value, displayLabels = {}, onchange }: Props = $props();

const options = $derived(
	(field.options ?? []).map((opt) => ({
		value: opt,
		label: displayLabels[opt] ?? opt,
	})),
);

const selectedLabel = $derived(displayLabels[value] ?? value);
</script>

<div class="space-y-2">
	<span class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
		{field.description || field.name}
	</span>
	<Select.Root type="single" {value} items={options} onValueChange={(v) => v && onchange(v)}>
		<Select.Trigger
			class="flex items-center justify-between w-full px-3 py-2 border border-[var(--border-default)]
				rounded bg-[var(--bg-surface)] hover:border-[var(--border-focus)] transition-colors"
		>
			<span class="text-sm">{selectedLabel}</span>
			<CaretDown class="size-4 text-[var(--text-muted)]" />
		</Select.Trigger>
		<Select.Portal>
			<Select.Content
				class="z-[60] border border-[var(--border-default)] bg-[var(--bg-elevated)]
					rounded shadow-lg p-1 animate-fade-in"
				sideOffset={4}
			>
				<Select.Viewport>
					{#each options as option}
						<Select.Item
							value={option.value}
							label={option.label}
							class="flex items-center justify-between px-3 py-2 text-sm rounded
								cursor-pointer hover:bg-[var(--bg-hover)] transition-colors"
						>
							{#snippet children({ selected })}
								{option.label}
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
