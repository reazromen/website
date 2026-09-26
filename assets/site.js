(()=>{const root=document.documentElement,key='vueuse-color-scheme',saved=localStorage.getItem(key)||'auto',mq=matchMedia('(prefers-color-scheme: dark)');const apply=dark=>{root.classList.toggle('dark',dark);document.querySelectorAll('.theme-toggle').forEach(btn=>{const moon=btn.querySelector('[data-theme-icon="moon"]'),sun=btn.querySelector('[data-theme-icon="sun"]');if(moon)moon.hidden=dark;if(sun)sun.hidden=!dark;btn.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode')})};apply(saved==='dark'||(saved==='auto'&&mq.matches));window.toggleTheme=()=>{const next=!root.classList.contains('dark');localStorage.setItem(key,next?'dark':'light');apply(next)};if(saved==='auto')mq.addEventListener?.('change',e=>apply(e.matches))})();

/* REAZ_MEDIA_SOURCE_CLOUDINARY_V1 */
;(() => {
  const HOST = 'https://res.cloudinary.com/';
  function optimizeCloudinary(url, width) {
    if (typeof url !== 'string' || !url.startsWith(HOST) || !url.includes('/upload/')) return url;
    if (/\/upload\/[^/]*(?:f_auto|q_auto)[^/]*\//.test(url)) return url;
    const w = Number(width);
    const transform = Number.isFinite(w) && w > 0 ? `f_auto,q_auto,w_${Math.round(w)}` : 'f_auto,q_auto';
    return url.replace('/upload/', `/upload/${transform}/`);
  }
  window.ReazMedia = Object.freeze({ defaultSource: 'cloudinary', cloudinaryHost: HOST, optimizeCloudinary });
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('img[data-image-source="cloudinary"]').forEach((img) => {
      const source = img.dataset.src || img.getAttribute('src') || '';
      img.src = optimizeCloudinary(source, img.dataset.width || img.width || 0);
      if (!img.hasAttribute('loading')) img.loading = 'lazy';
      if (!img.hasAttribute('decoding')) img.decoding = 'async';
      img.referrerPolicy = 'strict-origin-when-cross-origin';
    });
  });
})();
