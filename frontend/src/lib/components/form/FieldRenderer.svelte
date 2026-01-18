<script lang="ts">
import type { SchemaField } from '$lib/types/schema';
import FieldDatetime from './FieldDatetime.svelte';
import FieldReadonly from './FieldReadonly.svelte';
import FieldSelect from './FieldSelect.svelte';
import FieldText from './FieldText.svelte';
import FieldTextarea from './FieldTextarea.svelte';

interface Props {
	field: SchemaField;
	value: string | undefined;
	error?: string;
	displayLabels?: Record<string, string>;
	onchange?: (value: string) => void;
}

const { field, value, error, displayLabels, onchange }: Props = $props();

// No-op handler for readonly fields
const noop = () => {};
</script>

{#if field.type === 'text'}
	<FieldText {field} value={value ?? ''} {error} onchange={onchange ?? noop} />
{:else if field.type === 'textarea'}
	<FieldTextarea {field} value={value ?? ''} onchange={onchange ?? noop} />
{:else if field.type === 'select'}
	<FieldSelect {field} value={value ?? ''} {displayLabels} onchange={onchange ?? noop} />
{:else if field.type === 'readonly'}
	<FieldReadonly {field} {value} />
{:else if field.type === 'datetime'}
	<FieldDatetime {field} {value} />
{/if}
