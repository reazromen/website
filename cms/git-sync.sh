#!/usr/bin/env bash
set -u
repo=/home/romen/deployments/reazromen-git-cms-repo
cd "$repo" || exit 1

install_admin() {
  target=/home/romen/services/hserver-caddy/www/cms-admin
  for file in config.yml guide.html; do
    [ -f "cms/admin/$file" ] || continue
    cmp -s "cms/admin/$file" "$target/$file" && continue
    cp "cms/admin/$file" "$target/$file.tmp" && mv "$target/$file.tmp" "$target/$file"
  done
}

while true; do
  install_admin
  sleep 8
  [ -e .git/index.lock ] && continue
  [ -e .git/HEAD.lock ] && continue
  [ "$(git branch --show-current 2>/dev/null)" = "main" ] || continue
  [ -z "$(git status --porcelain 2>/dev/null)" ] || continue

  if ! git fetch -q origin main; then
    echo "cms-sync: fetch failed" >&2
    continue
  fi

  local_sha=$(git rev-parse main 2>/dev/null) || continue
  remote_sha=$(git rev-parse origin/main 2>/dev/null) || continue
  [ "$local_sha" = "$remote_sha" ] && continue
  base_sha=$(git merge-base main origin/main 2>/dev/null) || continue

  if [ "$base_sha" = "$remote_sha" ]; then
    echo "cms-sync: pushing local CMS commit(s)"
    git push origin main || true
  elif [ "$base_sha" = "$local_sha" ]; then
    echo "cms-sync: fast-forwarding generated remote commit(s)"
    git merge --ff-only origin/main || true
  else
    echo "cms-sync: reconciling concurrent remote changes"
    if git rebase origin/main; then
      git push origin main || true
    else
      git rebase --abort || true
      echo "cms-sync: rebase conflict; manual review required" >&2
    fi
  fi
done
