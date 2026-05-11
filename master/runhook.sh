#!/bin/sh
# Credentials must NOT live in git. Set on the host (systemd Environment=,
# /etc/buildbot/github-hook.env, etc.) then export before Buildbot runs hooks.
set -eu
: "${GITHUB_BUILDBOT_AUTH:?missing GITHUB_BUILDBOT_AUTH (form: user:token_or_password)}"
: "${GITHUB_BUILDBOT_SECRET:?missing GITHUB_BUILDBOT_SECRET (GitHub webhook secret)}"
exec python github_buildbot.py --level=debug --auth="$GITHUB_BUILDBOT_AUTH" --secret="$GITHUB_BUILDBOT_SECRET"
