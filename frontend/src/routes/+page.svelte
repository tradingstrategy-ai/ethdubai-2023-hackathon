<script lang="ts">
	import InvestWidget from './InvestWidget.svelte';
	import Backtest from './Backtest.svelte';
</script>

<main>
	<header class="container">
		<h1>ETHDubai 2023 hackathon</h1>
	</header>

	<InvestWidget />

	<section class="container">
		<h2>About this strategy</h2>
		<p>
			Lorem ipsum dolor sit amet consectetur adipisicing elit. Labore eius deserunt praesentium
			soluta cupiditate excepturi magnam ducimus nulla aspernatur voluptas, odio voluptate nobis
			adipisci distinctio ex vel rem ipsam ullam.
		</p>
	</section>

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
