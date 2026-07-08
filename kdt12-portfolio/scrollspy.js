(() => {
  if (window.__portfolioScrollSpyReady) return;
  window.__portfolioScrollSpyReady = true;

  const navItems = Array.from(document.querySelectorAll('.sidenav .nav-item[href^="#"]'));
  if (!navItems.length) return;

  const linkById = new Map();
  navItems.forEach((item) => {
    const href = item.getAttribute('href') || '';
    const id = decodeURIComponent(href.slice(1));
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    linkById.set(id, item);
    item.addEventListener('click', () => setActive(item), { passive: true });
  });

  const sections = Array.from(linkById.keys())
    .map((id) => document.getElementById(id))
    .filter(Boolean);
  if (!sections.length) return;

  function setActive(activeItem) {
    navItems.forEach((item) => {
      const isActive = item === activeItem;
      item.classList.toggle('active', isActive);
      item.setAttribute('aria-current', isActive ? 'true' : 'false');
    });
  }

  function updateActiveSection() {
    const triggerLine = Math.min(window.innerHeight * 0.36, 280);
    let current = sections[0];

    sections.forEach((section) => {
      const rect = section.getBoundingClientRect();
      if (rect.top <= triggerLine && rect.bottom > 80) {
        current = section;
      }
    });

    const activeItem = linkById.get(current.id);
    if (activeItem) setActive(activeItem);
  }

  let ticking = false;
  function requestUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(() => {
      ticking = false;
      updateActiveSection();
    });
  }

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  window.addEventListener('hashchange', () => window.setTimeout(updateActiveSection, 80));

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateActiveSection, { once: true });
  } else {
    updateActiveSection();
  }
})();
