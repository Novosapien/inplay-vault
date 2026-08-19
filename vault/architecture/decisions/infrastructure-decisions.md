---
description: "Decision record for GCP infrastructure — Cloud Run over GKE for APIs, Managed Instance Group for Centrifugo, a VM for the FIX gateway, and API Gateway"
---

# Infrastructure Decisions

> **Architecture:** [[architecture]]
> **Status:** Draft

## Compute Platform: Cloud Run (not GKE)

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| Cloud Run | **Chosen** | -- |
| GKE (Kubernetes) | Yes | Significant operational overhead for the scope of this project. Cloud Run provides equivalent capability for stateless services with less infrastructure management. Kubernetes adds complexity (cluster upgrades, node pool management, networking policies, RBAC) that is not justified for 5 API services. Revisit for year 2 if service count and operational requirements grow. |
| Compute Engine VMs (for everything) | Yes | No auto-scaling. Must pre-size VMs. More ops burden for stateless services that Cloud Run handles automatically. |
| Cloud Functions | Yes | Cold start latency too high for trading. No WebSocket support. Better suited for event-driven glue, not primary API serving. |

### Cloud Run vs GKE at a Glance

| | Cloud Run | GKE |
|---|---|---|
| You manage | A Dockerfile and some config | Cluster nodes, pod specs, networking, ingress, scaling policies, health checks |
| Scaling | Automatic, including to zero | You configure autoscaling rules (HPA, node pools) |
| Persistent connections | Discouraged -- connections killed on scale-down | First-class -- pods stay alive |
| Deployment | `gcloud run deploy` | Kubernetes manifests (YAML), Helm charts, kubectl |
| Cost model | Pay per use (expensive at constant high load) | Pay for cluster (expensive when idle) |
| Learning curve | Low | High -- Kubernetes is its own world |
| Ops burden | Minimal | Significant |

### Cloud Run vs AWS Equivalents

| InPlay Service | GCP Choice | AWS Equivalent |
|---|---|---|
| API Services | Cloud Run | ECS Fargate |
| Centrifugo | Managed Instance Group | ECS on EC2 |
| FIX Gateway | Compute Engine VM | EC2 instance |
| Redis | Memorystore | ElastiCache |
| PostgreSQL | Cloud SQL | RDS |
| Load Balancer | Cloud Load Balancer | ALB |
| CDN | Cloud CDN | CloudFront |
| Scheduled jobs | Cloud Run Jobs | Lambda |

## Centrifugo Hosting: Managed Instance Group (not Cloud Run)

WebSocket connections are long-lived (users stay connected for hours during games). Cloud Run recycles containers during scale-down, deployments, and maintenance -- each recycle drops every connection on that instance. At 1M-5M users, an instance holding 50K connections being recycled causes 50K simultaneous disconnects.

With a Managed Instance Group, VMs stay alive until explicitly removed, and scale-down can be scheduled for off-hours when users have naturally disconnected.

| | Cloud Run | Managed Instance Group |
|---|---|---|
| Ops effort | Near zero | Low -- VM image, instance template, scaling rules |
| Scaling speed | Seconds (new container) | Minutes (new VM boots) |
| Connection stability | Instances can be recycled anytime | VMs stay alive until you say otherwise |
| Cost model | Pay per use | Pay per VM |
| Right for WebSockets | Tolerable at small scale | Purpose-fit for long-lived connections |

## FIX Gateway: Compute Engine VM (not Cloud Run)

FIX 4.2 requires persistent TCP sessions with heartbeats, sequence numbers, and session state. Cloud Run recycles containers during scale-down and deployments, killing FIX sessions. A dropped session means orders in flight could be lost, full state replay required on reconnect (IOI/MD), and sequence number gaps.

Active/standby VM configuration with session state stored in Redis for failover.

## API Gateway: Google Cloud API Gateway

With 5 backend services, path-based routing is essential. Google Cloud API Gateway provides:

- Path-based routing (`/trading/*` → Trading Service, `/auth/*` → Auth Service, etc.)
- JWT validation at the edge
- Per-route rate limiting (stricter on `/trading/*`, relaxed on `/market/*`)
- ~$3-5 per million requests

See [[api-gateway]] for full configuration details.

## No Kubernetes -- Deliberate Decision

Cloud Run provides the auto-scaling, zero-downtime deployments, and managed infrastructure needed for this project without the operational overhead of Kubernetes. GKE adds cluster management, node pool sizing, networking configuration, and upgrade maintenance that is disproportionate to the project's 5-service architecture. The mid-August timeline favours proven, lower-overhead infrastructure. Kubernetes remains an option for year 2 if the service count or operational complexity grows to justify it.
