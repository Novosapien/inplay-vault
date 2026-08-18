---
description: "The MM boot healer went live on 17-08 after weeks inert — the blocker was a network firewall policy, not the unset env var everyone recorded"
---

# 2026-08-17f — the boot healer was never a config problem

> **Component:** [[market-maker/market-maker]] · **Status:** LIVE

---

## 1 · What the vault said, and what was true

Every recent note recorded the same thing: *"Boot healer INERT —
`MM_GATEWAY_OPS_URL` unset, failed open loudly as designed"*. Read as a
config task nobody had got round to.

**It was not.** Setting the variable would not have worked. The maker VM
could not reach the gateway's ops server at all:

```
maker    10.0.2.3  (nats-subnet)      →  gateway ops  10.0.1.2:8080
TCP connect: timed out
```

The blocker is `inplay-fw-policy`, a **network firewall policy**, which is
evaluated BEFORE VPC firewall rules and ends with:

```
64999  EGRESS   deny  0.0.0.0/0  all   "Default deny all egress"
65000  INGRESS  deny  0.0.0.0/0  all   "Default deny all ingress"
```

⚠ A VPC firewall rule cannot fix this. One was created first and had no
effect at all — the policy denies before VPC rules are consulted. It was
removed once the cause was understood.

## 2 · The fix — follow the policy's own convention

The policy pairs an SA-targeted EGRESS with a matching INGRESS (see 2085 /
2086 for maker→NATS, 2072 / 2075 for loadrunner→gateway). Two rules added:

| prio | dir | rule |
|---|---|---|
| 2087 | EGRESS | `market-maker-sa` → `10.0.1.2/32` tcp:8080 |
| 2088 | INGRESS | accept `10.0.2.3/32` tcp:8080 |

Then `MM_GATEWAY_OPS_URL=http://10.0.1.2:8080` in `/etc/mm-1/env` and
`MM_GATEWAY_OPS_KEY` (the gateway's `OPS_API_KEY`, sent as `X-Ops-Key`) in
`/etc/mm-1/env.secret` (0600).

Verified before restarting anything: `HTTP 200, 673 KB, 1,640 resting MM
orders`.

## 3 · ⭐ First run, and it earned its keep immediately

```
boot heal: DONE — 1646 MM orders at the venue
  cancelled 1645 unknown + 0 absent-at-venue
  kept 0 known · left 1 taker + 0 foreign
  ALARMED 0 ambiguous + 0 malformed
  62 ms wall, of which 37 ms was the ops read
```

**1,645 orders were resting at the venue that our side did not know
about** — the accumulated orphan population from every restart before
adoption existed, including the four that bled ~57 fills this afternoon.

Note `left 1 taker + 0 foreign`: the ownership rule from decisions
2026-08-15f working exactly as designed — `MMSN` is the taker's and was
correctly not touched, and nothing unrecognised was cancelled.

62 ms. This was owed for weeks.

## 4 · Two findings worth keeping

- **`allow-cloudrun-to-fixgw-ops` is a dead rule.** It targets network tag
  `fix-gateway-ops`, and the gateway VM carries **no tags at all**. It has
  never matched anything. Whoever wrote it believes Cloud Run can reach the
  ops server over that path. (The policy's own 2027/2028 pair does allow
  it, so Cloud Run is fine — but the VPC rule is a decoy.)
- **"Unset env var" was the recorded cause for weeks and was wrong.** The
  process failed open and said `MM_GATEWAY_OPS_URL is unset`, which is
  true and was read as sufficient. Nobody tested the path. When a
  component reports its own misconfiguration, check whether the
  configuration would have worked.

## 5 · State at close

Both bots healthy under systemd, `lost_fills: 0`, `open_orders: 1611`,
taker ~118 fills/30 s, engine on `CFG-0036` / `supervised39`.
