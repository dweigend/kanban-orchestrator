<script lang="ts">
import type { SchemaField } from '$lib/types/schema';

interface Props {
	field: SchemaField;
	value: string;
	onchange: (value: string) => void;
}

const { field, value, onchange }: Props = $props();
const inputId = $derived(`field-${field.name}`);
</script>

<div class="space-y-2">
	<label for={inputId} class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
		{field.description || field.name}
	</label>
	<textarea
		id={inputId}
		{value}
		oninput={(e) => onchange(e.currentTarget.value)}
		placeholder="Add {field.name}..."
		rows="4"
		class="w-full px-3 py-2 text-sm border border-[var(--border-default)] rounded
			bg-[var(--bg-surface)] focus:border-[var(--border-focus)] focus:outline-none
			placeholder:text-[var(--text-muted)] resize-none transition-colors"
	></textarea>
</div>
