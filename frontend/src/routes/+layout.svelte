<script lang="ts">
import { Tooltip } from 'bits-ui';
import './layout.css';
import favicon from '$lib/assets/favicon.svg';

const { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
<Tooltip.Provider>
	{@render children()}
</Tooltip.Provider>
