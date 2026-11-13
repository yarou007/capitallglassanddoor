# Mobile SEO, development and conversion assessment

Reviewed November 13, 2026 against the local checkout. Improvements are implemented locally; production deployment, live search rankings and actual call outcomes were not measured.

## Assessment and implemented changes

| Area | Finding | Change / outcome |
| --- | --- | --- |
| Mobile conversion | Call and WhatsApp had equal visual weight. “Call Now” concealed the number until activation. | Calls now have the solid primary style; WhatsApp uses an outlined secondary style. Hero, header and persistent call controls display 202-643-4062. |
| Homepage messaging | The long H1 and lead repeated the same cities, making the first screen harder to scan. | Short service-specific H1; lead explains glass, board-up, door help and coverage. Availability is discussed rather than promised. |
| Service discovery | Visitors reached the photo block before direct service choices. | Three large links immediately after the hero route broken glass, exposed openings and door hardware problems to relevant services. |
| Lead quality | Customers had to gather the repair process from longer sections. | A three-step section explains the first call, assessment and agreement on scope, pricing, access and timing. |
| Search snippets | Homepage title repeated a long list of cities; the description split attention between contact channels. | Shorter title retains the repair intent and regional coverage; description prioritizes calls. Open Graph and page/service structured descriptions stay consistent. |
| Mobile layout | Persistent controls need space above device safe areas; secondary buttons competed with calls. | Safe-area-aware bottom spacing, larger primary column, readable tap targets and consistent secondary styling. No new runtime dependencies or image downloads. |
| Keyboard access | An open mobile menu remained open when keyboard focus moved outside it. | Menu closes on focus leaving it, alongside the existing Escape and outside-click behavior. |
| Contact accuracy | The requested number was already the destination, but display formatting included +1. | Public HTML consistently displays 202-643-4062. Telephone links retain +12026434062; WhatsApp uses 12026434062. Those are international formats of the same number. |
| Trust | Credentials, ratings, operating hours and response-time claims need evidence. | No licenses, insurance, reviews, hours, guarantees or fabricated business details were added. Existing work photos remain the visual evidence. |

There are no public email links, forms, input fields or owner-facing ADD placeholders. WhatsApp remains a secondary option for sending photos to the same number. Nothing sends an email, submits a lead form or automatically contacts a customer.

## SEO strategy

Keep storefront glass repair as the main commercial topic. Board-up and commercial door repair support the same customer problem. Preserve the existing service and location URLs so internal links and existing search destinations keep working. Existing checks confirm unique titles/descriptions, canonicals, sitemap membership, local references, FAQ/schema agreement and image attributes.

The site has 53 HTML pages and 47 sitemap URLs. Six deliberate noindex pages remain excluded, including three locations whose coverage is not confirmed. Avoid expanding local-service claims beyond verified coverage or inventing branch addresses. FAQ schema describes the visible answers; it does not guarantee a Google rich result.

Location pages should earn their place through useful local access information and confirmed service scope. City-name substitutions alone are not a sustainable local SEO strategy. Improve them over time with verified project details and original photos where permission exists. Keep unconfirmed job locations, customer names, turnaround times and outcomes out of captions.

Many titles remain long because they include the full business name and specific service/location intent. Character counts are not a strict Google limit; prioritize meaningful terms at the beginning and use actual query/CTR evidence before mass title rewrites. The homepage title was shortened from 108 to 69 characters.

The next marketing measurement is the mobile funnel: search impressions → organic clicks → phone-link taps → answered calls → qualified jobs → booked clients. Use Search Console for query/page/device data and the business's call/job records for outcomes. Compare comparable periods and account for demand changes. No uplift percentage can be established from local code checks.

Existing call-click hooks record page, page type and CTA placement, without sending WhatsApp drafts or personal data. No analytics provider is configured. A phone-link tap indicates intent, not a connected call or booked job. A single-number policy means dynamic number swapping should not be introduced. Enabling analytics requires real account configuration and accurate privacy details, rather than fake IDs in source.

## Code structure

The static architecture is appropriate: server-rendered HTML, shared CSS, deferred vanilla JavaScript and no dependency/build requirement. Service information and contact links work without JavaScript. New sections use semantic headings, links and an ordered list; no plugin or client-side rendering was added.

Shared headers, footers, contact blocks and JSON-LD are repeated across 53 files. This raises maintenance risk: future updates must stay consistent across pages. The present change updates those files together and validates them. A later migration to build-time templates could reduce duplication while preserving every output URL, but adds a build workflow and is not required for these conversion improvements.

Unused placeholder-specific CSS was removed. The contact and menu enhancements remain in the existing shared files. No package manifest or application dependency was introduced.

## Validation of this revision

- Repository validator: 53 pages, 2,121 local references, 125 FAQ answers and 47 sitemap URLs pass.
- Comparison with the pre-change capture: all original HTML URLs and outgoing internal HTML destinations remain available.
- JavaScript syntax and Git whitespace checks pass.
- Chromium: 212 layout cases across 360×640, 390×844, 430×932 and 1440×900 pass, with no JavaScript errors or missing requests.
- Mobile menu, Escape/outside click, accordion, call/WhatsApp event hooks, no-JavaScript contact links and eight gallery image decodes pass.
- Additional HTTP-served browser checks at 320×568, 768×1024 and 844×390 pass for horizontal overflow, visible phone controls and service links. Keyboard focus leaving the mobile menu closes it.
- Axe-core 4.10.3 WCAG A/AA checks report zero violations on seven representative pages. Automated testing does not replace manual assistive-technology review.
- Contact audit finds only the requested phone destination, with no email links, forms or public placeholders.

Browser reports and screenshots for this run are in `/tmp/cgd-mobile-final/`. Axe was installed only under `/tmp/cgd-a11y/`, outside the repository. Historical Lighthouse scores in the earlier validation document were not remeasured for this revision. Production cache headers, indexing, Google Business Profile status, real-device performance and actual lead conversion require live-site/account evidence.
