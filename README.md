
## Domain links prepared October 31, 2026

This local project targets `https://warns.i4seer.com/`. Website links, metadata and page generators use the i4seer.com collection subdomains. The publisher bar links to i4Seer Home and all six collections, with a compact Collections menu on smaller screens. Family links open in the same tab; Amazon links remain unchanged. Local CNAME files are prepared for the target addresses. Deployment, GitHub Pages settings, DNS, redirects and validation are handled by the site owner. No deployment or validation is performed by this update. Historical verification records in docs retain their original addresses and dates.

## Common collection header

The Warns header uses the same brand, menu button and navigation structure as the other collection sites, with Warns colors and fonts. The i4Seer publisher bar sits above the site header. Home and map pages share this layout; neither overlays or darkens the publisher bar. The map begins below both navigation rows.

Run `python scripts/update_header.py` after changing the header template, navigation styles or menu behavior. It updates the shared navigation and active pages across all local headers, and refreshes stylesheet and script versions. It does not deploy, access GitHub, or run validation. Deployment and validation remain with the site owner.

People and Places share `/people-and-places/`, with jump links to each section. The old directory addresses forward to the corresponding section; individual person and place pages retain their addresses. The header links to the combined directory. Map access is available from Harmon, where named places link to their map markers, and from existing content and footer links.
