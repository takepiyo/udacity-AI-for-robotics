from math import *
import random

# helper function to map all angles onto [-pi, pi]


def angle_trunc(a):
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi


class robot:
    def __init__(self, x=None, y=None, heading=None, turning=2 * pi / 10, distance=1.0):
        """This function is called when you create a new robot. It sets some of
        the attributes of the robot, either to their default values or to the values
        specified when it is created."""
        if x is None:
            self.x = (random.random() - 0.5) * 10
        else:
            self.x = x
        if y is None:
            self.y = (random.random() - 0.5) * 10
        else:
            self.y = y
        if heading is None:
            self.heading = random.random() * 2.0 * pi
        else:
            self.heading = heading
        self.turning = (
            turning  # only applies to target robots who constantly move in a circle
        )
        self.distance = (
            # only applies to target bot, who always moves at same speed.
            distance
        )
        self.turning_noise = 0.0
        self.distance_noise = 0.0
        self.measurement_noise = 0.0

    def set_noise(self, new_t_noise, new_d_noise, new_m_noise):
        """This lets us change the noise parameters, which can be very
        helpful when using particle filters."""
        self.turning_noise = float(new_t_noise)
        self.distance_noise = float(new_d_noise)
        self.measurement_noise = float(new_m_noise)

    def move(self, turning, distance, tolerance=0.001, max_turning_angle=pi):
        """This function turns the robot and then moves it forward."""
        # apply noise, this doesn't change anything if turning_noise
        # and distance_noise are zero.
        turning = random.gauss(turning, self.turning_noise)
        distance = random.gauss(distance, self.distance_noise)

        # truncate to fit physical limitations
        turning = max(-max_turning_angle, turning)
        turning = min(max_turning_angle, turning)
        distance = max(0.0, distance)

        # Execute motion
        self.heading += turning
        self.heading = angle_trunc(self.heading)
        self.x += distance * cos(self.heading)
        self.y += distance * sin(self.heading)

    def move_in_circle(self):
        """This function is used to advance the runaway target bot."""
        self.move(self.turning, self.distance)

    def sense(self):
        """This function represents the robot sensing its location. When
        measurements are noisy, this will return a value that is close to,
        but not necessarily equal to, the robot's (x, y) position."""
        return (
            random.gauss(self.x, self.measurement_noise),
            random.gauss(self.y, self.measurement_noise),
        )

    def Gaussian(self, mu, sigma, x):

        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):

        # calculates how likely a measurement should be

        dist = sqrt((self.x - measurement[0])
                    ** 2 + (self.y - measurement[1]) ** 2)

        prob = self.Gaussian(0.0,
                             self.measurement_noise, dist)
        return prob

    def __repr__(self):
        """This allows us to print a robot's position"""
        return "[%.5f, %.5f]" % (self.x, self.y)
