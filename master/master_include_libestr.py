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

from master_includes import appendSchedulers
from master_includes import appendBuilders

# --- libestr factory settings
factoryLibestr= BuildFactory()
factoryLibestr.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibestr.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibestr.addStep(ShellCommand(command=["./configure", "--prefix=/usr"], logfiles={"config.log": "config.log"}))
factoryLibestr.addStep(ShellCommand(command=["make"]))
factoryLibestr.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# ---

# --- libestr factory settings
factoryLibestrSolaris= BuildFactory()
factoryLibestrSolaris.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibestrSolaris.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], env=solarisenv_gcc))
factoryLibestrSolaris.addStep(ShellCommand(command=["./configure", "--prefix=/usr", 'CC=/opt/solarisstudio12.4/bin/cc'], env=solarisenv_gcc, logfiles={"config.log": "config.log"}))
factoryLibestrSolaris.addStep(ShellCommand(command=["gmake", "V=0"], env=solarisenv_gcc))
factoryLibestrSolaris.addStep(ShellCommand(command=["gmake", "check", "V=0"], env=solarisenv_gcc, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# we now try different compilers. Here, we restrict ourselfs to just the
# build step in order to save ressources and time.
# GCC
factoryLibestrSolaris.addStep(ShellCommand(command=["gmake", "clean"], env=solarisenv_gcc))
factoryLibestrSolaris.addStep(ShellCommand(command=["./configure", "--prefix=/usr", 'CC=/opt/csw/bin/gcc'], env=solarisenv_gcc, logfiles={"config.log": "config.log"}, name="GCC configure"))
factoryLibestrSolaris.addStep(ShellCommand(command=["gmake", "V=0"], env=solarisenv_gcc))

#Add libfastjson builders for main repo
appendBuilders( lc, 'rsyslog', 'libestr',
		factoryLibestr,		# Debian 
		factoryLibestr,		# Debian 9
		factoryLibestr,		# Raspbian 
		factoryLibestr,		# Freebsd 
		factoryLibestr,		# Suse 
		factoryLibestr,		# Centos6
		factoryLibestr,		# Centos7
		factoryLibestr,		# Fedora23
		factoryLibestr,		# Fedora64
		factoryLibestr,		# Ubuntu
		factoryLibestr,		# Ubuntu16
		factoryLibestrSolaris,	# Solaris10x64
		factoryLibestrSolaris,	# Solaris10sparc
		factoryLibestrSolaris,	# Solaris11x64
		factoryLibestrSolaris,	# Solaris11sparc
		factoryLibestr,		# UbuntuCron
		factoryLibestr,		# DockerUbuntu
		factoryLibestr,		# DockerUbuntu18
		factoryLibestr,		# DockerUbuntu18on16
		factoryLibestr		# DockerCentos7
		)
