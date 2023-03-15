<script lang="ts">
	import 'sanitize.css';
	import 'sanitize.css/typography.css';
	import '../app.css';
	import icon from '$lib/assets/icon.svg';
	import { Header, Footer } from '$lib/components';
</script>

<svelte:head>
	<link rel="icon" type="image/svg+xml" href={icon} />
	<title>Citade-sashimi</title>
</svelte:head>

<Header />
<slot />
<Footer />
