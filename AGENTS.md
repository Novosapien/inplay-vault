# InPlay Vault

## Git Workflow

- **Never commit directly to main.** Always create a feature branch and open a pull request.
- Before starting work, create a new branch from main (e.g., `fix/linking-conventions`, `feat/trading-component`).
- Push the branch to origin and open a PR for review.
- All merges to main happen through pull requests only.

## Brand / CI (Corporate Identity) assets — `brand/`

The `brand/` folder holds InPlay's CI deliverables. Everything in it is
published automatically to the admin panel's **CI** tab (`/admin/ci`) on the
next sync — no code changes needed. See `brand/README.md` for the full convention.

- **Supported files:** `.svg` `.png` `.jpg` / `.jpeg` `.webp` `.gif` `.html`.
- **Categories = the first subfolder** (`brand/logos/`, `brand/imagery/`,
  `brand/guidelines/` …). Loose files at `brand/` root show under "General".
- **HTML** renders in a sandboxed preview (scripts blocked); keep guideline
  pages self-contained (inline CSS, relative image paths that sit beside the file).
- Optional `brand/manifest.json` overrides an asset's display `title`/`category`,
  keyed by its path relative to `brand/`.
- To add or update CI: drop files into `brand/<category>/` on a feature branch
  and open a PR (per the Git Workflow above). Merging to main triggers the
  panel sync that makes them appear.
