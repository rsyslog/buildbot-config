# Buildbot master configuration

This directory holds the Buildbot **master** configuration. Some files are **not** tracked in git (see repository [`.gitignore`](../.gitignore): `nogit*`).

## Include order (`master.cfg`)

1. **`nogit_secrets.py`** — API tokens and other secrets (`g['secret_*']`). **Never commit.**
2. **`nogit_master_www.py`** — Web UI auth (`UserPasswordAuth`, `RolesFromEmails`), GitHub hook wiring, and operational globals such as **`g['BB_MAIL_EXTRA_RECIPIENTS']`** for `MailNotifier`.
3. **`master_github_reporters.py`** — Committed reporter services: `MailNotifier`, `GitHubStatusPush`, optional **`GitHubIssuePush`** for Solaris 11x64 failures. Reads only `g[...]`; no embedded passwords.

## Secrets and tokens (`g` keys)

| Key | Purpose | Where to set |
|-----|---------|--------------|
| `secret_GITHUB_TOKEN` | GitHub commit statuses (`GitHubStatusPush`), PR hook API calls in `RsyslogGitHubEventHandler` | `nogit_secrets.py` |
| `secret_GITHUB_TOKEN_BUILD_SOLARIS_ISSUES` | Fine-grained PAT: **Issues read/write** on `rsyslog/rsyslog` only; used to open an issue when builder `rsyslog solaris11x64 rsyslog` fails | `nogit_secrets.py` |
| `secret_CODECOV_TOKEN` / `secret_CODECOV_TOKEN_LIBRELP` | Codecov uploads only — **not** for GitHub REST API | `nogit_secrets.py` |
| `BB_MAIL_EXTRA_RECIPIENTS` | List of email addresses for `MailNotifier` | Top of `nogit_master_www.py` (or optionally `nogit_secrets.py` if you prefer one file) |
| `BB_MAIL_FROMADDR` | `MailNotifier` From address | `nogit_master_www.py` (not in git-tracked reporter code) |

### Creating `secret_GITHUB_TOKEN_BUILD_SOLARIS_ISSUES`

1. GitHub → **Settings** → **Developer settings** → **Fine-grained personal access tokens**.
2. Resource owner: **rsyslog** org (or your user), **Repository access**: only **`rsyslog/rsyslog`**.
3. Permission: **Issues → Read and write** (Metadata stays read-only).
4. Generate the token once, assign: `g['secret_GITHUB_TOKEN_BUILD_SOLARIS_ISSUES'] = "…"` in **`nogit_secrets.py`** on the master host.
5. If the org uses **SAML SSO**, authorize the token for the org.
6. Smoke test: `curl -sS -o /dev/null -w "%{http_code}" -X POST https://api.github.com/repos/rsyslog/rsyslog/issues -H "Authorization: Bearer TOKEN" -H "Accept: application/vnd.github+json" -d '{"title":"token test","body":"delete me"}'` → expect **201**.

## Solaris 11x64 CI

- Builder **`rsyslog solaris11x64 rsyslog`** is removed from default PR/force Solaris schedulers; it runs on a **nightly** schedule on branch **`main`** (see `rsyslog_master_include.py`).
- On failure, **`GitHubIssuePush`** creates an issue in **`rsyslog/rsyslog`** using the fine-grained token above (body includes build URL and step summary).

## Operations

- After any leak of `nogit_secrets.py` or `nogit_master_www.py`, **rotate** all tokens and passwords.
- Validate config: `buildbot checkconfig master.cfg` (from this directory).

## Git: block accidental `nogit*` commits

`.gitignore` alone does not stop `git add -f`. One-time setup from the **repository root**:

```bash
sh scripts/install-git-hooks.sh
```

That installs `githooks/pre-commit` into `.git/hooks/pre-commit`. The hook (and **`scripts/verify-no-nogit-in-git.sh`**) refuse any commit that **stages** add/modify of a path whose basename starts with `nogit`, or that leaves such paths **tracked** in the index.

Manual check (e.g. in CI): `sh scripts/verify-no-nogit-in-git.sh`
