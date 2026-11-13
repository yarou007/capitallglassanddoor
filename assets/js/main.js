(function () {
  'use strict';
  const menu = document.querySelector('.menu-btn');
  const nav = document.querySelector('.main-nav');
  const path = window.location.pathname;
  const pageType = path.includes('/services/') ? 'service' : path.includes('/locations/') ? 'location' : path.includes('/blog/') ? 'blog' : (path === '/' || path.endsWith('/index.html')) ? 'home' : 'other';

  function closeMenu(returnFocus) {
    if (!menu || !nav) return;
    nav.classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
    if (returnFocus) menu.focus();
  }
  if (menu && nav) {
    menu.addEventListener('click', function () {
      const open = nav.classList.toggle('open');
      menu.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (event) { if (event.target.closest('a')) closeMenu(false); });
    document.addEventListener('click', function (event) {
      if (!nav.contains(event.target) && !menu.contains(event.target)) closeMenu(false);
    });
    document.addEventListener('focusin', function (event) {
      if (!nav.contains(event.target) && !menu.contains(event.target)) closeMenu(false);
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && nav.classList.contains('open')) closeMenu(true);
    });
    const desktop = window.matchMedia('(min-width: 1000px)');
    desktop.addEventListener('change', function () { closeMenu(false); });
    nav.querySelectorAll('a').forEach(function (link) {
      const linkPath = new URL(link.href).pathname;
      if (linkPath === path || (pageType === 'service' && linkPath.endsWith('/services.html')) || (pageType === 'location' && linkPath.endsWith('/locations.html')) || (pageType === 'blog' && linkPath.endsWith('/knowledge-center.html'))) {
        link.classList.add('active');
        if (linkPath === path) link.setAttribute('aria-current', 'page');
      }
    });
  }
  document.querySelectorAll('[data-year]').forEach(function (element) { element.textContent = String(new Date().getFullYear()); });

  // No analytics library loads here. An existing Google tag receives events when installed.
  // With GTM, use these dataLayer custom events; with a direct Google tag, use gtag events.
  const adsTargets = { call: '', whatsapp: '' };
  function placement(link) {
    if (link.closest('.float-cta')) return window.matchMedia('(min-width: 1000px)').matches ? 'floating_desktop' : 'sticky_mobile';
    if (link.closest('.hero')) return 'hero';
    if (link.closest('header')) return 'header';
    if (link.closest('footer')) return 'footer';
    if (link.closest('#whatsapp-guide')) return 'whatsapp_guide';
    return 'body';
  }
  document.addEventListener('click', function (event) {
    const link = event.target.closest('a[href]');
    if (!link) return;
    const url = new URL(link.href);
    const type = url.protocol === 'tel:' ? 'call' : (url.hostname === 'wa.me' && url.pathname === '/12026434062') ? 'whatsapp' : null;
    if (!type) return;
    const eventName = type === 'call' ? 'call_button_click' : 'whatsapp_button_click';
    // Never collect WhatsApp message text, personal details, or URL query parameters.
    const payload = { page_path: path, page_type: pageType, cta_placement: placement(link), contact_method: type, transport_type: 'beacon' };
    try {
      window.dataLayer = window.dataLayer || [];
      if (typeof window.gtag === 'function') {
        window.gtag('event', eventName, payload);
        if (adsTargets[type]) window.gtag('event', 'conversion', { send_to: adsTargets[type], transport_type: 'beacon' });
      } else {
        window.dataLayer.push(Object.assign({ event: eventName }, payload));
      }
    } catch (_) { /* Contact links keep working if analytics is unavailable. */ }
  });
})();
