# reazromen.com Deployment Architecture

Status: production Git-backed delivery active.

## Canonical source
- Repository: `reazromen/website`
- Branch: `main`
- Public source: repository root
- GitHub Pages publishes `main`
- Cloudflare Pages provides the public edge/router and authenticated `/admin`

## Operational authoring path
The verified workstation path is LOUP:
- clone: `/home/loup/projects/reazromen-website`
- GitHub account: `reazromen`
- Git transport: SSH
- helper command: `website-publish`

Routine commands:

```bash
website-publish status
website-publish sync
website-publish verify
website-publish release "content: describe the change" path/to/file
```

The release command stages only the explicit file paths provided. It refuses to publish if the branch is not `main`, if unrelated staged changes already exist, or if local `main` is not synchronized with `origin/main`.

## Delivery path
```
LOUP terminal or GitHub editor
→ reazromen/website:main
→ GitHub Pages
→ Cloudflare Pages edge router
→ reazromen.com
```

GitHub Pages origin:
`https://reazromen.github.io/website/`

Cloudflare Pages project:
`reazromen-static`

The Cloudflare worker:
- proxies public paths to GitHub Pages,
- serves `/admin` from Cloudflare assets behind Basic Auth,
- preserves clean URL fallbacks such as `/about` and `/portfolio`,
- adds `X-Reaz-Delivery: github-pages-via-cloudflare-pages`.

## Optional Pages CMS
The repository still contains `.pages.yml`. Pages CMS can be authorized later as an optional Git-backed GUI, but it is not required for production publishing.

## Production rules
1. Public content changes land in this repository.
2. Pushes to `main` publish through GitHub Pages.
3. LOUP or direct GitHub editing are canonical production-authoring paths.
4. Do not deploy the old hserver static tree for normal content changes.
5. Do not commit edge secrets, Basic Auth credentials, API tokens, or private runtime configuration.
6. The hserver website editor and old direct-upload scripts are rollback/reference only and cannot publish production.

## Verification
On 2026-09-28 a temporary file was committed and pushed from LOUP, appeared on both GitHub Pages and `reazromen.com`, then was deleted by a cleanup commit and disappeared from both origins.

Use `website-publish verify` to check:
- homepage,
- About,
- Portfolio,
- GitHub Pages origin,
- Cloudflare delivery header.
