#!/bin/bash
#
cd /var/lib/buildbot
cp buildbot.service /etc/systemd/system/buildbot.service

systemctl daemon-reload
systemctl enable buildbot.service
systemctl start buildbot.service

