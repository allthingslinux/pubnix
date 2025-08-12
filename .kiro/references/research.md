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

- tilde.tk/: Tilde subdomain project details (Cloudflare Pages hosting, Freenom registrar); manual email-based onboarding; TODOs for automation.
  - Transferable: if offering subdomains, automate DNS provisioning and onboarding emails.

- tilde/ (Hack Club tilde NixOS config): Flake-based host config, `addusr` script for creating required directories, strict CoC; services limited to static HTTP/Gemini; joining via Slack `#tilde` with SSH key.
  - Transferable: NixOS flake as an alternative ops stack; ensure `addusr`-like script in our provisioning.

- tildetown_ring/: Python/JS/Prolog web ring for tilde.town with join page.
  - Transferable: another webring implementation to study for join workflows.

- tilde-social/: Flat-file social network under `~/.social` with CLI `timeline` for feeds, posts, and follows; future roadmap includes replies/boosts/hashtags.
  - Transferable: consider optional CLI social tooling reading from home dirs; or integrate with our `comm` endpoints.

- tilde.etcskel/: `/etc/skel` contents and contribution model; encourages wiki-driven docs.
  - Transferable: ship a curated `/etc/skel` with helpful defaults.

- share/: Placeholder for shared assets; no substantive docs here.

- site/ and site/wiki/: tilde.club site source and wiki build flow; contributors submit markdown, `make` builds HTML; signup code reference included.
  - Transferable: keep site build simple, accept PRs for docs/wiki.

- tilde.club/: Code and utilities for running/managing tilde.club; community ethos and links to story/FAQ; volunteer-led model.
  - Transferable: emphasize volunteer onboarding and clear contribution channels.

- spsrv/: Spartan protocol server in Go with features: `/~user` support, directory listing, CGI, CONF/TOML config, systemd examples; caution around user CGI security.
  - Transferable: if offering Spartan/Gemini, consider spsrv; document CGI risks and sandboxing.

- webring/: XXIIVV webring with criteria and circular linking; requires 10+ content pages and a banner; join via PR to `index.html`.
  - Transferable: adopt quality criteria for our webring.

- tildes/: utilities for tildeverse (e.g., `code` to index user dirs into HTML).
  - Transferable: provide admin scripts to generate community indices (opt-in).

- where/: rewritten tool (Tcl + SQLite) to geolocate/where listing; caches IPs.
  - Transferable: pattern for lightweight service with caching.

- www-site/ and www-site-v2/: Dimension.sh website (Hugo in v2).
  - Transferable: Hugo is a good default for static sites.

- wiki/: Dimension.sh wiki markdown and style guide (WikiLinks, archival links).
  - Transferable: adopt WikiLinks-style internal linking.

- tildejsongen/: Python tool to generate Tilde Description Protocol `tilde.json`/yaml from INI config; outputs paths, users group id, signup URL, want_users flag.
  - Transferable: auto-publish our `tilde.json` and `tilde.yaml` to advertise services.

- website/: Project Segfault Svelte site; dev/prod instructions; envs for Ghost CMS and Uptime Kuma; Docker-first deploy.
  - Transferable: reference for integrating status/news feeds into our public site.

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

## Recommended roadmap (synthesis)

- Gemini and Gopher hosting
  - What: Offer `~/public_gemini` via Molly-Brown and `~/public_gopher` via Gophernicus; expose `gemini://` and `gopher://` endpoints.
  - Why: Core tilde experience widely offered by peers.
  - How: New Ansible roles (`gemini`, `gopher`) + nginx/Caddy fronting if needed; add docs, tests asserting directory mapping and service health.

- Pre/post provisioning hooks
  - What: Honor `/etc/pubnix/pre.d` and `/etc/pubnix/post.d` executable hooks in `ProvisioningService`.
  - Why: Operator extensibility without code changes (mkuser pattern).
  - How: Discover and execute hooks with clear env contract (username, uid, home), strict timeouts, logs, and exit-code handling.

- Public signup endpoint + Matrix notifications
  - What: `POST /public/signup {username,email,ssh}` that creates an `Application`, rate-limits, and notifies moderators via Matrix + email.
  - Why: Mirrors PublAPI; speeds operator response.
  - How: Add `MatrixNotifier` service; support Shoutrrr-like webhook fallback; optional IP allowlist.

- Webring helper and policy
  - What: Maintain `webring/members.json`, expose prev/next API, provide an HTML/JS widget snippet; adopt XXIIVV criteria incl. 88×31 banner.
  - Why: Community discovery with consistent UX.
  - How: CLI to validate entries; CI to build a static page; moderation workflow via PRs.

- tilde.json + yaml generation
  - What: Publish `/.well-known/tilde.json` and `/tilde.yaml` nightly.
  - Why: Interop and discovery across tildeverse.
  - How: Generate from config (name, url, signup_url, want_users, admin_email, paths) and deploy; add tests for endpoint presence.

- Domain/SSL expiry watcher
  - What: Monitor WHOIS expiry, ACME certificate expiry, and DNS health; export Prometheus metrics.
  - Why: Reduce outages; alert early.
  - How: Cron/systemd timer calling a watcher; push metrics and Matrix alerts.

- Harden `/etc/skel` + first-10-minutes docs
  - What: Ship curated skel (shell rc, `.plan`, `public_html` templates) and clear onboarding docs (SSH keys, `~user` web, CGI, IRC/Usenet).
  - Why: Smoother onboarding; consistent defaults.
  - How: Ansible role to install skel; docs under `/docs`, linked from MOTD and web.

- Optional Spartan server (spsrv)
  - What: Provide Spartan service with `~user` mapping; user CGI disabled by default.
  - Why: Complements Gemini/Gopher for enthusiasts.
  - How: Package and document; make opt-in via Ansible tag/var; note CGI risks.

- Backups with Borg/Borgmatic
  - What: Standard, robust backups for pubnix data.
  - Why: Widely used in peers; reliable.
  - How: Ansible role; integrate with our backup manifest and `/monitoring` health endpoint.

- Harden nginx userdir + headers
  - What: Ensure HSTS, content-type options, referrer policy, rate limits; secure userdir.
  - Why: Baseline hardening across sites.
  - How: Adopt best snippets from `pubnix-configs`; extend tests to assert HSTS.

## Per-repo deep dive and actionable items

- ansible/
  - Adopt roles: `borgmatic`, `certbot`, `cis` (subset), `efingerd`, `gemini`, `gopher`, `news`, `postfix`, `shell`, `www`.
  - Tag scheme: `base, ssh, quotas, userdir, mail, backups, services`.
  - Secrets: Vault for global/per-host; document operator flow.

- astral.social/, infra-2/
  - Separate public site vs ops repo; keep `pubnix/` automation isolated.
  - Consider Caddy+Geo/Tor only if we add multi-region.

- bb/
  - Package optional TUI bulletin board storing per-user data; aggregate read-only across users.
  - Bridge to our `comm` API for web/mobile listing.

- cosmic/
  - CI hygiene; no direct adoption.

- makeuser/ and mkuser/
  - Provide `pubnix-admin` CLI wrapping provisioning user creation.
  - Implement pre/post hooks with env contract.

- meta-ring/ and webring/
  - JSON members, static build, PR-based joins, clear quality criteria.
  - Provide validator CLI and PR template.

- publapi/
  - Implement minimal `POST /public/signup`; integrate Matrix/email; rate limit and optional IP allowlist.

- pubnix-configs/
  - Pull nginx hardening snippets and align with tests for HSTS/security headers.

- pubnix-domain-watcher/
  - Build a watcher for domains/certs; export metrics; add Matrix alerts.

- pubnix-site/
  - Optional Fresh/Deno site; otherwise keep current static site.

- Segfautils/
  - Microservice pattern for contact admin form; could be replaced by backend endpoint + Matrix relay.

- SF-UI/
  - Consider browser terminal for guided onboarding (sandboxed); otherwise defer.

- tilde.tk/
  - Automate subdomain provisioning (Cloudflare API), outbound mail verification policy, SPF/DMARC.

- tilde (Hack Club)
  - `addusr` behavior: ensure user provisioning creates `public_html`, `public_gmi`, `public_gopher` with templates; enforce CoC in docs.

- tildetown_ring/
  - Study join UX; support PR + form-to-PR workflow.

- tilde-social/
  - Optional CLI `timeline` leveraging `~/.social`; optionally sync to `comm` endpoints.

- tilde.etcskel/
  - Curate `/etc/skel` for friendly defaults; include `.ssh/config` sample, `.plan`.

- site/ and site/wiki/
  - Build contributor wiki; ship SSH/2FA/IRC/Usenet/CGI/editor guides; `make` build flow.

- tilde.club/
  - Codify ethos and volunteer onboarding in docs; contribute paths clear.

- spsrv/
  - Offer Spartan as opt-in; default user CGI off; document sandboxing.

- tildes/
  - Implement opt-in community indexers (e.g., `~/bin`, `~/projects`) generating a shared page.

- where/
  - Consider an opt-in location page with caching; privacy-first defaults.

- www-site, www-site-v2, wiki/
  - Hugo for public site; wiki with WikiLinks; promote archived external links.

- tildejsongen/
  - Generate/publish `tilde.json` and YAML nightly; tests and CI.

- website/ (Project Segfault)
  - Integrate status/news feeds if we run a blog/status; else link out.

## Skeleton (`/etc/skel`) deep dive and recommendations

Goals: secure defaults, great first-run UX, and compatibility with userdir (web), Gemini, Gopher, and optional services.

- Directory layout and permissions
  - `$HOME` (created by useradd): mode 0711 (traversable without listing); owner `user:user`.
  - `~/.ssh/`: 0700; `authorized_keys`: 0600; optional `config`: 0600 with minimal, non-host-specific examples commented out.
  - `~/public_html/`: 0755; include `index.html` (simple welcome) and `README.txt` with next steps; CGI folder `~/public_html/cgi-bin/` with 0755, sample script non-executable by default.
  - `~/public_gemini/`: 0755; `index.gmi` with a few links to docs.
  - `~/public_gopher/`: 0755; `gophermap` or `index.txt` per server’s expectation.
  - Optional: `~/bin/` (0755) added to PATH in shell rc; `~/projects/` (0755).

- Default files
  - `.bashrc`/`.bash_profile` or `.zshrc`: source `/etc/profile`, set `PATH` to include `~/bin`, add helpful aliases (ls -lah, grep --color), and a brief MOTD pointer.
  - `.profile`: minimal, non-duplicative, to support non-bash logins.
  - `.plan` and `.project`: 0644 with a template encouraging users to personalize; compatible with `finger`/`efingerd`.
  - `.hushlogin`: optional to suppress verbose login banners; we recommend keeping MOTD pointers visible initially.
  - `README_FIRST.txt`: short “first 10 minutes” checklist (upload key, create web page, join IRC/Usenet, where docs live).

- Web userdir and CGI guidance
  - Ensure nginx userdir config reads from `~/public_html`, and tests enforce security headers and userdir routing.
  - Include `public_html/README_CGI.txt` explaining security risks; default per-user CGI disabled at server level unless explicitly enabled.

- Gemini and Gopher
  - Provide minimal `index.gmi` and `gophermap` templates; link to service catalog and rules.

- Mail and forwarding (optional)
  - If `~/.forward` supported, document carefully; do not ship by default.

- Shell and editor
  - Offer commented samples in rc files for setting `$EDITOR` (nano/vim) and enabling useful prompt; avoid opinionated themes by default.

- Ansible role implementation
  - Idempotent tasks to create directories/files with exact modes.
  - Templated `index.html`, `index.gmi`, `README` files; jinja variables for instance name.
  - Post-provision hook to fix permissions if users pre-exist.

- Security notes
  - Enforce home 0711 to allow web traversal but not listing.
  - `.ssh` strict modes; fail2ban covers sshd; recommend ed25519 keys with `-a 100` in docs.

- Documentation
  - Link skel templates to `/docs` pages: SSH keys, userdir, Gemini/Gopher, CGI, IRC/Usenet, CoC.

## Notable references (files skimmed)

- Ansible production patterns: `.kiro/references/ansible/README.md`
- Tilde setup guide: `.kiro/references/tilde.club/docs/how-to-set-up-a-tilde.md`
- SSH guide: `.kiro/references/site/wiki/source/ssh.md`
- mkuser: `.kiro/references/mkuser/README.md`
- PublAPI: `.kiro/references/publapi/README.md`
- tilde.tk email: `.kiro/references/tilde.tk/docs/Email.md`
- Accounting: `.kiro/references/tilde.club/docs/accounting.md`
- Meta Ring: `.kiro/references/meta-ring/README.md`
