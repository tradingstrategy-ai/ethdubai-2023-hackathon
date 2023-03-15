<section class="container">
	<h2>About this strategy</h2>
	<p>
		This
		<a
			href="https://github.com/tradingstrategy-ai/ethdubai-2023-hackathon/blob/master/notebook/ethdubai-hackathon.ipynb"
			>example trading strategy</a
		>
		is based on a
		<a href="https://tradingstrategy.ai/glossary/portfolio-construction">portfolio construction</a> methodology.
		It trades using Sushi DEX on Polygon. As a long-only strategy, it only trades in a bull market, indicated
		by MATIC token 15 days simple moving average (SMA) price. The strategy identifies the top three assets
		based on alpha signals and allocates them to a weighted portfolio using 1/nth method. Stop loss is
		triggered at 3%, while profits are taken at 33%. The strategy maintain a 50% cash buffer, and only
		invests in assets with a minimum available liquidity of 300k USD.
	</p>
</section>
