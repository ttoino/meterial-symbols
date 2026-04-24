# AGENTS.md

This repo contains a Python font generator (root) and a SvelteKit website (`website/`). They are isolated: CI ignores `website/**` for the Python project, and vice versa.

## Python project

- **Runtime:** Python >= 3.13
- **Entrypoint:** `__main__.py` reads `symbols.json` and SVGs from `symbols/`, writes `dist/MeterialSymbols.{ttf,woff2}`
- **Dev env:** Nix flake available (`nix develop` or direnv); installs Python deps, Node, ruff, pyright, pytest
- **Task runner:** `tox` (configured in `pyproject.toml`)
  - `python -m tox -e format` — ruff format check
  - `python -m tox -e lint` — ruff lint
  - `python -m tox -e typecheck` — pyright
  - `python -m tox -e test` — pytest
  - `python -m tox -e build` — runs `python __main__.py`
- **Direct commands also work:** `ruff check .`, `ruff format --check .`, `pyright`, `pytest`, `python3 __main__.py`
- **Tests exist** in `tests/` (13 tests). Run with `pytest` or `python -m tox -e test`.
- **Adding symbols:** add entry to `symbols.json`, create `symbols/<name>/` with `_.svg` (default) and `<float>.svg` variants. All SVG variants must have the same number of contours and points in the same order (see `README.md` for constraints).

## Website (`website/`)

- **Stack:** Svelte 5 + SvelteKit 2 + Vite + TypeScript + Tailwind CSS v4, deployed to Cloudflare Workers
- **Package manager:** pnpm (pinned to 10.5.0 in `packageManager`). Always use `pnpm`.
- **Node:** 22
- **Key scripts:**
  - `pnpm dev` — dev server
  - `pnpm build` — production build
  - `pnpm check` — svelte-kit sync + svelte-check
  - `pnpm lint` — eslint
  - `pnpm format` — prettier check
  - `pnpm run deploy` — build + wrangler deploy
- **Build quirk:** `website/static/font` is a symlink to `../../dist`. The website build will fail if `dist/` does not exist at repo root. CI creates it with `mkdir dist` before `pnpm check` and `pnpm build`.
- **Config:** `wrangler.jsonc` lives at repo root, not in `website/`

## Gotchas

- `dist/` is gitignored but is the font build output. It must exist for website builds because `website/static/font` symlinks to it.
- The release workflow (`cd.yml`) builds fonts via tox and uploads `dist/` assets to GitHub releases.
