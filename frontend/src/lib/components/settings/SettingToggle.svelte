<script lang="ts">
import { Switch } from 'bits-ui';

interface Props {
	title: string;
	description: string;
	checked: boolean;
	onCheckedChange: (checked: boolean) => void;
}

const { title, description, checked, onCheckedChange }: Props = $props();
</script>

<div class="flex items-center justify-between">
	<div>
		<p class="text-sm font-medium">{title}</p>
		<p class="text-xs text-[var(--text-muted)]">{description}</p>
	</div>
	<Switch.Root
		{checked}
		{onCheckedChange}
		class="w-11 h-6 rounded-full bg-[var(--bg-surface)] border border-[var(--border-default)] data-[state=checked]:bg-[var(--accent-primary)] transition-colors"
	>
		<Switch.Thumb
			class="block size-5 rounded-full bg-white shadow-md transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0.5"
		/>
	</Switch.Root>
</div>
