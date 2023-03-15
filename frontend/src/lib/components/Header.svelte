<script lang="ts">
	import { Logo } from '$lib/components';
</script>

<header class="container">
	<a class="logo" href="/" aria-label="Home">
		<Logo />
	</a>
</header>

<style>
	header {
		padding-block: 2rem;
	}

	.logo {
		--logo-height: 4rem;
	}

	.logo,
	.logo:visited {
		color: white;
	}

	@media (max-width: 768px) {
		header {
			padding-block: 1rem;
		}

		.logo {
			--logo-height: 2.5rem;
		}
	}
</style>
