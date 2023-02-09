#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
STARTDELAY=25

echo "Preparing Unreal, ROS, and AirSim"
echo "The session will start in $STARTDELAY seconds"
{
	tmux kill-server
	docker stop unreal
	docker rm unreal
	docker stop ros-master
	docker rm ros-master
	docker stop airsim-ros
	docker rm airsim-ros
	rm -rf $SCRIPTPATH/shared/*
} &> /dev/null

tmux new-session -d -s Sim -n UnrealEngine "./run_docker.sh $1 $2; exec bash";
sleep 3
tmux new-window -n Monitor -t Sim:1 "docker exec -w /home/ue4/UnrealEngine/Engine/Binaries/Linux unreal python3 monitor.py; exec bash";
sleep 5
tmux new-window -t Sim:2 -n ROS './ros-master/run.sh; exec bash';
#tmux new-window -t Sim:3 -n Monitor-Host 'python3 monitor_host.py; exec bash';
cd $SCRIPTPATH/airsim-ros/
sleep $STARTDELAY
tmux new-window -t Sim:3 -n AirSim-Master './run_test_square.sh; exec bash';
tmux set-option -gw mouse on;
tmux attach-session -t Sim

tmux kill-server
