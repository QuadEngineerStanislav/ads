# -*- coding: utf-8 -*-
import threading
import time
import math
import rospy
from clover import srv
from std_srvs.srv import Trigger
from sensor_msgs.msg import Range
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clover.srv import SetLEDEffect

rospy.init_node('Hackathon')

set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

cor_x = 0.0
cor_y = 0.0

def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')

        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

def land_pro(z):
    navigate(z=z, speed=0.3, frame_id='aruco_90')
    print("Decrease in height...")
    set_effect(effect='blink', r=255, g=0, b=0)
    while get_telemetry().z > z:
 #       print(get_telemetry().z)
         rospy.sleep(0.1)
    print("Landing!")
    land()

#  image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback, queue_size=1)
#  rospy.spin()


def main():
    print("Takeoff!")
    set_effect(effect='blink', r=255, g=0, b=0)
    navigate_wait(x=0, y=0, z=3, frame_id='body', auto_arm=True)
    navigate_wait(x=0, y=0, z=3, frame_id='aruco_map')
    set_effect(effect='fade', r=0, g=255, b=0)
    print("Flight to the station... ")
    navigate_wait(x=8, y=0, z=3, speed=2, frame_id='aruco_map')

   # navigate(x=get_telemetry().x, y=get_telemetry().y, z=1.7, speed=2, frame_id='map')
    print("Capture")
    rospy.sleep(2)
    print("Taking CarGO!")
    set_effect(effect='blink', r=255, g=0, b=0)
    land()
    rospy.sleep(3)
    set_effect(effect='rainbow')
    print("Wait...")
    rospy.sleep(10)
    print("Takeoff!")
    print("Delivery: S1")
    set_effect(effect='blink', r=255, g=0, b=0)
    navigate_wait(x=0, y=0, z=1.5, speed=1, frame_id='body', auto_arm=True)
    set_effect(effect='fade', r=0, g=255, b=0)
    navigate_wait(x=7, y=8, z=3, speed=2, frame_id='aruco_map')
    print("Capture")
    navigate(x=get_telemetry().x, y=get_telemetry().y, z=1.7, speed=2, frame_id='map')
    
    print("Delivered OK!")
    print("Wait...")
    rospy.sleep(5)

    print("Flight to the station... ")
    navigate_wait(x=0, y=0, z=1.3, speed=1, frame_id='body', auto_arm=True)
    set_effect(effect='fade', r=0, g=255, b=0)
    navigate_wait(x=8, y=0, z=3, speed=2, frame_id='aruco_map')
   # navigate(x=get_telemetry().x, y=get_telemetry().y, z=1.7, speed=2, frame_id='map')
    print("Capture")
    rospy.sleep(2)
    set_effect(effect='blink', r=255, g=0, b=0)
    print("Taking CarGO!")
    land()
    rospy.sleep(2)
    set_effect(effect='rainbow')
    print("Wait...")
    rospy.sleep(10)
    print("Takeoff!")
    print("Delivery: S2")
    set_effect(effect='blink', r=255, g=0, b=0)
    navigate_wait(x=0, y=0, z=1.5, speed=1, frame_id='body', auto_arm=True)
    set_effect(effect='fade', r=0, g=255, b=0)
    navigate_wait(x=1, y=8, z=3, speed=2, frame_id='aruco_map')
    
    print("Capture")
    navigate(x=get_telemetry().x, y=get_telemetry().y, z=1.7, speed=2, frame_id='map')
    
    print("Delivered OK!")
    print("Wait...")
    rospy.sleep(5)
     
    print("RETURN!")
    navigate_wait(x=0, y=0, z=1.3, speed=1, frame_id='body', auto_arm=True)
    set_effect(effect='fade', r=0, g=0, b=255)
    navigate_wait(x=0, y=0, z=2, speed=2, frame_id='aruco_map')
    land_pro(0.2)
main() 


