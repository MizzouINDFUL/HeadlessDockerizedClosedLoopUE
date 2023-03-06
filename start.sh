#!/bin/bash

eval $(./parse_yaml.sh settings.yml)
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
STARTDELAY=25
MODULES=("Unreal")

if [ $ros == true ]; then
	# MODULES+=", ROS"
	if [ $airsim == true ]; then
		MODULES+=", ROS, and AirSim"
	else
		MODULES+=" and ROS"
	fi
elif [ $airsim == true ]; then
	MODULES+=" and AirSim"
fi

echo "Preparing ${MODULES[@]}"
echo "A new tmux session will be created with the name 'Sim' in about 10 seconds."
{
	tmux kill-session -t Sim
	docker stop unreal
	docker rm unreal
	docker stop ros-master
	docker rm ros-master
	docker stop airsim-ros
	docker rm airsim-ros
	rm -rf $SCRIPTPATH/shared/*.txt
} &> /dev/null

if [ $use_ue_docker == true ]; then
	tmux new-session -d -s Sim -n UnrealEngine "./run_ue_docker.sh $project_path $include_mindful_lib $include_python_script $num_simulations $editor_modifier_script; exec bash";
else
	tmux new-session -d -s Sim -n UnrealEngine "cd $custom_ue_path; ./UE4Editor-Cmd $project_path -game -RenderOffscreen; exec bash";
fi

# tmux new-window -n Monitor -t Sim:1 "docker exec -w /home/ue4/UnrealEngine/Engine/Binaries/Linux -u root:root unreal python3 monitor.py; exec bash";
tmux new-window -n Monitor -t Sim:1 "python3 monitor_v2.py; exec bash";

if [ $ros == true ]; then
	sleep 2
	tmux new-window -t Sim:2 -n ROS './ros-master/run.sh; exec bash';
fi

# if [ $airsim == true ]; then
# 	cd $SCRIPTPATH/airsim-ros/
# 	sleep $STARTDELAY
# 	tmux new-window -t Sim:3 -n AirSim-Master './run_test_square.sh; exec bash';
# fi
tmux set-option -gw mouse on;
tmux attach-session -t Sim

tmux kill-server
