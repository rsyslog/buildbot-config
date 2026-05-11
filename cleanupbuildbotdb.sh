#!/bin/bash
cd /var/lib/buildbot/master/
sudo -u buildbot /bin/bash -c 'source /var/lib/buildbot/venv/bin/activate && buildbot cleanupdb'
cd /var/lib/buildbot/

