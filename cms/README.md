# Website publishing

Open https://reazromen.com/admin. Authelia remains the only login. No GitHub token is requested by the CMS. The browser stays on /admin/ after sign-in; the studio hostname is only the protected upstream. Edge routing and its checks are versioned in cms/cloudflare-pages-router/.

## Where to edit

| CMS collection | Purpose |
| --- | --- |
| Writing | Existing engineering articles and new technical writing |
| Perspectives | Long-form essays |
| Music | Personal song notes, album notes, performance notes and research listening notes |
| বাংলা | Bangla articles |
| Topics | Broad subjects, their names, descriptions and archive introductions |
| Tags | Reusable detailed labels and tag archive descriptions |
| Pages | Homepage, About, portfolio/project pages, section introductions and other existing pages |
| Site settings → Menus | Header links, dropdowns, footer links, visibility and order |

Every legacy article is now a Markdown record with structured metadata. Its existing URL is retained. Unedited article bodies retain the original HTML internally so formatting, code, tables, links and images are preserved; editing the Body field renders the revised Markdown into that article's existing layout. You do not edit HTML templates through the CMS.

## Publish an article

1. Create a needed topic or tag first, or use existing entries.
2. Open the relevant writing collection and create an entry.
3. Enter title, date, excerpt, reading time and body. Select a topic and any tags using the searchable selectors.
4. Music also has artist, album, year and type. Research notes remain separate from personal listening notes.
5. New posts default to Draft. Save while writing. Turn Draft off and save when ready to publish.
6. Wait for the **Build and publish website** GitHub Action to finish. That build renders all content, archives, taxonomy pages, feeds, sitemap and search together, then publishes one complete artifact.

Dates describe publication history; entering a future date does not schedule a post. Use Draft until you want it public. The local Git sync normally pushes a clean CMS commit within about eight seconds; the site build takes a few minutes.

Keep an existing URL unchanged. New posts can leave URL empty and receive `/posts/<filename>.html`. If an existing article's URL is deliberately changed, the former article URL continues to serve the same content with the new canonical URL.

Featured articles take priority in the homepage's three recent-writing positions, followed by newest articles.

## Topics and tags

Topics are broad groupings such as telephony, embedded firmware or observability. Tags are narrower reusable labels. Change a taxonomy entry's title to rename its display everywhere while retaining the stable stored ID and URL. The public archives are `/topics.html` and `/tags.html`; individual archives list the matching published posts.

Do not delete a topic or tag until you have removed or reassigned every post using it. The renderer intentionally rejects dangling references, so a mistake cannot silently drop posts from their archives. Git history can restore any CMS deletion. Existing tag vocabulary was preserved, not editorially merged or rewritten.

## Pages and menus

Existing designed pages use named **Content blocks** and **Links**. Edit those normal fields to change their text and destinations while retaining their layout. Generated article lists are derived from posts and cannot be manually broken through the page editor. For topic names and descriptions, use Topics rather than the corresponding page heading.

For a new standalone page, supply a URL such as `/contact.html` and write its Body. Add it to Site settings → Menus if it should be in navigation. Drag menu entries to reorder them, add dropdown children, or switch Enabled off to hide a link without deleting the page.

Images are managed through the CMS media library (`static/uploads`). Article body images and optional cover image/alt text are supported.

## Architecture and recovery

Authelia → Decap proxy on hserver → repository-scoped SSH deploy key → GitHub → one render/search/Pages deployment → existing Cloudflare route. No database was added. The CMS admin configuration is versioned at `cms/admin/config.yml` and refreshed on hserver by the sync service.

Content source is in `content/`. Layouts and preservation fragments are in `cms/templates/`. The renderer validates URL collisions, taxonomy references and template locations before modifying output. Deleted and draft records are removed from the generated output using `cms/generated-manifest.json`. Only public files enter the deployment artifact; CMS source files and drafts are excluded.

The migration baseline commit and URL map are recorded in `content/migration.json`. `cms/migration-baseline.json` records original article text, links and images for the one-time preservation audit. `cms/validate_content.py` verifies migration fidelity; it should not be required after intentional editorial changes, which naturally differ from the baseline.

To roll back an editorial change, revert its Git commit and allow the publishing workflow to run. To restore the former publishing architecture, restore the pre-migration Git revision and its workflow files, set GitHub Pages to its former branch source, and restore the backed-up admin config and Git sync script on hserver.


## Publication year archives

The Archive now groups published posts by the recorded Date field. The year links cover 2017–2026 and update on each publish. Empty historical years remain empty until dated original material is supplied. Never change a publication date merely to fill a year. Bangla articles appear on the Bangla page across writing collections. The October 2 batch contains 100 short Bangla posts: 65 engineering notes, 25 essays and 10 research listening notes.
