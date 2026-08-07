# Infra changes — the Market Maker VM (2026-08-06)

> **For:** Hasan
> **From:** George / Novosapien (Claude session, 06-08)
> **Project:** `inplay-497712` · network `inplay-vpc` · zone `us-east4-a`
> **Principle:** every change is ADDITIVE — nothing existing was edited,
> disabled or deleted. Every item below lists its exact rollback command.
> The change-set follows your own patterns exactly (the loadrunner's
> firewall rules, per-VM service accounts, named static internal IPs).

## Why

The MM engine needs its own VM per the agreed design (one stateful
process beside NATS; not Cloud Run — the single-writer journal forbids
container recycling; not the gateway VM — no extra load on the
tZERO-whitelisted host). This change-set creates the VM, its journal
disk with hourly snapshots, and its NATS reachability. It does NOT
deploy or start the engine — that comes later, coordinated with you.

## The changes

| # | Change | Details |
|---|--------|---------|
| 1 | New service account `market-maker-sa` | Mirrors `loadrunner-sa` / `fix-gateway-sa`: one SA per VM, used only to scope firewall egress. Two standard IAM grants: `roles/logging.logWriter`, `roles/monitoring.metricWriter` |
| 2 | New static internal IP `inplay-market-maker-ip` = `10.0.2.3` | In `nats-subnet`, mirrors `inplay-nats-ip`. Address was unreserved and unused |
| 3 | New disk `inplay-market-maker-journal` | pd-ssd, 50 GB, us-east4-a. Holds the engine's event journal + checkpoints — fsync-latency sensitive, hence SSD. Separate from the boot disk by design |
| 4 | New snapshot schedule `mm-journal-hourly` | Hourly snapshots of the journal disk, 7-day retention. Attached to disk (3) |
| 5 | New VM `inplay-market-maker` | e2-medium · debian-12 · 20 GB pd-balanced boot · `nats-subnet` at `10.0.2.3` · **no external IP** · SA from (1) · disk (3) attached. SSH via IAP only (your rule 3000 covers it) |
| 6 | New firewall rule, priority **2085** (EGRESS) | `market-maker -> nats`: allow tcp:4222 to `10.0.2.2/32`, target `market-maker-sa` — the exact shape of your 2071 (`loadrunner -> nats`) |
| 7 | New firewall rule, priority **2086** (INGRESS) | `nats accept market-maker`: allow tcp:4222 from `10.0.2.3/32` — the exact shape of your 2074 (`nats accept loadrunner`) |
| 8 | OS-level, on the VM only | Journal disk formatted ext4, mounted `/var/lib/mm` via fstab (by disk id, `nofail`) |

Priorities 2085/2086 were unused; nothing was inserted between or above
existing rules in a way that changes their evaluation.

## Exact commands executed

```bash
# 1 — service account + the two standard grants
gcloud iam service-accounts create market-maker-sa \
  --project inplay-497712 --display-name "Market Maker engine VM"
gcloud projects add-iam-policy-binding inplay-497712 \
  --member serviceAccount:market-maker-sa@inplay-497712.iam.gserviceaccount.com \
  --role roles/logging.logWriter
gcloud projects add-iam-policy-binding inplay-497712 \
  --member serviceAccount:market-maker-sa@inplay-497712.iam.gserviceaccount.com \
  --role roles/monitoring.metricWriter

# 2 — static internal IP
gcloud compute addresses create inplay-market-maker-ip \
  --project inplay-497712 --region us-east4 \
  --subnet nats-subnet --addresses 10.0.2.3

# 3 — journal disk
gcloud compute disks create inplay-market-maker-journal \
  --project inplay-497712 --zone us-east4-a \
  --type pd-ssd --size 50GB

# 4 — snapshot schedule, attached to the disk
gcloud compute resource-policies create snapshot-schedule mm-journal-hourly \
  --project inplay-497712 --region us-east4 \
  --hourly-schedule 1 --start-time 00:00 --max-retention-days 7
gcloud compute disks add-resource-policies inplay-market-maker-journal \
  --project inplay-497712 --zone us-east4-a \
  --resource-policies mm-journal-hourly

# 5 — the VM
gcloud compute instances create inplay-market-maker \
  --project inplay-497712 --zone us-east4-a \
  --machine-type e2-medium \
  --image-family debian-12 --image-project debian-cloud \
  --boot-disk-size 20GB --boot-disk-type pd-balanced \
  --subnet nats-subnet --private-network-ip 10.0.2.3 --no-address \
  --service-account market-maker-sa@inplay-497712.iam.gserviceaccount.com \
  --scopes cloud-platform \
  --disk name=inplay-market-maker-journal,device-name=mm-journal,mode=rw

# 6 — egress rule (the 2071 pattern)
gcloud compute network-firewall-policies rules create 2085 \
  --project inplay-497712 --firewall-policy inplay-fw-policy \
  --global-firewall-policy --direction EGRESS --action allow \
  --layer4-configs tcp:4222 --dest-ip-ranges 10.0.2.2/32 \
  --target-service-accounts market-maker-sa@inplay-497712.iam.gserviceaccount.com \
  --description "market-maker -> nats"

# 7 — ingress rule (the 2074 pattern)
gcloud compute network-firewall-policies rules create 2086 \
  --project inplay-497712 --firewall-policy inplay-fw-policy \
  --global-firewall-policy --direction INGRESS --action allow \
  --layer4-configs tcp:4222 --src-ip-ranges 10.0.2.3/32 \
  --description "nats accept market-maker"

# 8 — on the VM via IAP SSH: format + mount the journal disk
#   mkfs.ext4 on /dev/disk/by-id/google-mm-journal (was blank)
#   mount at /var/lib/mm, fstab entry by UUID with nofail
```

## Verification performed

- VM boots and is reachable over IAP SSH.
- From the VM: TCP connect to `10.0.2.2:4222` succeeds (NATS reachable).
- No existing rule, route, address, disk, VM or IAM binding was
  modified. `gcloud compute instances list` / rules listing before and
  after differ only by the additions above.

## Rollback (removes everything this change-set added)

```bash
gcloud compute network-firewall-policies rules delete 2086 \
  --project inplay-497712 --firewall-policy inplay-fw-policy --global-firewall-policy
gcloud compute network-firewall-policies rules delete 2085 \
  --project inplay-497712 --firewall-policy inplay-fw-policy --global-firewall-policy
gcloud compute instances delete inplay-market-maker \
  --project inplay-497712 --zone us-east4-a
gcloud compute disks delete inplay-market-maker-journal \
  --project inplay-497712 --zone us-east4-a
gcloud compute resource-policies delete mm-journal-hourly \
  --project inplay-497712 --region us-east4
gcloud compute addresses delete inplay-market-maker-ip \
  --project inplay-497712 --region us-east4
gcloud projects remove-iam-policy-binding inplay-497712 \
  --member serviceAccount:market-maker-sa@inplay-497712.iam.gserviceaccount.com \
  --role roles/logging.logWriter
gcloud projects remove-iam-policy-binding inplay-497712 \
  --member serviceAccount:market-maker-sa@inplay-497712.iam.gserviceaccount.com \
  --role roles/monitoring.metricWriter
gcloud iam service-accounts delete \
  market-maker-sa@inplay-497712.iam.gserviceaccount.com --project inplay-497712
```

## Open with you (Hasan)

1. Please confirm the placement (nats-subnet, 10.0.2.3) and the two
   rules suit you — happy to adjust to any convention we missed.
2. The MM engine will NOT be started against production until the
   supervised-test posture is agreed (the production gateway forwards to
   the real venue path).
3. Separately owed to you: the sportradar service's MM publisher worker
   needs its worker-pool slot + NATS reachability from the Cloud Run
   subnet (rules 2019/2024 look like they already cover 10.0.8.0/22 —
   to confirm together).

---

## Addendum 2026-08-07 — the deploy channel + VM software (additive)

The engine was deployed to the VM and drilled (loopback only — nothing
touches production NATS or the gateway). Because the VM has no internet
egress (your NATs cover fix-gateway/mgmt/cloudrun subnets only — we
deliberately did NOT extend NAT to nats-subnet, since that would also
give the NATS VM egress; your call if ever wanted), artifacts ship
through a GCS bucket over Private Google Access:

| # | Change | Detail |
|---|---|---|
| 9 | New bucket `inplay-mm-deploy` | us-east4, uniform access. Deploy artifacts only (git bundles, docker images, python toolchain) |
| 10 | Bucket IAM | `market-maker-sa` → `roles/storage.objectViewer` on this bucket only |
| 11 | OS-level, on the VM only | git, docker.io (+ deps) installed; local drill containers `mm-nats`/`mm-gateway` (LOOPBACK_MODE) on a `mm-loopback` docker network; repo + Python 3.12 toolchain under the user home; drill journal at `/var/lib/mm/drill` |

Rollbacks:

```
gcloud storage rm -r gs://inplay-mm-deploy
# bucket IAM dies with the bucket; VM software: delete the VM's disks or
# apt remove docker.io git && docker rm -f mm-nats mm-gateway
```
