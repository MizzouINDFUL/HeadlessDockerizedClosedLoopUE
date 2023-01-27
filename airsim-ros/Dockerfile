FROM mindful-ros-noetic

# Install AirSim
RUN apt-get update && apt-get install -y ros-noetic-tf2-sensor-msgs ros-noetic-tf2-geometry-msgs ros-noetic-mavros*
RUN . /opt/ros/noetic/setup.sh && \
    git clone https://github.com/Microsoft/AirSim.git && \
    cd AirSim && \
    ./setup.sh && \
    ./build.sh && \
    cd ros && \
    catkin build

# Create a setup script
ADD setup.sh /root/setup.sh

# Set up .bashrc
RUN cp /etc/skel/.bashrc /root/.bashrc
RUN echo "source /root/setup.sh" >> /root/.bashrc