<script lang="ts">
	import { connected, defaultEvmStores, signerAddress } from 'svelte-ethers-store';
	import { formatAddress } from '$lib/helpers/formatters';
	import { Button } from '$lib/components';

	let investAmount = '';
</script>

<section class="container">
	<div class="invest-widget">
		<div class="info">
			<p>
				<span class="label">Your account:</span><br />
				{formatAddress($signerAddress)}
			</p>
			<p />
			<p>
				<span class="label">Wallet balance:</span><br />
				---
			</p>
			<p>
				<label for="invest-amount">Amount to invest:</label><br />
				<input id="invest-amount" type="number" bind:value={investAmount} disabled={!$connected} />
			</p>
			<p>
				<span class="label">Strategy vault address:</span><br />
				---
			</p>
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

	.info p {
		margin: 0 0 1.5rem 0;
		font-size: 18px;
	}

	.info label,
	.info span.label {
		font-weight: bold;
	}

	.info input {
		font-family: monospace;
		font-size: 18px;
		padding: 0.25rem;
	}
</style>
