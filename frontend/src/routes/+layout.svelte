<script lang="ts">
import { Tooltip } from 'bits-ui';
import { Toaster } from 'svelte-sonner';
import './layout.css';
import favicon from '$lib/assets/favicon.svg';
import { initSchemaStore } from '$lib/stores/schema.svelte';

const { children } = $props();

// Initialize schema store on app startup
$effect(() => {
	initSchemaStore();
});
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
<Tooltip.Provider>
	{@render children()}
</Tooltip.Provider>
<Toaster position="bottom-right" richColors theme="dark" />
