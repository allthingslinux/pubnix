# Pubnix/Tilde research notes

These are consolidated notes from the repos cloned into `.kiro/references/`. Focus: features that translate into a modern pubnix offering, operational ideas, and user experience touches. Includes a per-repo review and cross-cutting ideas.

## Per-repo findings

- ansible/: Production Ansible for Project Segfault with two playbooks: `all` (base) and `privfrontends` (Caddy+Docker). Uses Ansible Vault (`secrets.yaml`, per-host `host_vars`). Tags for selective runs (caddy-non-update, docker, cron). Includes geo frontends patterns and TOR onion config snippets.
  - Transferable: structure our ops repo similarly, tag roles (`ssh`, `quotas`, `nginx-userdir`, `fail2ban`, `backups`), and keep secrets in Vault. Consider Caddy for multi-region entry.

- astral.social/: Minimal readme; repo holds website and misc infra for astral.social.
  - Transferable: separate site content from core infra; keep infra scripts in a misc/ tree.

- bb/: Go bulletin board for pubnix where each user's posts live under their home; the tool collates across users. Interactive TUI + CLI args, pin/archive, simple moderation, extensible via `addons.go`.
  - Transferable: implement a similar per-user-file message board as an optional community feature; align with our `comm` APIs or expose a TUI client.

- cosmic/: Scripts/configs for cosmic.voyage. CI present, details light.
  - Transferable: example of publishing site-specific automation.

- infra/: Ansible roles for dimension.sh infra: borgmatic backups, certbot, CIS hardening subset, efingerd, gemini (Molly-Brown), gopher (Gophernicus), news, postfix, shell, nginx `www`. Meta roles for build/dev/mail/services/shell.
  - Transferable: mirror role coverage; especially backups (Borg/Borgmatic), Gemini/Gopher, efingerd, and a minimal “news” system.

- infra-2/: Misc infra/code for astral.social; pubnix scripts under `pubnix/`.
  - Transferable: separate pubnix automation into its own subtree.

- makeuser/: Shell-based `makeuser` installed to `/usr/local/bin` for admin account creation.
  - Transferable: provide an admin CLI wrapper calling our provisioning API.

- meta-ring/: Lume/Deno webring; members listed in JSON; Netlify functions handle redirects; local dev via `deno task`.
  - Transferable: ship a tiny webring helper and static generator.

- mkuser/: Python CLI wrapping `useradd`, driven by `/etc/login.defs`, email template at `/etc/mkuser/mail.tmpl`, pre/post hooks in `/etc/mkuser/pre.d` and `/etc/mkuser/post.d`.
  - Transferable: adopt hook directories in ProvisioningService; ship welcome templates.

- publapi/: Go API with `GET /users`, `POST /signup` (username/email/ssh), admin notifications via Shoutrrr; env-configurable; optional signup IP allowlist.
  - Transferable: add a similar public endpoint hooked into our Applications workflow and notifications.

- pubnix-configs/: Assorted configuration snippets for pubnix (e.g., nginx).
  - Transferable: compare nginx userdir/security defaults with ours; harvest hardening.

- pubnix-domain-watcher/: Scripts (sh/ts) to track domains; readme missing.
  - Transferable: add SSL/domain expiry watcher with notifications.

- pubnix-site/: Fresh/Deno starter-based site for a pubnix website.
  - Transferable: acceptable alternative to our docs site generator.

- Segfautils/: Go web utilities (contact form), Docker-first, TOML config.
  - Transferable: package small tools as containers; TOML/YAML config patterns.

- SF-UI/: Angular + Go bridge to provide a browser terminal over websockets to a backend SSH shell; Docker and nginx recipes; embeds UI assets.
  - Transferable: inspiration for onboarding/demo shell; likely out-of-scope for core.

- tilde.club/*, site/wiki/*, tilde.*: Rich user docs (SSH keys/2FA, IRC/Usenet, email, CGI, editors, `sshfs`, CoC, donations). Alternate SSH on 443; explicit keygen guidance (ed25519, `-a 100`).
  - Transferable: mirror content in our `/docs` and keep it first-run friendly.

- tilde.tk/: Email and outbound mail docs with verification via forwarding addresses.
  - Transferable: document outbound mail policy and verification; enforce SPF/DMARC.

- webring/, tildes/, where/, www-site, www-site-v2, wiki/: Site scaffolds, static content, security policy pages, wiki structures and templates.
  - Transferable: include security policy and a simple wiki template.

## Provisioning and user lifecycle

- mkuser (Python CLI):
  - Simple `mkuser username email sshkey` that shells to `useradd`, reads `/etc/login.defs` for defaults, supports `/etc/mkuser/pre.d` and `/etc/mkuser/post.d` hooks. Email template at `/etc/mkuser/mail.tmpl` (Python Template strings).
  - Idea: mirror the hook mechanism in our provisioning pipeline so operators can drop scripts without editing code. Provide Jinja2-based templates for welcome emails and shell skeleton.

- publapi (Go):
  - Minimal API: `GET /users`, `POST /signup` to create a registration stub and notify admins via Shoutrrr URLs; optional signup IP restriction.
  - Idea: keep public signup API very small; fan-out to notifications (Matrix/Email) and an operator queue. Our backend can expose a compatible `POST /integrations/signup` and produce a pending application record.

- tilde.club docs (how-to-set-up-a-tilde):
  - Classic flow (EC2, Apache UserDir, password auth, home `public_html`). Many steps are dated (password login, Amazon Linux specifics), but capture baseline expectations.
  - Idea: modernize with: users-only-SSH-keys, `nginx` userdir, systemd user slices, and infra-as-code (Ansible/Terraform) vs click-ops.

## Configuration management and infra

- ansible (Project Segfault):
  - Two playbooks: base system setup and geo privacy frontends (Caddy+Docker). Uses Ansible Vault for secrets (`secrets.yaml` + per-host `host_vars`). Tags for partial runs (caddy-non-update, docker, cron).
  - Idea: adopt tagged Ansible runs for core pubnix hosts: `base`, `ssh`, `quotas`, `nginx-userdir`, `fail2ban`, `apps`. Keep secrets in Vault; mirror per-host vars for machine-specific overrides.
  - Caddy-based frontends patterns (GeoDNS, Tor onion mappings) are a useful reference for multi-region web entry.

## User web hosting and UX

- site/wiki, tilde.club docs, www-site-v2, wiki/*:
  - Rich user-facing docs: SSH guides, 2FA, email, IRC/Usenet, editors, CGI how-tos, security, code of conduct, donations.
  - Idea: ship a curated docs site in-repo that mirrors these topics; integrate into `/docs` and auto-expose in web UI. Provide “first 10 minutes” flows and copy-paste commands for keys, `~/public_html`, CGI, `sshfs`.

- Nginx/Apache UserDir:
  - Tilde ecosystems standardize on `~/public_html`. Our tests already enforce nginx config for userdir and security headers. Cross-check examples in `pubnix-configs` and `www-site`.

## Community and social glue

- webring / meta-ring:
  - Simple JSON member lists + static site. Netlify/Deno-based functions and simple build.
  - Idea: expose a tiny `/webring` service that reads members from a repo and emits prev/next links as a widget snippet users can paste to personal pages.

- tildetown_ring / meta-ring success/join:
  - Lightweight join workflow through PRs and documentation.
  - Idea: keep contribution models trivial—PR to JSON, signed off by moderators; automate checks.

## Services and integrations

- tilde.* and site/wiki include operational guides for:
  - IRC server (and connection guidance), Usenet (leafnode/tin/slrn), email setup, finger, CGI, tmux/screen, shells.
  - Idea: build a “service catalog” page with status and docs: IRC, Gemini, Gopher, NNTP, `~user` web, pastebin, mail aliases, Matrix bridges. Wire health checks into `/monitoring` metrics.

- Segfautils / SF-UI:
  - UI assets, nginx snippets, noVNC vendor docs. Likely orthogonal but useful for admin consoles if needed.

## Operational patterns

- Accounting snippet (tilde.club): users + `ac` to get cumulative session time.
  - Idea: expose friendly stats: online users, cumulative activity (privacy-sensitive, opt-in) and publish periodic community stats.

- Security and auth:
  - All modern guides push SSH keys and optional 2FA for SSH. Fail2ban/AppArmor configs exist in several repos; we already enforce security headers and fail2ban defaults in tests.
  - Idea: document key requirements (ed25519), recommend `-a 100` KDF rounds, include agent usage, backups.

## Concrete feature ideas to adopt next

- Pre/Post provisioning hooks directory on the host that our ProvisioningService triggers.
- Minimal public signup endpoint that sends Matrix/email to moderators and writes an application record.
- Built-in webring helper: static JSON registry + API and a widget snippet.
- Comprehensive docs site generated from our `/docs` and mirrored topics: SSH, userdir, CGI, mail, IRC, Usenet, finger, safety, CoC.
- Admin playbooks with tags for `ssh`, `quotas`, `nginx-userdir`, `fail2ban`, `backups`.
- Publish a Service Catalog page with links and status, backed by our `/monitoring` endpoint.

## Notable references (files skimmed)

- Ansible production patterns: `.kiro/references/ansible/README.md`
- Tilde setup guide: `.kiro/references/tilde.club/docs/how-to-set-up-a-tilde.md`
- SSH guide: `.kiro/references/site/wiki/source/ssh.md`
- mkuser: `.kiro/references/mkuser/README.md`
- PublAPI: `.kiro/references/publapi/README.md`
- tilde.tk email: `.kiro/references/tilde.tk/docs/Email.md`
- Accounting: `.kiro/references/tilde.club/docs/accounting.md`
- Meta Ring: `.kiro/references/meta-ring/README.md`
