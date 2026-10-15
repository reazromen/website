# Reaz Romen website design-system audit

## Baseline

- Reference direction: the existing Antfu-inspired editorial shell: restrained palette, system typography, narrow readable prose, thin dividers, clear link hierarchy, and a shared responsive header/footer.
- Shared visual tokens and shell rules: `assets/site.css`.
- Cross-page component and editorial layout overrides: `assets/sitewide-v2.css`.
- Responsive layout and navigation: `assets/responsive-v3.css` and `assets/responsive-v3.js`.
- Page-specific styling is allowed where the content needs it (for example `assets/telecom.css`), but should use the shared tokens rather than introducing a second global shell.

## Findings

1. Multiple global CSS layers are loaded on most generated pages (`site.css`, `sitewide-v2.css`, `phase1.css`, `phase2.css`, `responsive-v3.css`). The order matters and overlapping selectors using `!important` make blanket stylesheet deletion unsafe.
2. The mobile navigation CSS deliberately hides `.nav-scroll` until `.rr-global-header.nav-open` is set, with a hamburger inserted by `responsive-v3.js`. This conflicts with the requirement that navigation links remain visible on mobile.
3. Several pages have page-specific header/footer markup (the Telecom template is one example), so visual consistency should be validated against generated output before consolidating markup.
4. The accessibility skip link and keyboard focus styles are intentional and must be retained; they are not stray tool annotations.

## Change made

At mobile widths (760px and below), navigation links now remain visible and wrap onto additional lines. The hamburger is hidden, the theme toggle remains visible, and menu links are not collapsed into a hidden panel. Desktop navigation behavior is unchanged.

## Verification checklist

- [x] CMS preservation/renderer validation passed: 1,127 preserved article URLs; title/body/link/image checks and CMS renderer/listing checks passed.
- [x] Public artifact rebuilt with `cms/package_public.py`.
- [x] Static audit confirms 2,247 site HTML files load `responsive-v3.css`; the two `reference-reader` aliases are intentionally standalone and do not use the global navigation shell.
- [ ] Visual browser checks at 320px, 375px, 430px, 760px, 761px, and desktop widths remain to be completed; no browser automation is installed in this hserver environment.
- [ ] Check light/dark mode, focus visibility, dropdowns, and page-specific headers/footers in a browser.
- [ ] Verify GitHub Pages origin and `reazromen.com` after publishing.

## Safe next steps

Consolidate duplicate global rules only after computed-style and rendered-page checks. Migrate page-specific shells in small batches, preserving existing URLs, article content, accessibility affordances, and specialized layouts.
