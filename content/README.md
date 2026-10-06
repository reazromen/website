# Structured CMS content

These folders are the authoring source for new CMS-created editorial content.

- music/ — listening notes, album notes and performance notes
- movies/ — movie notes and film essays
- perspectives/ — long-form technical/editorial writing
- bangla/ — Bangla writing

Sveltia CMS writes Markdown with YAML front matter here. The Build CMS content GitHub Action renders published entries into HTML files under posts and inserts archive entries into music.html, perspectives.html, and bangla.html.

Existing hand-authored HTML remains valid and is not migrated or overwritten.
