#!/bin/bash

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
