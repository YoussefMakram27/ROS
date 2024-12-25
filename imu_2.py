import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class ImuSubscriber(Node):

    def __init__(self):
        super().__init__('imu_subscriber')
        self.subscription = self.create_subscription(
            Imu,  # Type of message to subscribe to
            'imu_data',  # Topic name
            self.listener_callback,  # Callback function when data is received
            10  # QoS (Quality of Service) history depth
        )
        self.subscription  # Prevent unused variable warning

    def listener_callback(self, msg):
        # Callback that gets called when a message is received
        self.get_logger().info(f'Received IMU data: {msg.linear_acceleration}')

def main(args=None):
    rclpy.init(args=args)
    imu_subscriber = ImuSubscriber()
    rclpy.spin(imu_subscriber)  # Keeps the node running and listening to the topic
    imu_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
