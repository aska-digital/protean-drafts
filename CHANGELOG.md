# Changelog

All notable changes to this repository are recorded here. The format is a short
entry per release: what changed, why, and how it was verified.

## 1.0.0

- **What:** the first release of the `protean-drafts` ingredient: the capability payload,
  the machine descriptor `protean-ingredient.json`, the standalone installer
  `install.sh`, the declared gates under `gates/protean-drafts/`, and the test suite under
  `tests/`.
- **Why:** the capability was previously reachable only from inside a private
  working tree. This repository is its single public home, installable on its own.
- **Verification:** the declared gates and `python3 -m unittest discover -s tests`
  pass from a clean checkout of this commit. See the pull request body for the
  commands and their output.
- **Contract:** `The draft-review pipeline: render a draft as a self-contained dark HTML review page through one command that runs the prose, identifier, quote-integrity, and render-fidelity gates.`
- **License:** MIT. The committed `LICENSE` file is authoritative.
