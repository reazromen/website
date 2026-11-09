(() => {
  const init = () => {
    const bar = document.querySelector('.rr-share');
    if (!bar || bar.dataset.ready === 'true')
      return;
    bar.dataset.ready = 'true';

    const canonical = document.querySelector('link[rel="canonical"]')?.href || location.href;
    const url = canonical;
    const title = document.querySelector('main article h1')?.textContent?.trim()
      || document.title.replace(/\s*[—|]\s*Reaz Romen.*$/, '');
    const encodedUrl = encodeURIComponent(url);
    const encodedText = encodeURIComponent(title + ' — ' + url);
    const destinations = {
      facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + encodedUrl,
      whatsapp: 'https://api.whatsapp.com/send?text=' + encodedText,
      x: 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodedUrl,
      linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodedUrl,
      medium: 'https://medium.com/p/import?url=' + encodedUrl
    };

    bar.querySelectorAll('[data-share]').forEach((link) => {
      const destination = destinations[link.dataset.share];
      if (destination)
        link.href = destination;
      else
        link.remove();
    });

    const status = bar.querySelector('.rr-share-status');
    const copyButton = bar.querySelector('[data-share-copy]');
    const nativeButton = bar.querySelector('[data-share-native]');

    const copyText = async (value) => {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(value);
        return;
      }
      const field = document.createElement('textarea');
      field.value = value;
      field.setAttribute('readonly', '');
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.append(field);
      field.select();
      const copied = document.execCommand('copy');
      field.remove();
      if (!copied)
        throw new Error('Clipboard unavailable');
    };

    copyButton?.addEventListener('click', async () => {
      try {
        await copyText(url);
        if (status)
          status.textContent = 'Link copied.';
        copyButton.textContent = 'Copied';
        window.setTimeout(() => {
          copyButton.textContent = 'Copy link';
          if (status)
            status.textContent = '';
        }, 1800);
      }
      catch {
        if (status)
          status.textContent = 'Could not copy automatically. Copy the page address from your browser.';
      }
    });

    if (navigator.share && nativeButton) {
      nativeButton.hidden = false;
      nativeButton.addEventListener('click', async () => {
        try {
          await navigator.share({ title, text: title, url });
        }
        catch (error) {
          if (error?.name !== 'AbortError' && status)
            status.textContent = 'Sharing was not available on this device.';
        }
      });
    }
  };

  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', init, { once: true });
  else
    init();
})();
