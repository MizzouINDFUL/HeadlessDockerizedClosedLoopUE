FROM mindful-ros-noetic

# Create a setup script
ADD setup.sh /root/setup.sh

# Set up .bashrc
RUN cp /etc/skel/.bashrc /root/.bashrc
RUN echo "source /root/setup.sh" >> /root/.bashrc