# Call and WhatsApp click tracking

`assets/js/main.js` contains event hooks but does not load a tracking provider. Native Call/WhatsApp links work without a tag, JavaScript, cookies or browser storage.

| Event | Trigger | Parameters |
| --- | --- | --- |
| `call_button_click` | A `tel:` link is clicked | `page_path`, `page_type`, `cta_placement`, `contact_method`, `transport_type` |
| `whatsapp_button_click` | The business `wa.me/12026434062` link is clicked | Same |

Placement distinguishes `hero`, `header`, `body`, `footer`, `whatsapp_guide`, `sticky_mobile` and `floating_desktop`. Only the path is included; query strings, WhatsApp draft text, photos, addresses and visitor-entered information are not event parameters. Google’s own tag may collect additional page information; review that configuration independently before enabling it.

Choose one setup:

- **GTM:** install the approved container once on the site, add Custom Event triggers for the two names above, and map data-layer variables into GA4 events. The hooks push objects into `window.dataLayer` when no direct `gtag` function is installed.
- **Direct Google tag:** install the approved GA4 tag once before the deferred `main.js`, using the real `G-...` measurement ID. If `gtag` exists, the hooks send one event through `gtag('event', name, parameters)` and do not also push a duplicate custom object.

Do not configure a second GA4 tag for the same click event. Disable overlapping automatic telephone/WhatsApp tracking if it would duplicate these events.

For Google Ads, `adsTargets` has deliberately empty `call` and `whatsapp` destinations. Replace each with the real `AW-CONVERSION_ID/CONVERSION_LABEL` supplied by the owner, after a Google tag with the appropriate Ads configuration is installed. The optional code emits `gtag('event', 'conversion', {send_to: ..., transport_type: 'beacon'})` only when its destination is configured. Do not publish literal placeholder IDs.

Mark the desired events as key events/conversions in the corresponding account and validate in Tag Assistant/GA4 DebugView after deployment. A telephone click does not prove that a call connected; a WhatsApp click does not prove the user sent the draft. Configure separate answered-call/imported qualified-lead measurement if the owner wants those outcomes.

The browser checks exercise the dataLayer path, direct-gtag path, placement and absence of duplicate events without sending anything to Google. Actual delivery and attribution remain unverified until real account configuration and a deployed tag are available.

[Google event setup documentation](https://developers.google.com/analytics/devguides/collection/ga4/events).
