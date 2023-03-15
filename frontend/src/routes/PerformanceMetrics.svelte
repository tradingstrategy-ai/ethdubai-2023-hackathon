<section class="container">
	<h2>Strategy Performance Metrics</h2>

	<div class="tables">
		<table class="table-1">
			<tr>
				<th>Trading period length</th>
				<td>396 days</td>
			</tr>
			<tr>
				<th>Return %</th>
				<td>64.76%</td>
			</tr>
			<tr>
				<th>Annualised return %</th>
				<td>59.69%</td>
			</tr>
			<tr>
				<th>Cash at start</th>
				<td>$10,000.00</td>
			</tr>
			<tr>
				<th>Value at end</th>
				<td>$16,476.20</td>
			</tr>
			<tr>
				<th>Trade volume</th>
				<td>$404,971.56</td>
			</tr>
			<tr>
				<th>Trade win percent</th>
				<td>34.00%</td>
			</tr>
			<tr>
				<th>Total trades done</th>
				<td>50</td>
			</tr>
			<tr>
				<th>Won trades</th>
				<td>17</td>
			</tr>
			<tr>
				<th>Lost trades</th>
				<td>33</td>
			</tr>
			<tr>
				<th>Stop losses triggered</th>
				<td>33</td>
			</tr>
			<tr>
				<th>Stop loss % of all</th>
				<td>66.00%</td>
			</tr>
			<tr>
				<th>Stop loss % of lost</th>
				<td>100.00%</td>
			</tr>
			<tr>
				<th>Take profits triggered</th>
				<td>6</td>
			</tr>
			<tr>
				<th>Take profit % of all</th>
				<td>12.00%</td>
			</tr>
			<tr>
				<th>Take profit % of win</th>
				<td>35.29%</td>
			</tr>
			<tr>
				<th>Zero profit trades</th>
				<td>0</td>
			</tr>
			<tr>
				<th>Positions open at the end</th>
				<td>1</td>
			</tr>
			<tr>
				<th>Realised profit and loss</th>
				<td>$6,476.20</td>
			</tr>
		</table>

		<table class="table-2">
			<tr>
				<th>Portfolio unrealised value</th>
				<td>$8,238.10</td>
			</tr>
			<tr>
				<th>Extra returns on lending pool interest</th>
				<td>$0.00</td>
			</tr>
			<tr>
				<th>Cash left at the end</th>
				<td>$8,238.10</td>
			</tr>
			<tr>
				<th>Average winning trade profit %</th>
				<td>17.25%</td>
			</tr>
			<tr>
				<th>Average losing trade loss %</th>
				<td>-4.25%</td>
			</tr>
			<tr>
				<th>Biggest winning trade %</th>
				<td>44.19%</td>
			</tr>
			<tr>
				<th>Biggest losing trade %</th>
				<td>-6.08%</td>
			</tr>
			<tr>
				<th>Average duration of winning trades</th>
				<td>3 days</td>
			</tr>
			<tr>
				<th>Average duration of losing trades</th>
				<td>1 days</td>
			</tr>
			<tr>
				<th>LP fees paid</th>
				<td>$1,051.67</td>
			</tr>
			<tr>
				<th>LP fees paid % of volume</th>
				<td>0.26%</td>
			</tr>
			<tr>
				<th>Average trade:</th>
				<td>3.06%</td>
			</tr>
			<tr>
				<th>Median trade:</th>
				<td>-3.86%</td>
			</tr>
			<tr>
				<th>Consecutive wins</th>
				<td>4</td>
			</tr>
			<tr>
				<th>Consecutive losses</th>
				<td>9</td>
			</tr>
			<tr>
				<th>Biggest realized risk</th>
				<td>-2.15%</td>
			</tr>
			<tr>
				<th>Avg realised risk</th>
				<td>-1.04%</td>
			</tr>
			<tr>
				<th>Max pullback of total capital</th>
				<td>-10.39%</td>
			</tr>
			<tr>
				<th>Max loss risk at opening of position</th>
				<td>1.65%</td>
			</tr>
		</table>
	</div>
</section>

<style>
	.tables {
		display: grid;
		grid-template-columns: 1fr 1fr;
		overflow: auto;
		--c-alt-row-color: rgba(255, 255, 255, 0.05);
	}

	table {
		table-layout: fixed;
	}

	table tr:nth-child(odd) {
		background-color: var(--c-alt-row-color);
	}

	th,
	td {
		padding: 0.5rem 0.5rem;
		white-space: nowrap;
	}

	table th {
		text-align: left;
		width: 70%;
	}

	table td {
		text-align: right;
	}

	.table-1 td {
		padding-right: 2rem;
	}

	.table-2 th {
		padding-left: 2rem;
	}

	@media (max-width: 800px) {
		.tables {
			grid-template-columns: auto;
			gap: 0;
		}

		.table-1 td {
			padding-right: 1rem;
		}

		.table-2 th {
			padding-left: 1rem;
		}

		.table-2 tr:nth-child(odd) {
			background-color: var(--c-background);
		}
		.table-2 tr:nth-child(even) {
			background-color: var(--c-alt-row-color);
		}
	}
</style>
