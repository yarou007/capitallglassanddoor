# Validation results

Checked November 11, 2026 against the local static files. The original baseline contained 50 HTML pages; all remain at their original paths, plus three new requested location pages. No production deployment, Search Console account mutation or live contact was performed.

## Static checks

`python3 scripts/verify_site.py --baseline /tmp/cgd_baseline.json` passed:

- 53 HTML pages, 2,118 local references and 125 visible FAQ answers checked.
- All original HTML URLs and outgoing internal HTML destinations preserved.
- Unique page titles, meta descriptions and page-specific encoded WhatsApp drafts.
- Correct telephone/WhatsApp destinations; no fields, submission logic, SMS or email conversion actions.
- Valid JSON-LD; FAQ answers match visible accordions; public HTML and active JSON-LD contain no owner placeholders.
- No missing assets, broken local links/fragments, duplicate IDs or missing image dimensions/alt attributes.
- 47 intended indexable URLs in the sitemap; six deliberate noindex pages excluded.

`node --check assets/js/main.js` and `git diff --check` passed. The baseline file is an audit-session artifact; the checker also runs without it and needs only Python’s standard library.

## Browser and accessibility checks

53 pages × four viewports = **212 layout checks**, all passed:

- 360 × 640, 390 × 844, 430 × 932 and 1440 × 900.
- No horizontal scrolling, JavaScript exceptions or missing resource requests.
- Hero Call/WhatsApp controls fit above the mobile contact bar. All three hero service points also fit at 360 × 640.
- Contact controls use 54px minimum height. Mobile navigation opens/closes, closes on Escape/outside click and returns focus after Escape. FAQ accordions expand.
- Telephone and WhatsApp click hooks passed both the dataLayer and direct-gtag paths, with no duplicate event and no draft/query data in the payload. Ads targets remain empty.
- Call/WhatsApp links remain visible and usable without JavaScript.
- Axe WCAG A/AA checks found zero violations on the homepage, storefront page, Washington, DC location page, contact page, measuring article, work gallery and previous-work/review page. Automated checks do not replace review with real assistive technology.

The optional `scripts/browser_qa.py` uses an existing Playwright/Chrome installation; it is a development check, not a site dependency. Set `CHROME_PATH` to the installed browser and optionally `AXE_CORE_PATH` to a local `axe.min.js` to include those checks. Reports/screenshots go to the system temp directory or `CGD_QA_OUTPUT_DIR`.

## Lighthouse mobile lab results

| Page | Performance | Accessibility | Best practices | SEO | FCP | LCP | CLS | Total blocking time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Storefront glass repair | 100 | 100 | 100 | 100 | 0.9s | 1.1s | 0 | 0ms |
| Homepage | 99 | 100 | 100 | 100 | 0.9s | 2.0s | 0 | 0ms |
| Washington, DC | 100 | 100 | 100 | 100 | 0.9s | 1.1s | 0 | 0ms |
| Work photo gallery | 98 | 100 | 100 | 100 | 0.9s | 2.3s | 0 | 0ms |

These are Lighthouse simulated-mobile measurements over a temporary loopback HTTP server, using local assets. Production hosting, real-network latency, real-device interaction performance and future analytics or additional photo changes were not measured. Run production Lighthouse/PageSpeed after publication. The local stylesheet remains render-blocking, and the temporary server does not set production cache headers. Lighthouse also identifies optional image compression/sizing savings; all measured pages exceed the requested 90 performance target. No real-user INP measurement is claimed.

The owner confirmed that the supplied assets/images photos show previous client work and authorized their display. Eight selected originals are represented by 22 WebP variants with responsive srcset/sizes and explicit dimensions. Original files are preserved; derivatives have no EXIF metadata. Later photos are lazy-loaded, while the first visible homepage/gallery photo is prioritized. The gallery keeps each full photo at its original proportions. All eight gallery photos decoded successfully in the browser check. The selected largest variants total 861KB versus 5.77MB for their originals; the 360px variants total 215KB. The manifest records exact sources and sizes. Captions do not infer client identity, job city/date, repair outcome or before/after pairing.

Machine-readable results: [validation-results.json](validation-results.json). The storefront page contains 967 whitespace-delimited main-content words, including its hero, related links, contact controls and FAQs.

## Customer-copy cleanup

All 53 public HTML pages were checked after removing visible owner/setup notes, empty credentials/review blocks, pending labels and ADD markers, including HTML comments. Missing facts remain in the internal documentation and are not published as business claims. The verifier now rejects public placeholders and owner-facing phrases. Existing URLs, direct contact links, real work photos, all 125 FAQ/schema pairs and the three legacy coverage noindex settings remain intact. The browser checks passed 212 viewport cases and seven accessibility audits after cleanup; all eight gallery photos decoded. The Lighthouse measurements above are from the preceding photo-performance checks; this copy cleanup added no assets or runtime logic.
