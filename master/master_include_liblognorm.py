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

# --- liblognorm factory settings
factoryLibLogNorm = BuildFactory()
factoryLibLogNorm.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
#factoryLibLogNorm.addStep(Git(repourl='git://github.com/rsyslog/liblognorm.git', mode='full'))
factoryLibLogNorm.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibLogNorm.addStep(ShellCommand(command=["./configure", "--prefix=/usr", "--enable-regexp", "--enable-valgrind"], logfiles={"config.log": "config.log"}))
factoryLibLogNorm.addStep(ShellCommand(command=["make", "-j"]))
factoryLibLogNorm.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True))
factoryLibLogNorm.addStep(ShellCommand(command=["make", "distcheck", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

factoryLibLogNormSolaris = BuildFactory()
factoryLibLogNormSolaris.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
#factoryLibLogNormSolaris.addStep(Git(repourl='git://github.com/rsyslog/liblognorm.git', mode='full'))
factoryLibLogNormSolaris.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], env=solarisenv_gcc))
factoryLibLogNormSolaris.addStep(ShellCommand(command=["./configure", "--enable-regexp", "--enable-compile-warnings=no", 'CC=/opt/solarisstudio12.4/bin/cc'], env=solarisenv_gcc, logfiles={"config.log": "config.log"}))
factoryLibLogNormSolaris.addStep(ShellCommand(command=["gmake", "V=0"], env=solarisenv_gcc))
# DOES CURRENTLY NOT WORK! factoryLibLogNormSolaris.addStep(ShellCommand(command=["gmake", "check", "V=1"], env=solarisenv_gcc, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
#currently does not work due to env var factoryLibLogNormSolaris.addStep(ShellCommand(command=["gmake", "distcheck", "V=1"]))
# we now try different compilers. Here, we restrict ourselfs to just the
# build step in order to save ressources and time.
# GCC
factoryLibLogNormSolaris.addStep(ShellCommand(command=["gmake", "clean"], env=solarisenv_gcc))
factoryLibLogNormSolaris.addStep(ShellCommand(command=["./configure", "--prefix=/usr", 'CC=/opt/csw/bin/gcc'], env=solarisenv_gcc, logfiles={"config.log": "config.log"}))
factoryLibLogNormSolaris.addStep(ShellCommand(command=["gmake", "V=0"], env=solarisenv_gcc))

factoryLibLogNormFedora23 = BuildFactory()
factoryLibLogNormFedora23.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibLogNormFedora23.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibLogNormFedora23.addStep(ShellCommand(command=["./configure", "--prefix=/usr", "--enable-regexp", "--enable-valgrind"], env={'PKG_CONFIG_PATH':'/usr/local/lib/pkgconfig'}, logfiles={"config.log": "config.log"}))
factoryLibLogNormFedora23.addStep(ShellCommand(command=["make", "-j"]))
factoryLibLogNormFedora23.addStep(ShellCommand(command=["make", "check", "V=0"]))
factoryLibLogNormFedora23.addStep(ShellCommand(command=["make", "distcheck", "V=0"], env={'PKG_CONFIG_PATH':'/usr/local/lib/pkgconfig'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

factoryLibLogNormFedora64 = BuildFactory()
factoryLibLogNormFedora64.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibLogNormFedora64.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibLogNormFedora64.addStep(ShellCommand(command=["./configure", "--enable-regexp", "--enable-valgrind"], env={'PKG_CONFIG_PATH':'/usr/local/lib/pkgconfig'}, logfiles={"config.log": "config.log"}))
factoryLibLogNormFedora64.addStep(ShellCommand(command=["make", "-j2"]))
factoryLibLogNormFedora64.addStep(ShellCommand(command=["make", "check", "V=0"]))
factoryLibLogNormFedora64.addStep(ShellCommand(command=["make", "distcheck", "V=0"], env={'PKG_CONFIG_PATH':'/usr/local/lib/pkgconfig'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

factoryLibLogNormFreeBsd = BuildFactory()
factoryLibLogNormFreeBsd.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibLogNormFreeBsd.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibLogNormFreeBsd.addStep(ShellCommand(command=["./configure", "--prefix=/usr", "--enable-regexp"], env={}, logfiles={"config.log": "config.log"}))
factoryLibLogNormFreeBsd.addStep(ShellCommand(command=["make"]))
factoryLibLogNormFreeBsd.addStep(ShellCommand(command=["make", "check", "V=0"]))
factoryLibLogNormFreeBsd.addStep(ShellCommand(command=["make", "distcheck", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

factoryLibLogNormRaspian = BuildFactory()
factoryLibLogNormRaspian.addStep(Git(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibLogNormRaspian.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryLibLogNormRaspian.addStep(ShellCommand(command=["./configure", "--prefix=/usr", "--disable-valgrind", "--enable-regexp"], logfiles={"config.log": "config.log"}))
factoryLibLogNormRaspian.addStep(ShellCommand(command=["make", "-j2"]))
factoryLibLogNormRaspian.addStep(ShellCommand(command=["make", "check", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True))
factoryLibLogNormRaspian.addStep(ShellCommand(command=["make", "distcheck", "V=0"], logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
# ---

#Add liblognorm builders for main repo
appendBuilders(	'rsyslog', 'liblognorm', 
		factoryLibLogNorm,		# Debian 
		factoryLibLogNorm,		# Debian9
		factoryLibLogNormRaspian,	# Raspbian 
		factoryLibLogNormFreeBsd,	# Freebsd 
		factoryLibLogNorm,		# Suse 
		factoryLibLogNorm,		# Centos6
		factoryLibLogNorm, 		# Centos7
		factoryLibLogNormFedora23,	# Fedora23
		factoryLibLogNormFedora64,	# Fedora64
		factoryLibLogNorm, 		# Ubuntu
		factoryLibLogNorm, 		# Ubuntu16
		factoryLibLogNormSolaris,	# Solaris10x64
		factoryLibLogNormSolaris,	# Solaris10sparc
		factoryLibLogNormSolaris,	# Solaris11x64
		factoryLibLogNormSolaris,	# Solaris11sparc
		factoryLibLogNorm,		# UbuntuCron
		factoryLibLogNorm,		# DockerUbuntu
		factoryLibLogNorm,		# DockerUbuntu18
		factoryLibLogNorm,		# DockerUbuntu18on16
		factoryLibLogNorm		# DockerCentos7
		)
