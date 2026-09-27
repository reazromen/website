# Website content management

## Canonical production model

The public website is Git-backed and static.

```
Pages CMS or GitHub editor
→ reazromen/website (main)
→ repository verification / Pagefind rebuild when needed
→ GitHub Pages
→ Cloudflare Pages edge router
→ reazromen.com
```

The canonical production source is the public repository `reazromen/website`, branch `main`. The hserver is not required for normal publishing.

## Primary CMS

Pages CMS reads the repository-root `.pages.yml` configuration.

Hosted editor: https://app.pagescms.org

First-time use requires signing in with GitHub and granting the Pages CMS GitHub App access to `reazromen/website`. That authorization is the only account-side step; the CMS configuration is already versioned in the repository.

Pages CMS edits are Git commits, so CMS changes and direct code changes share the same history and rollback model.

## Managed content

- Navigation and submenus: `assets/navigation.json`
- Core pages: Homepage, About, Work, Perspectives, Music, Bangla, Stack, Writing, Topics, Archive, Search, Now, Notes and Services
- Articles: `posts/`
- Topics: `topics/`
- Domains: `domains/`
- Portfolio: `portfolio/`
- Music: `music/`
- Media uploads: `static/uploads/`
- Advanced theme/behavior files are exposed separately and should only be changed deliberately

Article HTML commits trigger `.github/workflows/rebuild-pagefind.yml`, which refreshes the Pagefind search and tag index and commits the generated index back to `main`.

## Cloudflare role

Cloudflare Pages project `reazromen-static` is the edge/router, not the public content source. Normal public requests are proxied to `https://reazromen.github.io/website/`. The authenticated `/admin` surface is served by the Cloudflare edge package.

## Legacy hserver editor

`studio.reazromen.com/website-editor/` is retained only as a rollback/reference editor for the local hserver copy. Its preview and production deployment actions are disabled after the GitHub Pages cutover.

Do not use the old `reazromen-antfu-live/deploy.sh` or `deploy-preview.sh` direct-upload path for production. Those scripts are guarded and exit intentionally.

## GitHub-only editing

Pages CMS is optional. Every source file remains editable directly in GitHub:

1. Open `reazromen/website`.
2. Edit the required file, or press `.` to use github.dev for multi-file changes.
3. Commit to `main`.
4. GitHub Pages republishes the repository; Cloudflare continues to serve it through the production domain.
