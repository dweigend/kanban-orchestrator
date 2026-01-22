<script lang="ts">
import { Tooltip } from 'bits-ui';
import { Toaster } from 'svelte-sonner';
import './layout.css';
import favicon from '$lib/assets/favicon.svg';
import { initSchemaStore } from '$lib/stores/schema.svelte';
import { applySettings, loadSettings } from '$lib/stores/settings.svelte';

const { children } = $props();

// Initialize stores on app startup (runs once)
$effect(() => {
	initSchemaStore();
	loadSettings();
	applySettings();
});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=Cascadia+Code:wght@400;500;600;700&family=Fira+Code:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Source+Code+Pro:wght@400;500;600;700&display=swap"
		rel="stylesheet"
	/>
</svelte:head>
<Tooltip.Provider>
	{@render children()}
</Tooltip.Provider>
<Toaster position="bottom-right" richColors theme="dark" />
