# Article version history (development preview)

Status: development-only. This feature is available on `dev.reazromen.com`; it is not enabled on `reazromen.com`.

## What readers can do

- Open **Article versions** on an article page.
- Select a saved version and preview its complete title, introduction and body text.
- Read the AI-generated summary of the changes from the preceding version, including additions, removals, revisions and whether the article's main argument changed.

## What editors can do

Authenticated editors can save a changed article as a new immutable version. The editor does not overwrite the published article. The first edit stores the currently published text as a baseline, then saves the new revision. Existing articles are not processed in bulk.

## AI and data integrity

Only a new, changed revision triggers a summary request. The request uses the same zero-cost AI mesh as Content Studio. A saved version is committed before the AI call; if the model fails, the version remains readable and the summary is marked failed. The AI never writes back into article text or earlier versions. Re-submitting identical content does not create a new version or call a model.

## Documentation and implementation

The API, schema migration, authentication boundary, validation and rollback procedure are documented in the Content Studio repository at `docs/article-version-history.md`. The browser interface is a dev-only asset, `assets/article-versioning-preview.js`. `cms/prepare_article_versioning_preview.py` applies that overlay to a completed `dist/` build; it is deliberately excluded from the public artifact because the `cms/` directory is not packaged. Public version reads are served by the dev API; revision writes are protected by the existing Authelia forward-auth gate.

## Production boundary

This is a preview environment. The production site is built from `reazromen/website` on `main` through the canonical GitHub Pages workflow. Do not publish the editor script or route to production until the development checks pass and the production cutover is explicitly approved.


## Preview deployment check — 2026-10-20

The dev site was rebuilt from the same canonical artifact as production at commit `ecf5a165de77f1f7bc9f75af935766c079c2bb46` (1,804 posts, 118 pages, 43 topics and 1,056 tags). The current production `sitewide.js` hotfix was synchronized into dev, with a hostname guard that disables analytics on `dev.reazromen.com` so preview traffic does not contaminate production metrics. This creates an intentional dev-specific asset hash; article content and build metadata are aligned. The dev host returns `X-Robots-Tag: noindex, nofollow` and a disallow-all `robots.txt`. Public history reads work; unauthenticated revision writes are denied. A synthetic two-version test generated a Kilo summary, retrieved both full text snapshots and verified duplicate submissions are idempotent; synthetic rows were removed afterward. Production was not modified.
