#!/bin/bash
# Run buildbot commands as the 'buildbot' user with the virtual environment activated
cd /var/lib/buildbot/
sudo -u buildbot /bin/bash -c 'source /var/lib/buildbot/venv/bin/activate && buildbot stop master'

