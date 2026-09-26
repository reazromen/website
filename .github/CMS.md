# Website content management

The public site stays static. Editing is Git-backed.

## Primary GUI

Pages CMS uses the repository-root `.pages.yml` file.

Hosted editor:
https://app.pagescms.org

Initial account setup requires signing in with GitHub and installing the Pages CMS GitHub App for `reazromen/website`. After that, edits made in Pages CMS are commits to this repository and the existing GitHub Pages deployment publishes them.

Official configuration documentation:
https://pagescms.org/docs/configuration/

## What is manageable

### Global controls
- Main navigation: `assets/navigation.json`
- Menu ordering and visibility
- Optional submenus
- Redirects

### Core pages
Homepage, About, Work, Perspectives, Music, Bangla, Stack, Writing, Topics, Archive, Search, Now, Notes and Services are available as code editors.

### Content collections
- Articles: `posts/`
- Topics: `topics/`
- Domains: `domains/`
- Portfolio: `portfolio/`
- Music: `music/`
- Archive and author pages

### Tags
Article tags already use Pagefind `topic` filters.
Editing article HTML and committing it triggers `.github/workflows/rebuild-pagefind.yml`, which rebuilds the search/tag index automatically.

### Advanced
Theme CSS, global behavior JS, responsive assets, tag/search behavior and HTTP headers are exposed under an Advanced group. Use these only for deliberate site-wide changes.

## Publication path

Pages CMS or GitHub web editor
→ commit to `main`
→ repository verification
→ Pagefind rebuild when HTML changed
→ GitHub Pages
→ Cloudflare edge
→ reazromen.com

The hserver is not required for normal content publishing.

## Safety

- Existing hardcoded navigation remains in HTML as fallback.
- `assets/navigation.json` is the live central navigation source.
- Core pages cannot be deleted from the Pages CMS UI.
- Generated `pagefind/` files are not edited manually.
- Cloudflare admin/runtime files are not stored in this public CMS repository.

## GitHub-only editing

Pages CMS is optional. Every source remains editable from GitHub:
1. Open `reazromen/website`.
2. Open the file.
3. Click Edit.
4. Commit to `main`.

For multiple files, press `.` on the repository page to open github.dev.
