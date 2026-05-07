(function () {
  const button = document.querySelector('.menu-btn');
  const nav = document.querySelector('.main-nav');
  const navLinks = document.querySelectorAll('.main-nav a');
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const fullPath = window.location.pathname;

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
})();
