#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 	* Copyright (C) 2013 Adiscon GmbH.
#	* This file is part of RSyslog
#	* 
#	* rsyslog factory settings
#	*

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.github import GitHub
from buildbot.steps.shell import ShellCommand
from buildbot.steps.shell import Configure 

#
# rsyslog-doc: right now, only on Ubuntu16 slave
#
factoryRsyslogDocUbuntu16 = BuildFactory()
factoryRsyslogDocUbuntu16.addStep(ShellCommand(command=["sleep", "2"], name="wait github sync"))
factoryRsyslogDocUbuntu16.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDocUbuntu16.addStep(ShellCommand(command=["git", "log", "-4"], name="git branch information"))
factoryRsyslogDocUbuntu16.addStep(ShellCommand(command=["docker", "pull", "rsyslog/rsyslog_doc_gen"], name="pull docker docgen image"))
factoryRsyslogDocUbuntu16.addStep(ShellCommand(command=["bash", "-c", "docker run -u`id -u`:`id -g` -eSPHINX_EXTRA_OPTS=-q -v`pwd`:/rsyslog-doc rsyslog/rsyslog_doc_gen"], logfiles={"preview_url": "preview_url"}, lazylogfiles=True, name="generate doc"))
factoryRsyslogDocUbuntu16.addStep(ShellCommand(command=["bash", "-c", "FILE=\"`date +doc-%Y-%m-%d-%H-%M-%S`-`git log -1 --pretty=format:\"%h\"`\"; mkdir /var/www/html/doc/; mkdir /var/www/html/doc/$FILE; cp -rv build/* /var/www/html/doc/$FILE; echo \"http://ubuntu16.rsyslog.com/doc/$FILE\" > preview_url"], logfiles={"preview_url": "preview_url"}, lazylogfiles=True, name="make PREVIEW available")) 

######### hardcoded scheduler for rsyslog-doc generation
# ----------------------------------------------------------------------
from buildbot.config import BuilderConfig

lc['builders'].append(
	BuilderConfig(name="rsyslog-doc ubuntu16 rsyslog",
		workernames=["slave-ubuntu16"],
		factory=factoryRsyslogDocUbuntu16, 
		tags=["rsyslog-doc rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog-doc",
		} ))

lc['schedulers'].append(ForceScheduler(
	name="pull_rsyslog_rsyslogdoc",
	label="1. Pull Requests-rsyslog-rsyslog-doc", 
	builderNames=[ "rsyslog-doc ubuntu16 rsyslog" ],
	codebases=[
		util.CodebaseParameter(
			"", 
			branch=util.StringParameter(
				name="branch", 
				label="Pull Request Number:", 
				required=True, 
				default="refs/pull/<NUMBER>/head", 
				size=80),
			),
	] ))

lc['schedulers'].append(ForceScheduler(
	name="forceall_rsyslog_rsyslog-doc",
	label="2. Force All-rsyslog-rsyslog-doc",
	builderNames=[ "rsyslog-doc ubuntu16 rsyslog" ] ))

lc['schedulers'].append(SingleBranchScheduler(
	name="github_rsyslog-rsyslog-doc",
	change_filter=filter.ChangeFilter(	category="pull", 
						project="rsyslog/rsyslog-doc"),
	builderNames=[ "rsyslog-doc ubuntu16 rsyslog"] ))

#
#lc['schedulers'].append(SingleBranchScheduler(
#	name="sched-rsyslog-rsyslog-doc-ubuntu16",
#	change_filter=filter.ChangeFilter(project="rsyslog-doc",branch="master"),
#	treeStableTimer=None,
#	builderNames=["rsyslog-doc ubuntu16 rsyslog"] ))
#
#
#
#lc['schedulers'].append(ForceScheduler(
#	name="force-rsyslog-rsyslog-doc-ubuntu16", 
#	builderNames=[ "rsyslog-doc ubuntu16 rsyslog" ] ))
#
# ----------------------------------------------------------------------
