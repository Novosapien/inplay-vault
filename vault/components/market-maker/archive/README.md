# Market Maker — Archive

> **Rule: nothing in this folder is current** (the vault-wide
> `vault/archive/README.md` convention). Kept as history; never a working
> document.

| Item | What it was | Superseded by |
|---|---|---|
| `call-questions-29-07.md` | The prep sheet for the 29-07 Edwin round | The call happened; answers absorbed into [[market-maker/open-questions]] and [[market-maker/decisions]] (sessions 2026-07-29) |
| `call-questions-30-07.md` | The prep sheet for the 30-07 ASMM-1/SNT-1 call | Same — see session 2026-07-30 and the [[market-maker/asmm1-adoption-spec]] |
| `mm-pipeline.html` | The 22-07-era interactive walk-through of deferred items | The v1.3 spec re-cut the deferred landscape; [[market-maker/open-questions]] is the live list, [[market-maker/build/index\|build/]] the as-built truth |
| `valuation-engine.md` | The pre-spec design narrative for the valuation engine (ESV era) | Built. [[market-maker/build/valuation\|build/valuation]] + the v1.3 spec Ch 3 + [[market-maker/decisions]] |
| `market-state.md` | The pre-spec design narrative for market state (classifier era) | Built (classifier superseded by σ²). [[market-maker/build/market-state\|build/market-state]] + spec Ch 6 |
| `quoting-engine.md` | The pre-spec design narrative for the SDMM | Built (re-cut by the ASMM-1 adoption). [[market-maker/build/quoting\|build/quoting]] + spec Ch 5 + [[market-maker/asmm1-adoption-spec]] |
| `decision-cycle-reference.md` | Every cycle function as pseudocode with 🟡 placeholder constants | The v1.3 spec supplied the real bodies; the real code is `inplay-market-maker/src/mm/`; constants live in `mm/config/dictionary.py` with statuses |
