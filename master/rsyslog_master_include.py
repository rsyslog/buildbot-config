#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 	* Copyright (C) 2018 Adiscon GmbH.
#	* This file is part of RSyslog
#	* 
#	* rsyslog factory settings
#	*

from buildbot.process.factory import BuildFactory
from buildbot.steps.source.github import GitHub
from buildbot.steps.shell import ShellCommand
from buildbot.steps.shell import Configure 

# --- rsyslog factory settings
factoryRsyslogCentos6 = BuildFactory()
factoryRsyslogCentos6.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogCentos6.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogCentos6.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryRsyslogCentos6.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-elasticsearch=no", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--disable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--disable-ax-compiler-flags"], env={'PKG_CONFIG_PATH': '/home/rger/localenv/lib/pkgconfig:/lib64/pkgconfig'}, logfiles={"config.log": "config.log"}))
#factoryRsyslogCentos6.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind"],  env={'PKG_CONFIG_PATH': '/lib64/pkgconfig:/home/rger/localenv/lib/pkgconfig'}, logfiles={"config.log": "config.log"}))
factoryRsyslogCentos6.addStep(ShellCommand(command=["make", "-j"]))
factoryRsyslogCentos6.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, name="make check"))

factoryRsyslogCentos7 = BuildFactory()
factoryRsyslogCentos7.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogCentos7.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_kubernetes_test_server.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"], name="clenup hanging instances"))
factoryRsyslogCentos7.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryRsyslogCentos7.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-ksi-ls12", "--enable-omjournal", "--enable-libsystemd=yes", "--enable-mmkubernetes", "--enable-imjournal", "--enable-omkafka", "--enable-imkafka", "--enable-ommongodb=no", "--enable-compile-warnings=error"], env={'PKG_CONFIG_PATH': '/usr/local/lib/pkgconfig:/usr/lib64/pkgconfig'}, logfiles={"config.log": "config.log"}))
factoryRsyslogCentos7.addStep(ShellCommand(command=["make", "-j4"], haltOnFailure=True))
factoryRsyslogCentos7.addStep(ShellCommand(command=["tools/rsyslogd", "-v"]))
factoryRsyslogCentos7.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

factoryRsyslogDebian = BuildFactory()
factoryRsyslogDebian.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDebian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogDebian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"]))
factoryRsyslogDebian.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
# use clang!
factoryRsyslogDebian.addStep(ShellCommand(command=["./configure", "--prefix=/opt/rsyslog", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-omkafka=no", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--without-valgrind-testbench"], env={'CC': 'clang', "CFLAGS":"-g -fsanitize=address"}, logfiles={"config.log": "config.log"}))
#factoryRsyslogDebian.addStep(ShellCommand(command=["./configure", "--prefix=/opt/rsyslog", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind"], logfiles={"config.log": "config.log"}))
factoryRsyslogDebian.addStep(ShellCommand(command=["make", "-j"], haltOnFailure=True))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
factoryRsyslogDebian.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.5"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
factoryRsyslogDebian.addStep(ShellCommand(command=["bash", "-c", "pwd; ls -l -tr tests/*.sh.log; ls -l tests/CI"]))
factoryRsyslogDebian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"]))

factoryRsyslogDebian9 = BuildFactory()
factoryRsyslogDebian9.addStep(ShellCommand(command=["sleep", "2"], name="wait for github"))
factoryRsyslogDebian9.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDebian9.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogDebian9.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"]))
factoryRsyslogDebian9.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
# use clang!
factoryRsyslogDebian9.addStep(ShellCommand(command=["./configure", "--prefix=/opt/rsyslog", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-omjournal", "--enable-imjournal", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-omkafka", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--without-valgrind-testbench"], env={'CC': 'clang', "CFLAGS":"-g -O2 -fsanitize=address"}, logfiles={"config.log": "config.log"}))
factoryRsyslogDebian9.addStep(ShellCommand(command=["make", "-j"], haltOnFailure=True))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
factoryRsyslogDebian9.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.5", 'LIBRARY_PATH': '/usr/local/lib', 'LD_LIBRARY_PATH': '/usr/local/lib'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=4600))
factoryRsyslogDebian9.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"]))

factoryRsyslogRaspbian_gcc = BuildFactory()
factoryRsyslogRaspbian_gcc.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogRaspbian_gcc.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=raspbianenv_gcc, haltOnFailure=True))
factoryRsyslogRaspbian_gcc.addStep(ShellCommand(command=["./configure", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--without-valgrind-testbench"], logfiles={"config.log": "config.log"}, env=raspbianenv_gcc, lazylogfiles=True, haltOnFailure=True, name="configure [gcc]"))
factoryRsyslogRaspbian_gcc.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True, name="make [gcc]"))

factoryRsyslogRaspbian = BuildFactory()
# NOTES:
# * valgrind does not work on raspbian -- there are lots of errors in dlload()
#   subsystem before it finally aborts. Not worth wasting time on that...
#   rgerhards, 2017-12-08
# * do NOT run more than 2 parallel make jobs -- we have seen the compiler
#   fail with "internal error", which most probably means it ran out of
#   memory (this was with -j4 and seldomly, so -j2 should be a safe bet).
# * we do no longer run the testbench here as this is done on the new
#   arm docker device (and we can't scale here, so this really blocks CI)
# GCC compile commented out as we try it in a separate builder, to be run in parallel!
factoryRsyslogRaspbian.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
# do not do at the moment! factoryRsyslogRaspbian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; fi"], name="cleanup hanging instances (if any)"))
factoryRsyslogRaspbian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"], name="cleanup for next tests"))
factoryRsyslogRaspbian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"], name="cleanup old instances"))
factoryRsyslogRaspbian.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=raspbianenv_gcc, haltOnFailure=True))
#factoryRsyslogRaspbian.addStep(ShellCommand(command=["./configure", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--without-valgrind-testbench"], logfiles={"config.log": "config.log"}, env=raspbianenv_gcc, lazylogfiles=True, haltOnFailure=True, name="configure [gcc]"))
#factoryRsyslogRaspbian.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True, name="make [gcc]"))
#factoryRsyslogRaspbian.addStep(ShellCommand(command=["make", "clean"], haltOnFailure=True, name="cleanup for next build"))

factoryRsyslogRaspbian.addStep(ShellCommand(command=["./configure", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes", "--without-valgrind-testbench", "--enable-compile-warnings=error"], logfiles={"config.log": "config.log"}, env={'CC':'clang', 'CFLAGS': '-g -O1', 'LC_ALL' : 'C', 'LIBRARY_PATH': '/usr/lib', 'LD_LIBRARY_PATH': '/usr/lib'}, lazylogfiles=True, haltOnFailure=True, name="configure [clang]"))
factoryRsyslogRaspbian.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True, name="make [clang]"))
# first let's get the build right, then look into the testbench
#factoryRsyslogRaspbian.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', 'LIBRARY_PATH': '/usr/lib', 'LD_LIBRARY_PATH': '/usr/lib'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
#factoryRsyslogRaspbian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather test logs"))

factoryRsyslogFedora23 = BuildFactory()
factoryRsyslogFedora23.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogFedora23.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogFedora23.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryRsyslogFedora23.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-omjournal", "--enable-mmkubernetes", "--enable-imjournal", "--enable-compile-warnings=yes"], env={'PKG_CONFIG_PATH':'/usr/local/lib/pkgconfig'}, logfiles={"config.log": "config.log"}))
factoryRsyslogFedora23.addStep(ShellCommand(command=["make", "-j"], haltOnFailure=True))
factoryRsyslogFedora23.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))

# This config will be retired (deleted) soon, it has already been
# replaced by F28 docker container build. rgerhards 2018-07-23
factoryRsyslogFedora64 = BuildFactory()
factoryRsyslogFedora64.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogFedora64.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_kubernetes_test_server.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogFedora64.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryRsyslogFedora64.addStep(ShellCommand(command=["./configure", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-elasticsearch-tests=no", "--enable-elasticsearch", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmcount", "--enable-imjournal", "--enable-omjournal", "--enable-gssapi-krb5", "--enable-rfc3195=no", "--enable-ommongodb", "--enable-mmkubernetes", "--enable-imkafka", "--enable-omkafka", "--enable-kafka-tests"], env={'LIBRARY_PATH': '/usr/local/lib:/usr/lib64', 'LD_LIBRARY_PATH': '/usr/local/lib:/usr/lib64', 'PKG_CONFIG_PATH':'/usr/local/lib/pkgconfig'}, logfiles={"config.log": "config.log"}, haltOnFailure=True))
factoryRsyslogFedora64.addStep(ShellCommand(command=["make", "-j", "V=0"], env={'LIBRARY_PATH': '/usr/local/lib:/usr/lib64', 'LD_LIBRARY_PATH': '/usr/local/lib:/usr/lib64'}, haltOnFailure=True))
factoryRsyslogFedora64.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'on', 'LD_LIBRARY_PATH': '/usr/local/lib:/usr/lib64'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=13600))
factoryRsyslogFedora64.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/try_merge.sh ] ; then tests/CI/try_merge.sh ; fi"], lazylogfiles=True, logfiles={"test-suite.log": "tests/test-suite.log"}, name="try merge"))

factoryRsyslogSuse = BuildFactory()
factoryRsyslogSuse.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogSuse.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"]))
factoryRsyslogSuse.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
factoryRsyslogSuse.addStep(ShellCommand(command=["./configure", "--prefix=/usr/local", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-debug", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--disable-libfaketime", "--enable-mmkubernetes", "--without-valgrind-testbench"], env={'CC': 'gcc', 'CFLAGS': '-g -fsanitize=address', 'PKG_CONFIG_PATH': '/usr/local/lib/pkgconfig'}, logfiles={"config.log": "config.log"}, haltOnFailure=True))
factoryRsyslogSuse.addStep(ShellCommand(command=["make", "-j"], haltOnFailure=True))
factoryRsyslogSuse.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', 'LD_LIBRARY_PATH': '/usr/local/lib'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=4000))
factoryRsyslogSuse.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather check logs"))

factoryRsyslogFreebsd = BuildFactory()
factoryRsyslogFreebsd.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogFreebsd.addStep(ShellCommand(command=["ps", "aux"]))
factoryRsyslogFreebsd.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
# Note: current version of valgrind is full of false positives, so
# we cannot use valgrind here. :-/
factoryRsyslogFreebsd.addStep(ShellCommand(command=["./configure", "--disable-dependency-tracking", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-pmnull", "--enable-valgrind", "--without-valgrind-testbench"], env={'PKG_CONFIG_PATH': '/usr/libdata/pkgconfig:/usr/local/lib/pkgconfig'}, logfiles={"config.log": "config.log"}, haltOnFailure=True))
factoryRsyslogFreebsd.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True))
# add for testing:  mmexternal-SegFault-vg.sh mmexternal-SegFault.sh
factoryRsyslogFreebsd.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
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
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["bash", "-c", "pwd; ls -l -tr tests/*.sh.log; ls -l tests/CI"]))
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"]))

factoryRsyslogUbuntuCron = BuildFactory()
factoryRsyslogUbuntuCron.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogUbuntuCron.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh; tests/CI/kill_all_kubernetes_test_server.sh  ; fi"]))
factoryRsyslogUbuntuCron.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"]))
factoryRsyslogUbuntuCron.addStep(ShellCommand(command=["autoreconf", "--force", "--verbose", "--install"]))
# note: we later might want to use clang, but for now we get some
# unexplainable errors if we use clang with this slave...
factoryRsyslogUbuntuCron.addStep(ShellCommand(command=["./configure", "--prefix=/opt/rsyslog", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-mmkubernetes", "--enable-valgrind", "--without-valgrind-testbench"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True))
#factoryRsyslogUbuntu.addStep(ShellCommand(command=["./configure", "--prefix=/opt/rsyslog", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--enable-silent-rules", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind"], logfiles={"config.log": "config.log"}))
factoryRsyslogUbuntuCron.addStep(ShellCommand(command=["make", "-j"], haltOnFailure=True))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
factoryRsyslogUbuntuCron.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
factoryRsyslogUbuntuCron.addStep(ShellCommand(command=["bash", "-c", "pwd; ls -l -tr tests/*.sh.log; ls -l tests/CI"]))
factoryRsyslogUbuntuCron.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"]))

factoryRsyslogUbuntu16 = BuildFactory()
factoryRsyslogUbuntu16.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["git", "log", "-4"], name="git branch information"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/kill_all_instances.sh ] ; then tests/CI/kill_all_instances.sh ; tests/CI/kill_all_kubernetes_test_server.sh ; fi"], name="kill left-over instances"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["./configure", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-elasticsearch-tests=no", "--enable-elasticsearch", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmnull", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--enable-mmsnmptrapd", "--enable-gnutls", "--enable-openssl", "--enable-usertools", "--enable-mysql", "--enable-imczmq", "--enable-omczmq", "--enable-valgrind", "--enable-imjournal","--enable-omjournal", "--enable-imkafka", "--enable-omkafka", "--enable-kafka-tests", "--enable-ommongodb", "--enable-omhiredis", "--enable-gssapi-krb5", "--enable-ksi-ls12", "--enable-mmkubernetes", "--enable-debug", "--without-valgrind-testbench"], env={'CC': 'gcc-7', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc-7)"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["make", "-j2", "check", "TESTS=", "V=0"], haltOnFailure=True, name="make (gcc-7)"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["make", "clean"], name="cleanup for next tests"))
# now compile plus dynamic testbench tests - do this last as it runs longest
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["./configure", "--mandir=/usr/share/man", "--infodir=/usr/share/info", "--datadir=/usr/share", "--sysconfdir=/etc", "--localstatedir=/var/lib", "--disable-dependency-tracking", "--docdir=/usr/share/doc/rsyslog", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-elasticsearch-tests=no", "--enable-elasticsearch", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-imczmq", "--enable-omczmq", "--enable-valgrind", "--enable-imjournal","--enable-omjournal", "--enable-imkafka", "--enable-omkafka", "--enable-kafka-tests", "--enable-ommongodb", "--enable-omhiredis", "--enable-gssapi-krb5", "--enable-ksi-ls12", "--without-valgrind-testbench"], env={'CC': 'clang-4.0', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="build with clang-4.0"))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["make", "-j2", "V=0"], haltOnFailure=True))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
factoryRsyslogUbuntu16.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="cleanup dependencies"))

# Solaris all except unstable10s, which is so slow that the testbench
# gets into timing issues.
# Build steps are disabled because dependencies are not yet ready
factoryRsyslogSolaris10x64 = BuildFactory()
# first step only in case git has aborted!
#	factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["rm", "-rf", "/export/home/buildbot-unstable10s/rsyslog/rsyslog_solaris10sparc_rsyslog/build/.git/index.lock"], env=solarisenv_gcc))
factoryRsyslogSolaris10x64.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
# cleanup
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["df", "-h"], env=solarisenv_sunstudio))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["rm", "-rf", "localenv"], env=solarisenv_sunstudio, name="cleanup dependencies"))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["git", "log", "-4"], env=solarisenv_sunstudio, name="git branch information"))
# begin work
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librelp.sh"], env=solarisenv_sunstudio, name="building librelp dependency", descriptionDone="built librelp dependency"))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_sunstudio, name="building libfastjson dependency", descriptionDone="built libfastjson dependency"))
#TESTING !!! factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librdkafka.sh"], env=solarisenv_sunstudio, name="building librdkafka dependency", descriptionDone="built librdkafka dependency"))

# begin "real" work
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio, name="autoreconf for SunStudio Compiler"))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}))
#TESTING: , "--enable-imkafka", "--enable-omkafka", "--enable-kafka-tests"
#	factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["cat", "configure"], env=solarisenv_sunstudio))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["gmake", "-j", "V=1"], env=solarisenv_sunstudio, name="build with SunStudio", haltOnFailure=True))
 
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["gmake", "check", "V=0"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3000, timeout=300))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh", "tests/*.sh.log"], env=solarisenv_sunstudio, maxTime=3000, timeout=60, name="gathering make check logs", descriptionDone="gathered make check logs"))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["df", "-h"], env=solarisenv_sunstudio))
#factoryRsyslogSolaris.addStep(ShellCommand(command=["qmake", "distcheck", "V=1"]))

# end now the same with GCC
#	factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librelp.sh"], env=solarisenv_gcc))
#	factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_gcc))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_gcc, name="autoreconf for gcc Compiler"))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_gcc, logfiles={"config.log": "config.log"}, name="configure", haltOnFailure=True))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["gmake", "-j", "V=1"], env=solarisenv_gcc, haltOnFailure=True))
#TEST DO NOT WORK YET 
#	factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["gmake", "check", "V=1"], env=solarisenv_gcc, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, timeout=3600))
# clean up
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["df", "-h"], env=solarisenv_sunstudio))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["gmake", "distclean"], env=solarisenv_sunstudio, maxTime=300, name="final cleanup" ))
factoryRsyslogSolaris10x64.addStep(ShellCommand(command=["df", "-h"], env=solarisenv_sunstudio))
# ---

# ---
factoryRsyslogSolaris11x64 = BuildFactory()
factoryRsyslogSolaris11x64.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
# cleanup
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["df", "-h"], env=solarisenv_sunstudio))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["rm", "-rf", "localenv"], env=solarisenv_sunstudio, name="cleanup dependencies"))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["git", "log", "-4"], env=solarisenv_sunstudio, name="git branch information"))
# begin work
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librelp.sh"], env=solarisenv_sunstudio, name="building librelp dependency", descriptionDone="built librelp dependency"))
# libfastjson currently not needed - maybe in the future again
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_sunstudio, name="building libfastjson dependency", descriptionDone="built libfastjson dependency"))
# begin "real" work
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio, name="autoreconf for SunStudio Compiler"))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["gmake", "-j", "V=0"], env=solarisenv_sunstudio, name="build with SunStudio", haltOnFailure=True))
# DISABLE if interactive testing is done on machine
#, "TESTS=imfile-readmode2.sh"
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["gmake", "check", "V=0"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3000, timeout=300))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh", "tests/*.sh.log"], env=solarisenv_sunstudio, maxTime=3000, timeout=60, name="gathering make check logs", descriptionDone="gathered make check logs"))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["df", "-h"], env=solarisenv_sunstudio))
factoryRsyslogSolaris11x64.addStep(ShellCommand(command=["gmake", "distclean"], env=solarisenv_sunstudio, maxTime=300, name="final cleanup" ))
# ---

# Solaris unstable10s, which is so slow that the testbench
# gets into timing issues.
# Build steps are disabled because dependencies are not yet ready
factoryRsyslogSolaris10sparc = BuildFactory()
# first step only in case git has aborted!
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["rm", "-rf", "/export/home/buildbot-unstable10s/rsyslog/rsyslog_solaris10sparc_rsyslog/build/.git/index.lock"], env=solarisenv_gcc))
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["pwd"]))
# cleanup
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["rm", "-rf", "localenv"], env=solarisenv_sunstudio, name="cleanup dependencies"))
# begin work
factoryRsyslogSolaris10sparc.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-librelp.sh"], env=solarisenv_sunstudio, name="building librelp dependency", descriptionDone="built librelp dependency"))
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_sunstudio, name="building libfastjson dependency", descriptionDone="built libfastjson dependency"))
# begin "real" work
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio, name="autoreconf for SunStudio Compiler"))
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}, name="configure"))
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["gmake", "-j", "V=0"], name="build with SunStudio", env=solarisenv_sunstudio))
# make check does not work here due to too-slow machine
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["bash", "-c", "tests/CI/interactive_exec_test_hook.sh", "tests/*.sh.log"], name="custom check scripts", env=solarisenv_sunstudio, maxTime=3000, timeout=60))
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh", "tests/*.sh.log"], env=solarisenv_sunstudio, maxTime=3000, timeout=60, name="gathering make check logs", descriptionDone="gathered make check logs"))
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["gmake", "check", "V=1", "TESTS=glbl-umask.sh empty-hostname.sh stop-localvar.sh"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, timeout=3600))
#factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["qmake", "distcheck", "V=1"]))

# Note: we do not try build with gcc, as this takes another 20 minutes; the x86 case should
# be good enough to cover this.
# clean up
factoryRsyslogSolaris10sparc.addStep(ShellCommand(command=["gmake", "distclean"], env=solarisenv_sunstudio, maxTime=300, name="final cleanup" ))
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
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["bash", "-c", "tests/solaris/prep-libfastjson.sh"], env=solarisenv_sunstudio, name="building libfastjson dependency", descriptionDone="built libfastjson dependency"))
# begin "real" work
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["autoreconf", "-fvi"], env=solarisenv_sunstudio, name="autoreconf for SunStudio Compiler"))
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["./configure", "V=0", "--disable-dependency-tracking", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-imfile", "--enable-impstats", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--disable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools=no", "--disable-valgrind"], env=solarisenv_sunstudio, logfiles={"config.log": "config.log"}, name="configure"))
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["gmake", "-j", "V=0"], name="build with SunStudio", env=solarisenv_sunstudio))
# make check does not work here due to too-slow machine
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["bash", "-c", "tests/CI/interactive_exec_test_hook.sh", "tests/*.sh.log"], name="custom check scripts", env=solarisenv_sunstudio, maxTime=3000, timeout=60))
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["bash", "-c", "tests/CI/gather_all_logs.sh", "tests/*.sh.log"], env=solarisenv_sunstudio, maxTime=3000, timeout=60, name="gathering make check logs", descriptionDone="gathered make check logs"))
#	factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["gmake", "check", "V=1", "TESTS=glbl-umask.sh empty-hostname.sh stop-localvar.sh"], env=solarisenv_sunstudio, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, timeout=3600))
#	factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["qmake", "distcheck", "V=1"]))

# Note: we do not try build with gcc, as this takes another 20 minutes; the x86 case should
# be good enough to cover this.
# clean up
factoryRsyslogSolaris11sparc.addStep(ShellCommand(command=["gmake", "distclean"], env=solarisenv_sunstudio, maxTime=300, name="final cleanup" ))
# ---

factoryRsyslogDockerUbuntu16 = BuildFactory()
factoryRsyslogDockerUbuntu16.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
# note: we later might want to use clang, but for now we get some
# unexplainable errors if we use clang with this slave... TODO: check, I guess that's wrong!
factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["./configure", "--enable-silent-rules", "--disable-generate-man-pages", "--enable-testbench", "--enable-imdiag", "--enable-elasticsearch","--enable-elasticsearch-tests",  "--enable-imfile", "--enable-impstats", "--enable-imptcp", "--enable-mmanon", "--enable-mmaudit", "--enable-mmfields", "--enable-mmjsonparse", "--enable-mmpstrucdata", "--enable-mmsequence", "--enable-mmutf8fix", "--enable-mail", "--enable-omprog", "--enable-omruleset", "--enable-omstdout", "--enable-omuxsock", "--enable-pmaixforwardedfrom", "--enable-pmciscoios", "--enable-pmcisconames", "--enable-pmlastmsg", "--enable-pmsnare", "--enable-libgcrypt", "--enable-mmnormalize", "--disable-omudpspoof", "--enable-relp", "--disable-snmp", "--disable-mmsnmptrapd", "--enable-gnutls", "--enable-usertools", "--enable-mysql", "--enable-valgrind", "--enable-mmkubernetes"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["make", "-j2"], haltOnFailure=True, name="build (make)"))
# for the time being, we need to turn of ASAN leak checking as it finds quite to
# many irrelevant non-cleanup leaks. In the longer term, we should remove them, but
# there is so much to do...
	# TODO NOT WORKIGN YET !!! factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600))
factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["make", "distcheck", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="distcheck"))
factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["bash", "-c", "cat $(find . -name test-suite.log); pwd; exit 0"], haltOnFailure=False, name="show distcheck test log"))
#rger 2018-06-29 factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=3600, haltOnFailure=True, name="check"))
#factoryRsyslogDockerUbuntu16.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather make check logs"))
# ---


# This is our environment for various LLVM checkers (ASAN, UBSAN, ...)
# We use high optimization level here to ensure we do not run into problems with that
# For the same reason, we activate common security hardening mechanisms
factoryRsyslogDockerUbuntu_18_SAN = BuildFactory()
factoryRsyslogDockerUbuntu_18_SAN.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerUbuntu_18_SAN.addStep(ShellCommand(command=["autoreconf", "-fvi"], haltOnFailure=True, name="autoreconf"))
factoryRsyslogDockerUbuntu_18_SAN.addStep(ShellCommand(command=["bash", "-c", "set -v; set -x; env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-valgrind --without-valgrind-testbench --disable-libfaketime"], env={'CC': 'clang', "CFLAGS":"-g  -fstack-protector -D_FORTIFY_SOURCE=2 -fsanitize=address,undefined,nullability,unsigned-integer-overflow -fno-sanitize-recover=undefined,nullability,unsigned-integer-overflow -g -O3 -fno-omit-frame-pointer -fno-color-diagnostics", "LSAN_OPTIONS":"detect_leaks=0", "UBSAN_OPTIONS":"print_stacktrace=1"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang-UBSAN-ASAN-O3-harden)"))
factoryRsyslogDockerUbuntu_18_SAN.addStep(ShellCommand(command=["make", "-j3", "V=0"], maxTime=1800, haltOnFailure=True, name="make"))
factoryRsyslogDockerUbuntu_18_SAN.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', "LSAN_OPTIONS":"detect_leaks=0", "UBSAN_OPTIONS":"print_stacktrace=1"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5000, haltOnFailure=False, name="make check"))
factoryRsyslogDebian.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/gather_all_logs.sh ] ; then tests/CI/gather_all_logs.sh ; fi"], name="gather check logs"))
# ---


# This is our "make distcheck" environment. Use conservative gcc - most important is that it
# checks if all files are present in tarball.
factoryRsyslogDockerUbuntu18_distcheck = BuildFactory()
factoryRsyslogDockerUbuntu18_distcheck.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerUbuntu18_distcheck.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerUbuntu18_distcheck.addStep(ShellCommand(command=["bash", "-c", "set -v; set -x; env; ./configure $RSYSLOG_CONFIGURE_OPTIONS"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerUbuntu18_distcheck.addStep(ShellCommand(command=["make", "distcheck", "V=0"], env={'USE_AUTO_DEBUG': 'off'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="distcheck"))
factoryRsyslogDockerUbuntu18_distcheck.addStep(ShellCommand(command=["bash", "-c", "cat $(find . -name test-suite.log); pwd; exit 0"], name="show distcheck test log"))
# ---

# EXPERIMENTAL arm - DETAILS WILL CHANGE LATER!
# Note: valgrind is quite slow here and has lots of false positives - so we disable
factoryRsyslogDockerArmUbuntu18 = BuildFactory()
factoryRsyslogDockerArmUbuntu18.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerArmUbuntu18.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerArmUbuntu18.addStep(ShellCommand(command=["bash", "-c", "set -v; set -x; env; ./configure $RSYSLOG_CONFIGURE_OPTIONS --disable-mmdblookup --without-valgrind-testbench --disable-valgrind --disable-elasticsearch-tests"], env={'CC': 'clang', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (clang)"))
factoryRsyslogDockerArmUbuntu18.addStep(ShellCommand(command=["make", "-j4"], haltOnFailure=True, name="make [clang]"))
factoryRsyslogDockerArmUbuntu18.addStep(ShellCommand(command=["make", "check", "V=0"], env={'USE_AUTO_DEBUG': 'off', 'LIBRARY_PATH': '/usr/lib', 'LD_LIBRARY_PATH': '/usr/lib', 'RS_PWORK': '/mnt/rswork/'}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=5400, name="make check"))
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




factoryRsyslogDockerCentos7 = BuildFactory()
factoryRsyslogDockerCentos7.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerCentos7.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerCentos7.addStep(ShellCommand(command=["bash", "-c", "set -v; set -x; env; ./configure $RSYSLOG_CONFIGURE_OPTIONS"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerCentos7.addStep(ShellCommand(command=["bash", "-c", "make distcheck V=0 RS_TESTBENCH_VALGRIND_EXTRA_OPTS=\"--suppressions=$(pwd)/tests/CI/centos7.supp\""], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="distcheck"))
factoryRsyslogDockerCentos7.addStep(ShellCommand(command=["bash", "-c", "cat $(find . -name test-suite.log); pwd; exit 0"], haltOnFailure=False, name="show distcheck test log"))



factoryRsyslogDockerSuse = BuildFactory()
factoryRsyslogDockerSuse.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerSuse.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerSuse.addStep(ShellCommand(command=["bash", "-c", "./configure $RSYSLOG_CONFIGURE_OPTIONS"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerSuse.addStep(ShellCommand(command=["bash", "-c", "make check V=0 RS_TESTBENCH_VALGRIND_EXTRA_OPTS=\"--suppressions=$(pwd)/tests/CI/centos7.supp\""], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=False, name="check"))



# ---
factoryRsyslogDockerFedora28 = BuildFactory()
factoryRsyslogDockerFedora28.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogDockerFedora28.addStep(ShellCommand(command=["autoreconf", "-fvi"], name="autoreconf"))
factoryRsyslogDockerFedora28.addStep(ShellCommand(command=["bash", "-c", "./configure $RSYSLOG_CONFIGURE_OPTIONS --enable-debug"], env={'CC': 'gcc', "CFLAGS":"-g"}, logfiles={"config.log": "config.log"}, haltOnFailure=True, name="configure (gcc)"))
factoryRsyslogDockerFedora28.addStep(ShellCommand(command=["make", "-j2"], lazylogfiles=True, maxTime=1000, haltOnFailure=True, name="make (gcc)"))
factoryRsyslogDockerFedora28.addStep(ShellCommand(command=["bash", "-c", "make check V=0"], env={'USE_AUTO_DEBUG': 'off', "ASAN_OPTIONS": "detect_leaks=0", "ASAN_SYMBOLIZER_PATH": "/usr/bin/llvm-symbolizer-3.4"}, logfiles={"test-suite.log": "tests/test-suite.log"}, lazylogfiles=True, maxTime=7200, haltOnFailure=True, name="check"))
# ---


####### Create Builders

factoryRsyslogStaticAnalyzer = BuildFactory()
factoryRsyslogStaticAnalyzer.addStep(GitHub(repourl=repoGitUrl, mode='full', retryFetch=True))
factoryRsyslogStaticAnalyzer.addStep(ShellCommand(command=["sleep", "2"], name="wait for github"))
factoryRsyslogStaticAnalyzer.addStep(ShellCommand(command=["bash", "-c", "if [ -f tests/CI/buildbot_cleanup.sh ] ; then tests/CI/buildbot_cleanup.sh ; fi"], name="cleanup"))
factoryRsyslogStaticAnalyzer.addStep(ShellCommand(command=["bash", "-c", "devtools/devcontainer.sh devtools/run-static-analyzer.sh"], name="clang static analyzer", logfiles={"report_url": "report_url"}, lazylogfiles=True, env={'RSYSLOG_DEV_CONTAINER':'rsyslog/rsyslog_dev_base_ubuntu:16.04', 'SCAN_BUILD_REPORT_BASEURL': 'http://ubuntu16.rsyslog.com/', 'SCAN_BUILD_REPORT_DIR': '/var/www/html', 'DOCKER_RUN_EXTRA_FLAGS': '-v /var/www/html:/var/www/html -e RSYSLOG_CONFIGURE_EXTRA_OPTS -eSCAN_BUILD_REPORT_DIR -eSCAN_BUILD_REPORT_BASEURL', 'RSYSLOG_CONFIGURE_OPTIONS_EXTRA': "--disable-ksi-ls12 --disable-omhiredis"}, haltOnFailure=True))

####### Create Builders

lc['builders'].append(
	BuilderConfig(name="rsyslog clang static analyzer",
		workernames=["slave-ubuntu16"],
		factory=factoryRsyslogStaticAnalyzer,
		tags=["rsyslog"], 
		properties={
			"github_repo_owner": "rsyslog",
			"github_repo_name": "rsyslog",
		} ))

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
      workernames=["slave-debian9", "slave-debian9-w2"],
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
    BuilderConfig(name="rsyslog raspbian rsyslog",
      workernames=["slave-raspbian"],
      factory=factoryRsyslogRaspbian,
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
    BuilderConfig(name="rsyslog centos7 rsyslog",
      workernames=["slave-centos7", "vm-centos7-5-w1"],
      factory=factoryRsyslogCentos7,
      tags=["rsyslog", "vm"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog fedora23x32 rsyslog",
      workernames=["slave-fedora23x32"],
      factory=factoryRsyslogFedora23,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
#lc['builders'].append(
#    BuilderConfig(name="rsyslog fedora26x64 rsyslog",
#      workernames=["slave-fedora26x64"],
#      factory=factoryRsyslogFedora64,
#      tags=["rsyslog"],
#      properties={
#	"github_repo_owner": "rsyslog",
#	"github_repo_name": "rsyslog",
#      },
#    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog docker-fedora28",
      workernames=["docker-fedora28-w1", "docker-fedora28-w2", "docker-fedora28-w3", "docker-fedora28-w4"],
      factory=factoryRsyslogDockerFedora28,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
    BuilderConfig(name="rsyslog freebsd rsyslog",
      workernames=["slave-freebsd"],
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
      factory=factoryRsyslogSolaris10x64,
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
      workernames=["docker-armbian-w1", "docker-armbian-w2", "docker-armbian-w3", "docker-armbian-w4"],
      factory=factoryRsyslogDockerArmUbuntu18,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-ubuntu16 rsyslog",
     workernames=["docker-ubuntu16", "docker-ubuntu16-w2", "docker-ubuntu16-w3", "docker-ubuntu16-w4"],
      factory=factoryRsyslogDockerUbuntu16,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-ubuntu18-san rsyslog",
     workernames=["docker-ubuntu18-san-w1", "docker-ubuntu18-san-w2", "docker-ubuntu18-san-w3", "docker-ubuntu18-san-w4"],
      factory=factoryRsyslogDockerUbuntu_18_SAN,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-ubuntu18-distcheck rsyslog",
     workernames=["docker-ubuntu18-distcheck-w1","docker-ubuntu18-distcheck-w2", "docker-ubuntu18-distcheck-w3", "docker-ubuntu18-distcheck-w4"],
      factory=factoryRsyslogDockerUbuntu18_distcheck,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-centos7 rsyslog",
      workernames=["docker-centos7", "docker-centos7-w2", "docker-centos7-w3", "docker-centos7-w4"],
      factory=factoryRsyslogDockerCentos7,
      tags=["rsyslog", "docker"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
lc['builders'].append(
   BuilderConfig(name="rsyslog docker-suse-tumbleweed",
      #workernames=[ "docker-suse-tumbleweed-w3_2"],
      workernames=["docker-suse-tumbleweed-w1", "docker-suse-tumbleweed-w2", "docker-suse-tumbleweed-w3", "docker-suse-tumbleweed-w3_2"],
      factory=factoryRsyslogDockerSuse,
      tags=["rsyslog", "docker"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))

# --- Cronjob only
lc['builders'].append(
   BuilderConfig(name="cron " + "rsyslog ubuntu16 rsyslog",
     workernames=["slave-ubuntu16"],
      factory=factoryRsyslogUbuntuCron,
      tags=["rsyslog"],
      properties={
	"github_repo_owner": "rsyslog",
	"github_repo_name": "rsyslog",
      },
    ))
# --- 

lc['schedulers'].append(ForceScheduler(
	name="pull_rsyslog_rsyslog",
	label="1. Pull Requests-rsyslog-rsyslog",
	builderNames=[  "rsyslog clang static analyzer"
			,"rsyslog ubuntu16 rsyslog"
			,"rsyslog debian rsyslog"
			,"rsyslog debian9 rsyslog"
			,"rsyslog raspbian gcc compile"
			,"rsyslog raspbian rsyslog"
			,"rsyslog centos6 rsyslog"
			,"rsyslog centos7 rsyslog"
			,"rsyslog fedora23x32 rsyslog"
			#,"rsyslog fedora26x64 rsyslog"
			,"rsyslog docker-fedora28"
			,"rsyslog freebsd rsyslog"
			,"rsyslog suse rsyslog"
			,"rsyslog solaris10x64 rsyslog"
			,"rsyslog solaris11sparc rsyslog"
			,"rsyslog solaris10sparc rsyslog"
			,"rsyslog solaris11x64 rsyslog"
			,"rsyslog docker-arm-ubuntu18"
			,"rsyslog docker-ubuntu16 rsyslog"
			,"rsyslog docker-ubuntu18-distcheck rsyslog"
			,"rsyslog docker-ubuntu18-san rsyslog"
			,"rsyslog docker-centos7 rsyslog"
			,"rsyslog docker-suse-tumbleweed"
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
			,"rsyslog ubuntu16 rsyslog"
			,"rsyslog debian rsyslog"
			,"rsyslog debian9 rsyslog"
			,"rsyslog raspbian gcc compile"
			,"rsyslog raspbian rsyslog"
			,"rsyslog centos6 rsyslog"
			,"rsyslog centos7 rsyslog"
			,"rsyslog fedora23x32 rsyslog"
			#,"rsyslog fedora26x64 rsyslog"
			,"rsyslog docker-fedora28"
			,"rsyslog freebsd rsyslog"
			,"rsyslog suse rsyslog"
			,"rsyslog solaris10x64 rsyslog"
			,"rsyslog solaris11sparc rsyslog"
			,"rsyslog solaris10sparc rsyslog"
			,"rsyslog solaris11x64 rsyslog"
			,"rsyslog docker-arm-ubuntu18"
			,"rsyslog docker-ubuntu16 rsyslog"
			,"rsyslog docker-ubuntu18-distcheck rsyslog"
			,"rsyslog docker-centos7 rsyslog"
			,"rsyslog docker-suse-tumbleweed"
			],
))

lc['schedulers'].append(SingleBranchScheduler(
	name="github_rsyslog_rsyslog",
	change_filter=filter.ChangeFilter(	category="pull", 
						project="rsyslog/rsyslog"),
	builderNames=[  "rsyslog clang static analyzer"
			,"rsyslog ubuntu16 rsyslog"
			,"rsyslog debian rsyslog"
			,"rsyslog debian9 rsyslog"
			,"rsyslog raspbian gcc compile"
			,"rsyslog raspbian rsyslog"
			,"rsyslog centos6 rsyslog"
			,"rsyslog centos7 rsyslog"
			,"rsyslog fedora23x32 rsyslog"
			#,"rsyslog fedora26x64 rsyslog"
			,"rsyslog docker-fedora28"
			,"rsyslog freebsd rsyslog"
			,"rsyslog suse rsyslog"
			,"rsyslog solaris10x64 rsyslog"
			,"rsyslog solaris11sparc rsyslog"
			,"rsyslog solaris10sparc rsyslog"
			,"rsyslog solaris11x64 rsyslog"
			,"rsyslog docker-arm-ubuntu18"
			,"rsyslog docker-ubuntu16 rsyslog"
			,"rsyslog docker-ubuntu18-distcheck rsyslog"
			,"rsyslog docker-ubuntu18-san rsyslog"
			,"rsyslog docker-centos7 rsyslog"
			,"rsyslog docker-suse-tumbleweed"
		],
))

lc['schedulers'].append(ForceScheduler(
	name="forceallcron_rsyslog_rsyslog",
	label="3. Force All Cron-rsyslog-rsyslog",
	builderNames=[ "cron rsyslog ubuntu16 rsyslog" ],
))
