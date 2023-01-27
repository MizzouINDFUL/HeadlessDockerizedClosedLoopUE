#!/bin/bash
tmux new-session -d -s ROS -n ROS 'source ~/setup.sh; roscore; exec bash'
tmux set-option -gw mouse on
tmux attach-session -t ROS