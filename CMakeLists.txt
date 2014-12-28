cmake_minimum_required(VERSION 2.8.3)
project(ros_package_web_server)

find_package(catkin REQUIRED)

catkin_package()

#############
## Install ##
#############

install(PROGRAMS
  scripts/server.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
