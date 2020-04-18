cmake_minimum_required(VERSION 2.8.3)
project(maskor_turtlesim)

find_package(catkin REQUIRED COMPONENTS geometry_msgs message_generation rosconsole roscpp roscpp_serialization roslib rostime std_msgs std_srvs)

find_package(Qt4 4.6 REQUIRED COMPONENTS QtCore QtGui)
include(${QT_USE_FILE})
find_package(Boost REQUIRED COMPONENTS thread)

include_directories(include ${catkin_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS} ${QT_INCLUDE_DIRS})
link_directories(${catkin_LIBRARY_DIRS})

add_message_files(DIRECTORY msg FILES 
                  Color.msg Pose.msg)
add_service_files(DIRECTORY srv FILES
                  Kill.srv
                  SetPen.srv
                  Spawn.srv
                  TeleportAbsolute.srv
                  TeleportRelative.srv)
generate_messages(DEPENDENCIES geometry_msgs std_msgs std_srvs)

catkin_package(CATKIN_DEPENDS geometry_msgs message_runtime std_msgs std_srvs)

set(turtlesim_node_SRCS
  src/turtlesim.cpp
  src/turtle.cpp
  src/turtle_frame.cpp
)
set(turtlesim_node_HDRS
  include/turtlesim/turtle_frame.h
)

qt4_wrap_cpp(turtlesim_node_MOCS ${turtlesim_node_HDRS})


add_executable(maskor_turtlesim_node ${turtlesim_node_SRCS} ${turtlesim_node_MOCS})
target_link_libraries(maskor_turtlesim_node ${QT_LIBRARIES} ${catkin_LIBRARIES} ${Boost_LIBRARIES})
add_dependencies(maskor_turtlesim_node turtlesim_gencpp)

add_executable(maskor_turtle_teleop_key tutorials/teleop_turtle_key.cpp)
target_link_libraries(maskor_turtle_teleop_key ${catkin_LIBRARIES})
add_dependencies(maskor_turtle_teleop_key turtlesim_gencpp)
add_executable(maskor_draw_square tutorials/draw_square.cpp)
target_link_libraries(maskor_draw_square ${catkin_LIBRARIES} ${Boost_LIBRARIES})
add_dependencies(maskor_draw_square turtlesim_gencpp)
add_executable(maskor_mimic tutorials/mimic.cpp)
target_link_libraries(maskor_mimic ${catkin_LIBRARIES})
add_dependencies(maskor_mimic turtlesim_gencpp)

install(TARGETS maskor_turtlesim_node maskor_turtle_teleop_key maskor_draw_square maskor_mimic
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

install(DIRECTORY images
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  FILES_MATCHING PATTERN "*.png" PATTERN "*.svg")
