# Website content management

## Canonical production model

Production source: `reazromen/website`, branch `main`.

GitHub web editor or authenticated LOUP terminal
→ reazromen/website (main)
→ repository checks / Pagefind rebuild when applicable
→ GitHub Pages
→ Cloudflare Pages edge router
→ reazromen.com

## Operational publishing

The verified operational publishing path is the LOUP workstation:
- local clone: `/home/loup/projects/reazromen-website`
- GitHub account: `reazromen`
- Git transport: SSH
- push target: `origin/main`

A live smoke test on 2026-09-28 pushed a temporary static file from LOUP, verified it on both GitHub Pages and `reazromen.com`, then removed it with a cleanup commit.

Routine workflow:

    cd /home/loup/projects/reazromen-website
    git pull --ff-only origin main
    # edit content
    git add <files>
    git commit -m "content: describe the change"
    git push origin main

Direct editing in GitHub or github.dev is equally canonical.

## Optional Pages CMS

The repository includes `.pages.yml`, so Pages CMS remains available as an optional Git-backed GUI. It is not required for production publishing. If authorized later, Pages CMS commits must still land in `reazromen/website` and use the same GitHub Pages → Cloudflare delivery path.

## Managed content

- Navigation: `assets/navigation.json`
- Core pages: repository-root HTML files
- Articles: `posts/`
- Topics: `topics/`
- Domains: `domains/`
- Portfolio: `portfolio/`
- Music: `music/`
- Media: `static/uploads/`

HTML commits trigger `.github/workflows/rebuild-pagefind.yml`, which refreshes the Pagefind search/tag index.

## Cloudflare and hserver

Cloudflare Pages project `reazromen-static` is the production edge/router, not the content source. Normal public requests are proxied to GitHub Pages. The authenticated `/admin` surface is served by Cloudflare edge assets.

The hserver `reazromen-antfu-live` tree and legacy website editor are rollback/reference only. Their preview/production deploy paths remain disabled.
