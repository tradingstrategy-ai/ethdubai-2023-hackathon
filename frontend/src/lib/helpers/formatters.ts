export function formatAddress(address: string | undefined) {
	if (!address) return '---';
	const pattern = /^(0x[a-zA-Z0-9]{4})[a-zA-Z0-9]+([a-zA-Z0-9]{4})$/;
	const match = address.match(pattern);
	return match ? `${match[1]}…${match[2]}` : address;
}
