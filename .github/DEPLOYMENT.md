# reazromen.com Deployment Architecture

Status: production cutover completed 2026-09-26.

## Canonical public source
- Repository: reazromen/website
- Branch: main
- Public source is the repository root.
- GitHub Pages builds and publishes every push to main.
- GitHub-hosted runners are used for repository verification; hserver is not required for normal public-site deployment.

## Delivery path
git push -> GitHub main -> GitHub Pages -> Cloudflare Pages edge router -> reazromen.com

GitHub Pages origin:
https://reazromen.github.io/website/

Cloudflare Pages project:
reazromen-static

The Cloudflare Pages project contains a small _worker.js edge router.
- Public paths are fetched from GitHub Pages.
- /admin and /admin/* remain served by the Cloudflare Pages ASSETS binding and existing Basic-auth protection.
- Clean URL fallbacks preserve /about, /writing, /systems and similar routes.

## Production rules
1. Public content changes happen in this repository.
2. Push/merge to main publishes through GitHub Pages automatically.
3. Do not deploy the old hserver static tree for normal content changes.
4. Do not commit admin runtime, _worker.js, _routes.json, passwords, API tokens or private configuration into this public repository.
5. The old Cloudflare Pages static deployment remains the rollback baseline only.
6. The private reazromen/reaz-portfolio-webapp repository remains the Payload/CMS migration workspace, not the current public deployment source.

## Cutover proof
Production edge deployment after cutover: cedd77d2 on reazromen-static.
Git bootstrap commit: c73de17acdc5d406438ed2ffa0be0525b55e2750.
Homepage, About, Writing, Systems, a representative article, feed.xml and site.css matched the locked pre-cutover production body hashes.
Admin continued to return HTTP 401 without credentials.
