docker run -it --rm --net ros --hostname airsim -e DISPLAY=host.docker.internal:0 -v $(pwd)/shared:/root/shared --name airsim-ros airsim-ros
