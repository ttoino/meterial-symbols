# AGENTS.md

This repo contains a Python font generator at the root and a SvelteKit website in `website/`. They are isolated: the root Python CI ignores `website/**`, and the website CI ignores root Python changes.

For website-specific instructions, see `website/AGENTS.md`.

## Python project

**Type**: Python package (hatchling build backend)
**Runtime**: Python >= 3.13
**Package manager**: uv
**Layout**: `src/meterial_symbols/`

### Development environment

A Nix flake is present for local dev. If using direnv, it loads automatically:

```bash
direnv allow
```

Otherwise:

```bash
nix develop
```

### Commands

- `uv sync` — install dependencies and the package in editable mode
- `uv run ruff check .` — lint
- `uv run ruff format --check .` — format check
- `uv run pyright` — typecheck
- `uv run pytest` — run tests
- `uv run python -m meterial_symbols` — generate the font

### Layout

- `src/meterial_symbols/__init__.py` — package metadata
- `src/meterial_symbols/font_generator.py` — font generation logic
- `src/meterial_symbols/data/symbols.json` — symbol metadata
- `src/meterial_symbols/data/symbols/` — SVG assets
- `tests/` — pytest test suite
- `dist/` — generated font output (gitignored)

### Adding new symbols

Add a new entry to `src/meterial_symbols/data/symbols.json` and create a directory with the same name under `src/meterial_symbols/data/symbols/`. Each symbol needs:

- `_.svg` — default glyph (at `PGRS = 0`)
- `<float>.svg` — variant glyphs for other axis values

All SVG variants for a symbol must have the same number of contours and points in the same order.

## Dependency automation

This project uses **Renovate**. Renovate opens a single monthly PR grouping npm, Nix, Python, and GitHub Actions updates. Patch and minor devDependencies are auto-merged.

## Gotchas

- `dist/` is gitignored but required for website builds because of the `website/static/font` symlink.
- The release workflow (`cd.yml`) builds fonts via `uv` and uploads `dist/` assets to GitHub releases.
- `wrangler.jsonc` lives at the repo root, not in `website/`.
