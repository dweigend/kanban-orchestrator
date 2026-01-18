<script lang="ts">
import type { SchemaField } from '$lib/types/schema';

interface Props {
	field: SchemaField;
	value: string;
	error?: string;
	onchange: (value: string) => void;
}

const { field, value, error, onchange }: Props = $props();
const inputId = $derived(`field-${field.name}`);
</script>

<div class="space-y-2">
	<label for={inputId} class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
		{field.description || field.name}
		{#if field.required}<span class="text-red-400">*</span>{/if}
	</label>
	<input
		id={inputId}
		type="text"
		{value}
		oninput={(e) => onchange(e.currentTarget.value)}
		placeholder="Enter {field.name}..."
		class="w-full px-3 py-2 text-sm border rounded bg-[var(--bg-surface)] transition-colors
			{error
			? 'border-red-500 focus:border-red-500'
			: 'border-[var(--border-default)] focus:border-[var(--border-focus)]'}
			placeholder:text-[var(--text-muted)] focus:outline-none"
	/>
	{#if error}
		<p class="text-xs text-red-400">{error}</p>
	{/if}
</div>
