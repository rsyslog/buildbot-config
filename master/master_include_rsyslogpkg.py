#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 	* Copyright (C) 2020 Adiscon GmbH.
#	* This file is part of RSyslog
#	* 
#	* rsyslog factory settings
#	*

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.github import GitHub
from buildbot.steps.shell import ShellCommand
from buildbot.steps.shell import Configure 

from buildbot.plugins import schedulers, util
from buildbot.config import BuilderConfig
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler
from buildbot.changes import filter

# --- Factory for checking RPM builds 
factoryRsyslogPkgRpmBuild = BuildFactory()
# - Prepare enviromment
factoryRsyslogPkgRpmBuild.addStep(ShellCommand(command=["bash", "-c", "./initenv.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'REPOUSERNAME': 'pkgbuild', "REPOURL":"rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR":"/home/pkg/rsyslog-pkg-rhel-centos", "PKGGITBRANCH":util.Interpolate('%(src::branch)s')},  haltOnFailure=True, name="Init environment"))
# - BUILD RPMS
factoryRsyslogPkgRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-6-i386/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-6", "RPM_ARCH":"i386", "RPM_REPO":"testing"}, logfiles={"root.log": "/var/lib/mock/epel-6-i386/result/root.log"}, maxTime=1200, timeout=1200, name="build epel-6/i386 rpms"))
factoryRsyslogPkgRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-6-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-6", "RPM_ARCH":"x86_64", "RPM_REPO":"testing"}, logfiles={"root.log": "/var/lib/mock/epel-6-x86_64/result/root.log"}, maxTime=1200, timeout=1200, name="build epel-6/x86_64 rpms"))
factoryRsyslogPkgRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-7-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable-el7', "RPM_PLATFORM":"epel-7", "RPM_ARCH":"x86_64", "RPM_REPO":"testing"}, logfiles={"root.log": "/var/lib/mock/epel-7-x86_64/result/root.log"}, name="build epel-7/x86_64 rpms"))
factoryRsyslogPkgRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-8-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable-el7', "RPM_PLATFORM":"epel-8", "RPM_ARCH":"x86_64", "RPM_REPO":"testing"}, logfiles={"root.log": "/var/lib/mock/epel-8-x86_64/result/root.log"}, name="build epel-8/x86_64 rpms"))

# --- Factory for building real RPM builds - includes UPLOAD!
factoryRsyslogPkgRealRpmBuild = BuildFactory()
# - Prepare enviromment
factoryRsyslogPkgRealRpmBuild.addStep(ShellCommand(command=["bash", "-c", "./initenv.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'REPOUSERNAME': 'pkgbuild', "REPOURL":"rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR":"/home/pkg/rsyslog-pkg-rhel-centos", "PKGGITBRANCH":util.Interpolate('%(src::branch)s')},  haltOnFailure=True, name="Init environment"))
# - BUILD RPMS
factoryRsyslogPkgRealRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-6-i386/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-6", "RPM_ARCH":"i386", "RPM_REPO":"v8-stable"}, logfiles={"root.log": "/var/lib/mock/epel-6-i386/result/root.log"}, maxTime=1200, timeout=1200, name="build epel-6/i386 rpms"))
factoryRsyslogPkgRealRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-6-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-6", "RPM_ARCH":"x86_64", "RPM_REPO":"v8-stable"}, logfiles={"root.log": "/var/lib/mock/epel-6-x86_64/result/root.log"}, maxTime=1200, timeout=1200, name="build epel-6/x86_64 rpms"))
factoryRsyslogPkgRealRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-7-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable-el7', "RPM_PLATFORM":"epel-7", "RPM_ARCH":"x86_64", "RPM_REPO":"v8-stable"}, logfiles={"root.log": "/var/lib/mock/epel-7-x86_64/result/root.log"}, name="build epel-7/x86_64 rpms"))
factoryRsyslogPkgRealRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-8-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable-el7', "RPM_PLATFORM":"epel-8", "RPM_ARCH":"x86_64", "RPM_REPO":"v8-stable"}, logfiles={"root.log": "/var/lib/mock/epel-8-x86_64/result/root.log"}, name="build epel-8/x86_64 rpms"))
# - UPLOAD RPMs to v8-stable repo
factoryRsyslogPkgRealRpmBuild.addStep(ShellCommand(command=["bash", "-c", "./do_upload.sh"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={"RPM_REPO":"v8-stable", "REPOUSERNAME": "pkgbuild", "REPOURL": "rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR": "/home/pkg/rsyslog-pkg-rhel-centos"}, name="upload to v8-stable repo"))

######### hardcoded scheduler for rsyslogrpm generation
# ----------------------------------------------------------------------
from buildbot.config import BuilderConfig

lc['builders'].append(
   BuilderConfig(name="rsyslogrpm rpmbuild",
     workernames=["docker-fedora30-pkgbuild"],
      factory=factoryRsyslogPkgRpmBuild,
      tags=["rsyslogrpm", "rpmbuild"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog-pkg-rhel-centos",
      },
    ))

lc['builders'].append(
   BuilderConfig(name="rsyslogrpm real rpmbuild",
     workernames=["docker-fedora30-pkgbuild"],
      factory=factoryRsyslogPkgRealRpmBuild,
      tags=["rsyslogrpm", "real", "rpmbuild"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog-pkg-rhel-centos",
      },
    ))

lc['schedulers'].append(ForceScheduler(
	name="pull_rsyslog_rsyslogrpm",
	label="1. Pull Requests-rsyslog-rsyslogrpm",
	builderNames=[ "rsyslogrpm rpmbuild" ],
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
	name="forceall_rsyslog_rsyslogrpm",
	label="2. Force All-rsyslog-rsyslogrpm",
	builderNames=[ "rsyslogrpm rpmbuild" ] ))

lc['schedulers'].append(SingleBranchScheduler(
	name="github_rsyslog-rsyslogrpm",
	change_filter=filter.ChangeFilter(	category="pull", 
						project="rsyslog/rsyslog-pkg-rhel-centos"),
	builderNames=[ "rsyslogrpm rpmbuild"] ))

lc['schedulers'].append(ForceScheduler(
	name="forceall_rsyslog_real_rsyslogrpm",
	label="1. Force All-rsyslog-real-rsyslogrpm",
	builderNames=[ "rsyslogrpm real rpmbuild" ] ))

# ----------------------------------------------------------------------
# SUSE OBS builders
# ----------------------------------------------------------------------

factory_obs_pkg_ci = BuildFactory()
factory_obs_pkg_ci.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
#factory_obs_pkg_ci.addStep(ShellCommand(command=["bash", "-c", "mkdir _OBS; cd _OBS; osc co home:rgerhards/rsyslog "], haltOnFailure=True, maxTime=1200, timeout=1200, name="checkout OBS rsyslog project"))
# We pull from git because SUSE OBS rate-limits frequent requests - not good for CI...
factory_obs_pkg_ci.addStep(ShellCommand(command=["bash", "-c", "mkdir _OBS; cd _OBS; git clone https://github.com/rsyslog/pkg_obs-clone.git ; ls ; find ."], haltOnFailure=True, maxTime=1200, timeout=1200, name="checkout OBS rsyslog project"))
factory_obs_pkg_ci.addStep(ShellCommand(command=["bash", "-c", 'cd _OBS/pkg_obs-clone/rsyslog ; osc repairwc . ; #rm *xz *dsc'], env={'PKG_PROJ':'../../..'}, haltOnFailure=True, maxTime=1200, timeout=1200, name="fix OBS work dir (due to git checkout)"))
factory_obs_pkg_ci.addStep(ShellCommand(command=["bash", "-c", 'cd _OBS/pkg_obs-clone/rsyslog ; source ./build-ubuntu.sh; git diff'], env={'PKG_PROJ':'../../..'}, haltOnFailure=True, maxTime=1200, timeout=1200, name="rebuild OBS debian package defs"))
factory_obs_pkg_ci.addStep(ShellCommand(command=["bash", "-c", 'cd _OBS/pkg_obs-clone/rsyslog ; osc build --trust-all-projects --local-package xUbuntu_20.04 x86_64'], haltOnFailure=True, maxTime=1200, timeout=1200, name="build Ubuntu 20.04 (focal)"))
factory_obs_pkg_ci.addStep(ShellCommand(command=["bash", "-c", 'cd _OBS/pkg_obs-clone/rsyslog ; osc build --trust-all-projects --local-package xUbuntu_18.04 x86_64'], haltOnFailure=True, maxTime=1200, timeout=1200, name="build Ubuntu 18.04 (bionic)"))
factory_obs_pkg_ci.addStep(ShellCommand(command=["bash", "-c", 'cd _OBS/pkg_obs-clone/rsyslog ; osc build --trust-all-projects --local-package xUbuntu_16.04 x86_64'], haltOnFailure=True, maxTime=1200, timeout=1200, name="build Ubuntu 16.04 (xenial)"))
factory_obs_pkg_ci.addStep(ShellCommand(command=["bash", "-c", 'cd _OBS/pkg_obs-clone/rsyslog ; osc build --trust-all-projects --local-package xUbuntu_14.04 x86_64'], haltOnFailure=True, maxTime=1200, timeout=1200, name="build Ubuntu 14.04 (trusty)"))
# 19.10 does currently not build for an OBS-internal reason factory_obs_pkg_ci.addStep(ShellCommand(command=["bash", "-c", 'cd _OBS/pkg_obs-clone/rsyslog ; osc build --trust-all-projects --local-package xUbuntu_19.10 x86_64'], haltOnFailure=True, maxTime=1200, timeout=1200, name="build Ubuntu 19.10 (eoan)"))

lc['builders'].append(
   BuilderConfig(name="rsyslog obs_pkg_ci",
     workernames=["docker-suse-obs"],
      factory=factory_obs_pkg_ci,
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog-pkg-ubuntu",
      },
    ))

lc['schedulers'].append(ForceScheduler(
	name="pull_rsyslog_rsyslog-pkg-ubuntu", # name is "fixed": pull_<org>_<project>
	label="PR scheduler for obs_pkg_ci",
	builderNames=[ "rsyslog obs_pkg_ci"],
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
	name="forceall_rsyslog_obs_pkg_ci",
	label="2. Force All-rsyslog_obs_pkg_ci",
	builderNames=[ "rsyslog obs_pkg_ci" ] ))

lc['schedulers'].append(SingleBranchScheduler(
	name="github_rsyslog_obs_pkg_ci",
	change_filter=filter.ChangeFilter(	category="pull", 
						project="rsyslog/rsyslog-pkg-ubuntu"),
	builderNames=[ "rsyslog obs_pkg_ci"] ))

