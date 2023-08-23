#include<iostream>
#include<string>
#include "ros/ros.h"
#include "std_msgs/Float64.h"
#include "std_msgs/String.h"

ros::Publisher leftPub,rightPub;


void commandsCllback(const std_msgs::String::ConstPtr &msg){
    float l_speed=0;
    float r_speed=0;
    std::string c=msg->data;
    
    std_msgs::Float64 msgLeft,msgRight;
    msgLeft.data=l_speed;
    msgRight.data=r_speed;
    leftPub.publish(msgLeft);
    rightPub.publish(msgRight);
}


int main(int argc,char **argv){
    ros::init(argc,argv,"motorController2");
    ros::NodeHandle n;
    ros::Subscriber commandSub=n.subscribe("motor_commands",1000,commandsCllback);
    leftPub=n.advertise<std_msgs::Float64>("/left_wheel_controller/command",1000);
    rightPub=n.advertise<std_msgs::Float64>("/right_wheel_controller/command",1000);
    ros::spin();
    return 0;
}