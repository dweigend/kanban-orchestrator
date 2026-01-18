<script lang="ts">
import type { SchemaField } from '$lib/types/schema';

interface Props {
	field: SchemaField;
	value: string | undefined;
}

const { field, value }: Props = $props();
</script>

{#if value}
	<div class="space-y-2">
		<span class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
			{field.description || field.name}
		</span>
		<div
			class="w-full px-3 py-2 text-sm border border-[var(--border-default)]
				rounded bg-[var(--bg-base)] whitespace-pre-wrap"
		>
			{value}
		</div>
	</div>
{/if}
