The draft-review pipeline: render a draft as a self-contained dark HTML review page through one command that runs the prose, identifier, quote-integrity, and render-fidelity gates.

# protean-drafts

The draft-review ingredient of the Protean Kit distribution. It renders a draft
as one self-contained dark HTML page, and it runs the gate sequence that decides
whether the draft may be posted at all.

## Do you need this?

ROLE: The draft-review ingredient. One command renders a draft as a self-contained dark HTML review page and runs the gate sequence that decides whether the draft may be posted.

USE WHEN:
- A pull request or issue draft must be shown to a human as a single page, using `templates/protean-drafts/pr-draft.md` or `issue-draft.md` through `scripts/protean-drafts/draft_pipeline.py`.
- The draft must clear the prose gate, the identifier and quote-integrity checks, and the renderer-defaults gate before posting.
- Only the renderer is needed. `scripts/protean-drafts/render_draft_html.py` runs standalone, with `markdown` and `pygments` required for rendering while every gate stays stdlib only.

SKIP WHEN:
- The need is to approve, merge, or audit on GitHub. That is `protean-github-flow`.
- The need is record or protocol validation. Record gates live in `protean-ops` and protocol validation lives in `protean-sym2p`.

## What it installs and where

| Path | Contents |
|---|---|
| `skills/draft-review-html/` | the procedure skill |
| `scripts/protean-drafts/` | `render_draft_html.py`, `draft_pipeline.py`, `check-prose.py` |
| `templates/protean-drafts/` | `pr-draft.md`, `issue-draft.md` |
| `gates/protean-drafts/` | the two gates and the leak blocklist |

## Install

```bash
bash install.sh --target <dir>
bash install.sh --target <dir> --dry-run
```

Bash and coreutils only, zero network calls, every written path printed, and no
`--target` means no run. A dry run writes nothing.

Installs alone with this command, resolving only its required dependencies listed
in its manifest entry. Optional relationships are reported, not fetched.

## Requirements and recommendations

Requires none. Recommends `protean-doctrine`: the renderer and the pipeline
enforce the writing discipline the doctrine states, and the prose gate names it
as its source.

## Use

```bash
python3 scripts/protean-drafts/draft_pipeline.py \
  --src <draft.md> --slug <slug> --tab "pull request draft" \
  --title "<draft title>" --owners <poster-handle> \
  --verify-against "<ref:path>" --open
```

`--drafts-root` defaults to `$PROTEAN_DRAFTS_ROOT`, else `./drafts`. The renderer
alone is available as

```bash
python3 scripts/protean-drafts/render_draft_html.py --in <draft.md> --out <out.html> \
  --repo "<owner>/<repo>" --tab "issue draft" --title "<title>"
```

Rendering needs the `markdown` and `pygments` libraries. Every gate is stdlib
only.

## Gates

| Gate | Command (declared) |
|---|---|
| internal-name gate | `python3 gates/protean-drafts/check-internal-names.py .` |
| prose | `python3 scripts/protean-drafts/check-prose.py skills/draft-review-html/SKILL.md` |
| renderer defaults | `python3 gates/protean-drafts/check-renderer-defaults.py .` |

## Single home for the prose gate

`check-prose.py` lives in this ingredient only. It is not installed by
`protean-ops`, which carries the record gates and nothing else. A procedure that
needs the prose gate declares the dependency rather than copying the file.

## Offline and cache behaviour

Used through the composer, this ingredient is fetched once from its pinned tag
and reused from a content-addressed cache keyed by commit SHA. `--offline`
performs zero network calls and fails closed when the cache entry is absent.

## Limits and open items

The renderer's owner chain is a neutral placeholder. An external post must pass
`--owners <poster-handle>`, because the placeholder chain is not an attribution.
The pipeline's identifier sweep ships no private pattern: supply deployment
patterns with `--denylist <file>`.

## License

MIT. The committed `LICENSE` file is authoritative.
