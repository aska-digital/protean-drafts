#!/usr/bin/env python3
"""check-renderer-defaults.py - the renderer's compiled-in header values are public-safe.

Reads the renderer's default header constants (owner chain, state line) and runs
the same two detectors the leak gate uses: token digests against the blocklist,
and private-path shapes. A compiled-in default that names a private identity or
an absolute path fails here, so the fix has to touch the code, not the docs.

Usage: python3 gates/check-renderer-defaults.py [path/to/repo]
Exit: 0 clean; 1 a default carries a private identity or path.
"""
import hashlib
import os
import re
import sys

TOKEN_RE = re.compile(r"[A-Za-z0-9]+")
CONST_RE = re.compile(r"^DEFAULT_[A-Z_]*OWNERS[A-Z_]*\s*=\s*(.+)$|"
                      r"^DEFAULT_STATE\s*=\s*(.+)$", re.M)
PATH_RES = [
    re.compile(r"/" + r"(?:Users|home|Volumes)" + r"/"),
    re.compile(r"~/\\.(?:hermes|config|local|cache)"),
    re.compile(r"(?:^|[^A-Za-z0-9_-])" + r"team[-_]skills" + r"(?:[^A-Za-z0-9_-]|$)"),
]
RENDERER = os.path.join("scripts", "protean-drafts", "render_draft_html.py")


def main():
    repo = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    if "--help" in sys.argv:
        print(__doc__.strip())
        return 0
    renderer = os.path.join(repo, RENDERER)
    if not os.path.isfile(renderer):
        print("gate error: renderer not found: " + RENDERER)
        return 2
    with open(os.path.join(repo, "gates", "internal-names.blocklist"),
              encoding="utf-8") as fh:
        digests = {line.strip() for line in fh
                   if line.strip() and not line.startswith("#")}
    with open(renderer, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    values = [m.group(1) or m.group(2) for m in CONST_RE.finditer(text)]
    if not values:
        print("gate error: no default header constant found in " + RENDERER)
        return 2
    findings = []
    for value in values:
        for token in TOKEN_RE.findall(value):
            digest = hashlib.sha256(token.lower().encode("utf-8")).hexdigest()
            if digest in digests:
                findings.append("blocked token in a compiled-in default")
        for rx in PATH_RES:
            if rx.search(value):
                findings.append("private path shape in a compiled-in default")
    if findings:
        print("DEFAULT NOT PUBLIC-SAFE: " + str(len(findings)) + " finding(s)")
        for f in findings:
            print("  " + f)
        return 1
    print("clean: " + str(len(values)) + " default header value(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
