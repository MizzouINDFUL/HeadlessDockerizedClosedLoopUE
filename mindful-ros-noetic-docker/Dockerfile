FROM ubuntu:20.04

# Set timezone
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ/etc/timezone

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    curl \
    git \
    gnupg \
    iproute2 \
    iputils-ping \
    libboost-iostreams-dev \
    libboost-numpy-dev \
    libboost-python-dev \
    libtbb-dev \
    libblosc-dev \
    mesa-utils \
    python3-pip \
    tmux \
    vim \
    wget \
    x11-apps

# Install ROS packages
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros-latest.list' && \
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - && \
    apt-get update && apt-get install -y --no-install-recommends \
    ros-noetic-desktop-full

WORKDIR /root

# Install common Python packages
RUN pip install numpy==1.22 open3d scipy av pyproj

# Set up rosdep
RUN apt-get install -y python3-catkin-tools python3-osrf-pycommon python3-rosdep
RUN rosdep init && rosdep update
