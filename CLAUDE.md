# InPlay Vault

## Market Maker work — read the working guide first

Before doing ANY work related to the market maker (anything under
`vault/components/market-maker/`, the valuation engine, market state, SDMM /
quoting engine, market supervision, or the standards in `vault/standards/`),
you MUST read `vault/components/market-maker/working-guide.md` and follow its
process: the mandatory reading order (hub → decisions → open-questions →
parameters → plan → latest session note), the ground rules (decisions.md
outranks the standards; the 22-07 platform-doc filter; every number needs a
status), and the session loop — every working session ends with a note in
`vault/components/market-maker/sessions/` plus updates to the working docs it
touched.

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

## Description frontmatter

Every markdown document in this vault carries a one-line `description:` in its
YAML frontmatter.

- When you create a markdown file, write its description in the same edit.
- When you edit a markdown file, re-read its description. If the description no
  longer matches what the page now says, rewrite it in the same edit.
- Format: one line, at most 160 characters, double-quoted, a sentence that says
  what the document IS. Never a quote from the page, a table fragment, or
  dialogue. Over 160 characters is INVALID, not merely truncated downstream.
- If you cannot summarise the page faithfully from its content, leave
  `description:` absent and say so — a confident wrong line is worse than none.
- Exempt (no description): files named `changelog.md` or `*changelog*.md`, files
  named `TEMPLATE.md` or `*template*.md`, and empty files.
