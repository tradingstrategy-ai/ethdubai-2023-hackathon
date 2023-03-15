<script lang="ts">
	import backtestPerformanceChart from '$lib/assets/charts/backtest-performance.svg';
</script>

<section class="container backtest">
	<h2>Backtesting performance</h2>
	<p>Backtesting was performed on historical Sushi DEX / Poloygon trading data.</p>

	<h3>Backtesting key metrics</h3>

	<table class="key-metrics">
		<tr>
			<th>Backtesting period</th>
			<td>2022-01-01 - 2023-02-01 (396 days)</td>
		</tr>
		<tr>
			<th>Annualised estimated return</th>
			<td>64%</td>
		</tr>
		<tr>
			<th>LP fees paid</th>
			<td>~$1000 USD</td>
		</tr>
		<tr>
			<th>Max pullback</th>
			<td>-10%</td>
		</tr>
	</table>

	<h3>Strategy benchmark</h3>

	<p>Strategy performance compared to various buy-and-hold benchmarks:</p>

	<ul>
		<li><span style:color="#008800">▬</span> Strategy</li>
		<li><span style:color="#add8e6">▬</span> MATIC</li>
		<li><span style:color="#ffa500">▬</span> ETC</li>
		<li><span style:color="#ff0000">▬</span> BTC</li>
		<li><span style:color="#000088">▬</span> USD (do nothing)</li>
	</ul>
	<img src={backtestPerformanceChart} alt="Backtest performance chart" />
</section>

<style>
	ul {
		list-style: none;
		margin: 0.5rem 0;
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

	table {
		background: var(--c-accent);
		border-radius: 1rem;
		border-collapse: separate;
	}

	th,
	td {
		padding: 0.5rem 1rem;
	}

	th {
		text-align: left;
		width: 30%;
	}
</style>
