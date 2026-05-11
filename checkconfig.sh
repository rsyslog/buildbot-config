#!/bin/bash
# Run buildbot commands as the 'buildbot' user with the virtual environment activated
sudo -u buildbot /bin/bash -c 'source /var/lib/buildbot/venv/bin/activate && buildbot checkconfig master'

