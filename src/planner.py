import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2 as cv
import numpy as np
from std_msgs.msg import Float64
from datetime import datetime
import time
val_prev=0
w=[-2,-1,0,1,2]
cir_x=[int(250+(300*x/4)) for x in range(0,5)]
prev_time=datetime.now().microsecond/1000
line_color = (0, 255, 0) 
line_thickness = 2
start_line=325
line_length=150
kp=0.4
ki=0
kd=0.3
base_speed=-2

def PID(current_val):
  global prev_time
  print('currrent val',current_val)
  e=0-current_val
  
  time_now=datetime.now().microsecond/1000
  #print('time_diff',time_now-prev_time)
  ie=e*(time_now-prev_time)/1000
  de=e/(time_now-prev_time)/1000
  calc_val=kp*e+ki*ie+kd*de
  prev_time=time_now
  left_speed=base_speed-calc_val
  right_speed=base_speed+calc_val
  
  print(left_speed,right_speed)
  return left_speed,right_speed



def get_sensor_val(image,img):
  global val_prev
  pix_val=[]
  total=0
  flag0=True
  flag1=True
  for i in range(0,5):
    if image[700,cir_x[i]]!=0:
      flag0=False
    else:
      flag1=False
    pix_val.append(image[700,cir_x[i]])
    total=total+(image[700,cir_x[i]]*w[i]/255)
    p=int(pix_val[i])
    cv.circle(img,(cir_x[i],700),3,(p,p,p),3)
  #print(pix_val)
  if flag0 or flag1:
    total=val_prev
  else:
    val_prev=total

  print(val_prev)
  return total,img


def proccess_image(raw_image):
  hsv_img=cv.cvtColor(raw_image,cv.COLOR_BGR2HSV)
  lower_yellow = np.array([20, 100, 100])  # Lower HSV values for yellow
  upper_yellow = np.array([40, 255, 255]) 
  yellow_msk=cv.inRange(hsv_img,lower_yellow,upper_yellow)
  yellow_extracted=cv.bitwise_and(raw_image,raw_image,mask=yellow_msk)
  return yellow_extracted

left_pub=rospy.Publisher('/left_wheel_controller/command',Float64,queue_size=1000)
right_pub=rospy.Publisher('/right_wheel_controller/command',Float64,queue_size=1000)
bridge=CvBridge()

def image_callback(data):
  try:
    img=bridge.imgmsg_to_cv2(data,"bgr8")
    img2=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    
    
    image_yellow=proccess_image(img)
    yellow_gray=cv.cvtColor(image_yellow,cv.COLOR_BGR2GRAY)
    _,th_image=cv.threshold(yellow_gray,0,255,cv.THRESH_BINARY)
    #cv.line(image_yellow, (start_line,700), (start_line+line_length,700), line_color, line_thickness)
    '''for i in cir_x:
      pix=int(th_image[i,700])
      cv.circle(image_yellow,(i,700),3,(pix,pix,pix),3)'''
    value,image2=get_sensor_val(th_image,img)
    left,right=PID(value)
    left_pub.publish(Float64(left))
    right_pub.publish(Float64(right))
    
    cv.imshow('Yellow image',th_image)
    cv.imshow('Raw image',image2)

    cv.waitKey(1)
  except Exception as e:
    print(e)

def main():
  rospy.init_node('image_reader')
  image_topic='/camera/image_raw'
  
  rospy.Subscriber(image_topic,Image,image_callback)
  rospy.spin()

if __name__ == "__main__":
  
  
  main()

