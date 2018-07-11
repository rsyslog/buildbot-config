#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 	* Copyright (C) 2013 Adiscon GmbH.
#	* This file is part of RSyslog
#	* 
#	* rsyslog factory settings
#	*

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.git import Git
from buildbot.steps.shell import ShellCommand
from buildbot.steps.shell import Configure 

# --- liblogging factory settings
factoryLiblogging= BuildFactory()
factoryLiblogging.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLiblogging.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLiblogging.addStep(ShellCommand(command=["./configure", "--prefix=/usr"], logfiles={"config.log": "config.log"}))
factoryLiblogging.addStep(ShellCommand(command=["make"]))
factoryLiblogging.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

factoryLibloggingDebian= BuildFactory()
factoryLibloggingDebian.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibloggingDebian.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibloggingDebian.addStep(ShellCommand(command=["./configure", "--prefix=/usr"], logfiles={"config.log": "config.log"}))
factoryLibloggingDebian.addStep(ShellCommand(command=["make"]))
factoryLibloggingDebian.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

# SOLARIS
factoryLibloggingSolaris = BuildFactory()
factoryLibloggingSolaris.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibloggingSolaris.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], env=solarisenv_gcc))
factoryLibloggingSolaris.addStep(ShellCommand(command=["./configure", "--prefix=/usr"], env=solarisenv_gcc, logfiles={"config.log": "config.log"}))
factoryLibloggingSolaris.addStep(ShellCommand(command=["gmake", "V=0"], env=solarisenv_gcc))
factoryLibloggingSolaris.addStep(ShellCommand(command=["gmake", "check", "V=0"], env=solarisenv_gcc, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# we now try different compilers. Here, we restrict ourselfs to just the
# build step in order to save ressources and time.
# GCC
factoryLibloggingSolaris.addStep(ShellCommand(command=["gmake", "clean"], env=solarisenv_gcc))
factoryLibloggingSolaris.addStep(ShellCommand(command=["./configure", "--prefix=/usr", 'CC=/opt/csw/bin/gcc'], env=solarisenv_gcc, logfiles={"config.log": "config.log"}, name="GCC configure"))
factoryLibloggingSolaris.addStep(ShellCommand(command=["gmake", "V=0"], env=solarisenv_gcc))

# BSD
factoryLibloggingFreeBsd = BuildFactory()
factoryLibloggingFreeBsd.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibloggingFreeBsd.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibloggingFreeBsd.addStep(ShellCommand(command=["./configure", "--prefix=/usr"], logfiles={"config.log": "config.log"}))
factoryLibloggingFreeBsd.addStep(ShellCommand(command=["make", "V=0"]))
factoryLibloggingFreeBsd.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# ---

#Add libfastjson builders for main repo
appendBuilders( 'rsyslog', 'liblogging',
		factoryLibloggingDebian,	# Debian 
		factoryLiblogging,		# Debian9
		factoryLiblogging,		# Raspbian 
		factoryLibloggingFreeBsd,	# Freebsd 
		factoryLiblogging,		# Suse 
		factoryLiblogging,		# Centos6
		factoryLiblogging,		# Centos7
		factoryLiblogging,		# Fedora23
		factoryLiblogging,		# Fedora64
		factoryLiblogging,		# Ubuntu
		factoryLiblogging,		# Ubuntu16
		factoryLibloggingSolaris,	# Solaris10x64
		factoryLibloggingSolaris,	# Solaris10sparc
		factoryLibloggingSolaris,	# Solaris11x64
		factoryLibloggingSolaris,	# Solaris11sparc
		factoryLiblogging,		# UbuntuCron
		factoryLiblogging,		# DockerUbuntu
		factoryLiblogging,		# DockerUbuntu18
		factoryLiblogging,		# DockerUbuntu18on16
		factoryLiblogging		# DockerCentos7
		)
