# Seer Warns Website — Modern Redesign

This build modernizes the existing Seer Warns site using the same broad design language as Seer Worlds while keeping Seer Warns adult, literary, and distinct.

## Design system

- Dark cinematic hero areas with warm paper content sections.
- EB Garamond remains the primary editorial typeface; Cinzel is used sparingly for navigation and labels.
- Deep ink/navy, warm cream, muted burgundy, and restrained gold replace the older mostly-flat paper treatment.
- Rounded cards, stronger spacing, responsive navigation, subtle shadows, and clearer call-to-action hierarchy.
- Mobile navigation uses the new shared `site.js` menu behavior.

## Image work

- `images/hero-home.webp`: new editorial composite built from the existing Harmon diner illustration and approved book covers.
- `images/hero-sub.webp`: optimized panoramic Harmon artwork for interior-page headers.
- `images/about-scene.webp`: professionally graded diner/Harmon illustration for About content.
- `images/harmon-map.webp`: optimized web version of the full Harmon map.
- `images/web/*.webp`: 20 optimized web-display book covers; the original 1600x2560 JPG covers remain in place as full-resolution source assets.
- `images/series-worlds.webp` and `images/series-frights.webp`: supporting art for the cross-series section.

## Site-wide updates

- Rebuilt the home page around the warning, Harmon, featured books, and the wider Seer catalog.
- Modernized all book, people, place, Harmon, Seer, About, and Press pages through the shared stylesheet.
- Added consistent responsive navigation and footer content across the site.
- Added Seer Worlds and Seer Frights links to the site-wide footer and the home page.
- Added a visual editorial block to About and a map-focused feature to Harmon.
- Added `robots.txt` and `sitemap.xml`.
- Preserved the interactive Leaflet map and its local libraries.

## October 22, 2026 refresh

- Synced all twenty front covers with the current SEERWARNS artwork; refreshed both the full-size JPGs and optimized WebP versions, with versioned references.
- Verified the six published books individually on Amazon in Kindle and paperback. Edition URLs and source paths are recorded in publication-sources.json. The Frights series URL supplied alongside Warns was excluded. Books 7–20 remain forthcoming.
- Added News, linked throughout the site, and updated the home page, book catalog, About publication status, and sitemap.
- Replaced the author biography with B. Carter’s supplied signed note.
- Rebuilt all twenty book pages with a title banner, cover/content columns, edition buttons, exact current cover copy, compact facts, and previous/next navigation. Existing cast, places, and story material remains in expandable story notes.
- Kept the Warns palette, typography, hero artwork, town pages, and interactive map.

### Latest cover refresh

All twenty website covers now use the front panels of the October 22 print-ready wraps. Extracted using each book’s print metadata, excluding the spine and bleed. Regenerated full-size JPG and optimized WebP assets, refreshed every cover URL version, and updated image dimensions to preserve the artwork’s proportions. Source paths and crop coordinates are recorded in publication-sources.json.

## October 26, 2026 artwork-only refresh

All 20 covers now use the current source cover-front.png exports, with full-size JPG and optimized WebP files. The home hero uses Book 1’s current clean kitchen illustration. Other editorial imagery, author, logo and map exports use the current source assets. Palette, type, layout, scripts and interactive map geometry are preserved. The stylesheet differs only in image cache versions; its normalized theme signature is recorded in data/warns-artwork.json. Run python scripts/sync_warns_artwork.py --source C:/SEERWARNS (Pillow, beautifulsoup4) to repeat. Purchase links and publication states are retained.
