(function () {
  const button = document.querySelector('.menu-btn');
  const nav = document.querySelector('.main-nav');
  const navLinks = document.querySelectorAll('.main-nav a');
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const fullPath = window.location.pathname;

  function getPageType(pathname) {
    if (pathname.includes('/services/')) return 'service';
    if (pathname.includes('/locations/')) return 'location';
    if (pathname.includes('/blog/')) return 'blog';
    if (pathname.endsWith('/services.html')) return 'services_hub';
    if (pathname.endsWith('/locations.html')) return 'locations_hub';
    if (pathname.endsWith('/contact.html')) return 'contact';
    if (pathname === '/' || pathname.endsWith('/index.html')) return 'home';
    return 'other';
  }

  function getCtaPlacement(element) {
    if (!element) return 'unknown';
    if (element.closest('.float-cta')) return 'sticky_mobile';
    if (element.closest('header')) return 'header';
    if (element.closest('.cta-band')) return 'cta_band';
    if (element.closest('footer')) return 'footer';
    if (element.closest('.hero')) return 'hero';
    return 'body';
  }

  function pushTrackingEvent(eventName, payload) {
    const data = Object.assign(
      {
        event: eventName,
        page_path: fullPath,
        page_type: getPageType(fullPath)
      },
      payload || {}
    );

    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(data);

    if (typeof window.gtag === 'function') {
      const gtagPayload = Object.assign({}, data);
      delete gtagPayload.event;
      window.gtag('event', eventName, gtagPayload);
    }
  }

  if (button && nav) {
    button.addEventListener('click', function () {
      const open = nav.classList.toggle('open');
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    navLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth <= 980) {
          nav.classList.remove('open');
          button.setAttribute('aria-expanded', 'false');
        }
      });
    });

    document.addEventListener('click', function (event) {
      if (window.innerWidth > 980) return;
      if (!nav.contains(event.target) && !button.contains(event.target)) {
        nav.classList.remove('open');
        button.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        button.setAttribute('aria-expanded', 'false');
        button.focus();
      }
    });
  }

  let hasExactActive = false;

  navLinks.forEach(function (link) {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('http') || href.startsWith('#')) return;
    const normalizedHref = href.split('?')[0].split('#')[0].split('/').pop() || 'index.html';
    if (normalizedHref === currentPath) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
      hasExactActive = true;
    }
  });

  if (!hasExactActive) {
    navLinks.forEach(function (link) {
      const href = link.getAttribute('href') || '';
      if (fullPath.includes('/services/') && href.includes('services.html')) {
        link.classList.add('active');
      }
      if (fullPath.includes('/locations/') && href.includes('locations.html')) {
        link.classList.add('active');
      }
      if (fullPath.includes('/blog/') && href.includes('knowledge-center.html')) {
        link.classList.add('active');
      }
    });
  }

  const yearTargets = document.querySelectorAll('[data-year]');
  const year = new Date().getFullYear();
  yearTargets.forEach(function (node) {
    node.textContent = String(year);
  });

  document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
    link.addEventListener('click', function () {
      pushTrackingEvent('call_button_click', {
        phone_href: link.getAttribute('href') || '',
        cta_text: (link.textContent || '').trim(),
        cta_placement: getCtaPlacement(link)
      });

      if (fullPath.includes('/services/')) {
        pushTrackingEvent('service_page_cta_click', {
          cta_type: 'call',
          cta_placement: getCtaPlacement(link),
          target_href: link.getAttribute('href') || ''
        });
      }

      if (fullPath.includes('/locations/')) {
        pushTrackingEvent('location_page_cta_click', {
          cta_type: 'call',
          cta_placement: getCtaPlacement(link),
          target_href: link.getAttribute('href') || ''
        });
      }
    });
  });

  document.querySelectorAll('a[href^="sms:"]').forEach(function (link) {
    link.addEventListener('click', function () {
      pushTrackingEvent('sms_button_click', {
        sms_href: link.getAttribute('href') || '',
        cta_text: (link.textContent || '').trim(),
        cta_placement: getCtaPlacement(link)
      });

      if (fullPath.includes('/services/')) {
        pushTrackingEvent('service_page_cta_click', {
          cta_type: 'sms',
          cta_placement: getCtaPlacement(link),
          target_href: link.getAttribute('href') || ''
        });
      }

      if (fullPath.includes('/locations/')) {
        pushTrackingEvent('location_page_cta_click', {
          cta_type: 'sms',
          cta_placement: getCtaPlacement(link),
          target_href: link.getAttribute('href') || ''
        });
      }
    });
  });

  document.querySelectorAll('a.btn, button.btn, a.nav-cta').forEach(function (cta) {
    cta.addEventListener('click', function () {
      const href = cta.getAttribute('href') || '';
      if (href.startsWith('tel:') || href.startsWith('sms:')) return;

      const label = (cta.textContent || '').trim().toLowerCase();
      const emergencyIntent =
        label.includes('emergency') ||
        label.includes('call now') ||
        label.includes('request service') ||
        label.includes('dispatch') ||
        href.includes('contact');

      if (emergencyIntent) {
        pushTrackingEvent('emergency_cta_click', {
          cta_text: (cta.textContent || '').trim(),
          cta_placement: getCtaPlacement(cta),
          target_href: href
        });
      }

      if (fullPath.includes('/services/')) {
        pushTrackingEvent('service_page_cta_click', {
          cta_type: 'generic',
          cta_placement: getCtaPlacement(cta),
          target_href: href,
          cta_text: (cta.textContent || '').trim()
        });
      }

      if (fullPath.includes('/locations/')) {
        pushTrackingEvent('location_page_cta_click', {
          cta_type: 'generic',
          cta_placement: getCtaPlacement(cta),
          target_href: href,
          cta_text: (cta.textContent || '').trim()
        });
      }
    });
  });

  document.querySelectorAll('form').forEach(function (form, index) {
    form.addEventListener('submit', function () {
      pushTrackingEvent('emergency_form_submit', {
        form_id: form.id || ('form_' + (index + 1)),
        form_action: form.getAttribute('action') || '',
        form_method: (form.getAttribute('method') || 'get').toLowerCase()
      });
    });
  });
})();
