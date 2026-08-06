# InPlay VPC Setup Guide

> ⚠️ **STALE — THE ADDRESSES IN THIS DOCUMENT ARE WRONG (verified
> 2026-08-03, N30 in [[market-maker/open-questions]]).** The deployed
> configuration disagrees with this draft on every address: gateway is
> **10.0.1.2** (not 10.0.0.2) · NATS is **10.0.2.2** (not 10.0.0.3) ·
> Redis **10.78.64.3** · Cloud SQL **10.78.65.3** — not one /24. The
> live source of truth is `inplay-admin-panel-trading/proxy/.env.example`;
> the full real layout is Hasan's to confirm (N30). Also superseded:
> this draft's "Cloud NAT not yet created" — **Cloud NAT exists**
> (George, 04-08). Do not build or configure anything from this
> document. ⚠ Line-number citations into this file recorded before
> 06-08 (e.g. "VPC Setup.md:660") predate this banner and are shifted.

Infrastructure setup for the FIX gateway VM, NATS JetStream, Centrifugo, and VPC networking on GCP.

---

## Architecture Overview

```
┌────────────────────────── VPC (10.0.0.0/24) ──────────────────────────┐
│                       us-east4 (Northern Virginia)                     │
│                                                                        │
│  10.0.0.2              10.0.0.3              10.0.0.4                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐         │
│  │ FIX Gateway  │─────►│ NATS JS      │◄─────│ Centrifugo   │         │
│  │ e2-medium    │      │ e2-small     │      │ e2-small     │         │
│  │              │      │              │      │              │         │
│  │ OE (60921)   │      │ Port 4222    │      │ Port 8000    │         │
│  │ MD (30921)   │      │ Internal only│      │ WebSocket    │         │
│  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘         │
│         │                     │                      │                 │
│   static public IP      no public IP           public IP              │
│   (outbound only)       ▲                      (inbound only)         │
│         ▼               │                            ▲                 │
│   tZERO (216.66.10.155) │                            │                 │
│                    Cloud Run services            Mobile app            │
│                    (via VPC connector)            (WebSocket)          │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

External (outside VPC):
  - Supabase (managed database)
  - Sportradar API → Cloud Run → VPC connector → NATS
  - Mobile app → Centrifugo (WebSocket)
  - Mobile app → Cloud Run (REST API)
```

### Data flow

```
Sportradar API → Sportradar service (Cloud Run) → NATS JetStream → Centrifugo → Users
tZERO          → FIX Gateway                    → NATS JetStream → Centrifugo → Users
Mobile app     → App API (Cloud Run)            → NATS JetStream → FIX Gateway → tZERO
```

### Why two separate VMs

The FIX gateway is a single point of failure (tZERO whitelists one static IP). Keeping NATS JetStream on a separate VM means:

- If the gateway restarts, NATS still has persisted data and Cloud Run services keep running
- If NATS needs maintenance, the FIX sessions stay connected
- Independent failure domains for ~$13/month extra

Both VMs are in the same subnet so inter-VM latency is <1ms.

### What lives where

| Component | Location | Public IP? | Why |
|-----------|----------|------------|-----|
| FIX Gateway | VM in VPC (10.0.0.2) | Yes (static, outbound) | tZERO whitelists this IP. Persistent TCP sessions need a stable host |
| NATS JetStream | VM in VPC (10.0.0.3) | No | Message broker between all services. No public exposure needed |
| Centrifugo | VM in VPC (10.0.0.4) | Yes (inbound) | WebSocket server for real-time fan-out to mobile users. Subscribes to NATS internally |
| Cloud Run (app API, sportradar) | Connects via VPC connector | N/A (managed) | Serverless, scales to zero, talks to NATS on internal IPs |
| Supabase | External (managed) | N/A | Cloud Run connects directly over internet |
| Sportradar | External API | N/A | Sportradar service (Cloud Run) polls/receives pushes |

---

## Prerequisites

- GCP project with billing enabled
- `gcloud` CLI installed and authenticated
- Permissions: Compute Admin, Serverless VPC Access Admin, IAP-Secured Tunnel User

---

## Setup Steps

### 1. Create the VPC network and subnet

```bash
# Create custom VPC (no auto-created subnets)
gcloud compute networks create inplay-vpc \
  --subnet-mode=custom

# Create subnet in us-east4 (closest to tZERO at 216.66.10.155)
# Private Google Access lets VMs without public IPs reach GCP APIs
# Flow Logs record connection metadata for debugging and auditing
gcloud compute networks subnets create inplay-subnet \
  --network=inplay-vpc \
  --region=us-east4 \
  --range=10.0.0.0/24 \
  --enable-private-ip-google-access \
  --enable-flow-logs \
  --logging-flow-sampling=0.5 \
  --logging-metadata=include-all
```

### 2. Reserve static external IP

```bash
gcloud compute addresses create inplay-fix-gateway \
  --region=us-east4 \
  --network-tier=PREMIUM

# Get the IP to send to tZERO
gcloud compute addresses describe inplay-fix-gateway \
  --region=us-east4 \
  --format='get(address)'
```

Send this IP to tZERO so they can whitelist it.

### 3. Create firewall rules

```bash
# Allow outbound to tZERO (Order Entry + Market Data ports)
gcloud compute firewall-rules create fix-egress-tzero \
  --network=inplay-vpc \
  --direction=EGRESS \
  --action=ALLOW \
  --rules=tcp:60921,tcp:30921 \
  --destination-ranges=216.66.10.155/32 \
  --target-tags=fix-gateway

# Allow internal traffic (NATS on 4222, Redis on 6379 if needed)
gcloud compute firewall-rules create allow-internal \
  --network=inplay-vpc \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:4222,tcp:6379,icmp \
  --source-ranges=10.0.0.0/24

# Allow SSH via IAP tunneling only (no public SSH exposure)
# 35.235.240.0/20 is Google's IAP IP range — the only source allowed to SSH in
gcloud compute firewall-rules create allow-iap-ssh \
  --network=inplay-vpc \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:22 \
  --source-ranges=35.235.240.0/20 \
  --target-tags=fix-gateway,nats-server,centrifugo

# Allow users to connect to Centrifugo via WebSocket (port 8000)
gcloud compute firewall-rules create allow-centrifugo-ws \
  --network=inplay-vpc \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:8000 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=centrifugo

# Allow Centrifugo to reach NATS internally
gcloud compute firewall-rules create allow-centrifugo-nats \
  --network=inplay-vpc \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:4222 \
  --source-tags=centrifugo \
  --target-tags=nats-server

# Allow VPC connector to reach NATS
gcloud compute firewall-rules create allow-vpc-connector \
  --network=inplay-vpc \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:4222 \
  --source-ranges=10.0.1.0/28 \
  --target-tags=nats-server
```

### 4. Create the FIX Gateway VM

```bash
gcloud compute instances create inplay-fix-gateway \
  --zone=us-east4-a \
  --machine-type=e2-medium \
  --network=inplay-vpc \
  --subnet=inplay-subnet \
  --private-network-ip=10.0.0.2 \
  --address=inplay-fix-gateway \
  --tags=fix-gateway \
  --image-family=ubuntu-2404-lts-amd64 \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-ssd \
  --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y python3 python3-pip python3-venv git

    # Install Cloud Ops Agent (sends logs + metrics to Cloud Logging/Monitoring)
    curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
    bash add-google-cloud-ops-agent-repo.sh --also-install
  '
```

### 5. Create the NATS JetStream VM

```bash
gcloud compute instances create inplay-nats \
  --zone=us-east4-a \
  --machine-type=e2-small \
  --network=inplay-vpc \
  --subnet=inplay-subnet \
  --private-network-ip=10.0.0.3 \
  --no-address \
  --tags=nats-server \
  --image-family=ubuntu-2404-lts-amd64 \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-ssd \
  --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y wget

    # Install NATS server
    wget https://github.com/nats-io/nats-server/releases/download/v2.10.24/nats-server-v2.10.24-linux-amd64.tar.gz
    tar -xzf nats-server-v2.10.24-linux-amd64.tar.gz
    cp nats-server-v2.10.24-linux-amd64/nats-server /usr/local/bin/

    # Create config
    mkdir -p /etc/nats
    cat > /etc/nats/nats.conf << EOF
    listen: 0.0.0.0:4222
    jetstream {
      store_dir: /var/lib/nats/jetstream
      max_mem: 512MB
      max_file: 5GB
    }
    EOF

    mkdir -p /var/lib/nats/jetstream

    # Create systemd service
    cat > /etc/systemd/system/nats.service << EOF
    [Unit]
    Description=NATS Server
    After=network.target

    [Service]
    ExecStart=/usr/local/bin/nats-server -c /etc/nats/nats.conf
    Restart=always
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    EOF

    systemctl enable nats
    systemctl start nats

    # Install Cloud Ops Agent
    curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
    bash add-google-cloud-ops-agent-repo.sh --also-install
  '
```

Note: the NATS VM has `--no-address` (no public IP). It is only reachable from within the VPC. Use IAP tunneling to SSH in (see SSH Access section below).

### 6. Create the Centrifugo VM

Centrifugo handles real-time WebSocket fan-out to mobile app users. It subscribes to NATS internally and pushes updates to connected clients.

```bash
gcloud compute instances create inplay-centrifugo \
  --zone=us-east4-a \
  --machine-type=e2-small \
  --network=inplay-vpc \
  --subnet=inplay-subnet \
  --private-network-ip=10.0.0.4 \
  --tags=centrifugo \
  --image-family=ubuntu-2404-lts-amd64 \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-ssd \
  --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y wget

    # Install Centrifugo
    wget https://github.com/centrifugal/centrifugo/releases/download/v5.4.8/centrifugo_5.4.8_linux_amd64.tar.gz
    tar -xzf centrifugo_5.4.8_linux_amd64.tar.gz
    cp centrifugo /usr/local/bin/

    # Create config
    mkdir -p /etc/centrifugo
    cat > /etc/centrifugo/config.json << EOF
    {
      "address": "0.0.0.0",
      "port": 8000,
      "api_key": "CHANGE_ME_TO_A_REAL_SECRET",
      "token_hmac_secret_key": "CHANGE_ME_TO_A_REAL_SECRET",
      "allowed_origins": ["*"],
      "broker": "nats",
      "nats_url": "nats://10.0.0.3:4222"
    }
    EOF

    # Create systemd service
    cat > /etc/systemd/system/centrifugo.service << EOF
    [Unit]
    Description=Centrifugo
    After=network.target

    [Service]
    ExecStart=/usr/local/bin/centrifugo -c /etc/centrifugo/config.json
    Restart=always
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    EOF

    systemctl enable centrifugo
    systemctl start centrifugo

    # Install Cloud Ops Agent
    curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
    bash add-google-cloud-ops-agent-repo.sh --also-install
  '
```

Note: Replace `CHANGE_ME_TO_A_REAL_SECRET` with real secrets before deploying. Use GCP Secret Manager for production. The `"broker": "nats"` config means Centrifugo subscribes directly to NATS — no consumer service needed in between.

### 7. Reserve a static IP for Centrifugo

```bash
gcloud compute addresses create inplay-centrifugo \
  --region=us-east4 \
  --network-tier=PREMIUM

# Attach to the VM
gcloud compute instances delete-access-config inplay-centrifugo \
  --zone=us-east4-a \
  --access-config-name="external-nat" 2>/dev/null; \
gcloud compute instances add-access-config inplay-centrifugo \
  --zone=us-east4-a \
  --address=inplay-centrifugo
```

Point your app's WebSocket URL to this IP (or put it behind a load balancer / domain).

### 8. Create VPC connector for Cloud Run

```bash
gcloud compute networks vpc-access connectors create inplay-connector \
  --region=us-east4 \
  --network=inplay-vpc \
  --range=10.0.1.0/28 \
  --min-instances=2 \
  --max-instances=3
```

### 9. Deploy Cloud Run services with VPC access

When deploying any Cloud Run service that needs to talk to the gateway or NATS:

```bash
gcloud run deploy <service-name> \
  --region=us-east4 \
  --vpc-connector=inplay-connector \
  --vpc-egress=private-ranges-only \
  --image=<image-url>
```

The `private-ranges-only` flag means Cloud Run only routes RFC 1918 traffic (10.x.x.x) through the VPC. External traffic (Supabase, Sportradar) goes directly over the internet without the connector overhead.

---

## SSH Access (IAP Tunneling)

Port 22 is not exposed to the public internet. All SSH access goes through Google's Identity-Aware Proxy (IAP), which authenticates you via your GCP IAM identity before the connection reaches the VM.

```bash
# SSH into the FIX gateway
gcloud compute ssh inplay-fix-gateway --tunnel-through-iap --zone=us-east4-a

# SSH into the NATS VM (works even though it has no public IP)
gcloud compute ssh inplay-nats --tunnel-through-iap --zone=us-east4-a

# SCP a file to the gateway
gcloud compute scp ./deploy.sh inplay-fix-gateway:~/deploy.sh --tunnel-through-iap --zone=us-east4-a

# Port forward (e.g., to access NATS monitoring locally)
gcloud compute ssh inplay-nats --tunnel-through-iap --zone=us-east4-a -- -L 8222:localhost:8222
```

Every IAP connection is logged in Cloud Audit Logs — who connected, when, from where.

---

## Observability

### VPC Flow Logs

Enabled on the subnet. Records metadata about every network connection (source, destination, port, bytes, RTT). Useful for:

- Debugging FIX connectivity (are packets reaching tZERO?)
- Verifying firewall rules are working as expected
- Monitoring for unexpected outbound connections

Query flow logs in Cloud Logging:

```
# All traffic to tZERO
resource.type="gce_subnetwork"
jsonPayload.connection.dest_ip="216.66.10.155"

# All denied connections (firewall blocks)
resource.type="gce_subnetwork"
jsonPayload.reporter="DEST"
jsonPayload.disposition="DENIED"
```

### Cloud Ops Agent

Installed on both VMs. Sends system logs and metrics (CPU, memory, disk) to Cloud Logging and Cloud Monitoring. If the FIX gateway crashes overnight, the logs are in Cloud Logging — not just on the VM's disk.

View logs:

```bash
# FIX gateway logs
gcloud logging read 'resource.type="gce_instance" AND resource.labels.instance_id="inplay-fix-gateway"' --limit=50

# Or use the Cloud Console: Logging > Logs Explorer
```

---

## Connection Details

### tZERO QA Environment

| Session | Target IP | Port | SenderCompID | TargetCompID |
|---------|-----------|------|--------------|--------------|
| Order Routing (FIX 4.2) | 216.66.10.155 | 60921 | FHINPLAY01 | TZFIXORDQA |
| Market Data (FIX 4.2) | 216.66.10.155 | 30921 | INPLAYQTSQA | TZFIXQTSQA |

Session schedule: Daily 00:01:00-23:59:00 ET, Sunday through Saturday.

### Internal Service Addresses

| Service | Internal IP | Public IP | Port |
|---------|-------------|-----------|------|
| FIX Gateway | 10.0.0.2 | Static (reserved) | — |
| NATS JetStream | 10.0.0.3 | None | 4222 |
| Centrifugo | 10.0.0.4 | Static (reserved) | 8000 (WebSocket) |

Cloud Run services connect to NATS at `nats://10.0.0.3:4222`.
Mobile app connects to Centrifugo at `ws://<centrifugo-public-ip>:8000/connection/websocket`.

---

## Environment Variables

Set these on the FIX Gateway VM (via `.env` or systemd environment):

```bash
# NATS
NATS_URL=nats://10.0.0.3:4222

# tZERO Order Entry
TZERO_FIX_HOST=216.66.10.155
TZERO_OE_PORT=60921
TZERO_OE_SENDER_COMP_ID=FHINPLAY01
TZERO_OE_TARGET_COMP_ID=TZFIXORDQA

# tZERO Market Data
TZERO_MD_PORT=30921
TZERO_MD_SENDER_COMP_ID=INPLAYQTSQA
TZERO_MD_TARGET_COMP_ID=TZFIXQTSQA

# FIX
FIX_HEARTBEAT_INTERVAL=30
FIX_BEGIN_STRING=FIX.4.2
```

---

## Cost Estimate (Monthly)

| Resource | Spec | Cost |
|----------|------|------|
| FIX Gateway VM | e2-medium (2 vCPU, 4GB RAM) | ~$25 |
| NATS JetStream VM | e2-small (2 vCPU, 2GB RAM) | ~$13 |
| Centrifugo VM | e2-small (2 vCPU, 2GB RAM) | ~$13 |
| Static IPs | 2x attached (gateway + centrifugo) | $0 |
| VPC connector | 2 min instances | ~$15 |
| SSD boot disks | 3x 20GB | ~$10 |
| Network egress | minimal (FIX is tiny, WS is small) | ~$2 |
| VPC Flow Logs | 50% sampling | ~$1 |
| Cloud Ops Agent | log ingestion (3 VMs) | ~$2 |
| **Total** | | **~$81/month** |

---

## Verification Checklist

After setup, verify:

- [ ] Static IPs reserved: `gcloud compute addresses list`
- [ ] Gateway VM has static IP: `gcloud compute instances describe inplay-fix-gateway --zone=us-east4-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'`
- [ ] Can SSH via IAP: `gcloud compute ssh inplay-fix-gateway --tunnel-through-iap --zone=us-east4-a`
- [ ] NATS is running: from gateway VM, `nc -zv 10.0.0.3 4222`
- [ ] Centrifugo is running: from gateway VM, `nc -zv 10.0.0.4 8000`
- [ ] Centrifugo can reach NATS: SSH into Centrifugo VM, `nc -zv 10.0.0.3 4222`
- [ ] Centrifugo reachable from internet: `curl http://<centrifugo-public-ip>:8000/health`
- [ ] Flow logs active: check Cloud Logging for `resource.type="gce_subnetwork"`
- [ ] Firewall allows tZERO: from gateway VM, `nc -zv 216.66.10.155 60921` (only after tZERO whitelists your IP)
- [ ] VPC connector exists: `gcloud compute networks vpc-access connectors list --region=us-east4`
- [ ] Send FIX gateway static IP to tZERO and confirm firewall policy is created on their end

---

## Application-Level Security (FIX Gateway)

The VPC secures the network layer. These are the application-layer protections built into the FIX gateway code:

### Input Validation

All outbound FIX messages are validated before being sent to tZERO:

| Check | What it prevents |
|-------|-----------------|
| ClOrdID max 20 chars, no leading zeroes | tZERO rejection — their strict format requirement |
| Symbol whitelist (163 IPTC symbols) | Typos or invalid symbols reaching the exchange |
| Side must be 1 (Buy) or 2 (Sell) | Invalid side codes |
| Quantity must be positive | Zero or negative share orders |
| Price must be positive | Zero or negative price orders |
| GTC/GTD requires RoutingInst="DNRI" | tZERO rejects GTC/GTD without this custom tag |
| GTD requires ExpireTime | Missing expiry on good-till-date orders |

### Inbound Message Validation

All FIX messages received from tZERO are validated on arrival:

| Check | What it catches |
|-------|----------------|
| Checksum verification (tag 10) | Corrupted or tampered messages in transit |
| Required tag 35 (MsgType) present | Malformed messages without a message type |
| Sequence number tracking | Duplicates, gaps, and replay attempts |
| Content-key deduplication | Duplicate executions processed twice |

### Structured Logging

All critical paths log to Python's `logging` module (picked up by Cloud Ops Agent):

- Order submissions (symbol, side, qty, price — no wallet IDs in logs)
- Session state transitions (logon, disconnect, subscription changes)
- Sequence number anomalies (gaps, duplicates, fatal mismatches)
- FIX message parsing (message type, sequence number)

### What the gateway does NOT handle (other teams own these)

| Concern | Owner |
|---------|-------|
| NATS authentication and topic authorization | NATS/infra team |
| Rate limiting on order submission | App API layer (Cloud Run) |
| User authentication and wallet ID mapping | App API layer |
| Database encryption | Supabase (managed) |

---

## Production Considerations

These are not blockers for QA/certification with tZERO, but must be addressed before production.

### TLS for Centrifugo (WebSocket encryption)

Centrifugo is currently configured on plain HTTP/WebSocket (`ws://` on port 8000). In production, mobile clients need `wss://` — iOS and Android block or warn on non-HTTPS connections, and App Store review may reject the app.

**Option A — GCP Load Balancer (recommended):**

```bash
# Reserve a global static IP
gcloud compute addresses create inplay-centrifugo-lb --global

# Create a managed SSL certificate (auto-renews)
gcloud compute ssl-certificates create inplay-centrifugo-cert \
  --domains=realtime.inplayglobal.com \
  --global

# Create a health check
gcloud compute health-checks create http inplay-centrifugo-health \
  --port=8000 \
  --request-path=/health

# Create a backend service pointing to the Centrifugo VM
# Then create a URL map, target HTTPS proxy, and forwarding rule
# (full LB setup is ~5 commands — see GCP docs for HTTPS LB with VM backends)
```

Point DNS for `realtime.inplayglobal.com` to the load balancer IP. The mobile app connects to `wss://realtime.inplayglobal.com/connection/websocket`.

**Option B — TLS directly on Centrifugo:**

Use Let's Encrypt / certbot on the VM and add to Centrifugo config:

```json
{
  "tls": true,
  "tls_cert": "/etc/letsencrypt/live/realtime.inplayglobal.com/fullchain.pem",
  "tls_key": "/etc/letsencrypt/live/realtime.inplayglobal.com/privkey.pem"
}
```

Simpler but requires managing cert renewal yourself. Option A is preferred for production.

### NATS Authentication

The current NATS config has no authentication — any process that can reach `10.0.0.3:4222` can publish and subscribe to any subject, including publishing fake order executions or market data.

The VPC and firewall rules limit network access, but every Cloud Run service connected through the VPC connector still has unrestricted access to every NATS subject. If one service is compromised or has a bug, it can inject messages into any stream.

**Recommended: per-service credentials with subject-level permissions.**

Add to `/etc/nats/nats.conf`:

```
authorization {
  users = [
    {
      user: "fix-gateway"
      password: "$FIX_GATEWAY_NATS_PASSWORD"
      permissions: {
        publish: ["orders.>", "executions.>", "marketdata.>"]
        subscribe: ["orders.>"]
      }
    },
    {
      user: "sportradar"
      password: "$SPORTRADAR_NATS_PASSWORD"
      permissions: {
        publish: ["sportradar.>"]
        subscribe: []
      }
    },
    {
      user: "centrifugo"
      password: "$CENTRIFUGO_NATS_PASSWORD"
      permissions: {
        publish: []
        subscribe: [">"]
      }
    },
    {
      user: "app-api"
      password: "$APP_API_NATS_PASSWORD"
      permissions: {
        publish: ["orders.submit"]
        subscribe: ["executions.>"]
      }
    }
  ]
}
```

Store passwords in GCP Secret Manager and inject them at startup. At minimum, use a shared token (`authorization { token: "..." }`) — even that prevents accidental cross-service interference.

### Cloud NAT (outbound internet for private VMs)

The NATS VM is created with `--no-address` (no public IP). While `--enable-private-ip-google-access` lets it reach GCP APIs, it **cannot reach the public internet**. This means:

- `apt-get update` / `apt-get install` in the startup script will fail (can't reach Ubuntu repos)
- `wget` of the NATS binary from GitHub will fail during provisioning
- No OS security updates after initial setup

The same applies to any VM without a public IP (currently just NATS, but also Centrifugo if its public IP is removed in favor of a load balancer).

**Fix — add Cloud NAT:**

```bash
# Create a Cloud Router (required by Cloud NAT)
gcloud compute routers create inplay-router \
  --network=inplay-vpc \
  --region=us-east4

# Create NAT gateway — allows outbound internet for VMs without public IPs
gcloud compute routers nats create inplay-nat \
  --router=inplay-router \
  --region=us-east4 \
  --auto-allocate-nat-external-ips \
  --nat-all-subnet-ip-ranges
```

Cost: ~$1-3/month. Without this, the NATS VM startup script as written will not complete successfully.

---

## Next Steps

1. Reserve the static IP and send it to tZERO
2. Run the setup commands above
3. Deploy the FIX gateway code to the VM
4. Test FIX Logon handshake with tZERO QA
5. Work through the FIX certification checklist
