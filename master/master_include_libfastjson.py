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

# --- libfastjson factory settings
factoryLibFastJson = BuildFactory()
factoryLibFastJson.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibFastJson.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibFastJson.addStep(ShellCommand(command=["./configure", "--enable-performance-testbench"], logfiles={"config.log": "config.log"}))
factoryLibFastJson.addStep(ShellCommand(command=["make"]))
factoryLibFastJson.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

factoryLibFastJsonFedora23 = BuildFactory()
factoryLibFastJsonFedora23.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibFastJsonFedora23.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibFastJsonFedora23.addStep(ShellCommand(command=["./configure"], logfiles={"config.log": "config.log"}))
factoryLibFastJsonFedora23.addStep(ShellCommand(command=["make"]))
factoryLibFastJsonFedora23.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

factoryLibFastJsonFedora64 = BuildFactory()
factoryLibFastJsonFedora64.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibFastJsonFedora64.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibFastJsonFedora64.addStep(ShellCommand(command=["./configure"], logfiles={"config.log": "config.log"}))
factoryLibFastJsonFedora64.addStep(ShellCommand(command=["make"]))
factoryLibFastJsonFedora64.addStep(ShellCommand(command=["make", "check", "V=0"], lazylogfiles=True, logfiles={"test-suite.log": "tests/test-suite.log"}, maxTime=3600))
factoryLibFastJsonFedora64.addStep(ShellCommand(command=["bash", "-c", "if [ -f CI/try_merge.sh ] ; then CI/try_merge.sh ; fi"], lazylogfiles=True, logfiles={"test-suite.log": "tests/test-suite.log"}))

# SOLARIS
factoryLibFastJsonSolaris = BuildFactory()
factoryLibFastJsonSolaris.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibFastJsonSolaris.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio))
factoryLibFastJsonSolaris.addStep(ShellCommand(command=["./configure", "--prefix=/usr"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}))
factoryLibFastJsonSolaris.addStep(ShellCommand(command=["gmake", "V=0"], env=solarisenv_sunstudio))
factoryLibFastJsonSolaris.addStep(ShellCommand(command=["gmake", "check", "V=0"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# we now try different compilers. Here, we restrict ourselfs to just the
# build step in order to save ressources and time.
# GCC
factoryLibFastJsonSolaris.addStep(ShellCommand(command=["gmake", "clean"], env=solarisenv_sunstudio))
factoryLibFastJsonSolaris.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_gcc))
factoryLibFastJsonSolaris.addStep(ShellCommand(command=["./configure", "--prefix=/usr", ], env=solarisenv_gcc, logfiles={"config.log": "config.log"}, name="GCC configure"))
factoryLibFastJsonSolaris.addStep(ShellCommand(command=["gmake", "V=0"], env=solarisenv_gcc))

# FREEBSD
factoryLibFastJsonFreeBsd = BuildFactory()
factoryLibFastJsonFreeBsd.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibFastJsonFreeBsd.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibFastJsonFreeBsd.addStep(ShellCommand(command=["./configure", "--prefix=/usr"], logfiles={"config.log": "config.log"}))
factoryLibFastJsonFreeBsd.addStep(ShellCommand(command=["make"]))
factoryLibFastJsonFreeBsd.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# ---

#Add libfastjson builders for main repo
appendBuilders( 'rsyslog', 'libfastjson',
		factoryLibFastJson,		# Debian 
		factoryLibFastJson,		# Debian9
		factoryLibFastJson,		# Raspbian 
		factoryLibFastJsonFreeBsd,	# Freebsd 
		factoryLibFastJson,		# Suse 
		factoryLibFastJson,		# Centos6
		factoryLibFastJson,		# Centos7
		factoryLibFastJsonFedora23,	# Fedora23
		factoryLibFastJsonFedora64,	# Fedora64
		factoryLibFastJson,		# Ubuntu
		factoryLibFastJson,		# Ubuntu16
		factoryLibFastJsonSolaris,	# Solaris10x64
		factoryLibFastJsonSolaris,	# Solaris10sparc
		factoryLibFastJsonSolaris,	# Solaris11x64
		factoryLibFastJsonSolaris,	# Solaris11sparc
		factoryLibFastJson,		# UbuntuCron
		factoryLibFastJson,		# DockerUbuntu
		factoryLibFastJson,		# DockerUbuntu18
		factoryLibFastJson,		# DockerUbuntu18on18
		factoryLibFastJson		# DockerCentos7
		)

