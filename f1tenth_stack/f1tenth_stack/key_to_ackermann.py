import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from ackermann_msgs.msg import AckermannDriveStamped

import time


class VelocityScaler:
    def __init__(self, min_val: float, max_val: float, steps: int = 3, init_step: int = 2):
        assert 1 <= init_step <= steps
        self.min = min_val
        self.max = max_val
        self.steps = steps
        self.step = init_step

        if steps > 1:
            self.step_incr = (max_val - min_val) / (steps - 1)
        else:
            self.step_incr = 0

    def set_step(self, step):
        self.step = max(1, min(self.steps, step))

    def scale(self, value: float) -> float:
        value = max(-1.0, min(1.0, value))
        max_val = self.min + self.step_incr * (self.step - 1)
        return value * max_val


class KeyToAckermann(Node):

    def __init__(self):
        super().__init__('key_to_ackermann')

        self._pub_cmd = self.create_publisher(AckermannDriveStamped, '/ackermann_cmd', 10)
        self._subscriber = self.create_subscription(Twist, '/key_vel', self.key_vel_callback, 10)

        self.linear_scaler = VelocityScaler(min_val=0.2, max_val=2.0, steps=3, init_step=2)
        self.angular_scaler = VelocityScaler(min_val=0.2, max_val=1.2, steps=3, init_step=2)

        self.get_logger().info("KeyToAckermann node initialized with velocity scaling.")

        self.timeout = 0.3 
        self.last_valid_time = time.time()
        self.last_valid_x = 0.0
        self.last_valid_z = 0.0

    def key_vel_callback(self, msg: Twist):
        current_time = time.time()
        x = msg.linear.x
        z = msg.angular.z

        if x == 0.0 and z == 0.0:
            if (current_time - self.last_valid_time) < self.timeout:
                x = self.last_valid_x
                z = self.last_valid_z
            else:
                self.last_valid_x = 0.0
                self.last_valid_z = 0.0
        else:
            self.last_valid_time = current_time
            self.last_valid_x = x
            self.last_valid_z = z

        scaled_speed = self.linear_scaler.scale(x)
        scaled_steering = self.angular_scaler.scale(z)

        ackermann_msg = AckermannDriveStamped()
        ackermann_msg.drive.speed = scaled_speed
        ackermann_msg.drive.acceleration = 1.0
        ackermann_msg.drive.jerk = 1.0
        ackermann_msg.drive.steering_angle = scaled_steering
        ackermann_msg.drive.steering_angle_velocity = 1.0

        self._pub_cmd.publish(ackermann_msg)


def main():
    rclpy.init()
    node = KeyToAckermann()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
