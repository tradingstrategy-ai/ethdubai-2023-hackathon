<script lang="ts">
	import { connected, defaultEvmStores, signerAddress } from 'svelte-ethers-store';
	import { formatAddress } from '$lib/helpers/formatters';
	import { Button } from '$lib/components';
</script>

<section class="container">
	<div class="invest-widget">
		<div class="info">
			<p><strong>Your account:</strong> {formatAddress($signerAddress)}</p>
		</div>

		<div class="ctas">
			{#if $connected && $signerAddress}
				<Button label="Disconnect wallet" on:click={() => defaultEvmStores.disconnect()} />
			{:else}
				<Button label="Connect wallet" on:click={() => defaultEvmStores.setProvider()} />
			{/if}
			<Button disabled label="Deposit MATIC" />
			<Button disabled label="Withsraw tokens" />
		</div>
	</div>
</section>

<style>
	.invest-widget {
		display: grid;
		grid-template-columns: 1fr auto;
		border-radius: 1rem;
		padding: 1.5rem;
		background: #eee;
	}

	.ctas {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
</style>
