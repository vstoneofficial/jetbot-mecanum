import time
import traitlets
from traitlets.config.configurable import SingletonConfigurable
from .MecanumRover_MotorDriver import MecanumRover_MotorDriver
from .motor import Motor


class Robot(SingletonConfigurable):

    f_left_motor = traitlets.Instance(Motor)
    r_left_motor = traitlets.Instance(Motor)
    f_right_motor = traitlets.Instance(Motor)
    r_right_motor = traitlets.Instance(Motor)

    # config
    f_left_motor_channel = traitlets.Integer(default_value=1).tag(config=True)
    f_left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    f_right_motor_channel = traitlets.Integer(default_value=2).tag(config=True)
    f_right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    r_left_motor_channel = traitlets.Integer(default_value=3).tag(config=True)
    r_left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    r_right_motor_channel = traitlets.Integer(default_value=4).tag(config=True)
    r_right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)

    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        self.motor_driver = MecanumRover_MotorDriver()
        self.f_right_motor = Motor(self.motor_driver, channel=self.f_right_motor_channel, alpha=self.f_right_motor_alpha)
        self.f_left_motor = Motor(self.motor_driver, channel=self.f_left_motor_channel, alpha=self.f_left_motor_alpha)
        self.r_right_motor = Motor(self.motor_driver, channel=self.r_right_motor_channel, alpha=self.r_right_motor_alpha)
        self.r_left_motor = Motor(self.motor_driver, channel=self.r_left_motor_channel, alpha=self.r_left_motor_alpha)

    def set_motors(self, f_left_speed, f_right_speed, r_left_speed, r_right_speed):
        self.f_left_motor._write_value(f_left_speed)
        self.f_right_motor._write_value(f_right_speed)
        self.r_left_motor._write_value(r_left_speed)
        self.r_right_motor._write_value(r_right_speed)

    def forward(self, speed=1.0, duration=None):
        self.f_left_motor._write_value(speed)
        self.f_right_motor._write_value(speed)
        self.r_left_motor._write_value(speed)
        self.r_right_motor._write_value(speed)

    def backward(self, speed=1.0):
        self.f_left_motor._write_value(-speed)
        self.f_right_motor._write_value(-speed)
        self.r_left_motor._write_value(-speed)
        self.r_right_motor._write_value(-speed)

    def left(self, speed=1.0):
        self.f_left_motor._write_value(-speed)
        self.f_right_motor._write_value(speed)
        self.r_left_motor._write_value(-speed)
        self.r_right_motor._write_value(speed)

    def right(self, speed=1.0):
        self.f_left_motor._write_value(speed)
        self.f_right_motor._write_value(-speed)
        self.r_left_motor._write_value(speed)
        self.r_right_motor._write_value(-speed)

    def leftTranslation(self, speed=1.0):
        self.f_left_motor._write_value(-speed)
        self.f_right_motor._write_value(speed)
        self.r_left_motor._write_value(speed)
        self.r_right_motor._write_value(-speed)

    def rightTranslation(self, speed=1.0):
        self.f_left_motor._write_value(speed)
        self.f_right_motor._write_value(-speed)
        self.r_left_motor._write_value(-speed)
        self.r_right_motor._write_value(speed)

    def stop(self):
        self.f_left_motor._write_value(0)
        self.f_right_motor._write_value(0)
        self.r_left_motor._write_value(0)
        self.r_right_motor._write_value(0)
