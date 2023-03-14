<script lang="ts">
	import backtestPerformanceChart from '$lib/assets/charts/backtest-performance.svg';
</script>

<section class="container backtest">
	<h2>Backtest performance</h2>
	<p>Strategy performance compared to various buy-and-hold benchmarks:</p>
	<ul>
		<li><span style:color="#008800">▬</span> Strategy</li>
		<li><span style:color="#880000">▬</span> MATIC</li>
		<li><span style:color="#ffa500">▬</span> ETC</li>
		<li><span style:color="#ff0000">▬</span> BTC</li>
		<li><span style:color="#000088">▬</span> USD (do nothing)</li>
	</ul>
	<img src={backtestPerformanceChart} alt="Backtest performance chart" />
</section>

<style>
	ul {
		list-style: none;
		margin: 0 0 0.5rem 0;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem 2rem;
		justify-content: space-around;
	}

	li span {
		display: inline-block;
		transform: scale(1.5, 1) translate(-2px, -1px);
	}
</style>
