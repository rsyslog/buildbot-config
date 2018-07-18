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
factoryLibrelp.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], name="autoreconf", description="autoreconf running", descriptionDone="autoreconf done"))
factoryLibrelp.addStep(ShellCommand(command=["./configure", "--prefix=/usr", "--enable-tls-openssl"], name="configure", description="configure running", descriptionDone="configure done", logfiles={"config.log": "config.log"}))
factoryLibrelp.addStep(ShellCommand(command=["make"]))
factoryLibrelp.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# ---

# --- Solaris
factoryLibrelpSolaris= BuildFactory()
factoryLibrelpSolaris.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelpSolaris.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio))
factoryLibrelpSolaris.addStep(ShellCommand(command=["./configure", "V=0", "--enable-tls-openssl"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}))
factoryLibrelpSolaris.addStep(ShellCommand(command=["make"], env=solarisenv_sunstudio))
factoryLibrelpSolaris.addStep(ShellCommand(command=["make", "check", "V=0"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# ---

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

