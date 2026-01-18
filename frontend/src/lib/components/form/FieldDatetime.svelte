<script lang="ts">
import type { SchemaField } from '$lib/types/schema';

interface Props {
	field: SchemaField;
	value: string | undefined;
}

const { field, value }: Props = $props();

const formattedDate = $derived(value ? new Date(value).toLocaleString() : '');
</script>

{#if value}
	<div class="space-y-2">
		<span class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
			{field.description || field.name}
		</span>
		<div class="px-3 py-2 text-sm text-[var(--text-muted)]">
			{formattedDate}
		</div>
	</div>
{/if}
