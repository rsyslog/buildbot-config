#! /usr/bin/env python
#      * Copyright (C) 2018 Adiscon GmbH.
#      * This file is part of RSyslog
#      * 
#      * rsyslog factory settings
#      *
#
# Note: solarisenv_gcc, solarisenv_sunstudio etc and some other
# standard values are set in master.cfg

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.github import GitHub
from buildbot.steps.source.git import Git
from buildbot.steps.shell import ShellCommand
from buildbot.steps.shell import Configure 

from buildbot.plugins import schedulers, util
from buildbot.config import BuilderConfig
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler
from buildbot.changes import filter

#some globals

# Note: small workers are to be used for -j1 check runs only; they should be
# reserved to checks known not to support concurrency due to time-sensitivy
# as well as Centos6, which does not support parallel builds.
generic_small_workers=['generic-s1', 'generic-s2','generic-s3']
generic_workers=['generic-w1', 'generic-w2', 'generic-w3', 'generic-w4', 'generic-w5', 'generic-w6']
generic_logfiles={'failed-tests.log': 'failed-tests.log',
          "test-suite.log": "tests/test-suite.log",
          "config.log": "config.log"
}
#docker_workers=["docker-ubuntu18-w1", "docker-ubuntu18", "docker-s1-ubuntu18", "docker-ubuntu18-w6"]
docker_workers=["docker-ubuntu18-w6"]

docker_cleanup_step = ShellCommand(command=["bash", "-c",
	'docker ps; '
	'if [ "$(docker ps -q)" != "" ]; then '
	'    docker kill $(docker ps -q); '
	'else '
	'    echo no hanging docker instances; '
	'fi; '
	'if [ "$(docker ps -q -a)" != "" ]; then '
	'    docker rm $(docker ps -q -a); '
	'fi '
], haltOnFailure=True, name="cleanup left-over docker containers")



# --- rsyslog factory settings
factoryRsyslogCentos6 = BuildFactory()
Centos6 = BuildFactory()
factoryRsyslogCentos6.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogCentos6.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogCentos6.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryRsyslogCentos6.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-elasticsearch=no", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--disable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--disable-ax-compiler-flags"], env={'PKG_CONFIG_PATH': '/home/rger/localenv/lib/pkgconfig:/lib64/pkgconfig'}, logfiles={"config.log": "config.log"}))
#factoryRsyslogCentos6.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind"],  env={'PKG_CONFIG_PATH': '/lib64/pkgconfig:/home/rger/localenv/lib/pkgconfig'}, logfiles={"config.log": "config.log"}))
factoryRsyslogCentos6.addStep(ShellCommand(command=["make", "-j"]))
factoryRsyslogCentos6.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "RSYSLOG_DEBUG_TIMEOUTS_TO_STDERR": "on", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, name="make check"))


factoryRsyslogCentos7VM = BuildFactory()
factoryRsyslogCentos7VM.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogCentos7VM.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"]))
factoryRsyslogCentos7VM.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryRsyslogCentos7VM.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imdocker", "--enable-imdocker-tests", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-improg", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-omjournal", "--enable-libsystemd=yes", "--enable-mmkubernetes", "--enable-imjournal", "--enable-omkafka", "--enable-imkafka", "--enable-ommongodb=no", "--enable-omrabbitmq", "--enable-journal-tests", "--enable-mmdarwin", "--enable-compile-warnings=error", "--disable-helgrind"], env={'PKG_CONFIG_PATH': '/usr/local/lib/pkgconfig:/usr/lib64/pkgconfig',  'CC': 'gcc', "CFLAGS":"-g -O0 -coverage", "LDFLAGS":"-lgcov"}, logfiles={"config.log": "config.log"}))
factoryRsyslogCentos7VM.addStep(ShellCommand(command=["make", "-j"], haltOnFailure=True))
factoryRsyslogCentos7VM.addStep(ShellCommand(command=["make", "-j4", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername'), "CI_ENV":"Centos7VM"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000))
factoryRsyslogCentos7VM.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh"], name="gather check logs"))
factoryRsyslogCentos7VM.addStep(ShellCommand(command=["bash", "-c", "curl -s https://codecov.io/bash >codecov.sh; chmod +x codecov.sh; ./codecov.sh -t" + g['secret_CODECOV_TOKEN'] + " -n\"rsyslog buildbot PR\"; rm codecov.sh || exit 0"], env={'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, name="CodeCov upload"))

# Centos 7 for background jobs (codecov)
factoryRsyslogCentos7VM_bg = BuildFactory()
factoryRsyslogCentos7VM_bg.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogCentos7VM_bg.addStep(ShellCommand(command=["bash", "-c", "tests/CI/buildbot_cleanup.sh"]))
factoryRsyslogCentos7VM_bg.addStep(ShellCommand(command=["autoreconf", "-fvi"]))
factoryRsyslogCentos7VM_bg.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-elasticsearch", "--enable-elasticsearch-tests", "--enable-imdocker", "--enable-imdocker-tests", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-omjournal", "--enable-libsystemd=yes", "--enable-mmkubernetes", "--enable-imjournal", "--enable-omkafka", "--enable-imkafka", "--enable-ommongodb=no", "--enable-journal-tests", "--without-valgrind-testbench", "--enable-compile-warnings=error"], env={'PKG_CONFIG_PATH': '/usr/local/lib/pkgconfig:/usr/lib64/pkgconfig',  'CC': 'gcc', "CFLAGS":"-g -O0 -coverage", "LDFLAGS":"-lgcov"}, logfiles={"config.log": "config.log"}))
factoryRsyslogCentos7VM_bg.addStep(ShellCommand(command=["make", "-j"], haltOnFailure=True))
factoryRsyslogCentos7VM_bg.addStep(ShellCommand(command=["make", "-j2", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000))
factoryRsyslogCentos7VM_bg.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh"], name="gather check logs"))
factoryRsyslogCentos7VM_bg.addStep(ShellCommand(command=["bash", "-c", "curl -s https://codecov.io/bash >codecov.sh; chmod +x codecov.sh; ./codecov.sh -t" + g['secret_CODECOV_TOKEN'] + " -n\"rsyslog buildbot PR\"; rm codecov.sh || exit 0"], env={'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, name="CodeCov upload"))


factoryRsyslogDebian = BuildFactory()
factoryRsyslogDebian.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDebian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogDebian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"]))
factoryRsyslogDebian.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
# use clang!
factoryRsyslogDebian.addStep(ShellCommand(command=["./configure", "--prefix=/opt/rsyslog", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-omkafka=no", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--without-valgrind-testbench"], env={'CC': 'clang', "CFLAGS":"-g -fsanitize=address"}, logfiles={"config.log": "config.log"}))
factoryRsyslogDebian.addStep(ShellCommand(command=["make", "-j"], haltOnFailure=True))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
factoryRsyslogDebian.addStep(ShellCommand(command=["make", "-j4", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.5", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
factoryRsyslogDebian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather check logs"))

factoryRsyslogDebian9 = BuildFactory()
factoryRsyslogDebian9.addStep(ShellCommand(command=["sleep", "2"], name="wait for github"))
factoryRsyslogDebian9.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDebian9.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogDebian9.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"]))
factoryRsyslogDebian9.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], name="autoreconf"))
# use clang!
factoryRsyslogDebian9.addStep(ShellCommand(command=["./configure", "--prefix=/opt/rsyslog", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--enable-imdocker", "--disable-generate-man-pages", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--enable-omjournal", "--enable-imjournal", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-omkafka", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--enable-impcap", "--enable-mmcapture", "-enable-omhttp", "--enable-mmdarwin", "--without-valgrind-testbench", "--enable-compile-warnings=error"], env={'CC': 'clang', "CFLAGS":"-g -O2 -fsanitize=address"}, logfiles={"config.log": "config.log"}, name="configure"))
factoryRsyslogDebian9.addStep(ShellCommand(command=["make", "-j", "V=1"], name="make", haltOnFailure=True))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
factoryRsyslogDebian9.addStep(ShellCommand(command=["make", "-j2", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/lib/llvm-3.8/bin/llvm-symbolizer", 'LIBRARY_PATH': '/usr/local/lib', 'LD_LIBRARY_PATH': '/usr/local/lib', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=4600, name="make check"))
#factoryRsyslogDebian9.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"]))

factoryRsyslogRaspbian_gcc = BuildFactory()
factoryRsyslogRaspbian_gcc.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogRaspbian_gcc.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=raspbianenv_gcc, haltOnFailure=True))
factoryRsyslogRaspbian_gcc.addStep(ShellCommand(command=["./configure", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imdocker=no", "--enable-impcap", "--enable-mmcapture", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--enable-omrabbitmq", "--enable-mmdarwin", "--without-valgrind-testbench"], logfiles={"config.log": "config.log"}, env=raspbianenv_gcc, lazylogfiles=True, haltOnFailure=True, name="configure [gcc]"))
factoryRsyslogRaspbian_gcc.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True, name="make [gcc]"))

factoryRsyslogRaspbian_clang = BuildFactory() # raspbian = "original" Raspberry Pi
# NOTES:
# * NOW (2018-10) only used for compilation, so no cleanup needed. We leave
#   the info items in just in case we can use it in the future!
# * valgrind does not work on raspbian -- there are lots of errors in dlload()
#   subsystem before it finally aborts. Not worth wasting time on that...
#   rgerhards, 2017-12-08
# * do NOT run more than 2 parallel make jobs -- we have seen the compiler
#   fail with "internal error", which most probably means it ran out of
#   memory (this was with -j4 and seldomly, so -j2 should be a safe bet).
# * we do no longer run the testbench here as this is done on the new
#   arm docker device (and we can't scale here, so this really blocks CI)
# GCC compile commented out as we try it in a separate builder, to be run in parallel!
factoryRsyslogRaspbian_clang.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogRaspbian_clang.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=raspbianenv_gcc, haltOnFailure=True))
factoryRsyslogRaspbian_clang.addStep(ShellCommand(command=["./configure", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-impcap", "--enable-mmcapture", "--enable-imdocker=no", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--without-valgrind-testbench", "--enable-omrabbitmq", "--enable-mmdarwin", "--enable-compile-warnings=error"], logfiles={"config.log": "config.log"}, env={'CC':'clang', 'CFLAGS': '-g -O1', 'LC_ALL' : 'C', 'LIBRARY_PATH': '/usr/lib', 'LD_LIBRARY_PATH': '/usr/lib'}, lazylogfiles=True, haltOnFailure=True, name="configure [clang]"))
factoryRsyslogRaspbian_clang.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True, name="make [clang]"))



factoryRsyslogSuse = BuildFactory()
factoryRsyslogSuse.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogSuse.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogSuse.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryRsyslogSuse.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-debug", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--disable-libfaketime", "--enable-mmkubernetes", "--without-valgrind-testbench"], env={'CC': 'gcc', 'CFLAGS': '-g -fsanitize=address', 'PKG_CONFIG_PATH': '/usr/local/lib/pkgconfig'}, logfiles={"config.log": "config.log"}, haltOnFailure=True))
factoryRsyslogSuse.addStep(ShellCommand(command=["make", "-j8"], haltOnFailure=True))
factoryRsyslogSuse.addStep(ShellCommand(command=["make", "-j2", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', 'LD_LIBRARY_PATH': '/usr/local/lib', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=4000))
factoryRsyslogSuse.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather check logs"))

factoryRsyslogFreebsd = BuildFactory()
factoryRsyslogFreebsd.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogFreebsd.addStep(ShellCommand(command=["bash", "-c", "killall -v rsyslogd || exit 0"], name="cleanup via killall"))
# regular cleanup does not yet work on FreeBSD, as it uses different commands
#factoryRsyslogFreebsd.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"], name="cleanup"))
factoryRsyslogFreebsd.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"], name="autoreconf"))
# Note: current version of valgrind is full of false positives, so
# we cannot use valgrind here. :-/
factoryRsyslogFreebsd.addStep(ShellCommand(command=["./configure", "--disable-dependency-tracking", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-testbench", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--enable-snmp", "--enable-snmp-tests", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-pmnull", "--enable-valgrind", "--without-valgrind-testbench"], env={'PKG_CONFIG_PATH': '/usr/libdata/pkgconfig:/usr/local/lib/pkgconfig'}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure"))
factoryRsyslogFreebsd.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True, name="build"))
# add for testing:  mmexternal-SegFault-vg.sh mmexternal-SegFault.sh
factoryRsyslogFreebsd.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=2500, name="check"))
factoryRsyslogFreebsd.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather check logs"))

#factoryRsyslogUbuntu = BuildFactory()
#factoryRsyslogUbuntu.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"], name="cleanup old instances"))
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"]))
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["bash", "-c", "pwd; ls -l -tr tests/*.sh.log; ls -l tests/CI"]))
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"]))


factoryRsyslogUbuntu16 = BuildFactory()
factoryRsyslogUbuntu16.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["git", "log", "-4"], name="git branch information"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"], name="kill left-over instances"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["./configure", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-elasticsearch-tests=no", "--enable-elasticsearch", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmnull", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--enable-mmsnmptrapd", "--enable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-imczmq", "--enable-omczmq", "--enable-valgrind", "--enable-imjournal","--enable-omjournal", "--enable-imkafka", "--enable-omkafka", "--enable-kafka-tests=no", "--enable-ommongodb", "--enable-omhiredis", "--enable-gssapi-krb5", "--enable-ksi-ls12", "--enable-mmkubernetes", "--enable-debug", "--without-valgrind-testbench"], env={'CC': 'gcc-7', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc-7)"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["make", "-j2", "check", "TESTS=", "V=0"], env={"RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, haltOnFailure=True, name="make (gcc-7)"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next tests"))
# now compile plus dynamic testbench tests - do this last as it runs longest
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["./configure", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-elasticsearch-tests=no", "--enable-elasticsearch", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-imczmq", "--enable-omczmq", "--enable-valgrind", "--enable-imjournal","--enable-omjournal", "--enable-imkafka", "--enable-omkafka", "--enable-kafka-tests=no", "--enable-ommongodb", "--enable-omhiredis", "--enable-gssapi-krb5", "--enable-ksi-ls12", "--without-valgrind-testbench"], env={'CC': 'clang-4.0', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="build with clang-4.0"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["make", "-j2", "V=0"], haltOnFailure=True))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="cleanup dependencies"))

# Solaris all except unstable10s, which is so slow that the testbench
# gets into timing issues.
# Build steps are disabled because dependencies are not yet ready
factoryRsyslogSolaris10x64_sunstudio = BuildFactory()
# first step only in case git has aborted!
#	factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["rm", "-rf", "/export/home/buildbot-unstable10s/rsyslog/rsyslog_solaris10sparc_rsyslog/build/.git/index.lock"], env=solarisenv_gcc))
factoryRsyslogSolaris10x64_sunstudio.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["bash", "-c", "tests/CI/buildbot_cleanup.sh"], name="cleanup"))
# cleanup
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["df", "-h"], env=solarisenv_sunstudio))
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["rm", "-rf", "localenv"], env=solarisenv_sunstudio, name="cleanup dependencies"))
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["git", "log", "-4"], env=solarisenv_sunstudio, name="git branch information"))
# begin work
# we only comment out dependencies as we may need them again when newer
# versions appear than are packaged for Solaris
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librelp.sh"], env=solarisenv_sunstudio, name="building librelp dependency", descriptionDone="built librelp dependency"))
#factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_sunstudio, name="building libfastjson dependency", descriptionDone="built libfastjson dependency"))
#TESTING !!! factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librdkafka.sh"], env=solarisenv_sunstudio, name="building librdkafka dependency", descriptionDone="built librdkafka dependency"))
# begin "real" work
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio, name="autoreconf for SunStudio Compiler"))
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}))
#TESTING: , "--enable-imkafka", "--enable-omkafka", "--enable-kafka-tests=yes"
#	factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["cat", "configure"], env=solarisenv_sunstudio))
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["gmake", "-j6", "V=1"], env=solarisenv_sunstudio, name="build with SunStudio", haltOnFailure=True))
 
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["gmake", "-j2", "check", "V=0"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3000, timeout=1200, name="make check"))
factoryRsyslogSolaris10x64_sunstudio.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh", "tests/*.sh.log"], env=solarisenv_sunstudio, maxTime=3000, timeout=60, name="gathering make check logs", descriptionDone="gathered make check logs"))



# and now the same with GCC
factoryRsyslogSolaris10x64_gcc = BuildFactory()
# first step only in case git has aborted!
#	factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["rm", "-rf", "/export/home/buildbot-unstable10s/rsyslog/rsyslog_solaris10sparc_rsyslog/build/.git/index.lock"], env=solarisenv_gcc))
factoryRsyslogSolaris10x64_gcc.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogSolaris10x64_gcc.addStep(ShellCommand(command=["bash", "-c", "tests/CI/buildbot_cleanup.sh"], name="cleanup"))
# cleanup
factoryRsyslogSolaris10x64_gcc.addStep(ShellCommand(command=["rm", "-rf", "localenv"], env=solarisenv_gcc, name="cleanup dependencies"))
# begin work
# we only comment out dependencies as we may need them again when newer
# versions appear than are packaged for Solaris
factoryRsyslogSolaris10x64_gcc.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librelp.sh"], env=solarisenv_gcc, name="building librelp dependency", descriptionDone="built librelp dependency"))
#factoryRsyslogSolaris10x64_gcc.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_gcc, name="building libfastjson dependency", descriptionDone="built libfastjson dependency"))
# begin "real" work
factoryRsyslogSolaris10x64_gcc.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_gcc, name="autoreconf for gcc Compiler"))
factoryRsyslogSolaris10x64_gcc.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_gcc, logfiles={"config.log": "config.log"}, name="configure", haltOnFailure=True))
factoryRsyslogSolaris10x64_gcc.addStep(ShellCommand(command=["gmake", "-j", "V=1"], env=solarisenv_gcc, haltOnFailure=True))
# ---

# ---
factoryRsyslogSolaris11x64 = BuildFactory()
factoryRsyslogSolaris11x64.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
# cleanup
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["df", "-h"], env=solarisenv_sunstudio))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["bash", "-c", "tests/CI/buildbot_cleanup.sh"], name="cleanup"))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["rm", "-rf", "localenv"], env=solarisenv_sunstudio, name="cleanup dependencies"))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["git", "log", "-4"], env=solarisenv_sunstudio, name="git branch information"))
# begin work
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librelp.sh"], env=solarisenv_sunstudio, name="building librelp dependency", descriptionDone="built librelp dependency"))
# libfastjson currently not needed - maybe in the future again
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_sunstudio, name="building libfastjson dependency", descriptionDone="built libfastjson dependency"))
# begin "real" work
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio, name="autoreconf for SunStudio Compiler"))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["gmake", "-j", "V=0"], env=solarisenv_sunstudio, name="build with SunStudio", haltOnFailure=True))
# DISABLE if interactive testing is done on machine
#, "TESTS=imfile-readmode2.sh"
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["gmake", "-j2", "check", "V=0"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3000, timeout=1200))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh", "tests/*.sh.log"], env=solarisenv_sunstudio, maxTime=3000, timeout=60, name="gathering make check logs", descriptionDone="gathered make check logs"))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["df", "-h"], env=solarisenv_sunstudio))
# ---

# Solaris unstable10s, which is so slow that the testbench
# gets into timing issues.
# Build steps are disabled because dependencies are not yet ready
factoryRsyslogSolaris10sparc = BuildFactory()
# first step only in case git has aborted!
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["rm", "-rf", "/export/home/buildbot-unstable10s/rsyslog/rsyslog_solaris10sparc_rsyslog/build/.git/index.lock"], env=solarisenv_gcc))
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["pwd"]))
# cleanup
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["rm", "-rf", "localenv"], env=solarisenv_sunstudio, name="cleanup dependencies"))
# begin work
factoryRsyslogSolaris10sparc.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librelp.sh"], env=solarisenv_sunstudio, name="building librelp dependency", descriptionDone="built librelp dependency"))
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_sunstudio, name="building libfastjson dependency", descriptionDone="built libfastjson dependency"))
# begin "real" work
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio, name="autoreconf for SunStudio Compiler"))
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}, name="configure"))
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["gmake", "-j4", "V=0"], name="build with SunStudio", env=solarisenv_sunstudio))
# make check does not work here due to too-slow machine
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["bash", "-c", "tests/CI/interactive_exec_test_hook.sh", "tests/*.sh.log"], name="custom check scripts", env=solarisenv_sunstudio, maxTime=3000, timeout=1200))
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh", "tests/*.sh.log"], env=solarisenv_sunstudio, maxTime=3000, timeout=60, name="gathering make check logs", descriptionDone="gathered make check logs"))

# Note: we do not try build with gcc, as this takes another 20 minutes; the x86 case should
# be good enough to cover this.
# clean up
# ---

# Solaris unstable11s, which is so slow that the testbench
# gets into timing issues.
# Build steps are disabled because dependencies are not yet ready
factoryRsyslogSolaris11sparc = BuildFactory()
# first step only in case git has aborted!
#	factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["rm", "-rf", "/export/home/buildbot-unstable10s/rsyslog/rsyslog_solaris10sparc_rsyslog/build/.git/index.lock"], env=solarisenv_gcc))
#	factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["pwd"]))
# cleanup
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["rm", "-rf", "localenv"], env=solarisenv_sunstudio, name="cleanup dependencies"))
# begin work
factoryRsyslogSolaris11sparc.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librelp.sh"], env=solarisenv_sunstudio, name="building librelp dependency", descriptionDone="built librelp dependency"))
#factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_sunstudio, name="building libfastjson dependency", descriptionDone="built libfastjson dependency"))
# begin "real" work
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio, name="autoreconf for SunStudio Compiler"))
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}, name="configure"))
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["gmake", "-j4", "V=0"], name="build with SunStudio", env=solarisenv_sunstudio))
# make check does not work here due to too-slow machine
#factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["gmake", "check", "-j2", "V=0", "xTESTS=diskqueue rsf_getenv queue-persist rcvr_fail_restore"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, timeout=3600, description="custom make check (very limited)"))
# this is needed for "semi-manual" tests: factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["bash", "-c", "tests/CI/interactive_exec_test_hook.sh", "tests/*.sh.log"], name="custom check scripts", env=solarisenv_sunstudio, maxTime=3000, timeout=60))
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh", "tests/*.sh.log"], env=solarisenv_sunstudio, maxTime=3000, timeout=60, name="gathering make check logs", descriptionDone="gathered make check logs"))
#	factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["qmake", "distcheck", "V=1"]))

# Note: we do not try build with gcc, as this takes another 20 minutes; the x86 case should
# be good enough to cover this.
# clean up
# not needed as buildbot does cleanup on startup factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["gmake", "distclean"], env=solarisenv_sunstudio, maxTime=700, name="final cleanup" ))
# ---

factoryRsyslogDockerUbuntu16 = BuildFactory()
factoryRsyslogDockerUbuntu16.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
# note: we later might want to use clang, but for now we get some
# unexplainable errors if we use clang with this slave... TODO: check, I guess that's wrong!
# OLD!!! factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["./configure", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-elasticsearch","--enable-elasticsearch-tests",  "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--enable-kafka-tests=no"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["bash", "-c", "env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-elasticsearch-tests --enable-kafka-tests=no"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True, name="build (make)"))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
	# TODO NOT WORKIGN YET !!! factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["make", "-j3", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="check"))
#rger 2018-06-29 factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, haltOnFailure=True, name="check"))
#factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather make check logs"))
# ---


################################################################################
# GENERIC DOCKER factories for use on docker-enabled VM - used for "load balancing" via
# buildbot.
# This is almost identical except for the options choosen.
factoryRsyslogGeneric_Ubuntu16 = BuildFactory()
factoryRsyslogGeneric_Ubuntu16.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Ubuntu16.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Ubuntu16.addStep(ShellCommand(command=["bash", "-c", "if [ -f devtools/run-ci.sh ] ; then devtools/devcontainer.sh --rm devtools/run-ci.sh; fi"],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_ubuntu:16.04',
		'CC': 'gcc',
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  '--disable-elasticsearch-tests --disable-kafka-tests '
			'--disable-omrabbitmq',
			#'--disable-omrabbitmq --disable-clickhouse-tests',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j8',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		"RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php",
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))
################################################################################


factoryRsyslogGeneric_Ubuntu18_SAN = BuildFactory()
factoryRsyslogGeneric_Ubuntu18_SAN.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Ubuntu18_SAN.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Ubuntu18_SAN.addStep(ShellCommand(command=['bash', '-c', 'devtools/devcontainer.sh --rm devtools/run-ci.sh'],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_ubuntu:18.04',
		'CC': 'clang',
		'CFLAGS':'-g  -fstack-protector -D_FORTIFY_SOURCE=2 '
			'-fsanitize=address,undefined,nullability,unsigned-integer-overflow '
			'-fno-sanitize-recover=undefined,nullability,unsigned-integer-overflow '
			'-g -O3 -fno-omit-frame-pointer -fno-color-diagnostics',
		'LSAN_OPTIONS':'detect_leaks=0',
		'UBSAN_OPTIONS':'print_stacktrace=1',
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  '--disable-elasticsearch-tests --disable-kafka-tests '
			'--disable-libfaketime --without-valgrind-testbench --disable-valgrind',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j2',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		'RSYSLOG_STATSURL': 'http://build.rsyslog.com/testbench-failedtest.php',
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))


factoryRsyslogGeneric_Ubuntu18_TSAN = BuildFactory()
factoryRsyslogGeneric_Ubuntu18_TSAN.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Ubuntu18_TSAN.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Ubuntu18_TSAN.addStep(ShellCommand(command=['bash', '-c', 'devtools/devcontainer.sh --rm devtools/run-ci.sh'],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_ubuntu:18.04',
		'CC': 'clang-8',
		'CFLAGS':'-fstack-protector -D_FORTIFY_SOURCE=2 -fsanitize=thread '
			'-g -O2 -fno-omit-frame-pointer -fno-color-diagnostics',
		'CI_SANITIZE_BLACKLIST':'tests/tsan.supp',
		'TSAN_OPTIONS':"halt_on_error=1",
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  '--disable-elasticsearch-tests '
			'--disable-impstats --disable-kafka-tests ' #ipstats has known and OK races
			'--disable-libfaketime --without-valgrind-testbench --disable-valgrind',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j3',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		'ABORT_ALL_ON_TEST_FAIL':'NO',
		'RSYSLOG_STATSURL': 'http://build.rsyslog.com/testbench-failedtest.php',
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=7200,
	haltOnFailure=False, name="run CI script"))


factoryRsyslogGeneric_Ubuntu18_distcheck = BuildFactory()
factoryRsyslogGeneric_Ubuntu18_distcheck.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Ubuntu18_distcheck.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Ubuntu18_distcheck.addStep(ShellCommand(command=['bash', '-c', 'devtools/devcontainer.sh --rm devtools/run-ci.sh'],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_ubuntu:18.04',
		'CC': 'gcc',
		'CFLAGS':'-g',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j3',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		'ABORT_ALL_ON_TEST_FAIL':'xYES',
		'RSYSLOG_STATSURL': 'http://build.rsyslog.com/testbench-failedtest.php',
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))


factoryRsyslogGeneric_Ubuntu18_codecov = BuildFactory()
factoryRsyslogGeneric_Ubuntu18_codecov.addStep(docker_cleanup_step);
factoryRsyslogGeneric_Ubuntu18_codecov.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Ubuntu18_codecov.addStep(ShellCommand(command=['bash', '-c', 'devtools/devcontainer.sh --rm devtools/run-ci.sh'],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_ubuntu:18.04',
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  ' --disable-kafka-tests --disable-imkafka '
			'--disable-omkafka --enable-debug --disable-elasticsearch '
			'--disable-elasticsearch-tests',
		'CC': 'gcc',
		'CFLAGS':'-g -O0 -coverage',
		'LDFLAGS':'-lgcov',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j4',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		'ABORT_ALL_ON_TEST_FAIL':'NO',
		'CI_CODECOV_TOKEN': g['secret_CODECOV_TOKEN'],
		'RSYSLOG_STATSURL': 'http://build.rsyslog.com/testbench-failedtest.php',
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))


#.addStep(ShellCommand(command=["bash", "-c", "make -j8 check V=0 RS_TESTBENCH_VALGRIND_EXTRA_OPTS=\"--suppressions=$(pwd)/tests/CI/centos7.supp\""], env={'ABORT_ALL_ON_TEST_FAIL':'YES', 'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4", "RSYSLOG_DEBUG_TIMEOUTS_TO_STDERR": "on", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="check"))

factoryRsyslogGeneric_Thumbleweed = BuildFactory()
factoryRsyslogGeneric_Thumbleweed.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Thumbleweed.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Thumbleweed.addStep(ShellCommand(command=['bash', '-c', 'devtools/devcontainer.sh --rm devtools/run-ci.sh'],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_suse:tumbleweed',
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  '--disable-elasticsearch-tests --disable-kafka-tests ',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j8',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		'RSYSLOG_STATSURL': 'http://build.rsyslog.com/testbench-failedtest.php',
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))


factoryRsyslogGeneric_Debian10 = BuildFactory()
factoryRsyslogGeneric_Debian10.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Debian10.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Debian10.addStep(ShellCommand(command=["bash", "-c", "if [ -f devtools/run-ci.sh ] ; then devtools/devcontainer.sh --rm devtools/run-ci.sh; fi"],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_debian:10',
		'CC': 'gcc',
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  '--disable-elasticsearch-tests --disable-kafka-tests '
			'--without-valgrind-testbench',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j8',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		"RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php",
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))


#.addStep(ShellCommand(command=["./configure", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--enable-testbench", "--enable-imdiag", "--enable-elasticsearch=no", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--disable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--disable-ax-compiler-flags"], logfiles={"config.log": "config.log"}))


factoryRsyslogGeneric_Centos6 = BuildFactory()
factoryRsyslogGeneric_Centos6.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Centos6.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Centos6.addStep(ShellCommand(command=["bash", "-c", "devtools/devcontainer.sh --rm devtools/run-ci.sh"],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_centos:6',
		'CC': 'gcc',
		'CFLAGS': '-g',
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  '--disable-elasticsearch-tests --disable-kafka-tests '
			'--disable-gnutls --disable-ax-compiler-flags --disable-mmdblookup '
			'--disable-mmexternal',
		'CI_MAKE_OPT': '-j10',
		'CI_MAKE_CHECK_OPT': '-j1', # does not support parallel builds at all!
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		'CI_VALGRIND_SUPPRESSIONS':'centos6-9.supp',
		'ABORT_ALL_ON_TEST_FAIL':'YES',
		'RSYSLOG_DEBUG_TIMEOUTS_TO_STDERR': 'on',
		'RSYSLOG_STATSURL': 'http://build.rsyslog.com/testbench-failedtest.php',
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))


factoryRsyslogGeneric_Centos7 = BuildFactory()
factoryRsyslogGeneric_Centos7.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Centos7.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Centos7.addStep(ShellCommand(command=["bash", "-c", "if [ -f devtools/run-ci.sh ] ; then devtools/devcontainer.sh --rm devtools/run-ci.sh; fi"],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_centos:7',
		'CC': 'gcc',
		'CFLAGS': '-g',
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  '--disable-elasticsearch-tests --disable-kafka-tests '
			'--disable-snmp-tests ', # temporary, snmptraprcvr needs to support port 0
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j4',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		'CI_VALGRIND_SUPPRESSIONS':'centos7.supp',
		"RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php",
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))


factoryRsyslogGeneric_Centos8 = BuildFactory()
factoryRsyslogGeneric_Centos8.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Centos8.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Centos8.addStep(ShellCommand(command=["bash", "-c", "if [ -f devtools/run-ci.sh ] ; then devtools/devcontainer.sh --rm devtools/run-ci.sh; fi"],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_centos:8',
		'CC': 'gcc',
		'CFLAGS': '-g',
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  '--disable-elasticsearch-tests --disable-kafka-tests ',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j4',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		"RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php",
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))


factoryRsyslogGeneric_Fedora30 = BuildFactory()
factoryRsyslogGeneric_Fedora30.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Fedora30.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Fedora30.addStep(ShellCommand(command=["bash", "-c", "if [ -f devtools/run-ci.sh ] ; then devtools/devcontainer.sh --rm devtools/run-ci.sh; fi"],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_fedora:30',
		'CFLAGS': '-g',
		'RSYSLOG_CONFIGURE_OPTIONS_EXTRA':  '--disable-elasticsearch-tests --disable-kafka-tests '
			'--enable-debug',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j8',
		'CI_CHECK_CMD': 'check',
		'USE_AUTO_DEBUG': 'off',
		"RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php",
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))


factoryRsyslogGeneric_Kafka_codecov = BuildFactory()
factoryRsyslogGeneric_Kafka_codecov.addStep(docker_cleanup_step)
factoryRsyslogGeneric_Kafka_codecov.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogGeneric_Kafka_codecov.addStep(ShellCommand(command=["bash", "-c", "if [ -f devtools/run-ci.sh ] ; then devtools/devcontainer.sh --rm devtools/run-ci.sh; fi"],
	env={
		'RSYSLOG_DEV_CONTAINER': 'rsyslog/rsyslog_dev_base_fedora:30',
		'CFLAGS': '-g -O0 -coverage',
		'LDFLAGS': '-lgcov',
		# Note: we completely override the container configure options here!
		'RSYSLOG_CONFIGURE_OPTIONS_OVERRIDE':  '--enable-testbench --enable-omstdout --enable-imdiag '
			'--disable-impstats --enable-imfile --disable-imfile-tests --disable-fmhttp '
			'--enable-valgrind --enable-valgrind-testbench --disable-helgrind '
			'--disable-default-tests --enable-kafka-tests --enable-omkafka '
			'--enable-imkafka',
		'CI_MAKE_OPT': '-j20',
		'CI_MAKE_CHECK_OPT': '-j2',
		'CI_CHECK_CMD': 'check',
		'CI_CODECOV_TOKEN': g['secret_CODECOV_TOKEN'],
		'USE_AUTO_DEBUG': 'off',
		"RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php",
		'CI_BUILD_URL': util.URLForBuild,
		'VCS_SLUG':util.Property('buildername')
	},
	logfiles=generic_logfiles,
	lazylogfiles=True, maxTime=3600,
	haltOnFailure=False, name="run CI script"))



# This is our environment for LLVM TSAN
factoryRsyslogDockerUbuntu_18_TSAN = BuildFactory()
factoryRsyslogDockerUbuntu_18_TSAN.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerUbuntu_18_TSAN.addStep(ShellCommand(command=["autoreconf", "-fvi"], haltOnFailure=True, name="autoreconf"))
factoryRsyslogDockerUbuntu_18_TSAN.addStep(ShellCommand(command=["bash", "-c", 'env; export CFLAGS="-g  -fstack-protector -D_FORTIFY_SOURCE=2 -fsanitize=thread -fsanitize-blacklist=$(pwd)/tests/tsan.supp -g -O2 -fno-omit-frame-pointer -fno-color-diagnostics"; echo "SHOWING NEW CFLAGS: " $CFLAGS; ./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-valgrind --without-valgrind-testbench --enable-imptcp --disable-impstats --disable-omprog --disable-elasticsearch --disable-elasticsearch-tests --disable-libfaketime --enable-kafka-tests=no'], env={'CC': 'clang-8', "CFLAGS":"-g  -fstack-protector -D_FORTIFY_SOURCE=2 -fsanitize=thread -g -O2 -fno-omit-frame-pointer -fno-color-diagnostics"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang-8-TSAN)"))
factoryRsyslogDockerUbuntu_18_TSAN.addStep(ShellCommand(command=["make", "-j2", "V=0"], maxTime=1800, haltOnFailure=True, name="make"))
factoryRsyslogDockerUbuntu_18_TSAN.addStep(ShellCommand(command=["make", "-j2", "check", "V=0"], env={'ABORT_ALL_ON_TEST_FAIL':'YES', 'TSAN_OPTIONS':"halt_on_error=1", 'USE_AUTO_DEBUG': 'off', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000, haltOnFailure=False, name="make check"))
factoryRsyslogDockerUbuntu_18_TSAN.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather check logs"))
# ---


# This is our environment for various LLVM checkers (ASAN, UBSAN, ...)
# We use high optimization level here to ensure we do not run into problems with that
# For the same reason, we activate common security hardening mechanisms
factoryRsyslogDockerUbuntu_18_SAN = BuildFactory()
factoryRsyslogDockerUbuntu_18_SAN.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerUbuntu_18_SAN.addStep(ShellCommand(command=["autoreconf", "-fvi"], haltOnFailure=True, name="autoreconf"))
factoryRsyslogDockerUbuntu_18_SAN.addStep(ShellCommand(command=["bash", "-c", "env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-valgrind --without-valgrind-testbench --disable-libfaketime --enable-kafka-tests=no"], env={'CC': 'clang', "CFLAGS":"-g  -fstack-protector -D_FORTIFY_SOURCE=2 -fsanitize=address,undefined,nullability,unsigned-integer-overflow -fno-sanitize-recover=undefined,nullability,unsigned-integer-overflow -g -O3 -fno-omit-frame-pointer -fno-color-diagnostics", "LSAN_OPTIONS":"detect_leaks=0", "UBSAN_OPTIONS":"print_stacktrace=1"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang-UBSAN-ASAN-O3-harden)"))
factoryRsyslogDockerUbuntu_18_SAN.addStep(ShellCommand(command=["make", "-j3", "V=0"], maxTime=1800, haltOnFailure=True, name="make"))
factoryRsyslogDockerUbuntu_18_SAN.addStep(ShellCommand(command=["make", "-j2", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "LSAN_OPTIONS":"detect_leaks=0", "UBSAN_OPTIONS":"print_stacktrace=1", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000, haltOnFailure=False, name="make check"))
factoryRsyslogDockerUbuntu_18_SAN.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather check logs"))
# ---

# gtls only special, as we need to test tcpflood 
factoryRsyslogDockerUbuntu_18_gtls_only = BuildFactory()
factoryRsyslogDockerUbuntu_18_gtls_only.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerUbuntu_18_gtls_only.addStep(ShellCommand(command=["autoreconf", "-fvi"], haltOnFailure=True, name="autoreconf"))
factoryRsyslogDockerUbuntu_18_gtls_only.addStep(ShellCommand(command=["bash", "-c", "./configure --enable-testbench --enable-omstdout --enable-imdiag --disable-fmhttp --enable-valgrind --disable-default-tests --enable-gnutls --enable-extended-tests"], env={'CC': 'clang', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang-gnutls)"))
factoryRsyslogDockerUbuntu_18_gtls_only.addStep(ShellCommand(command=["make", "-j8", "V=0"], maxTime=1800, haltOnFailure=True, name="make"))
factoryRsyslogDockerUbuntu_18_gtls_only.addStep(ShellCommand(command=["make", "-j4", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "LSAN_OPTIONS":"detect_leaks=0", "UBSAN_OPTIONS":"print_stacktrace=1", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000, haltOnFailure=False, name="make check"))
# ---


# This is our environment for various LLVM checkers (ASAN, UBSAN, ...)
# We use high optimization level here to ensure we do not run into problems with that
# For the same reason, we activate common security hardening mechanisms
factoryRsyslogDockerDebian_8 = BuildFactory()
factoryRsyslogDockerDebian_8.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerDebian_8.addStep(ShellCommand(command=["autoreconf", "-fvi"], haltOnFailure=True, name="autoreconf"))
factoryRsyslogDockerDebian_8.addStep(ShellCommand(command=["bash", "-c", "./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-elasticsearch-tests --without-valgrind-testbench"], logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (system default CC)"))
factoryRsyslogDockerDebian_8.addStep(ShellCommand(command=["make", "-j3", "V=0"], maxTime=1800, haltOnFailure=True, name="make"))
factoryRsyslogDockerDebian_8.addStep(ShellCommand(command=["make", "-j2", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "LSAN_OPTIONS":"detect_leaks=0", "UBSAN_OPTIONS":"print_stacktrace=1", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000, haltOnFailure=False, name="make check"))
factoryRsyslogDockerDebian_8.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather check logs"))
# ---


# This is our "make distcheck" environment. Use conservative gcc - most important is that it
# checks if all files are present in tarball.
factoryRsyslogDockerUbuntu18_distcheck = BuildFactory()
factoryRsyslogDockerUbuntu18_distcheck.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerUbuntu18_distcheck.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerUbuntu18_distcheck.addStep(ShellCommand(command=["bash", "-c", "env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --enable-mysql-tests=yes --enable-kafka-tests=yes"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerUbuntu18_distcheck.addStep(ShellCommand(command=["make", "-j4", "distcheck", "V=0"], env={'ABORT_ALL_ON_TEST_FAIL':'YES', 'USE_AUTO_DEBUG': 'off', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="distcheck"))
factoryRsyslogDockerUbuntu18_distcheck.addStep(ShellCommand(command=["bash", "-c", "cat $(find . -name test-suite.log); pwd; exit 0"], haltOnFailure=False, name="show distcheck test log"))
# ---

# CodeCov PR integration
factoryRsyslogDockerUbuntu18_codecov = BuildFactory()
factoryRsyslogDockerUbuntu18_codecov.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerUbuntu18_codecov.addStep(ShellCommand(command=["git", "log", "-3"], name="git branch information"))
factoryRsyslogDockerUbuntu18_codecov.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
# gcc codecov instrumentation causes some omprog tests to hang
factoryRsyslogDockerUbuntu18_codecov.addStep(ShellCommand(command=["bash", "-c", "env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-kafka-tests --disable-imkafka --disable-omkafka --enable-debug --disable-elasticsearch --disable-elasticsearch-tests"], env={'CC': 'gcc', "CFLAGS":"-g -O0 -coverage", "LDFLAGS":"-lgcov"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc, coverage)"))
# ... and clang codecov instrumentation misses quite some files :-(
# but with clang we have incomplete reports ... so for now keeping with gcc
#factoryRsyslogDockerUbuntu18_codecov.addStep(ShellCommand(command=["bash", "-c", "env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --enable-kafka-tests=yes --enable-debug --disable-helgrind"], env={'CC': 'clang', "CFLAGS":"-g -O0 -coverage", "LDFLAGS":"--coverage"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang, coverage)"))
factoryRsyslogDockerUbuntu18_codecov.addStep(ShellCommand(command=["make", "-j4", "check", "V=0"], env={'ABORT_ALL_ON_TEST_FAIL':'YES', 'CC': 'gcc', "CFLAGS":"-g -O0 -coverage", 'USE_AUTO_DEBUG': 'off', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=10000, haltOnFailure=False, name="check"))
factoryRsyslogDockerUbuntu18_codecov.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh"], name="gather check logs"))
# w/ LLVM: factoryRsyslogDockerUbuntu18_codecov.addStep(ShellCommand(command=["bash", "-c", "curl -s https://codecov.io/bash >codecov.sh; chmod +x codecov.sh; ./codecov.sh -x \"llvm-cov gcov\" -t" + g['secret_CODECOV_TOKEN'] + " -n\"rsyslog buildbot PR\"; rm codecov.sh || exit 0"], env={'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, name="CodeCov upload"))
factoryRsyslogDockerUbuntu18_codecov.addStep(ShellCommand(command=["bash", "-c", "curl -s https://codecov.io/bash >codecov.sh; chmod +x codecov.sh; ./codecov.sh -t" + g['secret_CODECOV_TOKEN'] + " -n\"rsyslog buildbot PR\"; rm codecov.sh || exit 0"], env={'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, name="CodeCov upload"))
# ---

# This is for the nightly builds. It's almost equivalent to the "regular" one, but
# with kafka tests enabled.
factoryRsyslogDockerFedora30_nightly = BuildFactory()
factoryRsyslogDockerFedora30_nightly.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerFedora30_nightly.addStep(ShellCommand(command=["git", "log", "-3"], name="git branch information"))
factoryRsyslogDockerFedora30_nightly.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerFedora30_nightly.addStep(ShellCommand(command=["bash", "-c", "env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-omprog --enable-extended-tests"], env={'CC': 'gcc', "CFLAGS":"-g", "LDFLAGS":"-lgcov"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerFedora30_nightly.addStep(ShellCommand(command=["make", "-j2", "check", "VERBOSE=1"], env={'USE_AUTO_DEBUG': 'off', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="check"))
factoryRsyslogDockerFedora30_nightly.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh"], name="gather test logs"))
# ---



# EXPERIMENTAL arm - DETAILS WILL CHANGE LATER!
# Note: valgrind is quite slow here and has lots of false positives - so we disable
factoryRsyslogDockerArmUbuntu18 = BuildFactory()
factoryRsyslogDockerArmUbuntu18.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerArmUbuntu18.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerArmUbuntu18.addStep(ShellCommand(command=["bash", "-c", "set -v; set -x; env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-mmdblookup --without-valgrind-testbench --disable-valgrind --enable-impcap --enable-mmcapture --enable-kafka-tests=no --disable-elasticsearch-tests"], env={'CC': 'clang', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang)"))
factoryRsyslogDockerArmUbuntu18.addStep(ShellCommand(command=["make", "-j4"], haltOnFailure=True, name="make [clang]"))
factoryRsyslogDockerArmUbuntu18.addStep(ShellCommand(command=["make", "-j2", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', 'LIBRARY_PATH': '/usr/lib', 'LD_LIBRARY_PATH': '/usr/lib', 'RS_PWORK': '/mnt/rswork/', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5400, name="make check"))
factoryRsyslogDockerArmUbuntu18.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather test logs"))
# ---


# EXPERIMENTAL armbian - DETAILS WILL CHANGE LATER!
factoryRsyslogDockerArmbian = BuildFactory()
factoryRsyslogDockerArmbian.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerArmbian.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerArmbian.addStep(ShellCommand(command=["bash", "-c", "set -v; set -x; env; ./configure $RSYSLOG_CONFIGURE_OPTIONS"], env={'CC': 'clang', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang)"))
#factoryRsyslogDockerArmbian.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "CFLAGS":"-g -fsanitize=address"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=72000, haltOnFailure=False, name="check"))
#factoryRsyslogDockerArmbian.addStep(ShellCommand(command=["bash", "-c", "cat $(find . -name test-suite.log); pwd; exit 0"], name="show distcheck test log"))
# ---



#factoryRsyslogDockerCentos6 = BuildFactory()
#factoryRsyslogDockerCentos6.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
#factoryRsyslogDockerCentos6.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
#factoryRsyslogDockerCentos6.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
#factoryRsyslogDockerCentos6.addStep(ShellCommand(command=["./configure", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-improg", "--enable-imtuxedoulog", "--enable-pmdb2diag", "--enable-imbatchreport", "--enable-testbench", "--enable-imdiag", "--enable-elasticsearch=no", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--disable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--disable-ax-compiler-flags"], logfiles={"config.log": "config.log"}))
#factoryRsyslogDockerCentos6.addStep(ShellCommand(command=["make", "-j"]))
#factoryRsyslogDockerCentos6.addStep(ShellCommand(command=["bash", "-c", "make -j2 check V=0 RS_TESTBENCH_VALGRIND_EXTRA_OPTS=\"--suppressions=$(pwd)/tests/CI/centos6-9.supp\""], env={'ABORT_ALL_ON_TEST_FAIL':'YES', "RSYSLOG_DEBUG_TIMEOUTS_TO_STDERR": "on", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, name="make check"))



factoryRsyslogDockerCentos7 = BuildFactory()
factoryRsyslogDockerCentos7.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerCentos7.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerCentos7.addStep(ShellCommand(command=["bash", "-c", "set -v; set -x; env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-elasticsearch-tests --enable-kafka-tests=no"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerCentos7.addStep(ShellCommand(command=["bash", "-c", "make -j3 distcheck V=0 RS_TESTBENCH_VALGRIND_EXTRA_OPTS=\"--suppressions=$(pwd)/tests/CI/centos7.supp\""], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="distcheck"))
factoryRsyslogDockerCentos7.addStep(ShellCommand(command=["bash", "-c", "cat $(find . -name test-suite.log); pwd; exit 0"], haltOnFailure=False, name="show distcheck test log"))
factoryRsyslogDockerCentos7.addStep(ShellCommand(command=["bash", "-c", "cat $(find . -name \"*.log\"); exit 0"], haltOnFailure=False, name="show individual test logs"))


factoryRsyslogDockerCentos8 = BuildFactory()
factoryRsyslogDockerCentos8.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerCentos8.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerCentos8.addStep(ShellCommand(command=["bash", "-c", "./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-elasticsearch-tests --enable-kafka-tests=no"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerCentos8.addStep(ShellCommand(command=["make", "-j4"], haltOnFailure=True, name="build"))
factoryRsyslogDockerCentos8.addStep(ShellCommand(command=["bash", "-c", "make -j3 check V=0 RS_TESTBENCH_VALGRIND_EXTRA_OPTS=\"--suppressions=$(pwd)/tests/CI/centos7.supp\""], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="check"))


factoryRsyslogDockerSuse = BuildFactory()
factoryRsyslogDockerSuse.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerSuse.addStep(ShellCommand(command=["bash", "-c", "devtools/run-configure.sh"], env={'CONFIGURE_OPTS_OVERRIDE': '--disable-elasticsearch --disable-elasticsearch-tests'}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="run-configure.sh"))
factoryRsyslogDockerSuse.addStep(ShellCommand(command=["make", "-j"], haltOnFailure=True, name="build"))
factoryRsyslogDockerSuse.addStep(ShellCommand(command=["bash", "-c", "make -j8 check V=0 RS_TESTBENCH_VALGRIND_EXTRA_OPTS=\"--suppressions=$(pwd)/tests/CI/centos7.supp\""], env={'ABORT_ALL_ON_TEST_FAIL':'YES', 'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4", "RSYSLOG_DEBUG_TIMEOUTS_TO_STDERR": "on", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="check"))



# ---
# This is both for Fedora30 and Fedora31 -- the container handles the differences
factoryRsyslogDockerFedora = BuildFactory()
factoryRsyslogDockerFedora.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerFedora.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
# we temporarily disable ES tests, as one valgrind test seems to fail consistently with
# lib-related issues. rgerhards, 2018-09-19
factoryRsyslogDockerFedora.addStep(ShellCommand(command=["bash", "-c", "./configure $RSYSLOG_CONFIGURE_OPTIONS --enable-kafka-tests=no --disable-elasticsearch-tests --enable-debug"], env={"CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerFedora.addStep(ShellCommand(command=["make", "-j6"], lazylogfiles=True, maxTime=1000, haltOnFailure=True, name="make (default cc)"))
factoryRsyslogDockerFedora.addStep(ShellCommand(command=["bash", "-c", "make -j2 check V=0"], env={'USE_AUTO_DEBUG': 'off', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=True, name="check"))
# ---

# check for elasticsearch, which is known to cause many false positives
factoryRsyslogElasticSearchPlain = BuildFactory()
factoryRsyslogElasticSearchPlain.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogElasticSearchPlain.addStep(ShellCommand(command=["autoreconf", "-fvi"], haltOnFailure=True, name="autoreconf"))

factoryRsyslogElasticSearchPlain.addStep(ShellCommand(command=["bash", "-c", "./configure --enable-testbench --enable-omstdout --enable-imdiag --enable-impstats --enable-imfile --disable-imfile-tests --disable-fmhttp --enable-valgrind --disable-default-tests --enable-elasticsearch-tests --enable-elasticsearch"], env={'PKG_CONFIG_PATH': '/usr/local/lib/pkgconfig:/usr/lib64/pkgconfig', 'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure"))
factoryRsyslogElasticSearchPlain.addStep(ShellCommand(command=["make", "-j", "V=0"], maxTime=1800, haltOnFailure=True, name="make"))
#factoryRsyslogElasticSearchPlain.addStep(ShellCommand(command=["make", "-j4", "distcheck", "V=0"], env={'USE_AUTO_DEBUG': 'off', "LSAN_OPTIONS":"detect_leaks=0", "UBSAN_OPTIONS":"print_stacktrace=1", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername'), 'PKG_CONFIG_PATH': '/usr/local/lib/pkgconfig:/usr/lib64/pkgconfig'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000, haltOnFailure=False, name="make distcheck"))
factoryRsyslogElasticSearchPlain.addStep(ShellCommand(command=["make", "-j4", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "LSAN_OPTIONS":"detect_leaks=0", "UBSAN_OPTIONS":"print_stacktrace=1", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername'), 'PKG_CONFIG_PATH': '/usr/local/lib/pkgconfig:/usr/lib64/pkgconfig'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000, haltOnFailure=False, name="make check"))
#factoryRsyslogElasticSearchPlain.addStep(ShellCommand(command=["bash", "-c", "cat $(find . -name test-suite.log); exit 0"], haltOnFailure=False, name="show distcheck test log"))
# ---

# check for elasticsearch, which is known to cause many false positives
factoryRsyslogElasticSearch_codecov = BuildFactory()
factoryRsyslogElasticSearch_codecov.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogElasticSearch_codecov.addStep(ShellCommand(command=["autoreconf", "-fvi"], haltOnFailure=True, name="autoreconf"))
factoryRsyslogElasticSearch_codecov.addStep(ShellCommand(command=["bash", "-c", "./configure --enable-testbench --enable-omstdout --enable-imdiag --enable-impstats --enable-imfile --disable-imfile-tests --disable-fmhttp --enable-valgrind --enable-valgrind-testbench --disable-helgrind --disable-default-tests --enable-elasticsearch-tests --enable-elasticsearch"], env={'PKG_CONFIG_PATH': '/usr/local/lib/pkgconfig:/usr/lib64/pkgconfig', 'CC': 'gcc', "CFLAGS":"-g -O0 -coverage", "LDFLAGS":"-lgcov"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (coverage)"))
factoryRsyslogElasticSearch_codecov.addStep(ShellCommand(command=["make", "-j", "V=0"], maxTime=1800, haltOnFailure=True, name="make"))
factoryRsyslogElasticSearch_codecov.addStep(ShellCommand(command=["bash", "-c", "make -j2 check V=0 RS_TESTBENCH_VALGRIND_EXTRA_OPTS=\"--suppressions=$(pwd)/tests/CI/centos7.supp\""], env={'ABORT_ALL_ON_TEST_FAIL':'YES', 'USE_AUTO_DEBUG': 'off', "LSAN_OPTIONS":"detect_leaks=0", "UBSAN_OPTIONS":"print_stacktrace=1", "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000, haltOnFailure=False, name="make check"))
factoryRsyslogElasticSearch_codecov.addStep(ShellCommand(command=["bash", "-c", "curl -s https://codecov.io/bash >codecov.sh; chmod +x codecov.sh; ./codecov.sh -t" + g['secret_CODECOV_TOKEN'] + " -n\"rsyslog buildbot PR\"; rm codecov.sh || exit 0"], env={'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, name="CodeCov upload"))
# ---

# check for kaffka, which is known to cause many false positives
#factoryRsyslogKafka_codecov = BuildFactory()
#factoryRsyslogKafka_codecov.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
#factoryRsyslogKafka_codecov.addStep(ShellCommand(command=["autoreconf", "-fvi"], haltOnFailure=True, name="autoreconf"))
#factoryRsyslogKafka_codecov.addStep(ShellCommand(command=["bash", "-c", "./configure --enable-testbench --enable-omstdout --enable-imdiag --disable-impstats --enable-imfile --disable-imfile-tests --disable-fmhttp --enable-valgrind --enable-valgrind-testbench --disable-helgrind --disable-default-tests --enable-kafka-tests --enable-omkafka --enable-imkafka"], env={'CC': 'gcc', "CFLAGS":"-g -O0 -coverage", "LDFLAGS":"-lgcov"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (coverage)"))
#factoryRsyslogKafka_codecov.addStep(ShellCommand(command=["make", "-j", "V=0"], maxTime=1800, haltOnFailure=True, name="make"))
## nothing in parallel!!! kafka is highly timing-sensitive
#factoryRsyslogKafka_codecov.addStep(ShellCommand(command=["bash", "-c", "make -j2 check"], env={'USE_AUTO_DEBUG': 'off', "RSYSLOG_STATSURL": "http://build.rsyslog.com/testbench-failedtest.php", 'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000, haltOnFailure=False, name="make check"))
#factoryRsyslogKafka_codecov.addStep(ShellCommand(command=["bash", "-c", "curl -s https://codecov.io/bash >codecov.sh; chmod +x codecov.sh; ./codecov.sh -t" + g['secret_CODECOV_TOKEN'] + " -n\"rsyslog buildbot PR\"; rm codecov.sh || exit 0"], env={'CI_BUILD_URL': util.URLForBuild, 'VCS_SLUG':util.Property('buildername')}, name="CodeCov upload"))
# ---



####### compile tests (some legacy compile tests are specified above as well!)
factoryRsyslog_compile_clang9 = BuildFactory()
factoryRsyslog_compile_clang9.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslog_compile_clang9.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslog_compile_clang9.addStep(ShellCommand(command=["bash", "-c", "./configure $RSYSLOG_CONFIGURE_OPTIONS"], env={'CC': 'clang-9', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang 9)"))
factoryRsyslog_compile_clang9.addStep(ShellCommand(command=["make", "-j1"], haltOnFailure=True, name="make (clang 9)"))

# we need dedicated machines as clang 9 currently requires dedicated container (issue with v8 coexistence)
lc['builders'].append(
	BuilderConfig(name="rsyslog compile clang9",
		workernames=["docker-ubuntu-compilecheck-ubuntu1910"],
		factory=factoryRsyslog_compile_clang9,
		tags=["rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog",
		} ))


factoryRsyslog_compile_clang10 = BuildFactory()
factoryRsyslog_compile_clang10.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslog_compile_clang10.addStep(ShellCommand(command=["devtools/run-configure.sh"], env={'CC': 'clang-10', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="run-configure (clang 10)"))
factoryRsyslog_compile_clang10.addStep(ShellCommand(command=["make", "-j1"], haltOnFailure=True, name="make (clang 10[experimental])"))

lc['builders'].append(
	BuilderConfig(name="rsyslog compile clang10",
		workernames=["docker-ubuntu-compilecheck-ubuntu1910"],
		factory=factoryRsyslog_compile_clang10,
		tags=["rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog",
		} ))



factoryRsyslog_compile_gcc9 = BuildFactory()
factoryRsyslog_compile_gcc9.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslog_compile_gcc9.addStep(ShellCommand(command=["devtools/run-configure.sh"], env={'CC': 'gcc-9', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="run-configure (gcc 9)"))
factoryRsyslog_compile_gcc9.addStep(ShellCommand(command=["make", "-j1"], haltOnFailure=True, name="make (gcc 9)"))

lc['builders'].append(
	BuilderConfig(name="rsyslog compile gcc9",
		workernames=["docker-ubuntu-compilecheck-ubuntu1910"],
		factory=factoryRsyslog_compile_gcc9,
		tags=["rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog",
		} ))



factoryRsyslog_compile_clang8 = BuildFactory()
factoryRsyslog_compile_clang8.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslog_compile_clang8.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslog_compile_clang8.addStep(ShellCommand(command=["bash", "-c", "./configure $RSYSLOG_CONFIGURE_OPTIONS"], env={'CC': 'clang-8', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang 8)"))
factoryRsyslog_compile_clang8.addStep(ShellCommand(command=["make", "-j1"], haltOnFailure=True, name="make (clang 8)"))

lc['builders'].append(
	BuilderConfig(name="rsyslog compile clang8",
		workernames=["docker-ubuntu-compilecheck"],
		factory=factoryRsyslog_compile_clang8,
		tags=["rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog",
		} ))


factoryRsyslog_compile_gcc8 = BuildFactory()
factoryRsyslog_compile_gcc8.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslog_compile_gcc8.addStep(ShellCommand(command=["devtools/run-configure.sh", "-fvi"], env={'CC': 'gcc-8'}, haltOnFailure=True, name="run-configure (gcc8)"))
factoryRsyslog_compile_gcc8.addStep(ShellCommand(command=["make", "-j1"], haltOnFailure=True, name="make (gcc8)"))

lc['builders'].append(
	BuilderConfig(name="rsyslog compile gcc8",
		workernames=["docker-ubuntu-compilecheck"],
		factory=factoryRsyslog_compile_gcc8,
		tags=["rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog",
		} ))


factoryRsyslog_compile_PRvalidate = BuildFactory()
factoryRsyslog_compile_PRvalidate.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslog_compile_PRvalidate.addStep(ShellCommand(command=["tests/CI/PR_validation.sh", "-fvi"], haltOnFailure=True, name="validate PR commit structure"))

lc['builders'].append(
	BuilderConfig(name="rsyslog PR structure validation",
		workernames=["docker-stylecheck"],
		factory=factoryRsyslog_compile_PRvalidate,
		tags=["rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog",
		} ))


####### Create Builders

factoryRsyslogCodeStyleCheck = BuildFactory()
factoryRsyslogCodeStyleCheck.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogCodeStyleCheck.addStep(ShellCommand(command=["bash", "-c",
	"if grep \"^export RSYSLOG_DEBUG=\" tests/diag.sh; then "
        "    echo >&2 'ERROR: DEBUG enabled in tests/diag.sh - this is known to NOT work!'; "
        "    echo >&2 'Most probably this was done accidently, so just comment it out again.'; "
	"    exit 1; "
	"fi"], haltOnFailure=True, name="check testbench DEBUG not enabled"))
factoryRsyslogCodeStyleCheck.addStep(ShellCommand(command=["devtools/check-codestyle.sh"], haltOnFailure=True, name="codestyle check"))

lc['builders'].append(
	BuilderConfig(name="rsyslog codestyle check",
		workernames=["docker-stylecheck"],
		factory=factoryRsyslogCodeStyleCheck,
		tags=["rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog",
		} ))


factoryRsyslogStaticAnalyzer = BuildFactory()
factoryRsyslogStaticAnalyzer.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogStaticAnalyzer.addStep(ShellCommand(command=["bash", "-c", "devtools/devcontainer.sh devtools/run-static-analyzer.sh"], name="clang static analyzer", logfiles={"report_url": "report_url"}, lazylogfiles=True, env={'RSYSLOG_DEV_CONTAINER':'rsyslog/rsyslog_dev_base_ubuntu:19.10', 'SCAN_BUILD_CC':'clang-9', 'SCAN_BUILD': 'scan-build-9', 'SCAN_BUILD_REPORT_BASEURL': 'http://ubuntu16.rsyslog.com/', 'SCAN_BUILD_REPORT_DIR': '/var/www/html', 'DOCKER_RUN_EXTRA_FLAGS': '-v /var/www/html:/var/www/html -e RSYSLOG_CONFIGURE_EXTRA_OPTS -eSCAN_BUILD_CC -eSCAN_BUILD -eSCAN_BUILD_REPORT_DIR -eSCAN_BUILD_REPORT_BASEURL', 'RSYSLOG_CONFIGURE_OPTIONS_EXTRA': "--disable-ksi-ls12"}, haltOnFailure=True))

lc['builders'].append(
	BuilderConfig(name="rsyslog clang static analyzer",
		workernames=["slave-ubuntu16"],
		factory=factoryRsyslogStaticAnalyzer,
		tags=["rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog",
		} ))

# --- Factory for checking RPM builds - this should be modelled very much after the nighly builder at
# the end of this file!!!!
factoryRsyslogRpmBuild = BuildFactory()
# Prepare enviromment
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "./initenv.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'REPOUSERNAME': 'pkgbuild', "REPOURL":"rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR":"/home/pkg/rsyslog-pkg-rhel-centos"},  haltOnFailure=True, name="Init environment"))

## DEBUG TESTING docker-fedora30-fix BRANCH 
#factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "git checkout -f docker-fedora30-fix && sed -i \"s/szLocalUser\=test/szLocalUser\=pkg/g\" config.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", haltOnFailure=True, name="DEBUG alorbach git update"))
#factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "./initenv.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'REPOUSERNAME': 'pkgbuild', "REPOURL":"rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR":"/home/pkg/rsyslog-pkg-rhel-centos"},  haltOnFailure=True, name="DEBUG Init environment 2"))
#factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "ls -al / && more config.sh && more /etc/mock/epel-7-x86_64.cfg"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'REPOUSERNAME': 'pkgbuild', "REPOURL":"rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR":"/home/pkg/rsyslog-pkg-rhel-centos"}, haltOnFailure=False, name="debug ls -al /"))

# - GET rsyslog latest master branch from github, prepare and build dist file
factoryRsyslogRpmBuild.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "autoreconf -fvi"], workdir="build/", name="autoreconf"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "./configure --disable-generate-man-pages"], workdir="build/", env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="dummy configure (gcc)"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "make dist"], haltOnFailure=True, workdir="build/", name="make dist (tar.gz)"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "ls -al"], haltOnFailure=True, workdir="build/", name="debug ls al ./"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "mv -f `ls *.tar.gz` /home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SOURCES/"],haltOnFailure=True, workdir="build/", name="move packagefile *.tar.gz for RPM build"))
# - GET rsyslog doc and BUILD
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "git clone https://github.com/rsyslog/rsyslog-doc.git"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", name="git clone rsyslog-doc"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "pip install -r requirements.txt"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/rsyslog-doc/", name="pip installed requirements"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "sed -E -i \"s/read -r REPLY//g\" tools/release_build.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/rsyslog-doc", name="remove 'read -r REPLY' from release_build.sh"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "chmod +x tools/release_build.sh && ./tools/release_build.sh"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/rsyslog-doc/", name="sphinx build doc"))
# - SET version and release in SPECFile
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_VERSION=`ls rpmbuild/SOURCES/*.tar.gz | sed s/[^0-9.]//g | rev | cut -c 4- | rev` && echo $RSYSLOG_VERSION && sed -E -i \"s/Version: (.*)/Version: $RSYSLOG_VERSION.master/g\" rpmbuild/SPECS/v8-stable.spec"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", logfiles={"v8-stable.spec": "/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SPECS/v8-stable.spec"}, name="replace rsyslog version in v8-stable"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_DATE=`date +\"%s\"` && echo $RSYSLOG_DATE && sed -E -i \"s/Release: (.*)/Release: $RSYSLOG_DATE/g\" rpmbuild/SPECS/v8-stable.spec"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", logfiles={"v8-stable.spec": "/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SPECS/v8-stable.spec"}, name="replace release number with date in v8-stable"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_VERSION=`ls rpmbuild/SOURCES/*.tar.gz | sed s/[^0-9.]//g | rev | cut -c 4- | rev` && echo $RSYSLOG_VERSION && sed -E -i \"s/Version: (.*)/Version: $RSYSLOG_VERSION.master/g\" rpmbuild/SPECS/v8-stable-el7.spec"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", logfiles={"v8-stable-el7.spec": "/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SPECS/v8-stable-el7.spec"}, name="replace rsyslog version in v8-stable-el7"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_DATE=`date +\"%s\"` && echo $RSYSLOG_DATE && sed -E -i \"s/Release: (.*)/Release: $RSYSLOG_DATE/g\" rpmbuild/SPECS/v8-stable-el7.spec"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", logfiles={"v8-stable-el7.spec": "/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SPECS/v8-stable-el7.spec"}, name="replace release number with date in v8-stable-el7"))
# - MOVE rsyslog-doc AFTER SPEC MODIFICATION!
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_VERSION=`ls rpmbuild/SOURCES/*.tar.gz | sed s/[^0-9.]//g | rev | cut -c 4- | rev` && echo $RSYSLOG_VERSION && cd rsyslog-doc && mv -f `ls *.tar.gz` /home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SOURCES/rsyslog-doc-$RSYSLOG_VERSION.master.tar.gz"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", name="move doc packagefile *.tar.gz for RPM build"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "ls -al"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SOURCES/", name="debug ls rpmbuild/SOURCES/"))
# - BUILD RPMS
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-8-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-8", "RPM_ARCH":"x86_64", "RPM_REPO":"testing"}, logfiles={"root.log": "/var/lib/mock/epel-8-x86_64/result/root.log"}, name="build epel-8/x86_64 rpms"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-7-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-7", "RPM_ARCH":"x86_64", "RPM_REPO":"testing"}, logfiles={"root.log": "/var/lib/mock/epel-7-x86_64/result/root.log"}, name="build epel-7/x86_64 rpms"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-6-i386/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-6", "RPM_ARCH":"i386", "RPM_REPO":"v8-stable-testing"}, logfiles={"root.log": "/var/lib/mock/epel-6-i386/result/root.log"}, maxTime=1200, timeout=1200, name="build epel-6/i386 rpms"))
factoryRsyslogRpmBuild.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-6-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-6", "RPM_ARCH":"x86_64", "RPM_REPO":"v8-stable-testing"}, logfiles={"root.log": "/var/lib/mock/epel-6-x86_64/result/root.log"}, maxTime=1200, timeout=1200, name="build epel-6/x86_64 rpms"))


lc['builders'].append(
   BuilderConfig(name="rsyslog rpmbuild",
     workernames=["docker-fedora30-pkgbuild"],
      factory=factoryRsyslogRpmBuild,
      tags=["rsyslog", "rpmbuild"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))


#lc['builders'].append(
   #BuilderConfig(name="rsyslog ubuntu rsyslog",
     #workernames=["slave-ubuntu"],
      #factory=factoryRsyslogUbuntu, 
      #tags=["rsyslog"], 
      #properties={
	#"github_repo_owner": "rsyslog",
	#"github_repo_name": "rsyslog",
      #},
    #))
lc['builders'].append(
   BuilderConfig(name="rsyslog ubuntu16 rsyslog",
     workernames=["slave-ubuntu16"],
      factory=factoryRsyslogUbuntu16,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog debian rsyslog",
      workernames=["slave-debian"],
      factory=factoryRsyslogDebian,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog debian9 rsyslog",
      workernames=["slave-debian9"],
      factory=factoryRsyslogDebian9,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog raspbian gcc compile",
      workernames=["slave-raspbian"],
      factory=factoryRsyslogRaspbian_gcc,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog raspbian clang compile",
      workernames=["slave-raspbian"],
      factory=factoryRsyslogRaspbian_clang,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog centos6 rsyslog",
    workernames=["slave-centos6"],
    factory=factoryRsyslogCentos6,
    tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog centos7-5",
      workernames=["vm-centos7-5-w1", "vm-centos7-5-w2", "vm-centos7-5-w3"],
      factory=factoryRsyslogCentos7VM,
      tags=["rsyslog", "vm"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog ElasticSearch",
      workernames=["vm-centos7-5-w1", "vm-centos7-5-w2", "vm-centos7-5-w3"],
      factory=factoryRsyslogElasticSearchPlain,
      tags=["rsyslog", "vm"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog ElasticSearch codecov",
      workernames=["vm-centos7-5-w1", "vm-centos7-5-w2", "vm-centos7-5-w3"],
      factory=factoryRsyslogElasticSearch_codecov,
      tags=["rsyslog", "vm"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen ubuntu16",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Ubuntu16,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen ubuntu18 TSAN",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Ubuntu18_TSAN,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen ubuntu18 SAN",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Ubuntu18_SAN,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen ubuntu18 codecov",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Ubuntu18_codecov,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen ubuntu18 distcheck",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Ubuntu18_distcheck,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen suse thumbleweed",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Thumbleweed,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen debian10",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Debian10,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen centos6",
      workernames=generic_small_workers,
      factory=factoryRsyslogGeneric_Centos6,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen centos7",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Centos7,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen centos8",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Centos8,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen fedora30",
      workernames=generic_workers,
      factory=factoryRsyslogGeneric_Fedora30,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog gen kafka codecov",
      workernames=generic_small_workers,
      factory=factoryRsyslogGeneric_Kafka_codecov,
      tags=["rsyslog", "generic"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
#lc['builders'].append(
    #BuilderConfig(name="rsyslog Kafka codecov",
      #workernames=['docker-s1-fedora30'],
      #factory=factoryRsyslogKafka_codecov,
      #tags=["rsyslog", "docker"],
      #properties={
	#"github_repo_owner": "rsyslog",
	#"github_repo_name": "rsyslog",
      #},
    #))
lc['builders'].append(
    BuilderConfig(name="rsyslog docker-fedora31",
      workernames=[ "docker-fedora31-w1"],
      factory=factoryRsyslogDockerFedora,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
#lc['builders'].append(
#    BuilderConfig(name="rsyslog docker-fedora30",
#      workernames=["docker-s1-fedora30"],
#      factory=factoryRsyslogDockerFedora,
#      tags=["rsyslog"],
#      properties={
#	"github_repo_owner": "rsyslog",
#	"github_repo_name": "rsyslog",
#      },
#    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog freebsd12 rsyslog",
      workernames=["slave-freebsd12"],
      factory=factoryRsyslogFreebsd,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog suse rsyslog",
      workernames=["slave-suse"],
      factory=factoryRsyslogSuse,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog solaris10sparc rsyslog",
      workernames=["slave-solaris10sparc"],
      factory=factoryRsyslogSolaris10sparc,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog solaris10x64 rsyslog",
      workernames=["slave-solaris10x64"],
      factory=factoryRsyslogSolaris10x64_gcc,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog solaris10x64 sunstudio",
      workernames=["slave-solaris10x64"],
      factory=factoryRsyslogSolaris10x64_sunstudio,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog solaris11sparc rsyslog",
      workernames=["slave-solaris11sparc"],
      factory=factoryRsyslogSolaris11sparc,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog solaris11x64 rsyslog",
      workernames=["slave-solaris11x64"],
      factory=factoryRsyslogSolaris11x64,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog docker-arm-ubuntu18",
      workernames=["docker-armbian-w1",
	"docker-armbian-w2",
	"docker-armbian-w3",
	#"docker-armbian-w4"
	],
      factory=factoryRsyslogDockerArmUbuntu18,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
#lc['builders'].append(
#   BuilderConfig(name="rsyslog docker-ubuntu16 rsyslog",
#     workernames=["docker-ubuntu16-w2", "docker-ubuntu16-w4", "docker-ubuntu16"],
#      factory=factoryRsyslogDockerUbuntu16,
#      tags=["rsyslog"],
#      properties={
#	"github_repo_owner": "rsyslog",
#	"github_repo_name": "rsyslog",
#      },
#    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-ubuntu18 GnuTLS only",
      workernames=docker_workers,
      factory=factoryRsyslogDockerUbuntu_18_gtls_only,
      tags=["rsyslog", "docker"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-ubuntu18-tsan rsyslog",
      workernames=docker_workers,
      factory=factoryRsyslogDockerUbuntu_18_TSAN,
      tags=["rsyslog", "docker"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-ubuntu18-san rsyslog",
      workernames=docker_workers,
      factory=factoryRsyslogDockerUbuntu_18_SAN,
      tags=["rsyslog", "docker"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
#lc['builders'].append(
#   BuilderConfig(name="rsyslog docker-debian10",
#     workernames=["docker-debian10-w1"],
#      factory=factoryRsyslogDockerDebian_8,
#      tags=["rsyslog", "docker"],
#      properties={
#        "github_repo_owner": "rsyslog",
#        "github_repo_name": "rsyslog",
#      },
#    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-ubuntu18-distcheck rsyslog",
      workernames=docker_workers,
      factory=factoryRsyslogDockerUbuntu18_distcheck,
      tags=["rsyslog", "docker"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-ubuntu18-codecov",
      workernames=docker_workers,
      factory=factoryRsyslogDockerUbuntu18_codecov,
      tags=["rsyslog", "docker", "codecov"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
#lc['builders'].append(
#   BuilderConfig(name="rsyslog docker-centos6",
#      workernames=["docker-centos6-wg1", "docker-centos6-w5"],
#      factory=factoryRsyslogDockerCentos6,
#      tags=["rsyslog", "docker"],
#      properties={
#	"github_repo_owner": "rsyslog",
#	"github_repo_name": "rsyslog",
#      },
#    ))
#lc['builders'].append(
#   BuilderConfig(name="rsyslog docker-centos7 rsyslog",
#      workernames=["docker-centos7", "docker-centos7-w4"],
#      factory=factoryRsyslogDockerCentos7,
#      tags=["rsyslog", "docker"],
#      properties={
#	"github_repo_owner": "rsyslog",
#	"github_repo_name": "rsyslog",
#      },
#    ))
#lc['builders'].append(
#   BuilderConfig(name="rsyslog docker-centos8 rsyslog",
#      workernames=["docker-centos8-w4"],
#      factory=factoryRsyslogDockerCentos8,
#      tags=["rsyslog", "docker"],
#      properties={
#	"github_repo_owner": "rsyslog",
#	"github_repo_name": "rsyslog",
#      },
#    ))
#lc['builders'].append(
#   BuilderConfig(name="rsyslog docker-suse-tumbleweed",
#      workernames=[#"docker-suse-tumbleweed-w5",
#	"docker-suse-tumbleweed-wg1"],
#      factory=factoryRsyslogDockerSuse,
#      tags=["rsyslog", "docker"],
#      properties={
#	"github_repo_owner": "rsyslog",
#	"github_repo_name": "rsyslog",
#      },
#    ))


lc['builders'].append(
   BuilderConfig(name="nightly rsyslog docker-fedora30",
     workernames=["docker-fedora30-nightly"],
      factory=factoryRsyslogDockerFedora30_nightly,
      tags=["rsyslog", "nightly", "docker"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))

lc['builders'].append(
   BuilderConfig(name="background rsyslog centos7-5",
     workernames=["vm-centos7-5-bgtasks"],
      factory=factoryRsyslogCentos7VM_bg,
      tags=["rsyslog", "bg", "vm"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))

lc['schedulers'].append(ForceScheduler(
	name="pull_rsyslog_rsyslog",
	label="1. Pull Requests-rsyslog-rsyslog",
	builderNames=[  "rsyslog clang static analyzer"
			,"rsyslog compile gcc9"
			,"rsyslog compile gcc8"
			,"rsyslog compile clang10"
			,"rsyslog compile clang9"
			,"rsyslog compile clang8"
			,"rsyslog rpmbuild"
			,"rsyslog gen ubuntu16"
			,"rsyslog gen ubuntu18 SAN"
			,"rsyslog gen ubuntu18 TSAN"
			,"rsyslog gen ubuntu18 distcheck"
			,"rsyslog gen ubuntu18 codecov"
			,"rsyslog codestyle check"
			,"rsyslog ubuntu16 rsyslog"
			,"rsyslog debian rsyslog"
			,"rsyslog debian9 rsyslog"
			,"rsyslog raspbian gcc compile"
			,"rsyslog raspbian clang compile"
			,"rsyslog centos6 rsyslog"
			,"rsyslog centos7-5"
			,"rsyslog ElasticSearch"
			,"rsyslog ElasticSearch codecov"
			#,"rsyslog Kafka codecov"
			,"rsyslog docker-fedora31"
			#,"rsyslog docker-fedora30"
			,"rsyslog freebsd12 rsyslog"
			,"rsyslog suse rsyslog"
			,"rsyslog solaris10x64 rsyslog"
			,"rsyslog solaris10x64 sunstudio"
			,"rsyslog solaris11sparc rsyslog"
			# far too slow at the moment, disable 2019-02-31 rgerhards: ,"rsyslog solaris10sparc rsyslog"
			,"rsyslog solaris11x64 rsyslog"
			,"rsyslog docker-arm-ubuntu18"
			#,"rsyslog docker-ubuntu16 rsyslog"
			,"rsyslog docker-ubuntu18-distcheck rsyslog"
			,"rsyslog docker-ubuntu18-san rsyslog"
			,"rsyslog docker-ubuntu18-tsan rsyslog"
			#,"rsyslog docker-debian10"
			,"rsyslog gen kafka codecov"
			,"rsyslog gen suse thumbleweed"
			,"rsyslog gen debian10"
			,"rsyslog gen centos6"
			,"rsyslog gen centos7"
			,"rsyslog gen centos8"
			,"rsyslog gen fedora30"
			#,"rsyslog docker-centos6"
			#,"rsyslog docker-centos7 rsyslog"
			#,"rsyslog docker-centos8 rsyslog"
			#,"rsyslog docker-suse-tumbleweed"
		],
	codebases=[
		util.CodebaseParameter(
			"", 
			branch=util.StringParameter(
				name="branch", 
				label="Pull Request Number:<br>", 
				required=True, 
				default="refs/pull/<NUMBER>/head", 
				size=80),
			),
	],
))

lc['schedulers'].append(ForceScheduler(
	name="forceall_rsyslog_rsyslog",
	label="2. Force All-rsyslog-rsyslog",
	builderNames=[	"rsyslog clang static analyzer"
			,"rsyslog compile gcc9"
			,"rsyslog compile gcc8"
			,"rsyslog compile clang10"
			,"rsyslog compile clang9"
			,"rsyslog compile clang8"
			,"rsyslog rpmbuild"
			,"rsyslog gen ubuntu16"
			,"rsyslog gen ubuntu18 SAN"
			,"rsyslog gen ubuntu18 TSAN"
			,"rsyslog gen ubuntu18 distcheck"
			,"rsyslog gen ubuntu18 codecov"
			,"rsyslog codestyle check"
			,"rsyslog ubuntu16 rsyslog"
			,"rsyslog debian rsyslog"
			,"rsyslog debian9 rsyslog"
			,"rsyslog raspbian gcc compile"
			,"rsyslog raspbian clang compile"
			,"rsyslog centos6 rsyslog"
			,"rsyslog centos7-5"
			,"rsyslog ElasticSearch"
			,"rsyslog ElasticSearch codecov"
			#,"rsyslog Kafka codecov"
			#,"rsyslog fedora26x64 rsyslog"
			,"rsyslog docker-fedora31"
			#,"rsyslog docker-fedora30"
			,"rsyslog freebsd12 rsyslog"
			,"rsyslog suse rsyslog"
			,"rsyslog solaris10x64 rsyslog"
			,"rsyslog solaris10x64 sunstudio"
			,"rsyslog solaris11sparc rsyslog"
			,"rsyslog solaris10sparc rsyslog"
			,"rsyslog solaris11x64 rsyslog"
			,"rsyslog docker-ubuntu18-san rsyslog"
			,"rsyslog docker-ubuntu18-tsan rsyslog"
			,"rsyslog docker-arm-ubuntu18"
			#,"rsyslog docker-ubuntu16 rsyslog"
			,"rsyslog docker-ubuntu18-distcheck rsyslog"
			#,"rsyslog docker-centos6"
			#,"rsyslog docker-debian10"
			,"rsyslog gen kafka codecov"
			,"rsyslog gen suse thumbleweed"
			,"rsyslog gen debian10"
			,"rsyslog gen centos6"
			,"rsyslog gen centos7"
			,"rsyslog gen centos8"
			,"rsyslog gen fedora30"
			#,"rsyslog docker-centos7 rsyslog"
			#,"rsyslog docker-centos8 rsyslog"
			#,"rsyslog docker-suse-tumbleweed"
			],
))

lc['schedulers'].append(SingleBranchScheduler(
	name="github_rsyslog_rsyslog",
	change_filter=filter.ChangeFilter(	category="pull", 
						project="rsyslog/rsyslog"),
	builderNames=[  "rsyslog clang static analyzer"
			,"rsyslog PR structure validation"
			,"rsyslog compile gcc9"
			,"rsyslog compile gcc8"
			,"rsyslog compile clang10"
			,"rsyslog compile clang9"
			,"rsyslog compile clang8"
			,"rsyslog rpmbuild"
			,"rsyslog gen ubuntu16"
			,"rsyslog gen ubuntu18 SAN"
			,"rsyslog gen ubuntu18 TSAN"
			,"rsyslog gen ubuntu18 distcheck"
			,"rsyslog gen ubuntu18 codecov"
			,"rsyslog codestyle check"
			,"rsyslog debian rsyslog"
			,"rsyslog debian9 rsyslog"
			,"rsyslog raspbian gcc compile"
			,"rsyslog raspbian clang compile"
			,"rsyslog centos7-5"
			,"rsyslog ElasticSearch"
			,"rsyslog ElasticSearch codecov"
			#,"rsyslog Kafka codecov"
			,"rsyslog docker-fedora31"
			#,"rsyslog docker-fedora30"
			,"rsyslog freebsd12 rsyslog"
			,"rsyslog suse rsyslog"
			,"rsyslog solaris10x64 rsyslog"
			,"rsyslog solaris10x64 sunstudio"
			,"rsyslog solaris11sparc rsyslog"
			# far too slow at the moment, disable 2019-02-31 rgerhards: ,"rsyslog solaris10sparc rsyslog"
			,"rsyslog solaris11x64 rsyslog"
			,"rsyslog docker-arm-ubuntu18"
			#,"rsyslog docker-ubuntu16 rsyslog"
			#,"rsyslog docker-ubuntu18-distcheck rsyslog"
			#,"rsyslog docker-ubuntu18-codecov"
			,"rsyslog docker-ubuntu18 GnuTLS only"
			#,"rsyslog docker-ubuntu18-san rsyslog"
			,"rsyslog docker-ubuntu18-tsan rsyslog"
			#,"rsyslog docker-centos6" # disable until stable!
			#,"rsyslog docker-debian10"
			,"rsyslog gen kafka codecov"
			,"rsyslog gen suse thumbleweed"
			,"rsyslog gen debian10"
			,"rsyslog gen centos6"
			,"rsyslog gen centos7"
			,"rsyslog gen centos8"
			,"rsyslog gen fedora30"
			#,"rsyslog docker-centos7 rsyslog"
			#,"rsyslog docker-centos8 rsyslog"
			#,"rsyslog docker-suse-tumbleweed"
		],
))

lc['schedulers'].append(ForceScheduler(
	name="forceallcron_rsyslog_rsyslog",
	label="3. Force All Cron-rsyslog-rsyslog",
	builderNames=["nightly rsyslog docker-fedora30"],
))

# Start Nightly Scheduler once at night!
# we do not need them any longer as we have the on-master-change schedulers
# They were originally meant for CodeCov, but also ensure that current master
# had is tested. Change on 2019-04-29 - probably delete this in two month from now.
# see also https://github.com/rsyslog/rsyslog/issues/2909
#lc['schedulers'].append(schedulers.Nightly(name='nightly',
#	branch='master',
#	builderNames=["nightly rsyslog docker-fedora30",
#	              "rsyslog docker-ubuntu18-codecov"],
#	hour=1, minute=0))

# build master commits so that CodeCov has references for all commits
lc['schedulers'].append(schedulers.SingleBranchScheduler(name='rsyslog-master-sched',
	change_filter=util.ChangeFilter(project='rsyslog/rsyslog', branch='master'),
	treeStableTimer=30, # otherwise a PR merge with n commits my start n builders
	builderNames=["rsyslog docker-ubuntu18-codecov"
			,"background rsyslog centos7-5"
			,"rsyslog gen kafka codecov"
			#,"rsyslog Kafka codecov"
		     ],
	# TODO: replace with this value: builderNames=["master rsyslog"],
	))

# --- Factory for nightly RPM build 
factoryRsyslogRpmBuild_nightly = BuildFactory()
# Prepare enviromment
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "./initenv.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'REPOUSERNAME': 'pkgbuild', "REPOURL":"rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR":"/home/pkg/rsyslog-pkg-rhel-centos"},  haltOnFailure=True, name="Init environment"))

## DEBUG TESTING docker-fedora30-fix BRANCH 
#factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "git checkout -f docker-fedora30-fix && sed -i \"s/szLocalUser\=test/szLocalUser\=pkg/g\" config.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", haltOnFailure=True, name="DEBUG alorbach git update"))
#factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "./initenv.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'REPOUSERNAME': 'pkgbuild', "REPOURL":"rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR":"/home/pkg/rsyslog-pkg-rhel-centos"},  haltOnFailure=True, name="DEBUG Init environment 2"))
#factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "ls -al / && more config.sh && more /etc/mock/epel-7-x86_64.cfg"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'REPOUSERNAME': 'pkgbuild', "REPOURL":"rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR":"/home/pkg/rsyslog-pkg-rhel-centos"}, haltOnFailure=False, name="debug ls -al /"))

# - GET rsyslog latest master branch from github, prepare and build dist file
factoryRsyslogRpmBuild_nightly.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "autoreconf -fvi"], workdir="build/", name="autoreconf"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "./configure --disable-generate-man-pages"], workdir="build/", env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="dummy configure (gcc)"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "make dist"], haltOnFailure=True, workdir="build/", name="make dist (tar.gz)"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "ls -al"], haltOnFailure=True, workdir="build/", name="debug ls al ./"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "mv -f `ls *.tar.gz` /home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SOURCES/"], haltOnFailure=True, workdir="build/", name="move packagefile *.tar.gz for RPM build"))
# - GET rsyslog doc and BUILD
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "git clone https://github.com/rsyslog/rsyslog-doc.git"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/", name="git clone rsyslog-doc"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "pip install -r requirements.txt"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/rsyslog-doc/", name="pip installed requirements"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "sed -E -i \"s/read -r REPLY//g\" tools/release_build.sh"], workdir="/home/pkg/rsyslog-pkg-rhel-centos/rsyslog-doc", name="remove 'read -r REPLY' from release_build.sh"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "chmod +x tools/release_build.sh && ./tools/release_build.sh"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/rsyslog-doc/", name="sphinx build doc"))
# - SET version and release in SPECFile
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_VERSION=`ls rpmbuild/SOURCES/*.tar.gz | sed s/[^0-9.]//g | rev | cut -c 4- | rev` && echo $RSYSLOG_VERSION && sed -E -i \"s/Version: (.*)/Version: $RSYSLOG_VERSION.master/g\" rpmbuild/SPECS/v8-stable.spec"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", logfiles={"v8-stable.spec": "/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SPECS/v8-stable.spec"}, name="replace rsyslog version in v8-stable"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_DATE=`date +\"%s\"` && echo $RSYSLOG_DATE && sed -E -i \"s/Release: (.*)/Release: $RSYSLOG_DATE/g\" rpmbuild/SPECS/v8-stable.spec"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", logfiles={"v8-stable.spec": "/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SPECS/v8-stable.spec"}, name="replace release number with date in v8-stable"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_VERSION=`ls rpmbuild/SOURCES/*.tar.gz | sed s/[^0-9.]//g | rev | cut -c 4- | rev` && echo $RSYSLOG_VERSION && sed -E -i \"s/Version: (.*)/Version: $RSYSLOG_VERSION.master/g\" rpmbuild/SPECS/v8-stable-el7.spec"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", logfiles={"v8-stable-el7.spec": "/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SPECS/v8-stable-el7.spec"}, name="replace rsyslog version in v8-stable-el7"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_DATE=`date +\"%s\"` && echo $RSYSLOG_DATE && sed -E -i \"s/Release: (.*)/Release: $RSYSLOG_DATE/g\" rpmbuild/SPECS/v8-stable-el7.spec"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", logfiles={"v8-stable-el7.spec": "/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SPECS/v8-stable-el7.spec"}, name="replace release number with date in v8-stable-el7"))
# - MOVE rsyslog-doc AFTER SPEC MODIFICATION!
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "export RSYSLOG_VERSION=`ls rpmbuild/SOURCES/*.tar.gz | sed s/[^0-9.]//g | rev | cut -c 4- | rev` && echo $RSYSLOG_VERSION && cd rsyslog-doc && mv -f `ls *.tar.gz` /home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SOURCES/rsyslog-doc-$RSYSLOG_VERSION.master.tar.gz"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", name="move doc packagefile *.tar.gz for RPM build"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "ls -al"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/rpmbuild/SOURCES/", name="debug ls rpmbuild/SOURCES/"))
# - BUILD RPMS
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-6-i386/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-6", "RPM_ARCH":"i386", "RPM_REPO":"v8-stable-nightly"}, logfiles={"root.log": "/var/lib/mock/epel-6-i386/result/root.log", "build.log": "/var/lib/mock/epel-6-i386/result/build.log"}, maxTime=1200, timeout=1200, name="build epel-6/i386 rpms"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-6-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-6", "RPM_ARCH":"x86_64", "RPM_REPO":"v8-stable-nightly"}, logfiles={"root.log": "/var/lib/mock/epel-6-x86_64/result/root.log", "build.log": "/var/lib/mock/epel-6-x86_64/result/build.log"}, maxTime=1200, timeout=1200, name="build epel-6/x86_64 rpms"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-7-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-7", "RPM_ARCH":"x86_64", "RPM_REPO":"v8-stable-nightly"}, logfiles={"root.log": "/var/lib/mock/epel-7-x86_64/result/root.log", "build.log": "/var/lib/mock/epel-7-x86_64/result/build.log", "state.log": "/var/lib/mock/epel-7-x86_64/result/state.log"}, name="build epel-7/x86_64 rpms"))
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "if ./rpmmaker.sh; then echo ok; exit 0; else cat /var/lib/mock/epel-8-x86_64/result/build.log; exit 1; fi"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={'RPM_SPEC': 'v8-stable', "RPM_PLATFORM":"epel-8", "RPM_ARCH":"x86_64", "RPM_REPO":"v8-stable-nightly"}, logfiles={"root.log": "/var/lib/mock/epel-8-x86_64/result/root.log", "build.log": "/var/lib/mock/epel-8-x86_64/result/build.log", "state.log": "/var/lib/mock/epel-8-x86_64/result/state.log"}, name="build epel-8/x86_64 rpms"))

# - UPLOAD RPMs to v8-stable-nightly repo
factoryRsyslogRpmBuild_nightly.addStep(ShellCommand(command=["bash", "-c", "./do_upload.sh"], haltOnFailure=True, workdir="/home/pkg/rsyslog-pkg-rhel-centos/", env={"RPM_REPO":"v8-stable-nightly", "REPOUSERNAME": "pkgbuild", "REPOURL": "rpms.adiscon.com:/home/makerpm/yumrepo", "PKGBASEDIR": "/home/pkg/rsyslog-pkg-rhel-centos"}, name="upload to v8-stable-nightly repo"))

# --- Builders for nightly RPM build
lc['builders'].append(
   BuilderConfig(name="nightly rsyslog rpmbuild",
     workernames=["docker-fedora30-pkgbuild"],
      factory=factoryRsyslogRpmBuild_nightly,
      tags=["rsyslog", "nightly", "rpmbuild"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))

# --- Schedulers for nightly RPM build
lc['schedulers'].append(ForceScheduler(
        name="forceallcron_rsyslog_rpmbuild",
        label="Force All Cron-rsyslog-rpmbuild",
        builderNames=["nightly rsyslog rpmbuild"],
))
lc['schedulers'].append(schedulers.Nightly(
	name='nightly rsyslog rpmbuild',
	branch='master',
	builderNames=["nightly rsyslog rpmbuild"], 
		hour=1, 
		minute=0))
# ---

