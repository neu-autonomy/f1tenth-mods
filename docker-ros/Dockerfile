FROM ros:humble

# ros stuff
RUN apt-get update && apt-get install -y \
    git \
    vim \
    nano \
    build-essential \
    openssh-client \
    ros-humble-ackermann-msgs \
    ros-humble-diagnostic-updater \
    ros-humble-asio-cmake-module \
    ros-humble-serial-driver \
    ros-humble-rviz2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source source ~/austin/ros2_ws/install/setup.bash" >> ~/.bashrc