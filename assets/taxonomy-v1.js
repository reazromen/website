document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('[data-taxonomy-filter]');
  if (!input) return;
  const rows = [...document.querySelectorAll('.taxonomy-index .topic-card')];
  const counter = document.querySelector('[data-taxonomy-count]');
  input.addEventListener('input', () => {
    const term = input.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const row of rows) {
      const match = row.querySelector('strong').textContent.toLocaleLowerCase().includes(term);
      row.hidden = !match;
      if (match) count++;
    }
    if (counter) counter.textContent = `${count} matches`;
  });
});
