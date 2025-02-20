import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from ultralytics import YOLO
import numpy as np

def camera_cb(data):
       bridge=CvBridge()
       frame = bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
       results = model(frame, show=True, conf=0.5,save=True)
       result = results[0]
       bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
       confidences = np.array(result.boxes.conf.cpu(), dtype="float")
       classes = np.array(result.boxes.cls.cpu(), dtype="int")
       for bbox, confi, cls in zip(bboxes, confidences, classes):
              (x, y, x2, y2) = bbox
              class_id = int(cls)
              object_name = model.names[class_id]
              cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
              cv2.putText(frame, f"{object_name} {confi:.2f}", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)
              cx = (int(x + x2) // 2)
              cy = (int(y + y2) // 2)
              cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
       cv2.imshow("Frame", frame)
       key = cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node('camera') 
    model = YOLO('best1.pt')  # load a custom model
    sub=rospy.Subscriber('image', Image, camera_cb)
    bridge=CvBridge()
    rospy.spin()

# Ros 2 Version

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from ultralytics import YOLO
import numpy as np

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.bridge = CvBridge()
        self.model = YOLO('best1.pt')  # Load the custom model
        self.subscription = self.create_subscription(
            Image,
            'image',
            self.camera_cb,
            10
        )
        self.subscription  # Prevent unused variable warning

    def camera_cb(self, data):
        frame = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
        results = self.model(frame, conf=0.5)
        result = results[0]
        
        bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
        confidences = np.array(result.boxes.conf.cpu(), dtype="float")
        classes = np.array(result.boxes.cls.cpu(), dtype="int")
        
        for bbox, confi, cls in zip(bboxes, confidences, classes):
            (x, y, x2, y2) = bbox
            class_id = int(cls)
            object_name = self.model.names[class_id]
            
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
            cv2.putText(frame, f"{object_name} {confi:.2f}", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)
            cx = (int(x + x2) // 2)
            cy = (int(y + y2) // 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
