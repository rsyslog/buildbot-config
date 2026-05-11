echo docker image is now in rsyslog dockerhub repository! See master.cfg for name.
echo git clone https://github.com/rsyslog/rsyslog-docker
echo "then: find . -name \"*buildbot*\""
echo after build:
echo  ./build.sh
echo  docker login
echo  docker push -img name-
exit 1
docker pull rsyslog/rsyslog_dev_base_ubuntu:16.04 # ensure we are current!
docker build -t buildslave-rsyslog-ubuntu1604 newcontainer
#docker build -t buildslave-rsyslog-ubuntu1604 - < ubuntu16.dockerfile
