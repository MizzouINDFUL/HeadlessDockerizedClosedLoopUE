# `mindful-ros-noetic` Docker Image
This is a Dockerfile that builds a minimal image containing ROS Noetic on Ubuntu 20.04. The image is intended to be used as a parent image for other projects, allowing you to build the ROS part (which takes a long time) only once as part of this image so that you can quickly interate on project-specific Dockerfiles.

### Build Instructions:
- Make sure that Docker Desktop is installed. This will require administrator permissions
    - You must add yourself to the `docker-users` group if you are not already in it. You can do this by running `lusrmgr` and going to Groups>docker-users>Add... and typing your full username (`UM-AD\pawprint`).
- Run `docker build -t mindful-ros-noetic .`
- `mindful-ros-noetic` should now appear under Images>Local in the Docker Desktop app.

### Usage:
- To test the container, you can run `docker run -it --rm mindful-ros-noetic`. This will give you an interactive bash terminal inside of the container. All changes will be deleted once the container stops.
    - You must run `source /opt/ros/noetic/setup.bash` inside of the container to get access to ROS commands.
    - You can stop the container at any time by running the `exit` command.
- The intended use for this is as a parent image for other docker images that contain project-specific code. You can do this by starting your other project's Dockerfile with `FROM mindful-ros-noetic`.
    - Note that this image needs to have been built before the project-specific image can be built for the first time, but it does NOT need to be rebuilt every time the project-specific image is rebuilt.