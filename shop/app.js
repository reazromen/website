const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.main-nav');
if (menuButton && navigation) {
  menuButton.addEventListener('click', () => {
    const isOpen = navigation.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
    menuButton.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
  });
  navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    navigation.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open navigation');
  }));
}
const year = document.querySelector('#year');
if (year) year.textContent = new Date().getFullYear();
const form = document.querySelector('#brief-form');
const note = document.querySelector('#form-note');
if (form && note) {
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const brief = [
      'PROJECT ENQUIRY — FimiT',
      `Name: ${data.get('name')}`,
      `Email: ${data.get('email')}`,
      `Service: ${data.get('service')}`,
      '',
      'Project overview:',
      data.get('message'),
      '',
      'Sent from https://reazromen.com/shop/'
    ].join('\n');
    try {
      await navigator.clipboard.writeText(brief);
      note.textContent = 'Your project brief has been copied. Open the GitHub contact link below and paste it into your message.';
      note.classList.add('success-note');
    } catch (error) {
      const temporary = document.createElement('textarea');
      temporary.value = brief;
      temporary.setAttribute('readonly', '');
      temporary.style.position = 'fixed';
      temporary.style.opacity = '0';
      document.body.appendChild(temporary);
      temporary.select();
      const copied = document.execCommand('copy');
      temporary.remove();
      note.textContent = copied ? 'Your project brief has been copied. Open the GitHub contact link below and paste it into your message.' : 'Copy was blocked by this browser. Please select and copy your details manually.';
      note.classList.toggle('success-note', copied);
    }
  });
}

[executed on device: hserver (4886fa43-9236-4369-8fb8-ad8f790e64ab)]