<script lang="ts">
import { Select } from 'bits-ui';
import CaretDown from 'phosphor-svelte/lib/CaretDown';
import Check from 'phosphor-svelte/lib/Check';

interface SelectOption {
	value: string;
	label: string;
}

interface Props {
	label: string;
	value: string;
	onValueChange: (value: string) => void;
	options: SelectOption[];
}

const { label, value, onValueChange, options }: Props = $props();

const selectedLabel = $derived(
	options.find((o) => o.value === value)?.label ?? 'Select...',
);
</script>

<div class="space-y-2">
	<span class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
		{label}
	</span>
	<Select.Root type="single" {value} {onValueChange} items={options}>
		<Select.Trigger
			class="flex items-center justify-between w-full px-3 py-2 border border-[var(--border-default)] rounded bg-[var(--bg-elevated)] hover:border-[var(--border-focus)] transition-colors"
		>
			<span class="text-sm">{selectedLabel}</span>
			<CaretDown class="size-4 text-[var(--text-muted)]" />
		</Select.Trigger>
		<Select.Portal>
			<Select.Content
				class="z-[60] border border-[var(--border-default)] bg-[var(--bg-elevated)] rounded shadow-lg p-1 animate-fade-in"
				sideOffset={4}
			>
				<Select.Viewport>
					{#each options as option}
						<Select.Item
							value={option.value}
							label={option.label}
							class="flex items-center justify-between px-3 py-2 text-sm rounded cursor-pointer hover:bg-[var(--bg-hover)] transition-colors"
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
