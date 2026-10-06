# CMS edge route

The public CMS entry is https://reazromen.com/admin. The Pages Worker proxies /admin/ and /admin/api/v1 to the existing Authelia-protected studio origin without moving the browser to that hostname. Authentication remains enforced upstream. Login return URLs point back to the public /admin/ path. Admin responses are never cached.

Deploy only _worker.js, _headers and _routes.json to the existing reazromen-static Pages project. Keep backup files and this documentation outside the upload directory. The GitHub Pages public-site route is unchanged.
