#!/usr/bin/env python3
"""Validate .claude-plugin/marketplace.json before it reaches a consumer.

WHY THIS EXISTS

marketplace.json is read by every `claude plugin install` and every plugin
update across the fleet. A single malformed entry -- a duplicate name, a source
URL pointing at a repository that no longer exists, a truncated JSON write --
breaks plugin resolution for everyone, and nothing on the way to `main` was
checking it (mk-0y69).

TWO PHASES, DELIBERATELY SEPARATE

  structural   offline. Parses the manifest and enforces the shape every
               consumer assumes. Cheap, deterministic, no network. This is the
               part that must never be skipped.

  sources      networked. Confirms each plugin's source actually resolves and
               carries a plugin manifest. Costs one API call per plugin, so it
               is opt-in via --check-sources and degrades to a warning when the
               network or the token is unavailable -- an unreachable API is an
               unknown, not a failure of the manifest.

WHY 404 IS A WARNING AND NOT AN ERROR

GitHub returns 404 both for "this repository does not exist" and for "your
token cannot see this repository", deliberately, so that private repositories
do not leak their existence. The two cannot be told apart from the response.

11 of this marketplace's sources are private and 2 belong to another owner, so
a workflow's default GITHUB_TOKEN -- scoped to this repository alone -- 404s on
a good sixth of the catalog. Treating that as an error would paint the gate red
forever and teach everyone to ignore it, which is the exact failure mk-0y69 is
about. So 404 is "unknown, not verified" unless --require-visible says the
running token is expected to see everything.


VERSION DRIFT IS A WARNING, NOT AN ERROR

A marketplace entry whose version trails the upstream plugin.json is normal for
the window between a plugin's release commit and the marketplace bump; that is
what `interpub:sweep` reconciles. Failing the build on drift would paint CI red
for a routine, self-healing state. Pass --strict-versions to promote it.

Exit 0 clean (warnings allowed), 1 on any error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_MANIFEST = ".claude-plugin/marketplace.json"

# Deliberately permissive: the loader accepts more than we do here only in ways
# that are ambiguous for humans. Names appear in `plugin@marketplace` ids and on
# the command line, so keep them boring.
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
GITHUB_URL_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$")

KNOWN_SOURCE_KINDS = {"url", "github", "git", "local"}


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def report(self) -> int:
        for w in self.warnings:
            print(f"warning: {w}")
        for e in self.errors:
            print(f"error: {e}")
        print()
        print(f"{len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        return 1 if self.errors else 0


def load_manifest(path: str, f: Findings) -> dict[str, Any] | None:
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        f.error(f"{path}: cannot read: {exc}")
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        # Line/column matter here: a truncated atomic write is the likeliest
        # way this file goes bad, and the caller wants to see where.
        f.error(f"{path}: invalid JSON at line {exc.lineno} column {exc.colno}: {exc.msg}")
        return None
    if not isinstance(data, dict):
        f.error(f"{path}: top level must be an object, got {type(data).__name__}")
        return None
    return data


def check_structure(data: dict[str, Any], f: Findings) -> list[dict[str, Any]]:
    for key in ("name", "owner", "plugins"):
        if key not in data:
            f.error(f"missing required top-level key: {key}")

    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        f.error("'plugins' must be an array")
        return []
    if not plugins:
        f.error("'plugins' is empty -- a marketplace with no plugins is almost certainly a bad write")
        return []

    seen: dict[str, int] = {}
    valid: list[dict[str, Any]] = []

    for i, entry in enumerate(plugins):
        where = f"plugins[{i}]"
        if not isinstance(entry, dict):
            f.error(f"{where}: must be an object, got {type(entry).__name__}")
            continue

        name = entry.get("name")
        if not isinstance(name, str) or not name:
            f.error(f"{where}: missing or non-string 'name'")
            continue
        where = f"plugins[{i}] ({name})"

        if not NAME_RE.match(name):
            f.error(f"{where}: name must be lowercase alphanumeric with hyphens")
        if name in seen:
            f.error(f"{where}: duplicate name, first seen at plugins[{seen[name]}]")
        else:
            seen[name] = i

        version = entry.get("version")
        if not isinstance(version, str) or not version:
            f.error(f"{where}: missing or non-string 'version'")
        elif not SEMVER_RE.match(version):
            f.error(f"{where}: version {version!r} is not semver")

        source = entry.get("source")
        if not isinstance(source, dict):
            f.error(f"{where}: missing or non-object 'source'")
        else:
            kind = source.get("source")
            if not isinstance(kind, str):
                f.error(f"{where}: source.source missing")
            elif kind not in KNOWN_SOURCE_KINDS:
                f.warn(f"{where}: unrecognised source kind {kind!r}")
            if kind == "url":
                url = source.get("url")
                if not isinstance(url, str) or not url:
                    f.error(f"{where}: source.source is 'url' but source.url is missing")
                elif not url.startswith("https://"):
                    f.error(f"{where}: source.url must be https, got {url!r}")

        if "strict" in entry and not isinstance(entry["strict"], bool):
            f.error(f"{where}: 'strict' must be a boolean")

        desc = entry.get("description")
        if desc is not None and not isinstance(desc, str):
            f.error(f"{where}: 'description' must be a string")

        valid.append(entry)

    return valid


def _api_get(url: str, token: str | None) -> tuple[int, bytes]:
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "validate-marketplace")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, b""


def check_sources(
    entries: list[dict[str, Any]], f: Findings, strict_versions: bool, require_visible: bool
) -> None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        f.warn("no GITHUB_TOKEN/GH_TOKEN in the environment; source checks run unauthenticated and may be rate-limited")

    # 404 means "absent or invisible" and the API will not say which. Only a
    # caller who knows its token sees the whole catalog may read it as absent.
    missing = f.error if require_visible else f.warn
    invisible = "does not exist" if require_visible else "is not visible to this token (private, or gone) -- unknown, not verified"

    for entry in entries:
        name = entry["name"]
        source = entry.get("source")
        if not isinstance(source, dict) or source.get("source") != "url":
            continue
        url = source.get("url")
        if not isinstance(url, str):
            continue

        m = GITHUB_URL_RE.match(url)
        if not m:
            f.warn(f"{name}: source.url is not a github.com repository; not checked")
            continue
        owner, repo = m.group(1), m.group(2)

        status, _ = _api_get(f"https://api.github.com/repos/{owner}/{repo}", token)
        if status == 404:
            missing(f"{name}: source repository {owner}/{repo} {invisible}")
            continue
        if status == 403:
            f.warn(f"{name}: rate-limited checking {owner}/{repo}; unknown, not verified")
            continue
        if status != 200:
            f.warn(f"{name}: unexpected HTTP {status} checking {owner}/{repo}; unknown, not verified")
            continue

        status, body = _api_get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/.claude-plugin/plugin.json", token
        )
        if status == 404:
            missing(f"{name}: {owner}/{repo} .claude-plugin/plugin.json {invisible}")
            continue
        if status != 200:
            f.warn(f"{name}: could not read plugin.json from {owner}/{repo} (HTTP {status}); unknown, not verified")
            continue

        try:
            import base64

            payload = json.loads(body)
            upstream = json.loads(base64.b64decode(payload["content"]))
        except Exception as exc:  # noqa: BLE001 - any parse failure is the same finding
            f.error(f"{name}: {owner}/{repo} plugin.json is unreadable: {exc}")
            continue

        upstream_name = upstream.get("name")
        if upstream_name != name:
            f.error(f"{name}: upstream plugin.json declares name {upstream_name!r}")

        upstream_version = upstream.get("version")
        entry_version = entry.get("version")
        if upstream_version != entry_version:
            msg = (
                f"{name}: marketplace says {entry_version}, upstream plugin.json says {upstream_version}"
            )
            if strict_versions:
                f.error(msg)
            else:
                f.warn(msg + " (drift; interpub:sweep reconciles this)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", nargs="?", default=DEFAULT_MANIFEST)
    ap.add_argument("--check-sources", action="store_true", help="resolve every plugin source over the network")
    ap.add_argument("--strict-versions", action="store_true", help="treat marketplace/upstream version drift as an error")
    ap.add_argument(
        "--require-visible",
        action="store_true",
        help="the running token is expected to see every source; read 404 as absent rather than invisible",
    )
    args = ap.parse_args()

    f = Findings()
    data = load_manifest(args.manifest, f)
    if data is None:
        return f.report()

    entries = check_structure(data, f)
    print(f"structural: checked {len(entries)} plugin entr{'y' if len(entries) == 1 else 'ies'} in {args.manifest}")

    if args.check_sources and entries:
        print("sources: resolving each plugin source ...")
        check_sources(entries, f, args.strict_versions, args.require_visible)

    return f.report()


if __name__ == "__main__":
    sys.exit(main())
