const PUBLIC_ORIGIN = "https://reazromen.github.io";
const PUBLIC_BASE = "/website";
const REFERENCE_INDEX =
  "https://raw.githubusercontent.com/reazromen/website/main/reference-reader/sites.json";


function githubTarget(pathname, search = "") {
  const path = pathname === "/" ? "/" : pathname;
  return new URL(PUBLIC_BASE + path + search, PUBLIC_ORIGIN);
}
async function fetchPublic(request, url) {
  const makeRequest = (pathname) => {
    const target = githubTarget(pathname, url.search);
    return new Request(target.toString(), request);
  };

  let response = await fetch(makeRequest(url.pathname));
  if ((request.method === "GET" || request.method === "HEAD") && response.status === 404) {
    const path = url.pathname;
    const hasExtension = /\/[^/]+\.[^/]+$/.test(path);
    if (!hasExtension && path !== "/") {
      const candidates = path.endsWith("/")
        ? [path + "index.html"]
        : [path + ".html", path + "/index.html"];
      for (const candidate of candidates) {
        const retry = await fetch(makeRequest(candidate));
        if (retry.status !== 404) {
          response = retry;
          break;
        }
      }
    }
  }

  const headers = new Headers(response.headers);
  headers.set("X-Reaz-Delivery", "github-pages-via-cloudflare-pages");
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("X-Frame-Options", "DENY");
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  headers.delete("content-security-policy");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

function escapeAttribute(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function cleanReferenceHtml(source, baseHref) {
  let html = source;
  html = html.replace(/<script\b[^>]*>[\s\S]*?<\/script\s*>/gi, "");
  html = html.replace(/<base\b[^>]*>/gi, "");
  html = html.replace(
    /<meta\b[^>]*http-equiv\s*=\s*["']?content-security-policy["']?[^>]*>/gi,
    ""
  );
  html = html.replace(
    /<meta\b[^>]*http-equiv\s*=\s*["']?refresh["']?[^>]*>/gi,
    ""
  );
  html = html.replace(
    /\son[a-z]+\s*=\s*(".*?"|'.*?'|[^\s>]+)/gi,
    ""
  );
  html = html.replace(
    /\scrossorigin(?:\s*=\s*(".*?"|'.*?'|[^\s>]+))?/gi,
    ""
  );

  const base = '<base href="' + escapeAttribute(baseHref) + '" target="_blank">';
  if (/<head\b[^>]*>/i.test(html)) {
    html = html.replace(/<head\b[^>]*>/i, (match) => match + base);
  } else {
    html = base + html;
  }
  return html;
}

async function fetchReferencePage(url) {
  const index = Number(url.searchParams.get("i"));
  if (!Number.isInteger(index) || index < 0) {
    return new Response("Invalid reference index", { status: 400 });
  }

  const listResponse = await fetch(REFERENCE_INDEX, {
    headers: { Accept: "application/json" },
  });
  if (!listResponse.ok) {
    return new Response("Reference index unavailable", { status: 502 });
  }

  const sites = await listResponse.json();
  if (!Array.isArray(sites) || index >= sites.length || !sites[index]?.url) {
    return new Response("Reference not found", { status: 404 });
  }
  let target;
  try {
    target = new URL(sites[index].url);
  } catch {
    return new Response("Invalid reference URL", { status: 400 });
  }
  if (target.protocol !== "https:" && target.protocol !== "http:") {
    return new Response("Unsupported reference URL", { status: 400 });
  }

  let upstream;
  try {
    upstream = await fetch(target.toString(), {
      redirect: "follow",
      headers: {
        Accept: "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
      },
    });
  } catch {
    return new Response("Reference site could not be reached", { status: 502 });
  }

  const contentType = upstream.headers.get("content-type") || "";
  if (!upstream.ok || !contentType.toLowerCase().includes("text/html")) {
    return new Response("Reference page could not be rendered", {
      status: upstream.status || 502,
    });
  }

  const body = cleanReferenceHtml(await upstream.text(), upstream.url || target.toString());
  const headers = new Headers({
    "Content-Type": "text/html; charset=UTF-8",
    "Cache-Control": "no-store",
    "X-Robots-Tag": "noindex, nofollow, noarchive",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy":
      "default-src 'none'; style-src 'self' 'unsafe-inline' https: http:; " +
      "img-src 'self' data: blob: https: http:; font-src 'self' data: https: http:; " +
      "media-src 'self' data: blob: https: http:; script-src 'none'; connect-src 'none'; " +
      "frame-src 'none'; object-src 'none'; form-action 'none'; base-uri *; frame-ancestors 'self'",
  });
  return new Response(body, { status: 200, headers });
}


const CMS_ORIGIN = "https://studio.reazromen.com";
const CMS_PUBLIC_ORIGIN = "https://reazromen.com";

function cmsLocation(value, upstreamUrl) {
  const location = new URL(value, upstreamUrl);
  if (location.origin === CMS_ORIGIN &&
      (location.pathname === "/admin" || location.pathname.startsWith("/admin/"))) {
    return CMS_PUBLIC_ORIGIN + location.pathname + location.search + location.hash;
  }
  if (location.origin === "https://auth.reazromen.com") {
    const returnTo = location.searchParams.get("rd");
    if (returnTo) {
      const destination = new URL(returnTo);
      if (destination.origin === CMS_ORIGIN &&
          (destination.pathname === "/admin" || destination.pathname.startsWith("/admin/"))) {
        location.searchParams.set("rd", CMS_PUBLIC_ORIGIN + destination.pathname + destination.search + destination.hash);
      }
    }
  }
  return location.toString();
}

async function fetchCms(request, url) {
  const headers = new Headers({
    "Cache-Control": "private, no-store, max-age=0",
    "X-Robots-Tag": "noindex, nofollow, noarchive",
    "X-Reaz-Admin": "same-origin-authelia",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "same-origin",
  });
  if (url.pathname === "/admin" || url.hostname === "www.reazromen.com") {
    const path = url.pathname === "/admin" ? "/admin/" : url.pathname;
    headers.set("Location", CMS_PUBLIC_ORIGIN + path + url.search);
    return new Response(null, { status: 308, headers });
  }

  const target = new URL(url.pathname + url.search, CMS_ORIGIN);
  const proxyRequest = new Request(target, request);
  let response;
  try {
    response = await fetch(proxyRequest, { redirect: "manual", cf: { cacheTtlByStatus: { "100-599": -1 } } });
  } catch {
    return new Response("CMS temporarily unavailable. Please try again.", { status: 502, headers });
  }
  const responseHeaders = new Headers(response.headers);
  for (const [key, value] of headers) responseHeaders.set(key, value);
  const originalLocation = responseHeaders.get("Location");
  if (originalLocation) {
    responseHeaders.set("Location", cmsLocation(originalLocation, target));
  }
  const isDocument = request.method === "GET" &&
    (url.pathname === "/admin/" || (request.headers.get("Accept") || "").includes("text/html"));
  if (response.status === 401 && originalLocation && isDocument) {
    // Authelia returns 401 + Location; document navigation needs an HTTP redirect.
    return new Response(null, { status: 302, headers: responseHeaders });
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: responseHeaders,
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/reference-reader/proxy") {
      return fetchReferencePage(url);
    }

    if (url.pathname === "/admin" || url.pathname.startsWith("/admin/")) {
      return fetchCms(request, url);
    }

    return fetchPublic(request, url);
  },
};
