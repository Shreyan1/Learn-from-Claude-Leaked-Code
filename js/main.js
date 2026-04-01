/* =====================================================================
   Claude Code Documentation - Main JavaScript
   Handles: dark mode, mobile nav, sidebar sub-nav (accordion),
            scroll spy into sidebar, copy buttons, heading anchors
   ===================================================================== */

(function () {
  'use strict';

  /* ------------------------------------------------------------------ */
  /* 1. Dark Mode                                                         */
  /* ------------------------------------------------------------------ */
  const THEME_KEY = 'cc-docs-theme';

  function getStoredTheme() {
    try { return localStorage.getItem(THEME_KEY); }
    catch { return null; }
  }

  function storeTheme(t) {
    try { localStorage.setItem(THEME_KEY, t); }
    catch {}
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const moon = document.getElementById('icon-moon');
    const sun  = document.getElementById('icon-sun');
    if (moon) moon.style.display = theme === 'dark' ? 'none' : '';
    if (sun)  sun.style.display  = theme === 'dark' ? ''     : 'none';
  }

  function initTheme() {
    const stored    = getStoredTheme();
    const preferred = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    applyTheme(stored || preferred);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next    = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    storeTheme(next);
  }

  /* ------------------------------------------------------------------ */
  /* 2. Sidebar Active Link                                               */
  /* ------------------------------------------------------------------ */
  function setActiveSidebarLink() {
    const path = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
      const href = link.getAttribute('href');
      // Strip any hash from the href for comparison
      const hrefPage = href ? href.split('#')[0] : '';
      if (hrefPage === path || (path === '' && hrefPage === 'index.html')) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }

  /* ------------------------------------------------------------------ */
  /* 3. Sidebar Sub-Nav (Accordion) — auto-generated from H2/H3s          */
  /* ------------------------------------------------------------------ */
  function buildSidebarSubNav() {
    const content = document.querySelector('.page-content');
    if (!content) return;

    // Collect all H2 and H3 headings
    const headings = Array.from(content.querySelectorAll('h2, h3'));
    if (headings.length < 2) return;

    // Find the active sidebar link (the current page)
    const activeLink = document.querySelector('.sidebar-nav a.active');
    if (!activeLink) return;

    // Ensure headings have IDs
    headings.forEach((h, i) => {
      if (!h.id) h.id = 'section-' + i;
      // Add anchor link
      if (!h.querySelector('.heading-anchor')) {
        const anchor = document.createElement('a');
        anchor.className = 'heading-anchor';
        anchor.href = '#' + h.id;
        anchor.textContent = '#';
        anchor.setAttribute('aria-hidden', 'true');
        h.appendChild(anchor);
      }
    });

    // Mark the active link as having a sub-nav
    activeLink.classList.add('nav-has-sub');

    // Add chevron to active link
    const chevron = document.createElement('span');
    chevron.className = 'nav-chevron';
    chevron.innerHTML = '&#9660;'; // ▼
    activeLink.appendChild(chevron);

    // Build the sub-nav <ul>
    const ul = document.createElement('ul');
    ul.className = 'sidebar-sub-nav';

    headings.forEach(h => {
      const li = document.createElement('li');
      if (h.tagName === 'H3') li.classList.add('sub-h3');

      const a = document.createElement('a');
      a.href = '#' + h.id;
      // Clean text: strip the anchor # character appended by anchor-link
      a.textContent = h.textContent.replace(/\s*#\s*$/, '').trim();
      a.dataset.target = h.id;

      a.addEventListener('click', e => {
        e.preventDefault();
        const target = document.getElementById(h.id);
        if (target) {
          const offset = 80;
          const top    = target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top, behavior: 'smooth' });
          history.pushState(null, '', '#' + h.id);
        }
      });

      li.appendChild(a);
      ul.appendChild(li);
    });

    // Insert sub-nav after the active link
    activeLink.parentNode.insertBefore(ul, activeLink.nextSibling);

    // Toggle collapse on clicking the active link
    activeLink.addEventListener('click', e => {
      // Only toggle if clicking the already-active page link (no navigation needed)
      const hrefPage = (activeLink.getAttribute('href') || '').split('#')[0];
      const currentPage = window.location.pathname.split('/').pop() || 'index.html';
      if (hrefPage === currentPage || hrefPage === '') {
        e.preventDefault();
        const isCollapsed = ul.classList.toggle('collapsed');
        activeLink.classList.toggle('sub-collapsed', isCollapsed);
      }
    });

    // Scroll to hash on load
    if (window.location.hash) {
      setTimeout(() => {
        const target = document.querySelector(window.location.hash);
        if (target) {
          const offset = 80;
          const top    = target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top, behavior: 'smooth' });
          // Activate the matching sub-nav item
          ul.querySelectorAll('a').forEach(a => {
            a.classList.toggle('sub-active', a.dataset.target === window.location.hash.slice(1));
          });
        }
      }, 100);
    }

    return { ul, headings };
  }

  /* ------------------------------------------------------------------ */
  /* 4. Sidebar Sub-Nav Scroll Spy                                        */
  /* ------------------------------------------------------------------ */
  function initSidebarScrollSpy(ul, headings) {
    if (!ul || !headings || !headings.length) return;

    const subLinks = Array.from(ul.querySelectorAll('a[data-target]'));

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          subLinks.forEach(a => {
            a.classList.toggle('sub-active', a.dataset.target === id);
          });
        }
      });
    }, {
      rootMargin: '-60px 0px -55% 0px',
      threshold: 0
    });

    headings.forEach(h => observer.observe(h));
  }

  /* ------------------------------------------------------------------ */
  /* 5. Legacy TOC Generation (hidden but keeps IDs/anchors working)      */
  /* ------------------------------------------------------------------ */
  function generateTOC() {
    const tocList = document.getElementById('toc-list');
    if (!tocList) return;

    const content = document.querySelector('.page-content');
    if (!content) return;

    const headings = content.querySelectorAll('h2, h3');
    headings.forEach((h, i) => {
      if (!h.id) h.id = 'section-' + i;
    });
  }

  /* ------------------------------------------------------------------ */
  /* 6. Mobile Sidebar                                                    */
  /* ------------------------------------------------------------------ */
  function initMobileNav() {
    const hamburger = document.getElementById('hamburger');
    const sidebar   = document.querySelector('.sidebar');
    const overlay   = document.getElementById('sidebar-overlay');

    function openSidebar() {
      sidebar?.classList.add('open');
      overlay?.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeSidebar() {
      sidebar?.classList.remove('open');
      overlay?.classList.remove('open');
      document.body.style.overflow = '';
    }

    hamburger?.addEventListener('click', () => {
      sidebar?.classList.contains('open') ? closeSidebar() : openSidebar();
    });

    overlay?.addEventListener('click', closeSidebar);

    // Close on non-hash nav link click (mobile)
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
      link.addEventListener('click', () => {
        const href = link.getAttribute('href') || '';
        if (window.innerWidth < 900 && !href.startsWith('#')) closeSidebar();
      });
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth >= 900) closeSidebar();
    });
  }

  /* ------------------------------------------------------------------ */
  /* 7. Copy Buttons                                                      */
  /* ------------------------------------------------------------------ */
  function initCopyButtons() {
    document.querySelectorAll('pre').forEach(pre => {
      if (pre.querySelector('.code-header')) return;

      const code = pre.querySelector('code');
      let lang = '';
      if (code) {
        const cls = Array.from(code.classList).find(c => c.startsWith('language-'));
        if (cls) lang = cls.replace('language-', '').toUpperCase();
      }

      const header  = document.createElement('div');
      header.className = 'code-header';

      const langSpan    = document.createElement('span');
      langSpan.className = 'code-lang';
      langSpan.textContent = lang;

      const btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.textContent = 'Copy';

      btn.addEventListener('click', () => {
        const text = code ? code.innerText : pre.innerText;
        navigator.clipboard.writeText(text).then(() => {
          btn.textContent = '✓ Copied!';
          btn.classList.add('copied');
          setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
        }).catch(() => {
          const ta = document.createElement('textarea');
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.textContent = '✓ Copied!';
          setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
        });
      });

      header.appendChild(langSpan);
      header.appendChild(btn);
      pre.insertBefore(header, pre.firstChild);
    });
  }

  /* ------------------------------------------------------------------ */
  /* 8. Keyboard Shortcuts                                                */
  /* ------------------------------------------------------------------ */
  function initKeyboardShortcuts() {
    document.addEventListener('keydown', e => {
      if (e.key === 'd' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const tag = document.activeElement?.tagName;
        if (tag !== 'INPUT' && tag !== 'TEXTAREA' && tag !== 'SELECT') {
          toggleTheme();
        }
      }
    });
  }

  /* ------------------------------------------------------------------ */
  /* 9. Smooth Anchor Scroll                                              */
  /* ------------------------------------------------------------------ */
  function initAnchorScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          const offset = 72;
          const top    = target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top, behavior: 'smooth' });
          history.pushState(null, '', this.getAttribute('href'));
        }
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 10. Sidebar Resize                                                   */
  /* ------------------------------------------------------------------ */
  const SIDEBAR_W_KEY = 'cc-sidebar-width';
  const SIDEBAR_MIN_W = 180;
  const SIDEBAR_MAX_W = 480;

  function getSavedSidebarWidth() {
    try { return parseInt(localStorage.getItem(SIDEBAR_W_KEY), 10) || null; }
    catch { return null; }
  }

  function saveSidebarWidth(w) {
    try { localStorage.setItem(SIDEBAR_W_KEY, String(w)); }
    catch {}
  }

  function applySidebarWidth(w) {
    document.documentElement.style.setProperty('--sidebar-w', w + 'px');
  }

  function initSidebarResize() {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;

    // Restore saved width
    const saved = getSavedSidebarWidth();
    if (saved) applySidebarWidth(saved);

    // Create the drag handle — fixed positioned, tracked by JS
    const handle = document.createElement('div');
    handle.className = 'sidebar-resize-handle';
    handle.setAttribute('aria-hidden', 'true');
    handle.title = 'Drag to resize · Double-click to reset';
    document.body.appendChild(handle);

    // Position the handle at the sidebar's right edge
    function positionHandle() {
      const rect = sidebar.getBoundingClientRect();
      handle.style.left = (rect.right - 3) + 'px';
    }

    positionHandle();
    window.addEventListener('resize', positionHandle);

    let dragging = false;
    let startX = 0;
    let startW = 0;

    handle.addEventListener('mousedown', e => {
      e.preventDefault();
      dragging = true;
      startX = e.clientX;
      startW = sidebar.getBoundingClientRect().width;
      handle.classList.add('dragging');
      document.body.classList.add('sidebar-dragging');
    });

    document.addEventListener('mousemove', e => {
      if (!dragging) return;
      const delta = e.clientX - startX;
      const newW = Math.min(SIDEBAR_MAX_W, Math.max(SIDEBAR_MIN_W, startW + delta));
      applySidebarWidth(newW);
      positionHandle();
    });

    document.addEventListener('mouseup', () => {
      if (!dragging) return;
      dragging = false;
      handle.classList.remove('dragging');
      document.body.classList.remove('sidebar-dragging');
      // Persist the final width
      const finalW = sidebar.getBoundingClientRect().width;
      if (finalW > 0) saveSidebarWidth(Math.round(finalW));
    });

    // Touch support
    handle.addEventListener('touchstart', e => {
      const touch = e.touches[0];
      dragging = true;
      startX = touch.clientX;
      startW = sidebar.getBoundingClientRect().width;
      handle.classList.add('dragging');
    }, { passive: true });

    document.addEventListener('touchmove', e => {
      if (!dragging) return;
      const touch = e.touches[0];
      const delta = touch.clientX - startX;
      const newW = Math.min(SIDEBAR_MAX_W, Math.max(SIDEBAR_MIN_W, startW + delta));
      applySidebarWidth(newW);
      positionHandle();
    }, { passive: true });

    document.addEventListener('touchend', () => {
      if (!dragging) return;
      dragging = false;
      handle.classList.remove('dragging');
      const finalW = sidebar.getBoundingClientRect().width;
      if (finalW > 0) saveSidebarWidth(Math.round(finalW));
    });

    // Double-click to reset to default width
    handle.addEventListener('dblclick', () => {
      applySidebarWidth(272);
      saveSidebarWidth(272);
      setTimeout(positionHandle, 50);
    });
  }

  /* ------------------------------------------------------------------ */
  /* 11. Back to Top Button                                               */
  /* ------------------------------------------------------------------ */
  function initBackToTop() {
    const btn = document.createElement('button');
    btn.className = 'back-to-top';
    btn.setAttribute('aria-label', 'Back to top');
    btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg>';
    document.body.appendChild(btn);

    const toggleVisibility = () => {
      if (window.scrollY > 300) {
        btn.classList.add('show');
      } else {
        btn.classList.remove('show');
      }
    };

    window.addEventListener('scroll', toggleVisibility, { passive: true });
    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ------------------------------------------------------------------ */
  /* 12. Init                                                             */
  /* ------------------------------------------------------------------ */
  function init() {
    initTheme();
    setActiveSidebarLink();
    generateTOC(); // ensures IDs exist

    // Build sub-nav and wire up scroll spy
    const result = buildSidebarSubNav();
    if (result) {
      initSidebarScrollSpy(result.ul, result.headings);
    }

    initSidebarResize();
    initMobileNav();
    initCopyButtons();
    initKeyboardShortcuts();
    initAnchorScroll();
    initBackToTop();

    document.getElementById('theme-toggle')?.addEventListener('click', toggleTheme);

    if (window.lucide) lucide.createIcons();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.addEventListener('load', () => {
    initCopyButtons();
    if (window.lucide) lucide.createIcons();
  });

})();
