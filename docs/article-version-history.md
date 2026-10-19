# Public article version history and editing

Status: enabled through the public article editor. The static site remains published through GitHub Pages; version snapshots and public edits are stored by the API hosted at `dev.reazromen.com`.

## Public behavior

- Any visitor can open **Article versions**, edit the title, introduction and article text, and save a new revision. There is no approval queue.
- A successfully saved revision immediately becomes the latest version shown to subsequent visitors. The original static article remains the fallback until a revision exists.
- Readers can select earlier snapshots and inspect the AI-generated change summary. Choosing an older version previews it locally; it does not roll back the shared latest version.
- The server labels edits as **Public contributor**; visitors cannot claim another person's identity through the editor.

## Integrity and abuse controls

Each revision is an immutable snapshot. The first edit records the current public article as a baseline. Identical submissions do not create duplicate versions. The free AI mesh summarizes diffs only; it never rewrites the saved article. If AI summary generation fails, the edit remains saved and the summary status reports failure.

Public writes are limited to article URL prefixes (`/posts/`, `/perspectives/`, `/research/`, `/writing/`, `/bangla/`), require a browser Origin from the configured site origins, and are rate-limited to eight writes per IP per hour per API process. These controls reduce accidental and automated abuse but do not provide moderation or guarantee that all contributions are appropriate. Since no approval is required, public edits can replace the current displayed version immediately.

## Operations

- Public API: `https://dev.reazromen.com/api/article-versions`
- Health: `https://dev.reazromen.com/health` on the internal API listener; the public proxy exposes the article API.
- API code: `app/article_versioning_api.py` in the Content Studio repository.
- UI: `assets/article-versioning-preview.js`; the public publishing workflow injects it only into rendered article pages.
- AI summaries use the existing zero-cost AI mesh. No bulk backfill is performed.

## Rollback

Remove the workflow injection step and editor asset to hide the UI. Stored history is retained in the database. To disable public writes, restore the Caddy forward-auth gate and the API authentication check, then redeploy the API. Do not drop the history table during routine rollback.

[executed on device: hserver (e3ce91f8-8d4c-413e-b14d-04ad4fe8d7e3)]