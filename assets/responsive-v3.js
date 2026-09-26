/* RR responsive navigation v3 */
(() => {
  const onReady = (fn) => {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn, {once:true});
    else fn();
  };
  const menuSvg = '<svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
  const closeSvg = '<svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg>';
  const githubSvg = '<svg class="icon icon-fill" aria-hidden="true" viewBox="0 0 24 24"><path d="M12 .7a11.3 11.3 0 0 0-3.57 22.03c.57.1.78-.25.78-.55v-2.18c-3.18.69-3.85-1.35-3.85-1.35-.52-1.32-1.27-1.67-1.27-1.67-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.75 2.68 1.25 3.33.95.1-.74.4-1.25.73-1.54-2.54-.29-5.21-1.27-5.21-5.65 0-1.25.45-2.27 1.18-3.07-.12-.29-.51-1.46.11-3.03 0 0 .96-.31 3.15 1.17A10.9 10.9 0 0 1 12 5.9c.98 0 1.96.13 2.87.39 2.19-1.48 3.15-1.17 3.15-1.17.62 1.57.23 2.74.11 3.03.74.8 1.18 1.82 1.18 3.07 0 4.39-2.68 5.35-5.23 5.64.41.36.78 1.06.78 2.14v3.18c0 .3.2.66.79.55A11.3 11.3 0 0 0 12 .7Z"/></svg>';
  const themeSvg = '<svg class="icon" data-theme-icon="moon" aria-hidden="true" viewBox="0 0 24 24"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3 6.5 6.5 0 0 0 21 12.8Z"/></svg><svg class="icon" data-theme-icon="sun" aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"/></svg>';

  function normalizeHeader(header, index) {
    if (header.dataset.responsiveReady === '1') return;
    let inner = header.querySelector('.site-header-inner');
    if (!inner) {
      inner = document.createElement('div');
      inner.className = 'site-header-inner';
      while (header.firstChild) inner.appendChild(header.firstChild);
      header.appendChild(inner);
    }
    const nav = inner.querySelector('.nav');
    if (!nav) return;
    let scroll = nav.querySelector('.nav-scroll');
    let actions = nav.querySelector('.nav-actions');
    const legacy = nav.querySelector('.nav-right');

    if (!scroll) {
      scroll = document.createElement('div');
      scroll.className = 'nav-scroll';
      if (legacy) {
        Array.from(legacy.children).forEach((el) => {
          if (el.tagName === 'A' && /github\.com/i.test(el.getAttribute('href') || '')) {
            if (!actions) {
              actions = document.createElement('div');
              actions.className = 'nav-actions';
            }
            el.classList.remove('desktop-only');
            el.classList.add('icon-link','github-action');
            el.setAttribute('aria-label','GitHub');
            el.innerHTML = githubSvg;
            actions.appendChild(el);
          } else if (el.matches('button,.theme-toggle')) {
            if (!actions) {
              actions = document.createElement('div');
              actions.className = 'nav-actions';
            }
            actions.appendChild(el);
          } else if (el.tagName === 'A') {
            el.classList.remove('desktop-only');
            scroll.appendChild(el);
          }
        });
        legacy.remove();
      }
      Array.from(nav.children).forEach((el) => {
        if (el !== scroll && el !== actions && el.tagName === 'DIV' && !el.children.length && !el.textContent.trim()) el.remove();
      });
      nav.prepend(scroll);
    }
    if (!actions) {
      actions = document.createElement('div');
      actions.className = 'nav-actions';
      nav.appendChild(actions);
    } else if (actions.parentElement !== nav) {
      nav.appendChild(actions);
    }

    const theme = actions.querySelector('.theme-toggle') || nav.querySelector('.theme-toggle');
    if (theme) {
      theme.classList.add('theme-toggle');
      theme.type = 'button';
      if (!theme.querySelector('svg')) theme.innerHTML = themeSvg;
      const dark = document.documentElement.classList.contains('dark');
      const moon = theme.querySelector('[data-theme-icon="moon"]');
      const sun = theme.querySelector('[data-theme-icon="sun"]');
      if (moon) moon.hidden = dark;
      if (sun) sun.hidden = !dark;
      theme.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      if (theme.parentElement !== actions) actions.appendChild(theme);
    }

    const menuId = 'rr-nav-menu-' + index;
    scroll.id = scroll.id || menuId;
    let toggle = actions.querySelector('.mobile-menu-toggle');
    if (!toggle) {
      toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'mobile-menu-toggle';
      toggle.setAttribute('aria-controls', scroll.id);
      toggle.setAttribute('aria-expanded','false');
      toggle.setAttribute('aria-label','Open menu');
      toggle.innerHTML = menuSvg;
      if (theme && theme.parentElement === actions) actions.insertBefore(toggle, theme);
      else actions.appendChild(toggle);
    }

    const close = (restoreFocus=false) => {
      header.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded','false');
      toggle.setAttribute('aria-label','Open menu');
      toggle.innerHTML = menuSvg;
      document.body.classList.remove('rr-menu-open');
      if (restoreFocus) toggle.focus();
    };
    const open = () => {
      header.classList.add('nav-open');
      toggle.setAttribute('aria-expanded','true');
      toggle.setAttribute('aria-label','Close menu');
      toggle.innerHTML = closeSvg;
      document.body.classList.add('rr-menu-open');
    };
    toggle.addEventListener('click', (event) => {
      event.stopPropagation();
      header.classList.contains('nav-open') ? close() : open();
    });
    scroll.addEventListener('click', (event) => {
      if (event.target.closest('a')) close();
    });
    document.addEventListener('click', (event) => {
      if (header.classList.contains('nav-open') && !header.contains(event.target)) close();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && header.classList.contains('nav-open')) close(true);
    });
    const mq = window.matchMedia('(min-width:761px)');
    const sync = () => { if (mq.matches) close(); };
    if (mq.addEventListener) mq.addEventListener('change', sync);
    else if (mq.addListener) mq.addListener(sync);
    header.dataset.responsiveReady = '1';
  }

  onReady(() => {
    document.querySelectorAll('.rr-global-header').forEach(normalizeHeader);
    document.documentElement.classList.add('rr-responsive-ready');
  });
})();
