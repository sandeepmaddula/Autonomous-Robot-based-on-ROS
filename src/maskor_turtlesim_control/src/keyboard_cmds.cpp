#include "ros/ros.h"
#include "std_msgs/String.h"


#include <termios.h>
#include <stdio.h>
#include <signal.h>


#define KEYCODE_R 0x43
#define KEYCODE_L 0x44
#define KEYCODE_U 0x41
#define KEYCODE_D 0x42
#define KEYCODE_Q 0x71
#define KEYCODE_PLUS 0x2B
#define KEYCODE_MINUS 0x2D
#define KEYCODE_k 0x6B
#define KEYCODE_r 0x72
#define KEYCODE_c 0x63
#define KEYCODE_s 0x73
#define KEYCODE_t 0x74
#define KEYCODE_T 0x54

using namespace std;

int kfd = 0;
struct termios cooked, raw;

ros::Publisher pub;

void quit(int sig)
{
  tcsetattr(kfd, TCSANOW, &cooked);
  ros::shutdown();
  exit(0);
}


void keyLoop()
{
  char c;
  bool dirty=false;


  // get the console in raw mode
  tcgetattr(kfd, &cooked);
  memcpy(&raw, &cooked, sizeof(struct termios));
  raw.c_lflag &=~ (ICANON | ECHO);
  // Setting a new line, then end of file
  raw.c_cc[VEOL] = 1;
  raw.c_cc[VEOF] = 2;
  tcsetattr(kfd, TCSANOW, &raw);

  puts("Reading from keyboard");
  puts("---------------------------");


  std_msgs::String string;

  for(;;)
  {
    // get the next event from the keyboard
    if(read(kfd, &c, 1) < 0)
    {
      perror("read():");
      exit(-1);
    }

    switch(c)
    {
      case KEYCODE_L:
        ROS_DEBUG("LEFT");
        string.data = "LEFT";
        dirty = true;
        break;
      case KEYCODE_R:
        ROS_DEBUG("RIGHT");
        string.data = "RIGHT";
        dirty = true;
        break;
      case KEYCODE_U:
        ROS_DEBUG("UP");
        string.data = "UP";
        dirty = true;
        break;
      case KEYCODE_D:
        ROS_DEBUG("DOWN");
        string.data = "DOWN";
        dirty = true;
        break;
      case KEYCODE_PLUS:
        ROS_DEBUG("PLUS");
        string.data = "PLUS";
        dirty = true;
        break;
      case KEYCODE_MINUS:
        ROS_DEBUG("MINUS");
        string.data = "MINUS";
        dirty = true;
        break;
      case KEYCODE_k:
        ROS_DEBUG("KILL");
        string.data = "KILL";
        dirty = true;
        break;
      case KEYCODE_r:
        ROS_DEBUG("RESET");
        string.data = "RESET";
        dirty = true;
        break;
      case KEYCODE_c:
        ROS_DEBUG("CLEAR");
        string.data = "CLEAR";
        dirty = true;
        break;
      case KEYCODE_s:
        ROS_DEBUG("SPAWN");
        string.data = "SPAWN";
        dirty = true;
        break;
      case KEYCODE_t:
        ROS_DEBUG("TELEPORT_REL");
        string.data = "TELEPORT_REL";
        dirty = true;
        break;
      case KEYCODE_T:
        ROS_DEBUG("TELEPORT_ABS");
        string.data = "TELEPORT_ABS";
        dirty = true;
        break;

    }

    if(dirty ==true)
    {
      pub.publish(string);
      dirty=false;
    }
  }


  return;
}





int main(int argc, char **argv)
{
  ros::init(argc, argv, "keyboard_cmds");
  ros::NodeHandle nh;

  pub = nh.advertise<std_msgs::String>("keyboard_cmd", 1);

  signal(SIGINT,quit);

  keyLoop();

  return 0;
}



