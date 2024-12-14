import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('py_test')
        self.get_logger().info('Hello ROS2 aaaaaaaaa')

def main(args = None):
    # intialize ros2 communication (you have to write this line in every node)
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node) # make the program keep running
    # shutdown the communication
    rclpy.shutdown()

if __name__ == "__main__":
    main()