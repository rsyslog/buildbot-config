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

# standard build steps
librelp_make_check=ShellCommand(command=["make", "check", "VERBOSE=1"], env={'UNDER_CI':'YES'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, timeout=300, name="distcheck (gtls only)")
librelp_gather_check_logs=ShellCommand(command=["bash", "-c", "ls -l tests; find . -name '*.log'; cat $(find $(find . -name tests) -name \"*.log\" ! -name \"librelp*\"); exit 0"], haltOnFailure=False, name="gather individual test logs")

# --- librelp default factory settings
factoryLibrelp= BuildFactory()
factoryLibrelp.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelp.addStep(ShellCommand(command=["bash", "-c", "ps aux|grep receive; killall lt-receive; ps aux|grep receive; exit 0"], name="process cleanup"))
factoryLibrelp.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], name="autoreconf", description="autoreconf running", descriptionDone="autoreconf done"))
# NO tls
factoryLibrelp.addStep(ShellCommand(command=["./configure", "--disable-tls", "--disable-tls-openssl"], name="configure (no tls)", logfiles={"config.log": "config.log"}))
factoryLibrelp.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp.addStep(librelp_make_check)
factoryLibrelp.addStep(librelp_gather_check_logs)
# gtls
factoryLibrelp.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next test"))
factoryLibrelp.addStep(ShellCommand(command=["./configure", "--enable-tls", "--disable-tls-openssl"], name="configure (gtls only)", logfiles={"config.log": "config.log"}))
factoryLibrelp.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp.addStep(librelp_make_check)
factoryLibrelp.addStep(librelp_gather_check_logs)
# openssl
factoryLibrelp.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next test"))
factoryLibrelp.addStep(ShellCommand(command=["./configure", "--disable-tls", "--enable-tls-openssl"], name="configure (ossl only)", logfiles={"config.log": "config.log"}))
factoryLibrelp.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp.addStep(librelp_make_check)
factoryLibrelp.addStep(librelp_gather_check_logs)
# both
factoryLibrelp.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next test"))
factoryLibrelp.addStep(ShellCommand(command=["./configure", "--enable-tls", "--enable-tls-openssl"], name="configure (both)", logfiles={"config.log": "config.log"}))
factoryLibrelp.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp.addStep(librelp_make_check)
factoryLibrelp.addStep(librelp_gather_check_logs)
# ---

# --- librelp no valgrind
factoryLibrelp_no_valgrind= BuildFactory()
factoryLibrelp_no_valgrind.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["bash", "-c", "ps aux|grep receive; killall lt-receive; ps aux|grep receive; exit 0"], name="process cleanup"))
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], name="autoreconf", description="autoreconf running", descriptionDone="autoreconf done"))
# NO tls
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["./configure", "--disable-tls", "--disable-tls-openssl", "--disable-valgrind"], logfiles={"config.log": "config.log"}, name="configure (no TLS)"))
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp_no_valgrind.addStep(librelp_make_check)
factoryLibrelp_no_valgrind.addStep(librelp_gather_check_logs)
# gtls
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next test"))
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["./configure", "--enable-tls", "--disable-tls-openssl", "--disable-valgrind"], logfiles={"config.log": "config.log"}, name="configure (gtls only)"))
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp_no_valgrind.addStep(librelp_make_check)
factoryLibrelp_no_valgrind.addStep(librelp_gather_check_logs)
# openssl
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next test"))
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["./configure", "--disable-tls", "--enable-tls-openssl", "--disable-valgrind"], logfiles={"config.log": "config.log"}, name="configure (ossl only)"))
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp_no_valgrind.addStep(librelp_make_check)
factoryLibrelp_no_valgrind.addStep(librelp_gather_check_logs)
# both
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next test"))
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["./configure", "--enable-tls", "--enable-tls-openssl", "--disable-valgrind"], name="configure (both)", logfiles={"config.log": "config.log"}))
factoryLibrelp_no_valgrind.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp_no_valgrind.addStep(librelp_make_check)
factoryLibrelp_no_valgrind.addStep(librelp_gather_check_logs)
# ---

# --- librelp ASAN
factoryLibrelp_asan_ubsan= BuildFactory()
factoryLibrelp_asan_ubsan.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["bash", "-c", "ps aux|grep receive; killall lt-receive; ps aux|grep receive; exit 0"], name="process cleanup"))
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], name="autoreconf", description="autoreconf running", descriptionDone="autoreconf done"))
# NO tls
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["./configure", "--disable-tls", "--disable-tls-openssl", "--disable-valgrind"], env={'CC':'clang', 'CFLAGS':'-g -O0 -fsanitize=address,undefined'}, name="configure (no tls)", logfiles={"config.log": "config.log"}))
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp_asan_ubsan.addStep(librelp_make_check)
factoryLibrelp_asan_ubsan.addStep(librelp_gather_check_logs)
# gtls
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next test"))
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["./configure", "--enable-tls", "--disable-tls-openssl", "--disable-valgrind"], env={'CC':'clang', 'CFLAGS':'-g -O0 -fsanitize=address,undefined'}, name="configure (gtls only)", logfiles={"config.log": "config.log"}))
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp_asan_ubsan.addStep(librelp_make_check)
factoryLibrelp_asan_ubsan.addStep(librelp_gather_check_logs)
# openssl
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next test"))
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["./configure", "--disable-tls", "--enable-tls-openssl", "--disable-valgrind"], env={'CC':'clang', 'CFLAGS':'-g -O0 -fsanitize=address,undefined'}, name="configure (ossl only)", logfiles={"config.log": "config.log"}))
factoryLibrelp_asan_ubsan.addStep(ShellCommand(command=["make"], name="make"))
factoryLibrelp_asan_ubsan.addStep(librelp_make_check)
factoryLibrelp_asan_ubsan.addStep(librelp_gather_check_logs)
# ---


# --- Solaris
factoryLibrelpFreebsd= BuildFactory()
factoryLibrelpFreebsd.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelpFreebsd.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio))
factoryLibrelpFreebsd.addStep(ShellCommand(command=["./configure", "V=0"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}))
factoryLibrelpFreebsd.addStep(ShellCommand(command=["make"], env=solarisenv_sunstudio))
factoryLibrelpFreebsd.addStep(ShellCommand(command=["make", "check", "V=0"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=600))
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

# build-only check: gcc8
factoryLibrelpDockerBuild_gcc8 = BuildFactory()
factoryLibrelpDockerBuild_gcc8.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelpDockerBuild_gcc8.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryLibrelpDockerBuild_gcc8.addStep(ShellCommand(command=["./configure", "--enable-tls", "--enable-tls-openssl"], env={'CC': 'gcc-8', "CFLAGS":"-pedantic"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure"))
factoryLibrelpDockerBuild_gcc8.addStep(ShellCommand(command=["make", "-j4"], maxTime=1000, name="make"))
factoryLibrelpDockerBuild_gcc8.addStep(ShellCommand(command=["make", "check", "TESTS="], maxTime=500, name="make testbench tools"))

# CodeCov PR integration
factoryLibrelpDockerUbuntu18_codecov = BuildFactory()
factoryLibrelpDockerUbuntu18_codecov.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryLibrelp.addStep(ShellCommand(command=["bash", "-c", "ps aux|grep receive; killall lt-receive; ps aux|grep receive; exit 0"], name="process cleanup"))
factoryLibrelpDockerUbuntu18_codecov.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryLibrelpDockerUbuntu18_codecov.addStep(ShellCommand(command=["bash", "-c", "./configure --enable-tls --enable-tls-openssl"], env={'CC': 'gcc', "CFLAGS":"-g -O0 --coverage", "LDFLAGS":"-lgcov"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc, coverage)"))
factoryLibrelpDockerUbuntu18_codecov.addStep(ShellCommand(command=["make", "check", "V=0"], env={'UNDER_CI':'YES'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=1800, haltOnFailure=False, name="check"))
factoryLibrelpDockerUbuntu18_codecov.addStep(ShellCommand(command=["bash", "-c", "curl -s https://codecov.io/bash >codecov.sh; chmod +x codecov.sh; ./codecov.sh -t" + secret_CODECOV_TOKEN_LIBRELP + " -n\"librelp buildbot PR\"; rm codecov.sh; find . -name '*.gcov' || exit 0"], env={'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, name="CodeCov upload"))


#Add libfastjson builders for main repo
appendBuilders( 'rsyslog', 'librelp',
		factoryLibrelp,		# Debian 
		factoryLibrelp,		# Debian9
		factoryLibrelp_no_valgrind,	# Raspbian 
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
		factoryLibrelp_asan_ubsan,	# DockerUbuntu18
		factoryLibrelp,		# DockerUbuntu18on16
		factoryLibrelp,		# DockerCentos7
		)

lc['builders'].append(
   BuilderConfig(name="librelp koobs freebsd",
     workernames=[  "koobs-freebsd-current" ],
      factory=factoryLibrelpFreebsd,
      tags=["librelp", "vm"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "librelp",
      },
    ))
lc['builders'].append(
   BuilderConfig(name="librelp build gcc-8",
     workernames=[  "docker-ubuntu18-buildtests-w1"
		  , "docker-ubuntu18-buildtests-w2"],
      factory=factoryLibrelpDockerBuild_gcc8,
      tags=["librelp", "docker"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "librelp",
      },
    ))
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
	builderNames=[	"librelp codecov"
		      , "librelp koobs freebsd"
		      , "librelp build gcc-8"]
))
lc['schedulers'].append(ForceScheduler(
	name="forceall-librelp",
	builderNames=[	"librelp codecov"
		      , "librelp koobs freebsd"
		      , "librelp build gcc-8"]
))

# build master commits so that CodeCov has references for all commits
lc['schedulers'].append(schedulers.SingleBranchScheduler(name='librelp-master-sched',
	change_filter=util.ChangeFilter(project='rsyslog/librelp', branch='master'),
	treeStableTimer=30, # otherwise a PR merge with n commits my start n builders
	builderNames=["librelp codecov"]
	))

