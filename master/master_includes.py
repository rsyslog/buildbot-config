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

# Global reference to access secrets
g = None

# Function to initialize global variables
def init_globals(globalvars_dict):
	global g
	g = globalvars_dict.get('g', {})

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
	#lc['schedulers'].append(SingleBranchScheduler(
			    #name="sched-" + szRepoOwner + "-" + szRepoProject + "-ubuntu24",
			    #change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    #treeStableTimer=None,
			    #builderNames=[szRepoProject + " ubuntu24 " + szRepoOwner]))
#	lc['schedulers'].append(SingleBranchScheduler(
#			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-docker-ubuntu24",
#			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
#			    treeStableTimer=None,
#			    builderNames=[szRepoProject + " docker-ubuntu24 " + szRepoOwner]))
	#lc['schedulers'].append(SingleBranchScheduler(
			    #name="sched-" + szRepoOwner + "-" + szRepoProject + "-debian",
			    #change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    #treeStableTimer=None,
			    #builderNames=[szRepoProject + " debian " + szRepoOwner]))
	#lc['schedulers'].append(SingleBranchScheduler(
			    #name="sched-" + szRepoOwner + "-" + szRepoProject + "-debian9",
			    #change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    #treeStableTimer=None,
			    #builderNames=[szRepoProject + " debian9 " + szRepoOwner]))
	#lc['schedulers'].append(SingleBranchScheduler(
	#		    name="sched-" + szRepoOwner + "-" + szRepoProject + "-raspbian",
	#		    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
	#		    treeStableTimer=None,
	#		    builderNames=[szRepoProject + " raspbian " + szRepoOwner]))
	lc['schedulers'].append(SingleBranchScheduler(
			    name="sched-" + szRepoOwner + "-" + szRepoProject + "-centos",
			    change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    treeStableTimer=None,
			    builderNames=[	szRepoProject + " centos6 " + szRepoOwner, 
						#szRepoProject + " centos7 " + szRepoOwner,
						]))
	#lc['schedulers'].append(SingleBranchScheduler(
			    #name="sched-" + szRepoOwner + "-" + szRepoProject + "-suse",
			    #change_filter=filter.ChangeFilter(project=szRepoProject,branch=szGitBranch),
			    #treeStableTimer=None,
			    #builderNames=[szRepoProject + " suse " + szRepoOwner]))
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
#						szRepoProject + " solaris10x64 " + szRepoOwner, 
						szRepoProject + " solaris11sparc " + szRepoOwner, 
#						szRepoProject + " solaris10sparc " + szRepoOwner,
						szRepoProject + " solaris11x64 " + szRepoOwner, 
					]))

#Append Builders Helper Function 
def appendBuilders(	lc, szRepoOwner, szRepoProject, 
			factoryDebian, 
			factoryRaspbian, 
			factoryFreebsd, 
			factorySuse, 
			factoryCentos6, 
			factoryCentos7, 
			factoryFedora23, 
			factoryFedora64, 
			factoryUbuntu, 
			factoryUbuntu24, 
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
	#lc['builders'].append(
	   #BuilderConfig(name=szRepoProject + " ubuntu24 " + szRepoOwner,
	     #workernames=["slave-ubuntu24"],
	      #factory=factoryUbuntu24,
	      #tags=[szRepoProject + " " + szRepoOwner],
	      #properties={
		#"github_repo_owner": szRepoOwner,
		#"github_repo_name": szRepoProject,
	      #},
	    #))
	#lc['builders'].append(
	    #BuilderConfig(name=szRepoProject + " debian " + szRepoOwner,
	      #workernames=["slave-debian"],
	      #factory=factoryDebian,
	      #tags=[szRepoProject + " " + szRepoOwner],
	      #properties={
		#"github_repo_owner": szRepoOwner,
		#"github_repo_name": szRepoProject,
	      #},
	    #))
#	# SECURITY DISABLED !
#	lc['builders'].append(
#	    BuilderConfig(name=szRepoProject + " raspbian " + szRepoOwner,
#	      workernames=["docker-armbian-compilecheck"], # slave-raspbian"],
#	      factory=factoryRaspbian,
#	      tags=[szRepoProject + " " + szRepoOwner],
#	      properties={
#		"github_repo_owner": szRepoOwner,
#		"github_repo_name": szRepoProject,
#	      },
#	    ))
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
	#lc['builders'].append(
	#    BuilderConfig(name=szRepoProject + " centos7 " + szRepoOwner,
	#      workernames=["vm-centos7-5-w1"],
	#      factory=factoryCentos7,
	#      tags=[szRepoProject + " " + szRepoOwner],
	#      properties={
	#	"github_repo_owner": szRepoOwner,
	#	"github_repo_name": szRepoProject,
	#      },
	#    ))
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
	#lc['builders'].append(
	    #BuilderConfig(name=szRepoProject + " suse " + szRepoOwner,
	      #workernames=["slave-suse"],
	      #factory=factorySuse,
	      #tags=[szRepoProject + " " + szRepoOwner],
	      #properties={
		#"github_repo_owner": szRepoOwner,
		#"github_repo_name": szRepoProject,
	      #},
	    #))
#	lc['builders'].append(
#	    BuilderConfig(name=szRepoProject + " solaris10sparc " + szRepoOwner,
#	      workernames=["slave-solaris10sparc"],
#	      factory=factorySolaris10sparc,
#	      tags=[szRepoProject + " " + szRepoOwner],
#	      properties={
#		"github_repo_owner": szRepoOwner,
#		"github_repo_name": szRepoProject,
#	      },
#	    ))
#	lc['builders'].append(
#	    BuilderConfig(name=szRepoProject + " solaris10x64 " + szRepoOwner,
#	      workernames=["slave-solaris10x64"],
#	      factory=factorySolaris10x64,
#	      tags=[szRepoProject + " " + szRepoOwner],
#	      properties={
#		"github_repo_owner": szRepoOwner,
#		"github_repo_name": szRepoProject,
#	      },
#	    ))
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
#	lc['builders'].append(
#	   BuilderConfig(name=szRepoProject + " docker-ubuntu24 " + szRepoOwner,
#	     workernames=["docker-ubuntu24"],
#	      factory=factoryUbuntuDocker,
#	      tags=[szRepoProject + " " + szRepoOwner],
#	      properties={
#		"github_repo_owner": szRepoOwner,
#		"github_repo_name": szRepoProject,
#	      },
#	    ))
#	lc['builders'].append(
#	   BuilderConfig(name=szRepoProject + " docker-ubuntu18 " + szRepoOwner,
#	     workernames=["docker-ubuntu18"],
#	      factory=factoryUbuntu18Docker,
#	      tags=[szRepoProject + " " + szRepoOwner],
#	      properties={
#		"github_repo_owner": szRepoOwner,
#		"github_repo_name": szRepoProject,
#	      },
#	    ))
#	lc['builders'].append(
#	   BuilderConfig(name=szRepoProject + " docker-centos7 " + szRepoOwner,
#	     workernames=["docker-centos7"],
#	      factory=factoryCentos7Docker,
#	      tags=[szRepoProject + " " + szRepoOwner],
#	      properties={
#		"github_repo_owner": szRepoOwner,
#		"github_repo_name": szRepoProject,
#	      },
#	    ))

# --- Cronjob only
	#lc['builders'].append(
	   #BuilderConfig(name="cron " + szRepoProject + " ubuntu24 " + szRepoOwner,
	     #workernames=["slave-ubuntu24"],
	      #factory=factoryUbuntuCron,
	      #tags=[szRepoProject + " " + szRepoOwner],
	      #properties={
		#"github_repo_owner": szRepoOwner,
		#"github_repo_name": szRepoProject,
	      #},
	    #))
# --- 

	lc['schedulers'].append(ForceScheduler(
		name="pull_" + szRepoOwner + "_" + szRepoProject,
		label="1. Pull Requests-" + szRepoOwner + "-" + szRepoProject,
		builderNames=[  #szRepoProject + " ubuntu24 " + szRepoOwner
				#,szRepoProject + " debian " + szRepoOwner
#				,szRepoProject + " raspbian " + szRepoOwner
				szRepoProject + " centos6 " + szRepoOwner
				#,szRepoProject + " suse " + szRepoOwner
				,szRepoProject + " solaris11sparc " + szRepoOwner
				,szRepoProject + " solaris11x64 " + szRepoOwner
#				,szRepoProject + " docker-ubuntu24 " + szRepoOwner
#				,szRepoProject + " docker-ubuntu18 " + szRepoOwner
#				,szRepoProject + " docker-centos7 " + szRepoOwner
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
		builderNames=[	#szRepoProject + " ubuntu24 " + szRepoOwner
				#,szRepoProject + " debian " + szRepoOwner
#				,szRepoProject + " raspbian " + szRepoOwner
				#szRepoProject + " suse " + szRepoOwner
				szRepoProject + " solaris11sparc " + szRepoOwner
				,szRepoProject + " solaris11x64 " + szRepoOwner
#				,szRepoProject + " docker-ubuntu24 " + szRepoOwner
#				,szRepoProject + " docker-ubuntu18 " + szRepoOwner
#				,szRepoProject + " docker-centos7 " + szRepoOwner
				],
	))
	
	lc['schedulers'].append(SingleBranchScheduler(
		name="github_" + szRepoOwner + "_" + szRepoProject,
		change_filter=filter.ChangeFilter(	category="pull", 
							project=szRepoOwner + "/" + szRepoProject),
		builderNames=[  #szRepoProject + " ubuntu24 " + szRepoOwner
				#,szRepoProject + " debian " + szRepoOwner
#				,szRepoProject + " raspbian " + szRepoOwner
				#szRepoProject + " suse " + szRepoOwner
				szRepoProject + " solaris11sparc " + szRepoOwner
				,szRepoProject + " solaris11x64 " + szRepoOwner
#				,szRepoProject + " docker-ubuntu24 " + szRepoOwner
#				,szRepoProject + " docker-ubuntu18 " + szRepoOwner
#				,szRepoProject + " docker-centos7 " + szRepoOwner
			],
	))


# ----------------------------------------------
####### GITHUB HOOK
import logging
import re
import fnmatch
from twisted.internet import defer
from dateutil.parser import parse as dateparse
from buildbot.www.hooks.github import GitHubEventHandler
from buildbot.util import httpclientservice
from twisted.python import log

# Custom GitHubEventHandler for RSyslog
class RsyslogGitHubEventHandler(GitHubEventHandler):
	# File patterns to ignore (similar to GitHub Actions paths-ignore)
	IGNORE_PATTERNS = [
		'ChangeLog',
		'*.md',
		'*.txt',
		'*.rst',
		'*.yaml',
		'*.yml',
		'*.json',
		'*.xml',
		'*.html',
		'*.sh',  # Ignore all .sh files by default
		'.github',  # Ignore .github folder
	]
	
	# File patterns that should trigger builds (override ignore patterns)
	BUILD_PATTERNS = [
		'tests/*.sh',  # Only tests/*.sh files should trigger builds
	]

	def _has_skip(self, msg):
		# The message contains the skipping keyword no not.
		# :return type: Bool
		for skip in self.skips:
			if re.search(skip, msg):
				return True
		return False

	@defer.inlineCallbacks
	def _get_pr_files(self, repo, pr_number):
		'''
		Get list of files changed in a PR
		:param repo: the repo full name, ``{owner}/{project}``
		:param pr_number: PR number
		:return: list of file paths
		'''
		log.msg("RsyslogGitHubEventHandler: DEBUG - Getting PR files for repo: {}, PR: {}".format(repo, pr_number))
		
		headers = {
			'User-Agent': 'Buildbot'
		}
		if g['secret_GITHUB_TOKEN']:
			headers['Authorization'] = 'token ' + g['secret_GITHUB_TOKEN']
			log.msg("RsyslogGitHubEventHandler: DEBUG - Using GitHub token authentication")
		else:
			log.msg("RsyslogGitHubEventHandler: DEBUG - No GitHub token found")

		url = '/repos/{}/pulls/{}/files'.format(repo, pr_number)
		log.msg("RsyslogGitHubEventHandler: DEBUG - Making API call to: {}".format(url))
		
		http = yield httpclientservice.HTTPClientService.getService(
			self.master, self.github_api_endpoint, headers=headers,
			debug=self.debug, verify=self.verify)
		res = yield http.get(url)
		log.msg("RsyslogGitHubEventHandler: DEBUG - API response status: {}".format(res.code))
		
		data = yield res.json()
		log.msg("RsyslogGitHubEventHandler: DEBUG - Raw API response data: {}".format(str(data)[:500] + "..." if len(str(data)) > 500 else str(data)))
		
		files = [f['filename'] for f in data]
		log.msg("RsyslogGitHubEventHandler: DEBUG - Extracted filenames: {}".format(files))
		defer.returnValue(files)

	def _should_skip_files(self, files):
		'''
		Check if PR should be skipped based on changed files
		:param files: list of file paths
		:return: True if all files match ignore patterns
		'''
		log.msg("RsyslogGitHubEventHandler: DEBUG - Checking if files should be skipped")
		log.msg("RsyslogGitHubEventHandler: DEBUG - Files to check: {}".format(files))
		log.msg("RsyslogGitHubEventHandler: DEBUG - Ignore patterns: {}".format(self.IGNORE_PATTERNS))
		log.msg("RsyslogGitHubEventHandler: DEBUG - Build patterns: {}".format(self.BUILD_PATTERNS))
		
		if not files:
			log.msg("RsyslogGitHubEventHandler: DEBUG - No files found, not skipping")
			return False
			
		build_trigger_files = []
		ignored_files = []
		
		for filename in files:
			log.msg("RsyslogGitHubEventHandler: DEBUG - Checking file: {}".format(filename))
			
			# First check if file matches any build pattern (these override ignore patterns)
			matches_build_pattern = False
			for pattern in self.BUILD_PATTERNS:
				full_match = fnmatch.fnmatch(filename, pattern)
				log.msg("RsyslogGitHubEventHandler: DEBUG - Build pattern '{}' vs '{}': full_match={}".format(
					pattern, filename, full_match))
				
				if full_match:
					matches_build_pattern = True
					log.msg("RsyslogGitHubEventHandler: DEBUG - File '{}' matches build pattern '{}'".format(filename, pattern))
					break
			
			if matches_build_pattern:
				build_trigger_files.append(filename)
				log.msg("RsyslogGitHubEventHandler: DEBUG - File '{}' will trigger build".format(filename))
				continue
			
			# If no build pattern matched, check if file matches any ignore pattern
			matches_ignore = False
			for pattern in self.IGNORE_PATTERNS:
				# Check both full path and basename
				full_match = fnmatch.fnmatch(filename, pattern)
				basename_match = fnmatch.fnmatch(filename.split('/')[-1], pattern)
				
				log.msg("RsyslogGitHubEventHandler: DEBUG - Ignore pattern '{}' vs '{}': full_match={}, basename_match={}".format(
					pattern, filename, full_match, basename_match))
				
				if full_match or basename_match:
					matches_ignore = True
					log.msg("RsyslogGitHubEventHandler: DEBUG - File '{}' matches ignore pattern '{}'".format(filename, pattern))
					break
			
			# Categorize files
			if matches_ignore:
				ignored_files.append(filename)
				log.msg("RsyslogGitHubEventHandler: DEBUG - File '{}' will be ignored".format(filename))
			else:
				build_trigger_files.append(filename)
				log.msg("RsyslogGitHubEventHandler: DEBUG - File '{}' does NOT match any ignore pattern and will trigger build".format(filename))
		
		log.msg("RsyslogGitHubEventHandler: DEBUG - Summary: {} ignored files, {} build trigger files".format(
			len(ignored_files), len(build_trigger_files)))
		log.msg("RsyslogGitHubEventHandler: DEBUG - Ignored files: {}".format(ignored_files))
		log.msg("RsyslogGitHubEventHandler: DEBUG - Build trigger files: {}".format(build_trigger_files))
		
		# If any file should trigger a build, don't skip
		should_skip = len(build_trigger_files) == 0
		log.msg("RsyslogGitHubEventHandler: DEBUG - Should skip build: {}".format(should_skip))
		
		return should_skip

	@defer.inlineCallbacks
	def _get_commit_msg(self, repo, sha):
		'''
		:param repo: the repo full name, ``{owner}/{project}``.
		    e.g. ``buildbot/buildbot``
		'''
		headers = {
			'User-Agent': 'Buildbot'
		}
		if g['secret_GITHUB_TOKEN']:
			headers['Authorization'] = 'token ' + g['secret_GITHUB_TOKEN']

		url = '/repos/{}/commits/{}'.format(repo, sha)
		http = yield httpclientservice.HTTPClientService.getService(
			self.master, self.github_api_endpoint, headers=headers,
			debug=self.debug, verify=self.verify)
		res = yield http.get(url)
		data = yield res.json()
		msg = data['commit']['message']
		defer.returnValue(msg)

	@defer.inlineCallbacks
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

		pr_files = None
		# Check if only documentation files are changed
		log.msg("RsyslogGitHubEventHandler: DEBUG - Starting file filtering check for PR #{}".format(number))
		try:
			log.msg("RsyslogGitHubEventHandler: DEBUG - Calling _get_pr_files for repo: {}, PR: {}".format(repo_full_name, number))
			pr_files = yield self._get_pr_files(repo_full_name, number)
			log.msg("RsyslogGitHubEventHandler: DEBUG - Successfully retrieved {} files for PR #{}".format(len(pr_files), number))
			log.msg("RsyslogGitHubEventHandler: ALL FILES CHANGED IN PR #{}: {}".format(number, pr_files))
			
			log.msg("RsyslogGitHubEventHandler: DEBUG - Calling _should_skip_files with {} files".format(len(pr_files)))
			should_skip = self._should_skip_files(pr_files)
			log.msg("RsyslogGitHubEventHandler: DEBUG - _should_skip_files returned: {}".format(should_skip))
			
			if should_skip:
				log.msg("RsyslogGitHubEventHandler: GitHub PR #{}, SKIPPING BUILD: only documentation files changed".format(number))
				
				# Post status to GitHub indicating build was skipped
				yield self._post_github_status(
					repo_full_name, 
					head_sha, 
					'success', 
					'Build skipped - only documentation files changed',
					'buildbot/file-filter'
				)
				
				log.msg("RsyslogGitHubEventHandler: DEBUG - Returning empty changes list to skip build")
				defer.returnValue(([], 'git'))
			else:
				log.msg("RsyslogGitHubEventHandler: GitHub PR #{}, PROCEEDING WITH BUILD: non-documentation files changed".format(number))
				
				# Post status to GitHub indicating build will proceed
				yield self._post_github_status(
					repo_full_name, 
					head_sha, 
					'success', 
					'Build triggered - code files changed',
					'buildbot/file-filter'
				)
				
		except Exception as e:
			log.msg("RsyslogGitHubEventHandler: ERROR - Could not check PR files for #{}: {}".format(number, str(e)))
			log.msg("RsyslogGitHubEventHandler: DEBUG - Exception details: {}".format(repr(e)))
			import traceback
			log.msg("RsyslogGitHubEventHandler: DEBUG - Traceback: {}".format(traceback.format_exc()))
			# Continue with build if file check fails

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
			'files': pr_files if pr_files is not None else [],
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

		_files_for_change = change['files']
		log.msg(
			"RsyslogGitHubEventHandler: DEBUG - PR #{} change['files'] count={} (for scheduler filters): {}".format(
				number, len(_files_for_change), _files_for_change))

		#	yield c['schedulers']["pull_" + szRepoOwner + "_" + szRepoProject].force('user', branch='b', revision='c', repository='d', project='p',

		log.msg("RsyslogGitHubEventHandler: Received {} changes from GitHub PR #{}".format(len(changes), number))
		log.msg("RsyslogGitHubEventHandler: END handle_pull_request")

		# Do some magic here
		defer.returnValue((changes, 'git'))
		#return [changes], 'git'

	@defer.inlineCallbacks
	def _post_github_status(self, repo, sha, state, description, context="buildbot/file-filter"):
		"""
		Post a status update to GitHub
		:param repo: the repo full name, ``{owner}/{project}``
		:param sha: commit SHA
		:param state: one of 'error', 'failure', 'pending', 'success'
		:param description: status description
		:param context: status context (appears in PR checks)
		"""
		log.msg("RsyslogGitHubEventHandler: Posting GitHub status - repo: {}, sha: {}, state: {}, context: {}".format(
			repo, sha, state, context))
		
		headers = {
			'User-Agent': 'Buildbot',
			'Accept': 'application/vnd.github.v3+json'
		}
		if g['secret_GITHUB_TOKEN']:
			headers['Authorization'] = 'token ' + g['secret_GITHUB_TOKEN']
			log.msg("RsyslogGitHubEventHandler: Using GitHub token for status update")
		else:
			log.msg("RsyslogGitHubEventHandler: WARNING - No GitHub token found for status update")
			defer.returnValue(None)

		url = '/repos/{}/statuses/{}'.format(repo, sha)
		payload = {
			'state': state,
			'description': description,
			'context': context
		}
		
		log.msg("RsyslogGitHubEventHandler: Making status API call to: {} with payload: {}".format(url, payload))
		
		try:
			http = yield httpclientservice.HTTPClientService.getService(
				self.master, self.github_api_endpoint, headers=headers,
				debug=self.debug, verify=self.verify)
			res = yield http.post(url, json=payload)
			log.msg("RsyslogGitHubEventHandler: Status API response: {}".format(res.code))
			
			if res.code in (200, 201):
				log.msg("RsyslogGitHubEventHandler: Successfully posted GitHub status")
			else:
				log.msg("RsyslogGitHubEventHandler: GitHub status API returned code: {}".format(res.code))
				
		except Exception as e:
			log.msg("RsyslogGitHubEventHandler: ERROR posting GitHub status: {}".format(str(e)))
			import traceback
			log.msg("RsyslogGitHubEventHandler: Status error traceback: {}".format(traceback.format_exc()))


# Paths under which PR changes do not warrant Solaris builders (plugins not built
# on Solaris, etc.). Same fnmatch rules as IGNORE_PATTERNS: match full path or basename.
SOLARIS_PR_IGNORE_PATTERNS = [
	'plugins/omkafka/*',
	'plugins/imkafka/*',
	'plugins/omotel/*',
	'plugins/mmjsontransform/*',
	'plugins/translate.c/*',
]


def _solaris_pr_path_ignored(filename):
	for pattern in SOLARIS_PR_IGNORE_PATTERNS:
		base = filename.split('/')[-1]
		full_match = fnmatch.fnmatch(filename, pattern)
		base_match = fnmatch.fnmatch(base, pattern)
		log.msg(
			"SolarisPRFilter: DEBUG - ignore pattern '{}' vs '{}': full_match={}, basename_match={}".format(
				pattern, filename, full_match, base_match))
		if full_match or base_match:
			log.msg(
				"SolarisPRFilter: DEBUG - path '{}' matches SOLARIS_PR_IGNORE_PATTERNS entry '{}'".format(
					filename, pattern))
			return True
	return False


def change_triggers_rsyslog_solaris_pr(change):
	"""
	True if this change should schedule rsyslog Solaris PR builders: at least one
	changed file is .c/.h and not covered by SOLARIS_PR_IGNORE_PATTERNS.
	"""
	files = change.files or []
	proj = getattr(change, 'project', '')
	cat = getattr(change, 'category', '')
	log.msg(
		"SolarisPRFilter: DEBUG - change_triggers_rsyslog_solaris_pr project={!r} category={!r} file_count={}".format(
			proj, cat, len(files)))
	log.msg("SolarisPRFilter: DEBUG - SOLARIS_PR_IGNORE_PATTERNS: {}".format(SOLARIS_PR_IGNORE_PATTERNS))
	if not files:
		log.msg("SolarisPRFilter: DEBUG - no files on change; Solaris PR builders will not run")
		return False
	for filename in files:
		base = filename.split('/')[-1].lower()
		if base.endswith('.c'):
			pass
		elif base.endswith('.h') and not base.endswith('.hpp'):
			pass
		else:
			log.msg(
				"SolarisPRFilter: DEBUG - skip non-C/H file for Solaris gate: {}".format(filename))
			continue
		log.msg(
			"SolarisPRFilter: DEBUG - candidate .c/.h for Solaris: {}".format(filename))
		if _solaris_pr_path_ignored(filename):
			log.msg(
				"SolarisPRFilter: DEBUG - file excluded by Solaris ignore list: {}".format(filename))
			continue
		log.msg(
			"SolarisPRFilter: DEBUG - MATCH: Solaris PR builders allowed (file: {})".format(filename))
		return True
	log.msg("SolarisPRFilter: DEBUG - no qualifying .c/.h after ignores; Solaris PR builders will not run")
	return False
