<script lang="ts">
	export let disabled: boolean | undefined = undefined;
	export let rel: string | undefined = undefined;
	export let href: string | undefined = undefined;
	export let label: string = '';
	export let submit = false;
	export let target: string | undefined = undefined;

	$: tag = href && !disabled ? 'a' : 'button';
</script>

<svelte:element
	this={tag}
	class="button"
	{href}
	{target}
	{rel}
	{disabled}
	type={submit ? 'submit' : undefined}
	on:click
>
	<slot>{label}</slot>
</svelte:element>

<style>
	.button {
		display: inline-block;
		padding: 0.5rem 1.5rem;
		border: 1px solid transparent;
		border-radius: 1.5rem;
		background: var(--button-background, #dddddd);
		font: inherit;
		font-weight: 600;
		letter-spacing: 0.02em;
		cursor: pointer;
		transition: all 0.25s;
	}

	.button:hover,
	.button:focus {
		filter: brightness(90%);
		outline: none;
	}

	.button:active {
		opacity: 0.8;
	}

	.button[disabled] {
		color: inherit;
		filter: none;
		opacity: 0.65;
		cursor: not-allowed;
	}

	@media (max-width: 768px) {
		.button {
			padding: 0.25rem 1rem;
			font-size: 14px;
		}
	}
</style>
