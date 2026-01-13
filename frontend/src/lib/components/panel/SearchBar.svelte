<script lang="ts">
import MagnifyingGlass from 'phosphor-svelte/lib/MagnifyingGlass';

interface Props {
	placeholder?: string;
	onSearch?: (query: string) => void;
}

const { placeholder = 'Search knowledge base...', onSearch }: Props = $props();

let inputValue = $state('');

function handleKeydown(event: KeyboardEvent) {
	if (event.key === 'Enter' && inputValue.trim()) {
		onSearch?.(inputValue.trim());
	}
}
</script>

<div class="px-3">
	<div
		class="flex items-center gap-2 px-3 py-2 rounded border border-[var(--border-muted)] bg-[var(--bg-surface)] focus-within:border-[var(--border-focus)] transition-colors"
	>
		<MagnifyingGlass class="size-4 text-[var(--text-muted)] shrink-0" />
		<input
			type="text"
			bind:value={inputValue}
			onkeydown={handleKeydown}
			{placeholder}
			class="flex-1 bg-transparent text-sm text-[var(--text-primary)] placeholder:text-[var(--text-muted)] outline-none"
		/>
	</div>
</div>
