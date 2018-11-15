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

# --- librelp factory settings
factoryLibrelp= BuildFactory()
factoryLibrelp.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelp.addStep(ShellCommand(command=["bash", "-c", "ps aux|grep receive; killall lt-receive; ps aux|grep receive; exit 0"], name="process cleanup"))
factoryLibrelp.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], name="autoreconf", description="autoreconf running", descriptionDone="autoreconf done"))
#factoryLibrelp.addStep(ShellCommand(command=["./configure", "--prefix=/usr", "--enable-tls-openssl"], name="configure", description="configure running", descriptionDone="configure done", logfiles={"config.log": "config.log"}))
factoryLibrelp.addStep(ShellCommand(command=["./configure", "--enable-tls"], name="configure", description="configure running", descriptionDone="configure done", logfiles={"config.log": "config.log"}))
#factoryLibrelp.addStep(ShellCommand(command=["make"]))
factoryLibrelp.addStep(ShellCommand(command=["make", "distcheck", "VERBOSE=1"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# ---

# --- Solaris
factoryLibrelpSolaris= BuildFactory()
factoryLibrelpSolaris.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelpSolaris.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio))
factoryLibrelpSolaris.addStep(ShellCommand(command=["./configure", "V=0"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}))
#factoryLibrelpSolaris.addStep(ShellCommand(command=["./configure", "V=0", "--enable-tls-openssl"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}))
factoryLibrelpSolaris.addStep(ShellCommand(command=["make"], env=solarisenv_sunstudio))
factoryLibrelpSolaris.addStep(ShellCommand(command=["make", "check", "V=0"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# ---

# CodeCov PR integration
factoryLibrelpDockerUbuntu18_codecov = BuildFactory()
factoryLibrelpDockerUbuntu18_codecov.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelp.addStep(ShellCommand(command=["bash", "-c", "ps aux|grep receive; killall lt-receive; ps aux|grep receive; exit 0"], name="process cleanup"))
factoryLibrelpDockerUbuntu18_codecov.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryLibrelpDockerUbuntu18_codecov.addStep(ShellCommand(command=["bash", "-c", "./configure --enable-tls"], env={'CC': 'gcc', "CFLAGS":"-g -O0 --coverage", "LDFLAGS":"-lgcov"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc, coverage)"))
factoryLibrelpDockerUbuntu18_codecov.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=1800, haltOnFailure=False, name="check"))
factoryLibrelpDockerUbuntu18_codecov.addStep(ShellCommand(command=["bash", "-c", "curl -s https://codecov.io/bash >codecov.sh; chmod +x codecov.sh; ./codecov.sh -t" + secret_CODECOV_TOKEN_LIBRELP + " -n\"librelp buildbot PR\"; rm codecov.sh; find . -name '*.gcov' || exit 0"], env={'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, name="CodeCov upload"))


#Add libfastjson builders for main repo
appendBuilders( 'rsyslog', 'librelp',
		factoryLibrelp,		# Debian 
		factoryLibrelp,		# Debian9
		factoryLibrelp,		# Raspbian 
		factoryLibrelp,		# Freebsd 
		factoryLibrelp,		# Suse 
		factoryLibrelp,		# Centos6
		factoryLibrelp,		# Centos7
		factoryLibrelp,		# Fedora23
		factoryLibrelp,		# Fedora64
		factoryLibrelp,		# Ubuntu
		factoryLibrelp,		# Ubuntu16
		factoryLibrelpSolaris,	# Solaris10x64
		factoryLibrelpSolaris,	# Solaris10sparc
		factoryLibrelpSolaris,	# Solaris11x64
		factoryLibrelpSolaris,	# Solaris11sparc
		factoryLibrelp,		# UbuntuCron
		factoryLibrelp,		# DockerUbuntu
		factoryLibrelp,		# DockerUbuntu18
		factoryLibrelp,		# DockerUbuntu18on16
		factoryLibrelp,		# DockerCentos7
		)

lc['builders'].append(
   BuilderConfig(name="librelp codecov",
     workernames=["docker-ubuntu18-codecov-w4"],
      factory=factoryLibrelpDockerUbuntu18_codecov,
      tags=["librelp", "docker", "codecov"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "librelp",
      },
    ))

lc['schedulers'].append(SingleBranchScheduler(
	name="github_librelp",
	change_filter=filter.ChangeFilter(	category="pull", 
						project="rsyslog/librelp"),
	builderNames=[	"librelp codecov"]
))
lc['schedulers'].append(ForceScheduler(
	name="forceall-librelp",
	builderNames=[	"librelp codecov"]
))

# build master commits so that CodeCov has references for all commits
lc['schedulers'].append(schedulers.SingleBranchScheduler(name='librelp-master-sched',
	change_filter=util.ChangeFilter(project='rsyslog/rsyslog', branch='master'),
	treeStableTimer=30, # otherwise a PR merge with n commits my start n builders
	builderNames=["librelp codecov"]
	# TODO: replace with this value: builderNames=["master rsyslog"],
	))

