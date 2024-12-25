#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import NavSatFix
from random import uniform

class Gps_Node(Node) :
    def __init__ (self):
        super().__init__("gps_node")

        self.publisher_ = self.create_publisher(NavSatFix , 'gps_topic' , 10)
        self.timer = self.create_timer(0.5 , self.publish_gps_data)
        self.get_logger().info("Gps Node Has Been Started ")

    def publish_gps_data(self):
        gps_msg = NavSatFix()
        gps_msg.latitude = uniform(-90.0, 90.0)  
        gps_msg.longitude = uniform(-180.0, 180.0)  
        gps_msg.altitude = uniform(0, 100)  
        gps_msg.header.stamp = self.get_clock().now().to_msg()

        self.get_logger().info(f'Publishing GPS data: {gps_msg.latitude}, {gps_msg.longitude}, {gps_msg.altitude}')
        self.publisher_.publish(gps_msg)

def main(args = None):
    rclpy.init(args = args)
    node = Gps_Node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__" :
    main()    