#!/bin/sh
# Credentials must NOT live in git. Defaults: /etc/buildbot/github-hook.env
# (override path with GITHUB_BUILDBOT_ENVFILE); or export vars via systemd.
set -eu
ENVFILE="${GITHUB_BUILDBOT_ENVFILE:-/etc/buildbot/github-hook.env}"
if [ -r "$ENVFILE" ]; then
	# shellcheck disable=SC1090
	set -a && . "$ENVFILE" && set +a
fi
: "${GITHUB_BUILDBOT_AUTH:?missing GITHUB_BUILDBOT_AUTH (form: user:token_or_password)}"
: "${GITHUB_BUILDBOT_SECRET:?missing GITHUB_BUILDBOT_SECRET (GitHub webhook secret)}"
exec python github_buildbot.py --level=debug --auth="$GITHUB_BUILDBOT_AUTH" --secret="$GITHUB_BUILDBOT_SECRET"
