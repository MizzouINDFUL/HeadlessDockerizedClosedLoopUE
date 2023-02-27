docker run -it --rm --net host -e DISPLAY=$DISPLAY -v $(pwd)/shared:/root/shared --name airsim-ros airsim-ros bash -c "~/shared/start_tmux_windows.sh"
