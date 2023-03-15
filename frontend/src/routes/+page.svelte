<script lang="ts">
	import InvestWidget from './InvestWidget.svelte';
	import Backtest from './Backtest.svelte';
	import AboutStrategy from './AboutStrategy.svelte';
</script>

<main>
	<header class="container">
		<h1>ETHDubai 2023 hackathon</h1>
	</header>

	<InvestWidget />
	<AboutStrategy />

	<section class="container">
		<h2>Current performance</h2>
		<p>
			<strong>Not enough data.</strong>
		</p>
		<p>
			This strategy has not been running long enough to gather sufficient live trading performance
			data. Strategies may do trades weekly or monthly and it will take several rebalance cycles to
			refelct the true performance.
		</p>
	</section>

	<Backtest />

	<section class="container">
		<h2>Strategy execution and source code</h2>
		<p>
			View <a
				href="https://github.com/tradingstrategy-ai/ethdubai-2023-hackathon/blob/master/notebook/ethdubai-hackathon.ipynb"
				>strategy notebook source code</a
			> on GitHub.
		</p>
	</section>
</main>
