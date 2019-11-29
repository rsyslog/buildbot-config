#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 	* Copyright (C) 2013 Adiscon GmbH.
#	* This file is part of RSyslog
#	* 
#	* rsyslog factory settings
#	*

from buildbot.config import BuilderConfig
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler
from buildbot.changes import filter
from buildbot.plugins import schedulers, util

# Local reference to c
# lc = None

# --- FUNCTIONS
#Append Schedulers Helper Function
def appendSchedulers(lc, szRepoOwner, szRepoProject, szGitBranch):
	#lc['schedulers'].append(SingleBranchScheduler(
			    #name="sched-" + szRepoOwner + "-" + szRepoProject + "-ubuntu",
			    #change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    #treeStableTimer=None,
			    #builderNames=[szRepoProject + " ubuntu " + szRepoOwner]))
	#lc['schedulers'].append(SingleBranchScheduler(
			    #name="sched-cron-" + szRepoOwner + "-" + szRepoProject + "-ubuntu",
			    #change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    #treeStableTimer=None,
			    #builderNames=["cron " + szRepoProject + " ubuntu " + szRepoOwner]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-ubuntu16",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[szRepoProject + " ubuntu16 " + szRepoOwner]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-docker-ubuntu16",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[szRepoProject + " docker-ubuntu16 " + szRepoOwner]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-debian",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[szRepoProject + " debian " + szRepoOwner]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-debian9",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[szRepoProject + " debian9 " + szRepoOwner]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-raspbian",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[szRepoProject + " raspbian " + szRepoOwner]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-centos",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[	szRepoProject + " centos6 " + szRepoOwner, 
						szRepoProject + " centos7 " + szRepoOwner,
						szRepoProject + " fedora26x64 " + szRepoOwner ]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-suse",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[szRepoProject + " suse " + szRepoOwner]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-freebsd12",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[szRepoProject + " freebsd12 " + szRepoOwner]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-solaris",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[
						szRepoProject + " solaris10x64 " + szRepoOwner, 
						szRepoProject + " solaris11sparc " + szRepoOwner, 
						szRepoProject + " solaris10sparc " + szRepoOwner,
						szRepoProject + " solaris11x64 " + szRepoOwner, 
					]))

#Append Builders Helper Function 
def appendBuilders(	lc, szRepoOwner, szRepoProject, 
			factoryDebian, 
			factoryDebian9, 
			factoryRaspbian, 
			factoryFreebsd, 
			factorySuse, 
			factoryCentos6, 
			factoryCentos7, 
			factoryFedora23, 
			factoryFedora64, 
			factoryUbuntu, 
			factoryUbuntu16, 
			factorySolaris10x64, 
			factorySolaris10sparc, 
			factorySolaris11x64, 
			factorySolaris11sparc,
			factoryUbuntuCron, 
			factoryUbuntuDocker,
			factoryUbuntu18Docker,
			factoryUbuntu18on16Docker,
			factoryCentos7Docker):
	#lc['builders'].append(
	   #BuilderConfig(name=szRepoProject + " ubuntu " + szRepoOwner,
	     #workernames=["slave-ubuntu"],
	      #factory=factoryUbuntu, 
	      #tags=[szRepoProject + " " + szRepoOwner], 
	      #properties={
		#"github_repo_owner": szRepoOwner,
		#"github_repo_name": szRepoProject,
	      #},
	    #))
	lc['builders'].append(
	   BuilderConfig(name=szRepoProject + " ubuntu16 " + szRepoOwner,
	     workernames=["slave-ubuntu16"],
	      factory=factoryUbuntu16,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " debian " + szRepoOwner,
	      workernames=["slave-debian"],
	      factory=factoryDebian,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " debian9 " + szRepoOwner,
	      workernames=["slave-debian9"],
	      factory=factoryDebian9,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " raspbian " + szRepoOwner,
	      workernames=["slave-raspbian"],
	      factory=factoryRaspbian,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " centos6 " + szRepoOwner,
	    workernames=["slave-centos6"],
	    factory=factoryCentos6,
	    tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " centos7 " + szRepoOwner,
	      workernames=["slave-centos7"],
	      factory=factoryCentos7,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " fedora26x64 " + szRepoOwner,
	      workernames=["slave-fedora26x64"],
	      factory=factoryFedora64,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " freebsd12 " + szRepoOwner,
	      workernames=["slave-freebsd12"],
	      factory=factoryFreebsd,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " suse " + szRepoOwner,
	      workernames=["slave-suse"],
	      factory=factorySuse,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " solaris10sparc " + szRepoOwner,
	      workernames=["slave-solaris10sparc"],
	      factory=factorySolaris10sparc,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " solaris10x64 " + szRepoOwner,
	      workernames=["slave-solaris10x64"],
	      factory=factorySolaris10x64,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " solaris11sparc " + szRepoOwner,
	      workernames=["slave-solaris11sparc"],
	      factory=factorySolaris11sparc,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	    BuilderConfig(name=szRepoProject + " solaris11x64 " + szRepoOwner,
	      workernames=["slave-solaris11x64"],
	      factory=factorySolaris11x64,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))

	lc['builders'].append(
	   BuilderConfig(name=szRepoProject + " docker-ubuntu16 " + szRepoOwner,
	     workernames=["docker-ubuntu16"],
	      factory=factoryUbuntuDocker,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	   BuilderConfig(name=szRepoProject + " docker-ubuntu18 " + szRepoOwner,
	     workernames=["docker-ubuntu18"],
	      factory=factoryUbuntu18Docker,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
	lc['builders'].append(
	   BuilderConfig(name=szRepoProject + " docker-centos7 " + szRepoOwner,
	     workernames=["docker-centos7"],
	      factory=factoryCentos7Docker,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))

# --- Cronjob only
	lc['builders'].append(
	   BuilderConfig(name="cron " + szRepoProject + " ubuntu16 " + szRepoOwner,
	     workernames=["slave-ubuntu16"],
	      factory=factoryUbuntuCron,
	      tags=[szRepoProject + " " + szRepoOwner],
	      properties={
		"github_repo_owner": szRepoOwner,
		"github_repo_name": szRepoProject,
	      },
	    ))
# --- 

	lc['schedulers'].append(ForceScheduler(
		name="pull_" + szRepoOwner + "_" + szRepoProject,
		label="1. Pull Requests-" + szRepoOwner + "-" + szRepoProject,
		builderNames=[  szRepoProject + " ubuntu16 " + szRepoOwner
				,szRepoProject + " debian " + szRepoOwner
				,szRepoProject + " debian9 " + szRepoOwner
				,szRepoProject + " raspbian " + szRepoOwner
				,szRepoProject + " centos6 " + szRepoOwner
				,szRepoProject + " centos7 " + szRepoOwner
				,szRepoProject + " fedora26x64 " + szRepoOwner
				,szRepoProject + " freebsd12 " + szRepoOwner
				,szRepoProject + " suse " + szRepoOwner
				,szRepoProject + " solaris10x64 " + szRepoOwner
				,szRepoProject + " solaris11sparc " + szRepoOwner
				,szRepoProject + " solaris10sparc " + szRepoOwner
				,szRepoProject + " solaris11x64 " + szRepoOwner
				,szRepoProject + " docker-ubuntu16 " + szRepoOwner
				,szRepoProject + " docker-ubuntu18 " + szRepoOwner
				,szRepoProject + " docker-centos7 " + szRepoOwner
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
		name="forceall_" + szRepoOwner + "_" + szRepoProject,
		label="2. Force All-" + szRepoOwner + "-" + szRepoProject,
		builderNames=[	szRepoProject + " ubuntu16 " + szRepoOwner
				,szRepoProject + " debian " + szRepoOwner
				,szRepoProject + " debian9 " + szRepoOwner
				,szRepoProject + " raspbian " + szRepoOwner
				,szRepoProject + " centos6 " + szRepoOwner
				,szRepoProject + " centos7 " + szRepoOwner
				,szRepoProject + " fedora26x64 " + szRepoOwner
				,szRepoProject + " freebsd12 " + szRepoOwner
				,szRepoProject + " suse " + szRepoOwner
				,szRepoProject + " solaris10x64 " + szRepoOwner
				,szRepoProject + " solaris11sparc " + szRepoOwner
				,szRepoProject + " solaris10sparc " + szRepoOwner
				,szRepoProject + " solaris11x64 " + szRepoOwner
				,szRepoProject + " docker-ubuntu16 " + szRepoOwner
				,szRepoProject + " docker-ubuntu18 " + szRepoOwner
				,szRepoProject + " docker-centos7 " + szRepoOwner
				],
	))
	
	lc['schedulers'].append(SingleBranchScheduler(
		name="github_" + szRepoOwner + "_" + szRepoProject,
		change_filter=filter.ChangeFilter(	category="pull", 
							project=szRepoOwner + "/" + szRepoProject),
		builderNames=[  szRepoProject + " ubuntu16 " + szRepoOwner
				,szRepoProject + " debian " + szRepoOwner
				,szRepoProject + " debian9 " + szRepoOwner
				,szRepoProject + " raspbian " + szRepoOwner
				,szRepoProject + " centos6 " + szRepoOwner
				,szRepoProject + " centos7 " + szRepoOwner
				,szRepoProject + " fedora26x64 " + szRepoOwner
				,szRepoProject + " freebsd12 " + szRepoOwner
				,szRepoProject + " suse " + szRepoOwner
				,szRepoProject + " solaris10x64 " + szRepoOwner
				,szRepoProject + " solaris11sparc " + szRepoOwner
				,szRepoProject + " solaris10sparc " + szRepoOwner
				,szRepoProject + " solaris11x64 " + szRepoOwner
				,szRepoProject + " docker-ubuntu16 " + szRepoOwner
				,szRepoProject + " docker-ubuntu18 " + szRepoOwner
				,szRepoProject + " docker-centos7 " + szRepoOwner
			],
	))

	lc['schedulers'].append(ForceScheduler(
		name="forceallcron_" + szRepoOwner + "_" + szRepoProject,
		label="3. Force All Cron-" + szRepoOwner + "-" + szRepoProject,
		builderNames=[ "cron " + szRepoProject + " ubuntu16 " + szRepoOwner ],
	))

# ----------------------------------------------
####### GITHUB HOOK
import logging
import re
from twisted.internet import defer
from dateutil.parser import parse as dateparse
from buildbot.www.hooks.github import GitHubEventHandler
from twisted.python import log

# Custom GitHubEventHandler for RSyslog
class RsyslogGitHubEventHandler(GitHubEventHandler):
	def _has_skip(self, msg):
		# The message contains the skipping keyword no not.
		# :return type: Bool
		for skip in self.skips:
			if re.search(skip, msg):
				return True
		return False

	def _get_commit_msg(self, repo, sha):
		'''
		:param repo: the repo full name, ``{owner}/{project}``.
		    e.g. ``buildbot/buildbot``
		'''
		headers = {
			'User-Agent': 'Buildbot'
		}
		if self._token:
			headers['Authorization'] = 'token ' + self._token

		url = '/repos/{}/commits/{}'.format(repo, sha)
		http = yield httpclientservice.HTTPClientService.getService(
			self.master, self.github_api_endpoint, headers=headers,
			debug=self.debug, verify=self.verify)
		res = yield http.get(url)
		data = yield res.json()
		msg = data['commit']['message']
		defer.returnValue(msg)

	def handle_pull_request(self, payload, event):
		changes = []
		
		log.msg("RsyslogGitHubEventHandler: ENTER handle_pull_request from ", str(event) )
		log.msg("RsyslogGitHubEventHandler: Repo = ", payload['pull_request']['base']['repo']['full_name'] )
		
		#debug log.msg("RsyslogGitHubEventHandler: Got payload: %s %s", str(payload) )
		
		#Get variables
		number = payload['number']
		refname = 'refs/pull/{}/merge'.format(number)
		commits = payload['pull_request']['commits']
		title = payload['pull_request']['title']
		comments = payload['pull_request']['body']
		repo_full_name = payload['repository']['full_name']
		head_sha = payload['pull_request']['head']['sha']
		
		log.msg('RsyslogGitHubEventHandler: Processing GitHub PR #{}'.format(number), logLevel=logging.DEBUG)

		head_msg = yield self._get_commit_msg(repo_full_name, head_sha)
		'''
		if self._has_skip(head_msg):
			log.msg("RsyslogGitHubEventHandler: GitHub PR #{}, Ignoring: head commit message contains skip pattern".format(number))
			defer.returnValue(([], 'git'))
		'''

		action = payload.get('action')
		if action not in ('opened', 'reopened', 'synchronize'):
			log.msg("RsyslogGitHubEventHandler: GitHub PR #{} {}, ignoring".format(number, action))
			defer.returnValue((changes, 'git'))

		properties = self.extractProperties(payload['pull_request'])
		properties.update({'event': event})
		change = {
			'revision': payload['pull_request']['head']['sha'],
			'when_timestamp': dateparse(payload['pull_request']['created_at']),
			'branch': refname,
			'revlink': payload['pull_request']['_links']['html']['href'],
			'repository': payload['repository']['html_url'],
			'project': repo_full_name,
			'category': 'pull',
			# TODO: Get author name based on login id using txgithub module
			'author': payload['sender']['login'],
			'comments': u'GitHub Pull Request #{0} ({1} commit{2})\n{3}\n{4}'.format(number, commits, 's' if commits != 1 else '', title, comments),
			'properties': properties,
		}

		if callable(self._codebase):
			change['codebase'] = self._codebase(payload)
		elif self._codebase is not None:
			change['codebase'] = self._codebase

		changes.append(change)


		#	yield c['schedulers']["pull_" + szRepoOwner + "_" + szRepoProject].force('user', branch='b', revision='c', repository='d', project='p',

		log.msg("RsyslogGitHubEventHandler: Received {} changes from GitHub PR #{}".format(len(changes), number))
		log.msg("RsyslogGitHubEventHandler: END handle_pull_request")

		# Do some magic here
		defer.returnValue((changes, 'git'))
		#return [changes], 'git'
