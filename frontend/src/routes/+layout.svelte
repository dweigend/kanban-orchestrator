<script lang="ts">
import { Tooltip } from 'bits-ui';
import { untrack } from 'svelte';
import { Toaster } from 'svelte-sonner';
import './layout.css';
import favicon from '$lib/assets/favicon.svg';
import { initSchemaStore } from '$lib/stores/schema.svelte';
import {
	applySettings,
	loadBackendSettings,
	loadSettings,
} from '$lib/stores/settings.svelte';

const { children } = $props();

// Initialize stores on app startup (runs once, untracked to prevent re-runs)
$effect(() => {
	untrack(() => {
		initSchemaStore();
		loadSettings();
		applySettings();
		// Load backend settings (async, non-blocking)
		loadBackendSettings();
	});
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
