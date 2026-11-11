# Capital Glass and Door Services

A static HTML/CSS website with vanilla JavaScript. Serve or upload these files directly; there is no framework, dependency installation or build step.

Primary actions are **Call** (`tel:+17032440559`) and **WhatsApp** (`https://wa.me/17032440559` with an encoded, page-specific draft). There are no request fields or submission endpoints.

The site leads with storefront glass repair and replacement, then emergency board-up, commercial doors/hardware and locksmith services. Existing `.html` URLs and outgoing internal HTML destinations are retained. Three requested market pages were added.

- [Audit and strategy](docs/project-strategy.md)
- [Internal business-fact checklist](docs/owner-confirmations.md)
- [Tracking setup](docs/tracking.md)
- [Validation results](docs/validation.md)
- [Eight additional blog topics](docs/blog-topics.md)
- [Location sources](docs/location-sources.md), [service sources](docs/service-sources.md), [blog sources](docs/blog-sources.md)

## Local preview and verification

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/`. No compilation is required.

```sh
python3 scripts/verify_site.py
node --check assets/js/main.js
```

The optional baseline flag verifies preserved URLs and internal destinations against a pre-edit capture: `python3 scripts/verify_site.py --baseline /path/to/baseline.json`.

## Customer copy and internal documentation

Public pages contain customer-facing service information, actual work photos and Call/WhatsApp links. Missing-business-fact requests and setup notes live only in `docs/owner-confirmations.md`; public HTML and runtime JavaScript contain no ADD markers or owner-facing notes. Unverified hours, credentials, reviews, warranty and business-profile details are omitted from customer copy and structured data. Three legacy coverage pages and three informational pages retain `noindex, follow`; the sitemap contains only intended indexable pages.

No Google Analytics or Google Ads library loads yet. The contact-click hooks work locally and can feed an installed Google tag or GTM. Add real IDs, approved privacy details and the appropriate measurement configuration before enabling collection. A click records intent to contact, not a completed phone call or a customer message.

The owner confirmed that the photographs in `assets/images/` show previous client work by Capital Glass and Door Services and authorized their use on the website. Curated work photos support the gallery and proof sections, with responsive WebP variants in `assets/images/work/`; the original files remain unchanged. The [asset manifest](assets/images/work/manifest.json) records the selected originals and generated variants.

Captions describe what is visible. Client names, project cities, dates, turnaround times and before/after pairings are not inferred from filenames or image appearance. Add those details only after specific confirmation. The photos do not establish reviews, licensing, insurance, service hours or warranty terms.
