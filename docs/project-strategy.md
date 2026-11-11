# Conversion and local SEO audit

This replaces the previous form/SMS strategy. The Search Console figures below are owner-supplied findings, not a fresh account export. Work is prepared locally; production publication and Search Console submission have not been performed.

## Findings ranked by impact

| Priority | Finding in the original source | Customer/search impact | Implemented change |
| --- | --- | --- | --- |
| 1 | Two request forms, including an external formsubmit.co endpoint; SMS and contact-page detours competed with calling. | Adds friction for urgent mobile visitors and offers a contact path the owner does not want. | Removed all fields, submission logic and SMS actions. Contact page is Call/WhatsApp. Both actions exist as ordinary links without JavaScript. |
| 2 | Storefront page had limited useful copy and no specific local H1; homepage led with broad emergency services. | Weak match to the storefront queries responsible for the visible impressions. | Storefront-led homepage, detailed 700–1,000-word storefront guide, links to every market and supporting service. |
| 3 | Repeated DMV/city strings and near-identical city pages; geographic detail was weak. | Owner reports impressions from Dublin and Jackson rather than the target region. | Consistent Washington, DC / Arlington, VA / Baltimore, MD signals in homepage title, H1, opening paragraph and NAP footer; unique local business/access context and FAQs. |
| 4 | Published 24/7, licensed/insured, same-day, no-hidden-fees claims, review quotations and Baltimore/DC/Arlington job outcomes without verification. | Trust and brand clarity suffer when claims cannot be supported. | Removed unsupported claims and retained hypothetical scenarios. The owner subsequently confirmed the supplied photos as previous client work and authorized display; descriptive work photos now support the proof sections. Reviews, credentials and other unknown business details remain in the internal checklist and are omitted from customer pages. Exact full business name retained. |
| 5 | Sticky controls were absent on desktop; mobile contact targets could be below 52px and body/footer space did not reserve room for the fixed bar. Mobile hero imagery pushed content down. | Makes the main action harder to find and can obscure content. | Two 54px mobile split buttons, safe-area padding, desktop floating pair, compact first-screen hero, native FAQ accordions and accessible menu. |
| 6 | All 95 image placements lacked explicit dimensions; remote font requests and large unverified job photos added cost. | Layout movement and slower phone rendering. | Local system font, dimensioned imagery, responsive WebP variants and below-fold lazy loading. Curated previous-work photos are used after owner confirmation; original files are preserved. |
| 7 | Several head sections had a malformed canonical tag and stray markup; metadata and schema carried unsupported hours. | Unreliable parsing and inconsistent entity signals. | Valid heads, unique metadata, canonical URLs, LocalBusiness/Service/Breadcrumb/FAQ graphs; no fabricated address/hours/reviews. |
| 8 | Tracking covered telephone/SMS/form submissions but not WhatsApp, and existing strategy instructed adding forms. | Cannot compare the requested contact methods; future edits could regress. | Call and WhatsApp event hooks, disabled Ads destinations, setup notes and repeatable static verification. |

## Targeting and architecture

Primary money page: `/services/storefront-glass-repair.html`. Support it with emergency glass repair, board-up, commercial door/hardware and locksmith pages. The homepage and five customer segments link into those services. City pages link to storefront/supporting services and nearby areas; blogs link to relevant commercial services. All original HTML paths and outgoing internal HTML destinations remain available.

Use full `City, ST` spelling, including `Washington, DC`, rather than ambiguous short place names. The supplied market list does not establish a business address. Never invent a local office or turn neighborhood references into completed-job claims.

All ten city markets supplied by the owner, plus Downtown and Inner Harbor, have indexable local content. Legacy Rockville, Towson and Fell’s Point pages are retained and pending confirmation because they were not in the supplied market list. These three pages use `noindex, follow`, are omitted from the sitemap and are not asserted in active `areaServed`. Their URLs remain intact, with customer-facing repair and availability guidance.

## Previous-work photographs

The owner confirmed that the photographs supplied in `assets/images/` are previous client work by Capital Glass and Door Services and authorized their use. The gallery and proof sections use a curated selection with descriptive captions and responsive WebP derivatives. `assets/images/work/manifest.json` maps selected originals to the generated variants; originals remain unchanged.

This confirmation supports identifying the images as previous client work. It does not establish client identities, project cities or dates, turnaround times, specific outcomes or before/after pairings. Captions stay within visible image content. Reviews, licensing, insurance, hours and warranty terms still need their own evidence.

## Honest structured data

Use Schema.org `HomeAndConstructionBusiness` under `LocalBusiness`, with `Locksmith` on the locksmith page, and separate `Service.serviceType` entries. `GlassRepair` is not an established Schema.org type; it is not emitted. District-level service areas use `Place`, and city markets use `City`. Shared `@id`, name and telephone are consistent.

`sameAs`, `openingHours`, a public postal address, ratings and review records remain absent until verified. Google’s LocalBusiness rich-result requirements include a physical address; the current service-area graph describes the business honestly but does not establish rich-result eligibility. Match the real Business Profile before adding address data. [Google LocalBusiness documentation](https://developers.google.com/search/docs/appearance/structured-data/local-business), [HomeAndConstructionBusiness](https://schema.org/HomeAndConstructionBusiness), [Locksmith](https://schema.org/Locksmith), [Service.serviceType](https://schema.org/serviceType).

FAQPage markup matches visible accordions. It helps describe the page but does not promise a Google FAQ rich result; Google’s current documentation records that the feature no longer appears. [Schema.org FAQPage](https://schema.org/FAQPage), [Google documentation updates](https://developers.google.com/search/updates).

## Publication and measurement

1. Resolve the owner checklist, especially actual service coverage, contact availability and GBP consistency. Keep missing facts in the internal checklist; publish business claims only after they are supported by evidence.
2. Upload the static files to the existing domain. Keep existing paths and canonical host; do not introduce redirects for current HTML URLs.
3. Validate deployed pages and submit the updated sitemap in the owner’s Search Console. Request recrawl for the storefront page, homepage and primary cities. This local change does not submit anything automatically.
4. Configure exactly one GA4 event route and test both contact hooks. Configure Ads only with real conversion IDs/labels. Click events measure attempts, not answered calls or sent messages.
5. Compare US impressions, relevant city queries, storefront-page engagement and real call/message outcomes over subsequent reporting periods. Check whether irrelevant-city impressions decline. No ranking or lead-volume gain is guaranteed.

The additional eight editorial topics are in `docs/blog-topics.md`. Build them only after the service and local pages have been reviewed; keep the same evidence standard.
