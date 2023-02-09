SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
docker run -it --rm --net ros --hostname ros-master -e DISPLAY=host.docker.internal:0 -v $SCRIPTPATH/shared:/root/shared --name ros-master ros-master bash -c "source setup.sh; sleep 3; roscore"
