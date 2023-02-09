#!/bin/bash
tmux new-window -t Sim:2 -n ROS 'source ~/setup.sh; roscore; exec bash'
