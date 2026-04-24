# AGENTS.md

This repo contains a Python font generator (root) and a SvelteKit website (`website/`). They are isolated: CI ignores `website/**` for the Python project, and vice versa.

## Python project

- **Runtime:** Python >= 3.13
- **Entrypoint:** `__main__.py` reads `symbols.json` and SVGs from `symbols/`, writes `dist/MeterialSymbols.{ttf,woff2}`
- **Dev env:** Nix flake available (`nix develop` or direnv); installs Python deps, Node, ruff, pyright
- **Task runner:** `tox` (configured in `pyproject.toml`)
  - `python -m tox -e format` — ruff format check
  - `python -m tox -e lint` — ruff lint
  - `python -m tox -e typecheck` — pyright
  - `python -m tox -e build` — runs `python __main__.py`
- **Direct commands also work:** `ruff check .`, `ruff format --check .`, `pyright`, `python3 __main__.py`
- **No tests** — verification is format + lint + typecheck + build
- **Adding symbols:** add entry to `symbols.json`, create `symbols/<name>/` with `_.svg` (default) and `<float>.svg` variants. See `__main__.py` docstring for SVG constraints (same contour/point count and order).

## Website (`website/`)

- **Stack:** SvelteKit 5 + Vite + TypeScript + Tailwind CSS v4, deployed to Cloudflare Pages
- **Package manager:** pnpm (pinned to 10.5.0 in `packageManager`). Always use `pnpm`.
- **Node:** 22
- **Key scripts:**
  - `pnpm dev` — dev server
  - `pnpm build` — production build
  - `pnpm check` — svelte-check + typecheck (requires `svelte-kit sync` first)
  - `pnpm lint` — eslint
  - `pnpm format` — prettier check
  - `pnpm run deploy` — build + wrangler pages deploy
- **Quirk:** `pnpm check` and `pnpm build` may need a `dist/` folder at repo root to succeed (CI does `mkdir dist` from root before these steps)
- **Config:** `wrangler.jsonc` lives at repo root, not in `website/`

## Gotchas

- `dist/` is gitignored but is the font build output. The website CI creates it manually because something in the build pipeline expects it.
- The release workflow (`cd.yml`) builds fonts via tox and uploads `dist/` assets to GitHub releases.
- There are no unit or integration tests in either package.
