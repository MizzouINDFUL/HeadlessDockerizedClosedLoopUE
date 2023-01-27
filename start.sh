tmux new-session -d -s Sim -n Monitor 'python3 python/monitor.py; exec bash'
cd ros-master
tmux new-window -n ROS "docker run -it --rm --net ros --hostname ros-master -e DISPLAY=host.docker.internal:0 -v $(pwd)/shared:/root/shared --name ros-master ros-master bash -c ~/shared/start_ros.sh; exec bash"
cd ..
cd airsim-ros
tmux new-window -n AirSim 'source ~/setup.sh; sleep 3; cd ~/shared/launch; roslaunch airsim_all.launch; exec bash'
tmux new-window -n Publisher 'source ~/setup.sh; sleep 6; python3 ~/shared/src/airsim_publisher.py; exec bash'
tmux new-window -n Controller "source ~/setup.sh; sleep 9; python3 ~/shared/src/$2; exec bash"
cd ..
tmux new-window -n UnrealEngine "./run_docker.sh $1 $2; exec bash"
tmux set-option -gw mouse on
tmux attach-session -t Sim
