#!/usr/bin/env bash
# DV-IAS 项目 → 课程仓库 同步脚本
# 用法：在项目根目录（数字乡村/）执行 bash course/sync/sync-from-project.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CR="$ROOT/course"
PREF="$CR/project-ref"
cd "$ROOT"

echo "→ 1/4 同步项目文档"
cp -f docs/0*.md docs/1*.md "$PREF/" 2>/dev/null || true
mkdir -p "$PREF/adr" && cp -f docs/adr/*.md "$PREF/adr/" 2>/dev/null || true

echo "→ 2/4 同步工程教学素材"
mkdir -p "$PREF/perf" "$PREF/test" "$PREF/scripts"
cp -f dv-ias/perf/*.js "$PREF/perf/" 2>/dev/null || true
cp -f dv-ias/perf/locustfile.py "$PREF/perf/" 2>/dev/null || true
cp -f dv-ias/test/*.py "$PREF/test/" 2>/dev/null || true
cp -f dv-ias/scripts/*.sh "$PREF/scripts/" 2>/dev/null || true

echo "→ 3/4 敏感信息扫描"
if grep -rInE "szxc@2026|SzxcRedis|SzxcRo-|SzxcJwt|BEGIN (RSA|EC) PRIVATE" \
     --include="*.md" "$PREF" >/tmp/sync_secret_hit.txt 2>/dev/null; then
  if [ -s /tmp/sync_secret_hit.txt ]; then
    echo "!! 检出疑似敏感信息，已中止。请人工处理："; cat /tmp/sync_secret_hit.txt
    exit 1
  fi
fi

echo "→ 4/4 提交"
cd "$CR"
git add -A
MSG="sync(project): 同步项目更新 [$(date +%F)]"
if ! git diff --cached --quiet; then
  git commit -m "$MSG"
  echo "✓ 已提交：$MSG（记得 git push）"
else
  echo "✓ 无变更"
fi