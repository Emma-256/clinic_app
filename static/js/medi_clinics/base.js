/**
 * base.js
 * Save to: static/js/medi_clinics/base.js
 *
 * Handles:
 *  1. User dropdown (open / close)
 *  2. Mobile nav drawer (open / close)
 *  3. Sidebar collapse / expand (with localStorage persistence)
 *  4. Flash alert dismiss buttons
 */

(function () {
  'use strict';

  /* ═══════════════════════════════════════════════════
     1. USER DROPDOWN
  ═══════════════════════════════════════════════════ */
  const userPill     = document.getElementById('userPill');
  const userDropdown = document.getElementById('userDropdown');

  if (userPill && userDropdown) {
    // Toggle on pill click
    userPill.addEventListener('click', function (e) {
      e.stopPropagation();
      userDropdown.classList.toggle('open');
    });

    // Close when clicking anywhere else on the page
    document.addEventListener('click', function () {
      userDropdown.classList.remove('open');
    });

    // Prevent clicks inside the dropdown from closing it
    userDropdown.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  /* ═══════════════════════════════════════════════════
     2. MOBILE NAV DRAWER
  ═══════════════════════════════════════════════════ */
  const hamburger     = document.getElementById('mcHamburger');
  const mobileNav     = document.getElementById('mcMobileNav');
  const mobileClose   = document.getElementById('mcMobileClose');
  const mobileOverlay = document.getElementById('mcMobileOverlay');

  function openMobileNav() {
    if (mobileNav) mobileNav.classList.add('open');
    document.body.style.overflow = 'hidden'; // prevent scroll behind drawer
  }

  function closeMobileNav() {
    if (mobileNav) mobileNav.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (hamburger)     hamburger.addEventListener('click', openMobileNav);
  if (mobileClose)   mobileClose.addEventListener('click', closeMobileNav);
  if (mobileOverlay) mobileOverlay.addEventListener('click', closeMobileNav);

  // Close mobile nav on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMobileNav();
  });

  /* ═══════════════════════════════════════════════════
     3. SIDEBAR COLLAPSE / EXPAND
  ═══════════════════════════════════════════════════ */
  const sidebar   = document.getElementById('mcSidebar');
  const sbToggle  = document.getElementById('sbToggleBtn');
  const STORE_KEY = 'mc_sidebar_collapsed';

  if (sidebar && sbToggle) {
    // Restore saved state immediately (avoids layout flash)
    if (localStorage.getItem(STORE_KEY) === 'true') {
      sidebar.classList.add('collapsed');
    }

    sbToggle.addEventListener('click', function () {
      const isNowCollapsed = sidebar.classList.toggle('collapsed');
      localStorage.setItem(STORE_KEY, String(isNowCollapsed));
    });
  }

  /* ═══════════════════════════════════════════════════
     4. FLASH ALERT DISMISS
  ═══════════════════════════════════════════════════ */
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('.mc-alert-close');
    if (!btn) return;

    const alert = btn.closest('.mc-alert');
    if (!alert) return;

    // Fade out then remove
    alert.style.transition = 'opacity .25s ease, transform .25s ease';
    alert.style.opacity    = '0';
    alert.style.transform  = 'translateY(-4px)';

    setTimeout(function () {
      alert.remove();
    }, 260);
  });

})();
