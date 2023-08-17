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

    if(c=="GO"){
        l_speed=-1.0;
        r_speed=-1.0;
    }else if(c=="GO_REALLY_FAST"){
        l_speed=-10;                //radian per sec
        r_speed=-10;

    }else if(c=="BACK"){
        l_speed=0.5;
        r_speed=0.5;

    }else if(c=="LEFT"){
        l_speed=-0.5;
        r_speed=-1.0;
    }else if(c=="RIGHT"){
        l_speed=-1.0;
        r_speed=-0.5;
    }else{
        l_speed=0;
        r_speed=0;
    }
    std_msgs::Float64 msgLeft,msgRight;
    msgLeft.data=l_speed;
    msgRight.data=r_speed;
    leftPub.publish(msgLeft);
    rightPub.publish(msgRight);
}


int main(int argc,char **argv){
    ros::init(argc,argv,"motorController");
    ros::NodeHandle n;
    ros::Subscriber commandSub=n.subscribe("motor_commands",1000,commandsCllback);
    leftPub=n.advertise<std_msgs::Float64>("/left_wheel_controller/command",1000);
    rightPub=n.advertise<std_msgs::Float64>("/right_wheel_controller/command",1000);
    ros::spin();
    return 0;
}