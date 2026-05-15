#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Adiscon GmbH.
# Buildbot master — GitHub status, mail, and optional GitHub issue reporter.
# Safe to commit: no passwords, no raw tokens (reads g[...] from nogit_secrets / nogit_master_www).
#
# master.cfg must includefile nogit_secrets, then nogit_master_www, then this file.

from twisted.internet import defer
from twisted.python import log

from buildbot import config
from buildbot.process.properties import Interpolate
from buildbot.plugins import reporters, util
from buildbot.reporters.base import ReporterBase
from buildbot.reporters.generators.build import BuildStatusGenerator
from buildbot.util import httpclientservice

GITHUB_API = "https://api.github.com"


class GitHubIssuePush(ReporterBase):
    """POST an issue to GitHub when selected builders fail (fine-grained PAT: Bearer)."""

    name = "GitHubIssuePush"

    def checkConfig(self, owner, repo, token, generators=None, **kwargs):
        if generators is None:
            config.error("GitHubIssuePush: generators= is required")
        super().checkConfig(generators=generators, **kwargs)
        httpclientservice.HTTPClientService.checkAvailable(self.__class__.__name__)

    @defer.inlineCallbacks
    def reconfigService(self, owner, repo, token, generators, **kwargs):
        self._owner = owner
        self._repo = repo
        token = yield self.renderSecrets(token)
        yield super().reconfigService(generators=generators, **kwargs)
        self._http = yield httpclientservice.HTTPClientService.getService(
            self.master,
            GITHUB_API,
            headers={
                "Authorization": "Bearer " + token,
                "Accept": "application/vnd.github+json",
                "User-Agent": "buildbot-rsyslog-ci",
            },
            debug=False,
            verify=True,
        )

    @defer.inlineCallbacks
    def sendMessage(self, reports):
        for report in reports:
            title = report.get("subject") or "[CI] Build failure"
            body = report.get("body") or ""
            if isinstance(body, bytes):
                body = body.decode("utf-8", errors="replace")
            title = str(title).strip().replace("\n", " ")
            if len(title) > 250:
                title = title[:247] + "..."
            if len(body) > 60000:
                body = (
                    body[:59900]
                    + "\n\n_(truncated: GitHub issue body limit ~65k)_"
                )
            path = "/repos/{0}/{1}/issues".format(self._owner, self._repo)
            try:
                response = yield self._http.post(
                    path, json={"title": title, "body": body}
                )
                if response.code // 100 != 2:
                    content = yield response.content()
                    log.msg(
                        "GitHubIssuePush: POST {0} failed code={1} body={2}".format(
                            path, response.code, content[:500]
                        )
                    )
            except Exception as e:
                log.err(e, "GitHubIssuePush: failed to create issue")


context = Interpolate("buildbot/%(prop:buildername)s")

_mail_generator = reporters.BuildStatusGenerator(
    mode=("warnings", "failing", "exception"),
    message_formatter=reporters.MessageFormatter(
        template="STATUS: {{ summary }}",
    ),
)
mn = reporters.MailNotifier(
    fromaddr=g["BB_MAIL_FROMADDR"],
    sendToInterestedUsers=False,
    extraRecipients=g["BB_MAIL_EXTRA_RECIPIENTS"],
    generators=[_mail_generator],
)

githubstatus = reporters.GitHubStatusPush(
    token=g["secret_GITHUB_TOKEN"],
    context=context,
)

lc["services"].append(mn)
lc["services"].append(githubstatus)

_solaris_issue_formatter = reporters.MessageFormatter(
    subject="[CI] Solaris 11x64 rsyslog failed — {{ buildername }} — {{ summary }}",
    template="""## Solaris 11x64 rsyslog CI failure

**Summary:** {{ summary }}
**Builder:** {{ buildername }}
**Build:** {{ build_url }}
**Revision:** {{ build['properties'].get('got_revision', ['(unknown)'])[0] }}
**Worker:** {{ workername }}

### Steps
{% if build['steps'] %}{% for step in build['steps'] %}
- {{ step['number'] }}: {{ step['name'] }} — {{ result_names[step['results']] }}{% if step.get('logs') %} — {% for log in step['logs'] %}[{{ log.name }}]({{ log.url }}) {% endfor %}{% endif %}
{% endfor %}{% else %}
_(no step data)_
{% endif %}
""",
    want_steps=True,
    want_logs=True,
)

_solaris_issue_generators = [
    BuildStatusGenerator(
        builders=["rsyslog solaris11x64 rsyslog"],
        mode=("failing", "exception"),
        message_formatter=_solaris_issue_formatter,
    )
]

_issue_token = g.get("secret_GITHUB_TOKEN_BUILD_SOLARIS_ISSUES") or g.get(
    "secret_GITHUB_TOKEN"
)
if _issue_token:
    lc["services"].append(
        GitHubIssuePush(
            owner="rsyslog",
            repo="rsyslog",
            token=_issue_token,
            generators=_solaris_issue_generators,
        )
    )
else:
    log.msg(
        "master_github_reporters: GitHubIssuePush skipped "
        "(no secret_GITHUB_TOKEN_BUILD_SOLARIS_ISSUES or secret_GITHUB_TOKEN)"
    )
