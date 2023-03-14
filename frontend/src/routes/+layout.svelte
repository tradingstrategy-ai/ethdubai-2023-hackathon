<script lang="ts">
	import 'sanitize.css';
	import 'sanitize.css/typography.css';
	import '../app.css';
	import { Header, Footer } from '$lib/components';
</script>

<Header />
<slot />
<Footer />
