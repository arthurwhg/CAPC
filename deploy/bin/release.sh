#!/bin/sh

PWD=$(pwd)

WORKDIR=$HOME/Documents/sproject/capc/CAPC/deploy
IMAGETAG=arthurwhg/capc:preview
TARGETPLATFORM=linux/amd64

echo "building image by docker ..."
cd $WORKDIR
#docker build --platform linux/amd64 -t $IMAGETAG .
#docker login
sudo docker buildx build --no-cache --platform=$TARGETPLATFORM -t $IMAGETAG -o type=registry .

rc=$?
if [ $rc != 0 ]; then
  echo "Image built failed."
  exit $rc
fi
#echo "Calendar module image was built."
#
#echo pushing image $IMAGETAG ...
#docker push $IMAGETAG
#
#rc=$?
#if [ $rc != 0 ]; then
#  echo "push image failed." $IMAGETAG
#  exit $rc
#fi
echo image $IMAGETAG has been pushed.

cd $PWD