<script lang="ts">
	import { utils } from 'ethers';
	import {
		connected,
		chainData,
		defaultEvmStores,
		signerAddress,
		signer
	} from 'svelte-ethers-store';
	import { formatAddress } from '$lib/helpers/formatters';
	import { Button } from '$lib/components';

	let investAmount = '';
	let balance: string = '---';

	$: updateBalance($signer, $chainData);

	async function updateBalance(signer, chainData) {
		balance = '---';
		if (signer) {
			const rawBalance = await signer.getBalance();
			const value = utils.formatUnits(rawBalance, chainData.nativeCurrency.decimals);
			balance = `${value} ${chainData.nativeCurrency.symbol}`;
		}
	}
</script>

<section class="container">
	<div class="invest-widget">
		<div class="info">
			<p>
				<span class="label">Your account:</span><br />
				{formatAddress($signerAddress)}
			</p>
			<p>
				<span class="label">Wallet balance:</span><br />
				{balance}
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
				<Button label="Connect MetaMask" on:click={() => defaultEvmStores.setProvider()} />
			{/if}
			<Button disabled label="Deposit USDC" />
			<Button disabled label="Withdraw tokens" />
		</div>
	</div>
</section>

<style>
	.invest-widget {
		display: grid;
		grid-template-columns: 1fr auto;
		border-radius: 1rem;
		padding: 1.5rem;
		font-size: 18px;
		background: var(--c-accent);
	}

	.ctas {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.info p {
		margin: 0 0 1.5rem 0;
	}

	.info label,
	.info span.label {
		font-weight: bold;
	}

	.info input {
		font-family: monospace;
		font-size: inherit;
		padding: 0.25rem;
		width: 9em;
	}

	@media (max-width: 576px) {
		.invest-widget {
			grid-template-columns: auto;
		}
	}
</style>
