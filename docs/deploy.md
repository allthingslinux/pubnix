# ATL Pubnix Production Deployment Guide

This guide outlines a minimal, repeatable deployment of ATL Pubnix.

## Prerequisites

- A provisioned Linux host (e.g., via Terraform in `infrastructure/terraform/hetzner`)
- A production PostgreSQL instance reachable from the host
- DNS records for your domain (e.g., `atl.sh`) pointing to the host
- Email SMTP credentials for outbound notifications

## System setup (Ansible)

1. Add your server to `infrastructure/ansible/inventory.ini`.
2. Run:
   ```bash
   cd infrastructure/ansible
   ansible-playbook -i inventory.ini site.yml
   ```
   This installs and configures: hardened `sshd`, nginx with userdir support, Fail2Ban, AppArmor, and `fcgiwrap`.

## Install application

- Place the repository under `/opt/pubnix` on the server (e.g., clone or deploy artifacts).
- Ensure Python and uv available:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  apt-get install -y python3.11 python3.11-venv  # or distro equivalent
  ```
- Install backend dependencies:
  ```bash
  cd /opt/pubnix/backend
  uv sync
  uv run alembic upgrade head
  ```

## Configure environment

Create `/etc/pubnix/backend.env` (or copy example from `infrastructure/systemd/atl-pubnix-backend.env.example`) with:

```
PUBNIX_ENV=production
PUBNIX_DEBUG=false
PUBNIX_LOG_LEVEL=INFO
DATABASE_URL=postgresql://pubnix:strong_password@db-host:5432/pubnix
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=REDACTED
FROM_EMAIL=noreply@atl.sh
FROM_NAME=ATL Pubnix
INTEGRATIONS_API_KEY=generate_a_strong_token
```

## Configure systemd service

Install unit files from `infrastructure/systemd`:

```bash
cp infrastructure/systemd/atl-pubnix-backend.service /etc/systemd/system/
cp infrastructure/systemd/nginx-reload.service /etc/systemd/system/
cp infrastructure/systemd/nginx-reload.timer /etc/systemd/system/
install -D -m 0640 infrastructure/systemd/atl-pubnix-backend.env.example /etc/pubnix/backend.env
systemctl daemon-reload
systemctl enable --now atl-pubnix-backend.service
systemctl enable --now nginx-reload.timer
```

Check status:

```bash
systemctl status atl-pubnix-backend.service
journalctl -u atl-pubnix-backend.service -f
```

## Nginx

- Ensure nginx site is enabled and reloaded (Ansible does this):
  - API is proxied under `/api/` to backend on `http://127.0.0.1:8000/`
  - Landing page is served at `/landing`
  - User web roots at `/~username`

## Monitoring

- Point Prometheus at: `http://<host>/api/v1/monitoring/metrics`

## Backups

- Mount remote storage (e.g., Hetzner Storage Box) and configure a periodic job invoking `BackupService`.
- Verify backup integrity via the manifest before uploads.

## Smoke test checklist

- Create an application via `/api/v1/applications/` and approve it
- Verify user is created and default limits exist
- Add an SSH key via `/api/v1/ssh-keys/`
- Access `/~username` after creating `~/public_html/index.html`
- Verify `/api/v1/monitoring/metrics` and `/api/v1/monitoring/alerts/health`
- Run a backup and test restore on a scratch directory
