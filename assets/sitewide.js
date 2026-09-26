document.addEventListener('DOMContentLoaded', async () => {
  const currentPath = location.pathname.replace(/\/index\.html$/, '/');
  const existingActiveHref =
    document.querySelector('.rr-global-header a[aria-current="page"]')?.getAttribute('href') || '';

  const activeFor = (href) => {
    try {
      const path = new URL(href, location.origin).pathname.replace(/\/index\.html$/, '/');
      if (existingActiveHref && href === existingActiveHref)
        return true;
      return path === currentPath
        || (path === '/portfolio.html' && (currentPath.startsWith('/portfolio/') || currentPath.startsWith('/projects/')))
        || (path === '/perspectives.html' && (currentPath.startsWith('/posts/') || currentPath.startsWith('/topics/') || currentPath === '/archive.html'))
        || (path === '/music.html' && currentPath.startsWith('/music/'))
        || (path === '/about.html' && currentPath.startsWith('/about/'))
        || (path === '/systems.html' && (currentPath === '/systems/' || currentPath.startsWith('/use/')));
    }
    catch {
      return false;
    }
  };

  const markActiveNavigation = () => {
    document.querySelectorAll('.rr-global-header a[href]').forEach((a) => {
      activeFor(a.getAttribute('href') || '')
        ? a.setAttribute('aria-current', 'page')
        : a.removeAttribute('aria-current');
    });
    document.querySelectorAll('.rr-global-header .nav-group').forEach((group) => {
      group.toggleAttribute('data-current', Boolean(group.querySelector('a[aria-current="page"]')));
    });
  };

  const createLink = (item, labelOverride = '') => {
    if (!item || item.enabled === false || !item.href)
      return null;
    const a = document.createElement('a');
    a.href = item.href;
    a.textContent = labelOverride || item.label || item.href;
    if (item.lang)
      a.lang = item.lang;
    if (item.target) {
      a.target = item.target;
      if (item.target === '_blank')
        a.rel = 'noopener';
    }
    return a;
  };

  const createNavigationNode = (item) => {
    if (!item || item.enabled === false || !item.label)
      return null;

    const children = Array.isArray(item.children)
      ? item.children.filter((child) => child && child.enabled !== false && child.label && child.href)
      : [];

    if (!children.length)
      return createLink(item);

    const group = document.createElement('details');
    group.className = 'nav-group';
    const summary = document.createElement('summary');
    summary.textContent = item.label;
    if (item.lang)
      summary.lang = item.lang;

    const submenu = document.createElement('div');
    submenu.className = 'nav-submenu';

    if (item.href) {
      const overview = createLink(item, 'Overview');
      if (overview) {
        overview.classList.add('nav-submenu-overview');
        submenu.append(overview);
      }
    }

    children.forEach((child) => {
      const link = createLink(child);
      if (link)
        submenu.append(link);
    });

    group.append(summary, submenu);
    return group;
  };

  const renderNavigation = (items) => {
    if (!Array.isArray(items) || !items.length)
      return;
    document.querySelectorAll('.rr-global-header .nav-scroll, .rr-global-header .nav-right').forEach((container) => {
      const nodes = items.map(createNavigationNode).filter(Boolean);
      if (!nodes.length)
        return;
      container.replaceChildren(...nodes);
      container.dataset.navigationSource = 'central';
    });
  };

  try {
    const response = await fetch('/assets/navigation.json', { cache: 'no-cache' });
    if (response.ok) {
      const navigation = await response.json();
      renderNavigation(navigation.main);
    }
  }
  catch {
    // Keep the hardcoded HTML navigation as an offline/failure fallback.
  }

  markActiveNavigation();

  document.addEventListener('click', (event) => {
    document.querySelectorAll('.rr-global-header .nav-group[open]').forEach((group) => {
      if (!group.contains(event.target))
        group.removeAttribute('open');
    });
  });
  document.querySelectorAll('.rr-global-header .nav-submenu a').forEach((a) => {
    a.addEventListener('click', () => a.closest('.nav-group')?.removeAttribute('open'));
  });

  document.querySelectorAll('main a[target="_blank"]:not(.icon-link)').forEach((a) => {
    if (a.querySelector('.ext-icon'))
      return;
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'icon ext-icon');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('viewBox', '0 0 24 24');
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6');
    svg.append(path);
    a.append(svg);
  });

  document.querySelectorAll('pre').forEach((pre) => {
    if (pre.querySelector('.copy-code'))
      return;
    const tools = document.createElement('div');
    tools.className = 'code-tools';
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-code';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code');
    btn.addEventListener('click', async () => {
      const code = pre.querySelector('code')?.innerText || pre.innerText;
      try {
        await navigator.clipboard.writeText(code.replace(/^Copy\s*/, ''));
        btn.textContent = 'Copied';
        setTimeout(() => btn.textContent = 'Copy', 1200);
      }
      catch {}
    });
    tools.append(btn);
    pre.prepend(tools);
  });

  document.querySelectorAll('table').forEach((table) => {
    if (table.parentElement?.classList.contains('table-wrap'))
      return;
    const wrap = document.createElement('div');
    wrap.className = 'table-wrap';
    table.parentNode.insertBefore(wrap, table);
    wrap.append(table);
  });
});
