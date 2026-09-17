---
name: draft-review-html
description: "Use when a GitHub issue or pull request draft must be shown for review. Render it as a self-contained, dark single-file HTML page."
version: 1.0.0
author: the Protean publication
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Draft, Review, HTML, Markdown, SOP]
    related_skills: [protean-operating-doctrine, external-writing-discipline, github-pr-audit]
---

# Draft Review - HTML procedure

## Purpose

When a team member or the operator asks for a draft that will be posted on
GitHub (issue body, pull request body, release note, comment) and a human must
review it first, the draft must be shown as a **self-contained, dark-styled
single-file HTML page** in the browser, not as raw markdown pasted in chat.
Reviewing the exact rendered artifact prevents whitespace, light-flash, and
formatting surprises at posting time.

This is the standing standard: *"every time a draft of something is to be posted
on GitHub so I can review it, make it like this. Make it an SOP."*

## When to use

- Any GitHub-posted text is drafted and needs operator review before
  `gh issue create` or `gh pr create`.
- The user explicitly asks for a draft to review.

## Ownership (mandate)

- Draft text and body: the writing role. Architecture and specification text:
  the architecture role. The renderer and the page structure: the build role.
  Adversarial fact-checking of the draft against its evidence file: the QA role.
  The final read before posting: the orchestrator. Show the operator the HTML
  before posting.
- A placeholder that only a post-push fact can fill (a head commit SHA, a diff
  count) is filled by the orchestrator after the push, before posting, and the
  substituted source is re-gated. Render the substituted text to a
  `*-final.html` beside the approved file so the approved artifact is not
  overwritten.

## Deliverable

One `.html` file per draft, HTML only, placed in a dated batch folder under the
drafts root: `<drafts root>/YYYY-MM-DD - HHhMMm/<slug>.html`. Create one folder
per review batch at review time. No `.md` alongside the HTML: markdown sources
live only in the evidence mirror for posting-time `--body-file` use. Text must be
**byte-identical** to the source markdown: markdown prose becomes rendered text,
with no added links and no dropped lines. Present the operator the dated-folder
paths. The review copy is always the HTML, never chat-pasted markdown.

## Build (single command)

Use the reusable renderer, once per draft:

    python3 scripts/protean-drafts/render_draft_html.py \
      --in <draft.md> --out <out.html> \
      --repo "<owner>/<repo>" \
      --tab "issue draft" \
      --title "<draft title>" \
      --badge "DRAFT - NOT POSTED" \
      --from-html-baseline <previous.html> \
      --baseline-label "previous review render"

On every re-render, state and highlight the changes visibly. Pass
`--diff-base <previous.md>` when the previous markdown exists, or
`--from-html-baseline <previous.html>` when only the previous HTML exists. The
renderer must include a prominent added and removed count banner, a readable
change-detail panel, and green in-place marks on added rendered blocks. Never
claim "no change" without a baseline. For an unchanged draft, show an explicit
"No content change" banner. Preserve the approved markdown text exactly:
highlighting is a view-layer annotation, not a rewrite. Keep the previous render
until the new render has been compared and the fidelity gate passes.

If the renderer is missing, reconstruct it from the page spec below. It embeds
one fetch-once copy of the GitHub markdown stylesheet, uses the markdown and
pygments libraries, and keeps the palette in its own header. Do not invent a
different palette.

## One command per draft

    python3 scripts/protean-drafts/draft_pipeline.py \
      --src <draft.md> --slug <slug> --tab "pull request draft" \
      --title "<draft title>" --owners <poster-handle> \
      --verify-against "origin/main:<path>" --open

One pass runs every gate in order: prose, identifier sweep, verbatim fences
(`--verify-against REF:PATH` or a file path, repeatable), oversight blockquote,
render, text fidelity, palette, self-containment, chrome, change banner. It
writes `<drafts root>/<batch>/<slug>.html`, keeps the previous render as
`<slug>.prev.html` and feeds it to the renderer as the baseline so every
re-render carries a change banner, and exits non-zero if any gate fails.

Start from a template instead of a blank file: `templates/protean-drafts/pr-draft.md`
or `templates/protean-drafts/issue-draft.md`. The templates plus the pipeline are
the scaffolding: never rebuild the gate sequence by hand, and never retype a
quoted source block. Slice it: the pipeline proves byte-identity.

## Attribution (external vs internal)

The header owner chain is chrome, not posted body text, and it must name whoever
is actually posting:

- **External drafts** (repositories outside this organization): pass
  `--owners <poster handle>`, and use the poster's own commit identity. Never put
  internal team names or agent handles on an external post.
- **Internal drafts**: omit `--owners` to use the renderer's neutral placeholder
  chain, or pass the real chain explicitly.
- The identifier sweep already refuses private paths, temporary paths, hostnames,
  and email addresses in the body. Use `--allow-identifier <literal>` only for a
  value the post genuinely needs.
- The sweep's own pattern list carries no private name. Supply deployment-specific
  patterns with `--denylist <file>` (one regular expression per line).

## Page spec (dark, GitHub-styled)

Single self-contained file. Inline `<style>` only, with no CDN, webfont, or
external fetch at view time, and `<meta name="color-scheme" content="dark">` in
the head. The
root and body background `#0d1117` so it opens dark with no light flash. A 768px
centered reading column.

Tokens (exact):

    page/gutter background  #0d1117   gutter border        #30363d
    base text               #c9d1d9   headings             #f0f6fc
    muted                   #8b949e   accent links         #58a6ff
    inline/fence background #161b22   fence border         #30363d
    table header            #161b22   table borders        #30363d
    zebra alt row           #161b22 (or #0f141b)
    blockquote border       #30363d   blockquote text      #8b949e
    draft badge text        #f85149   draft badge bg       #3d1d20, border #f85149
    fence language tab      #8b949e   code content         #c9d1d9

Structure:

- Header gutter: `#010409` and `#0d1117`, the repo path, an open tab labelled
  `issue draft` or `pull request draft`, and a `DRAFT - NOT POSTED` badge with the
  owner chain and the state line.
- Body: the full draft rendered in GitHub style: headings, code fences with a
  language tab and syntax color, tables with full width and header emphasis,
  blockquote, and a trailing
  `> Automated posting by agentic team with human oversight.` blockquote exactly
  once as the last line.
- Issue references stay plain text and are never auto-linked.

## Verification gates (run before presenting)

1. `python3 scripts/protean-drafts/check-prose.py <draft.md>` exits 0, and the
   identifier sweep is clean on the markdown that will be posted.
2. Text fidelity: extract the text of source and rendered HTML. Zero lines
   missing, token diff passing, fences byte-identical, no added links, and no
   external asset fetch in the HTML.
3. Palette present: the core tokens and the color-scheme meta are all present.
4. Only after the operator approves the HTML may anyone push or create the issue
   or pull request.

## Posting flow (on approval)

- Push the branch, create the issue, then the pull request, passing the markdown
  with `--body-file`.
- Read the posted body back through the API, diff it against the approved
  markdown, and accept only a trailing-newline difference.
- A fork account without triage permission cannot apply labels upstream. Post
  unlabeled and record the suggested labels in the completion metadata, or the
  operator adds them.
- Journal the posting (issue and pull request numbers) in the propagation journal.

## Pitfalls

- **Never retype quoted source text. Extract it programmatically.** A model
  writing a "before" block from memory silently normalises characters. Build
  every quoted block by slicing the source file in Python and asserting equality
  before rendering. Retyping is the defect path, not a style preference.
- **Diff quoted blocks byte-for-byte after every render, and confirm expected
  special characters survive.** A quote that is the same length as its source
  with the first divergence at a single index is the signature of a punctuation
  substitution.
- Do not re-emit the draft markdown in chat as the review copy. Always the HTML.
- Do not let the page fetch CDN assets: a reviewer opening a local path offline
  must see the full render.
- Do not change draft text while rendering. The HTML is a view, not a rewrite.
  Text edits go back to the writing role, then re-render.
