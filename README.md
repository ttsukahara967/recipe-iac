# recipe-iac

An Infrastructure-as-Code sample built around a small recipe site ("おうちレシピ帖").
Runs locally with docker compose; on AWS, Terraform + SST build and tear down develop / staging / production.

## Screenshots

**Recipe list**

![Recipe list](docs/screenshots/home.png)

**Category filter**

![Category filter](docs/screenshots/category-filter.png)

**Recipe detail**

![Recipe detail](docs/screenshots/recipe-detail.png)

**Mobile**

<p>
  <img src="docs/screenshots/mobile-home.png" alt="Mobile recipe list" width="280">
  &nbsp;
  <img src="docs/screenshots/mobile-detail.png" alt="Mobile recipe detail" width="280">
</p>

## Architecture

```
          ┌──────── SST (frontend/sst.config.ts) ────────┐       ┌──────────────── Terraform (infra/stack) ────────────────┐
Browser ─▶ CloudFront ─▶ Next.js (Lambda / OpenNext) ─SSR fetch─▶ ALB ─▶ ECS Fargate (FastAPI, arm64) ─▶ Aurora PostgreSQL
                                                                  └─ public subnet ───────────┘   └ private subnet ┘
                                                                               ▲ image: ECR (infra/bootstrap, shared by all envs)
```

| Layer | Local | AWS |
|---|---|---|
| Frontend | Next.js 16 (docker) | SST v4 `sst.aws.Nextjs` → CloudFront + Lambda |
| API | FastAPI + uvicorn (docker) | ECS Fargate + ALB (image in ECR) |
| DB | PostgreSQL 17 (docker) | Aurora PostgreSQL Serverless v2 |

- All API calls are made server-side by Next.js; the browser never calls the API directly
- The DB password is stored in Secrets Manager and injected into the container via ECS `secrets`
- Tables are created and seed data is loaded on API startup (`backend/app/seed.py`). There is no admin UI
- Recipe images live in `frontend/public/images/*.svg`

## Run locally

Requires: Docker

```bash
make local-up      # http://localhost:3000 / http://localhost:8000/docs
make local-down    # stop
make local-clean   # stop and delete DB data
```

## Deploy to AWS

Requires: Docker, Node.js, AWS credentials (`~/.aws/credentials` or `AWS_PROFILE`)

- If Terraform / AWS CLI are not installed, the official docker images (`hashicorp/terraform`, `amazon/aws-cli`) are used automatically
- Region is `ap-northeast-1` (override with `AWS_REGION=...`)
- The bootstrap state (`infra/bootstrap/terraform.tfstate`) stays on your machine and is git-ignored because it contains your AWS account ID. Keep it: `make nuke` needs it to delete the state bucket and ECR

```bash
export AWS_PROFILE=your-profile

make bootstrap                    # once: create the S3 state bucket and ECR
make deploy ENV=develop           # push image -> Terraform (VPC/Aurora/ECS) -> SST (Next.js)
make deploy ENV=staging
make deploy ENV=production
```

The `url` printed by SST at the end of a deploy is the site URL.

Other commands:

```bash
make plan    ENV=develop   # preview changes
make outputs ENV=develop   # show the API URL and other outputs
```

## Custom domain

Set `domain_name` in `infra/stack/envs/<env>.tfvars` to a domain whose hosted zone exists in Route 53 (registering the domain in Route 53 creates it). Leave it empty to use the default AWS hostnames.

| Environment | Site | API |
|---|---|---|
| production | `ouchirecipes.com` (+ `www` redirect) | `api.ouchirecipes.com` |
| staging | `staging.ouchirecipes.com` | `api.staging.ouchirecipes.com` |
| develop | `develop.ouchirecipes.com` | `api.develop.ouchirecipes.com` |

- Terraform creates the API certificate (ACM, ap-northeast-1), the DNS records, and an HTTPS listener on the ALB; port 80 redirects to HTTPS
- SST creates the site certificate (ACM, us-east-1) and DNS records for CloudFront
- ACM certificates are free and renew automatically; the domain itself is about $16/year and the hosted zone $0.50/month
- `make destroy` removes the per-environment records and certificates; the domain and hosted zone are kept

## How deploys work

Everything is built on the local machine from the current working tree (including uncommitted changes) and then shipped to AWS.

- **Backend**: the image tag is a hash of the backend sources. `make deploy` builds an arm64 image, pushes it to ECR, and passes it to Terraform. A new task definition revision triggers an ECS rolling update (new task passes the ALB health check → old task is drained; automatic rollback on failure). Unchanged sources produce the same tag, so nothing is redeployed.
- **Frontend**: SST builds Next.js with OpenNext. Static files (`public/images`, `_next/static`) go to S3, SSR runs on Lambda, and CloudFront routes between them. The CloudFront cache is invalidated on every deploy.
- **Seed data** is only inserted when the table is empty, so editing `seed.py` after the first deploy does not update an existing database.

## Tear down

```bash
make destroy ENV=develop   # delete one environment (asks for confirmation; YES=1 to skip)
make nuke                  # delete every environment + state bucket + ECR
```

Teardown order is SST (frontend) → Terraform (ECS/ALB/DB/VPC). Takes around 10 minutes because of Aurora.

## Per-environment settings

Edit `infra/stack/envs/<env>.tfvars`. All environments currently use the minimum spec.

| Setting | Value |
|---|---|
| Aurora capacity | 0–1 ACU (auto-pauses after 5 idle minutes) |
| ECS task | 0.25 vCPU / 0.5 GB (arm64) × 1 |
| NAT Gateway | none (tasks use public IPs for egress; inbound only from the ALB) |

## Cost

Roughly **$35–40 per month per environment** just for existing (Tokyo region estimate).

| Resource | Approx. / month |
|---|---|
| ALB | ~$18 |
| Fargate 0.25 vCPU / 0.5 GB arm64 | ~$7 |
| Public IPv4 (ALB ×2 + task ×1) | ~$11 |
| Aurora | mostly storage only, since it pauses at 0 ACU |
| Secrets Manager / ECR / logs | a few tens of cents |

- Aurora only auto-pauses when there are **zero** DB connections, so the API opens a connection per request (SQLAlchemy `NullPool`) instead of keeping a pool. With a connection pool, Aurora would stay at 0.5 ACU 24/7 and add roughly **$55–70 per month** per environment
- Destroy environments you are not using (`make deploy` recreates them in ~15 minutes)
- The first request after Aurora pauses waits ~15 s for it to resume. Reload if it times out

## Before running real production

- ECS tasks run in public subnets → move to private subnets with a NAT Gateway or VPC endpoints
- Add ECS auto scaling and set `api_desired_count` to 2+ to spread across AZs
- `skip_final_snapshot = true` / `deletion_protection = false` (for one-command teardown) → enable protection for production
- Set Aurora `db_min_acu` to 0.5+ in production to avoid resume latency
- Replace startup `create_all` with Alembic migrations
- Move deploys to CI/CD (e.g. GitHub Actions with OIDC) instead of deploying from a laptop

## Layout

```
backend/            FastAPI (same Dockerfile for local and ECS)
frontend/           Next.js + sst.config.ts
infra/bootstrap/    account-wide: Terraform state S3 bucket, ECR
infra/stack/        per environment: VPC / ALB / ECS / Aurora / Secrets Manager (switch via envs/*.tfvars)
Makefile            entry point for everything
```
