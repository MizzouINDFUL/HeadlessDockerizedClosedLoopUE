#!/bin/bash
{
        tmux kill-session -t Sim
	docker stop unreal
	docker rm unreal
        docker stop ros-master
        docker rm ros-master
        docker stop airsim-ros
        docker rm airsim-ros 
} &> /dev/null
