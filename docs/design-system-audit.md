# Reaz Romen website design-system audit

## Baseline

- Reference direction: the existing Antfu-inspired editorial shell: restrained palette, system typography, narrow readable prose, thin dividers, clear link hierarchy, and a shared responsive header/footer.
- Shared visual tokens and shell rules: `assets/site.css`.
- Cross-page component and editorial layout overrides: `assets/sitewide-v2.css`.
- Responsive layout and navigation: `assets/responsive-v3.css` and `assets/responsive-v3.js`.
- Page-specific styling is allowed where the content needs it (for example `assets/telecom.css`), but should use the shared tokens rather than introducing a second global shell.

## Findings

1. Multiple global CSS layers are loaded on most generated pages (`site.css`, `sitewide-v2.css`, `phase1.css`, `phase2.css`, `responsive-v3.css`). The order matters and overlapping selectors using `!important` make blanket stylesheet deletion unsafe.
2. The old mobile navigation CSS deliberately hid `.nav-scroll` until `.rr-global-header.nav-open` was set, with a hamburger inserted by `responsive-v3.js`.
3. The source audit found 30 pages without a footer and 39 pages using legacy `nav-right` header markup. The current HTML output has been normalized to the shared header/footer from `cms/shell.tpl`; the special research-listening note is retained as a secondary footer note.
4. Some article source metadata has older publication dates than the current published HTML. A full CMS rebuild can therefore change article dates; date/source reconciliation is required before a full content rebuild.
5. The accessibility skip link and keyboard focus styles are intentional and must be retained; they are not stray tool annotations.

## Change made

At mobile widths (760px and below), navigation links remain visible and wrap onto additional lines. The hamburger is hidden, the theme toggle remains visible, and menu links are not collapsed into a hidden panel. The override lives in the new `assets/mobile-nav.css` path to avoid the stale cached `responsive-v3.css` URL. The shared header/footer now use the canonical shell, missing skip links and footers were added, and the research-listening note was preserved where it applies. Changes were restricted to header/footer/accessibility chrome and stylesheet references; the 2,247 pages’ `<main>` content hashes were verified unchanged.

## Verification checklist

- [x] CMS preservation/renderer validation passed: 1,127 preserved article URLs; title/body/link/image checks and CMS renderer/listing checks passed.
- [x] Public artifact rebuilt with `cms/package_public.py`.
- [x] Static audit confirms 2,247 content pages use the shared header/footer and load the new `mobile-nav.css`; the two `reference-reader` aliases are intentionally standalone and do not use the global navigation shell.
- [x] CMS preservation/renderer validation passed after the chrome-only patch. A full output rebuild was not retained because it would revert some published article dates to stale source metadata.
- [ ] Visual browser checks at 320px, 375px, 430px, 760px, 761px, and desktop widths remain to be completed; no browser automation is installed in this hserver environment.
- [ ] Check light/dark mode, focus visibility, dropdowns, and page-specific headers/footers in a browser.
- [ ] Verify GitHub Pages origin and `reazromen.com` after publishing.

## Safe next steps

The old mobile-collapse rules have been removed from `responsive-v3.css`; `mobile-nav.css` now owns the visible/wrapping mobile-navigation behavior. Broader global CSS consolidation still requires rendered browser checks because the site has overlapping `!important` rules. Reconcile stale source publication dates before any full CMS rebuild, and verify the deployed mobile layout at 320px, 375px, 430px, 760px, 761px, and desktop widths.
