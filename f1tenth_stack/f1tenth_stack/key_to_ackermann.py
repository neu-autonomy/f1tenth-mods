import rclpy

from geometry_msgs.msg import Twist
from rclpy.node import Node


from ackermann_msgs.msg import AckermannDriveStamped

class KeyToAckermann(Node):

    def __init__(self):
        super().__init__('key_to_ackermann')

        self._pub_cmd = self.create_publisher(AckermannDriveStamped, '/ackermann_cmd', 10)
        self._subscriber = self.create_subscription(Twist, '/key_vel', self.key_vel_callback, 10)


    def key_vel_callback(self, msg: Twist):
        x = msg.linear.x

        rad_z = msg.angular.z

        ackermann_msg = AckermannDriveStamped()
        ackermann_msg.drive.speed = x
        ackermann_msg.drive.acceleration = 1.0
        ackermann_msg.drive.jerk = 1.0
        ackermann_msg.drive.steering_angle = rad_z
        ackermann_msg.drive.steering_angle_velocity = 1.0

        self._pub_cmd.publish(ackermann_msg)


def main():
    try:
        rclpy.init()

        node = KeyToAckermann()

        rclpy.spin(node)

        node.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
