#!/bin/bash
tmux new-session -d -s AirSim -n AirSim 'source ~/setup.sh; sleep 3; cd ~/shared/launch; roslaunch airsim_all.launch; exec bash'
tmux new-window -n Publisher 'source ~/setup.sh; sleep 6; python3 ~/shared/src/airsim_publisher.py; exec bash'
tmux new-window -n Controller 'source ~/setup.sh; sleep 9; python3 ~/shared/src/waypoint_test_square.py; exec bash'
#tmux new-window -n Collector 'source ~/setup.sh; sleep 12; python3 ~/shared/src/image_extractor.py; exec bash'
tmux set-option -gw mouse on
tmux attach-session -t AirSim
