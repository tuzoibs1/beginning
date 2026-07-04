# AGENTS.md

## Cursor Cloud specific instructions

### Repository overview
This repository's default branch (`master`) is a beginner Git-learning scratch repo. It contains only:

- `README.md` — a short intro note.
- `Git Commands` — a plain-text git cheat sheet.

There is **no application code, no dependency manifest (no `package.json`, `requirements.txt`, `pyproject.toml`, etc.), no build system, and no runnable services** on `master`. Nothing needs to be installed, linted, tested, built, or run for the `master` branch.

### Environment / setup
- No dependency installation is required on `master`. The startup update script is intentionally a no-op.
- Preinstalled tooling on the VM includes Node.js (v22.x) and Python 3.12, available if future code is added.

### Note on other branches
Some unmerged remote branches contain actual projects and would need their own setup if checked out (do not switch branches unless explicitly asked):

- `origin/cursor/setup-vibe-code-cad-assistant-project-*` — a Python/Flask CAD-assistant web app (`app.py`, `requirements.txt`, `run.sh`, `.env.example`). Setup: create a virtualenv and `pip install -r requirements.txt`; likely needs an API key from `.env.example`.
- `origin/cursor/create-case-tool-website-*` — a static website (`index.html`, `script.js`, `styles.css`); no build system, serve statically.
