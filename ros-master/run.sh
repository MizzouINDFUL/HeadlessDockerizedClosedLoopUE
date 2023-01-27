docker run -it --rm --net ros --hostname ros-master -e DISPLAY=host.docker.internal:0 -v $(pwd)/shared:/root/shared --name ros-master ros-master bash -c "~/shared/start_ros.sh"
