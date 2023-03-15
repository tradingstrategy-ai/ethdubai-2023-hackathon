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
			Veritatis, sequi, laborum cum laboriosam veniam ipsum optio accusantium officiis at accusamus
			voluptates nesciunt. Voluptatem, eius modi! Architecto illo pariatur ipsa obcaecati.
		</p>
	</section>

	<Backtest />

	<section class="container">
		<h2>Strategy execution and source code</h2>
		<p>
			Soluta nesciunt aliquam unde, dolor commodi obcaecati error porro, accusamus nam tenetur a
			magni explicabo vero labore similique eveniet ullam dignissimos officiis?
		</p>
	</section>
</main>
