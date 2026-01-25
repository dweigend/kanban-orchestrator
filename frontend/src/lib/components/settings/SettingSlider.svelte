<script lang="ts">
import { Slider } from 'bits-ui';

interface Props {
	label: string;
	value: number;
	onValueChange: (value: number) => void;
	min: number;
	max: number;
	step?: number;
	unit?: string;
}

const {
	label,
	value,
	onValueChange,
	min,
	max,
	step = 1,
	unit = '',
}: Props = $props();
</script>

<div class="space-y-2">
	<div class="flex items-center justify-between">
		<span class="text-xs text-uppercase-tracking text-[var(--text-muted)]">
			{label}
		</span>
		<span
			class="px-2 py-1 text-xs border border-[var(--border-default)] rounded bg-[var(--bg-elevated)]"
		>
			{value}{unit}
		</span>
	</div>
	<Slider.Root
		type="single"
		{value}
		{onValueChange}
		{min}
		{max}
		{step}
		class="relative flex items-center w-full h-5 touch-none select-none"
	>
		<span
			class="relative h-1 w-full grow cursor-pointer overflow-hidden rounded-full bg-[var(--bg-surface)]"
		>
			<Slider.Range class="absolute h-full bg-[var(--accent-primary)]" />
		</span>
		<Slider.Thumb
			index={0}
			class="block size-4 rounded-full bg-[var(--accent-primary)] border-2 border-[var(--bg-elevated)] shadow-md focus-ring cursor-pointer"
		/>
	</Slider.Root>
</div>
