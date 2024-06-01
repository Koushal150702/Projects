from controller import Robot, Motor, DistanceSensor, PositionSensor, Camera, Accelerometer
import math
import numpy as np

MAX = 6.28

def angle_between_vectors(vector1, vector2):
    dot_product = np.dot(vector1, vector2) # angle between the vectors

    magnitude_vector1 = np.linalg.norm(vector1) 
    magnitude_vector2 = np.linalg.norm(vector2)

    cosine_angle = dot_product / (magnitude_vector1 * magnitude_vector2)

    angle_radians = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    cross = np.cross(vector1, vector2)
    return np.sign(cross)*(angle_radians)
    
# create the Robot instance.
robot = Robot()

time_step = int(64)
# get a handler to the motors and set target position to infinity (speed control).
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(6)
right_motor.setVelocity(6)


gps = robot.getDevice('gps')
gps.enable(time_step)

GOAL_POINT = np.array([0.2, 0.2])


# main loop
while robot.step(time_step) != -1:

    #goal Vector
    robotPosition = np.array(gps.getValues()[:2])
    vecToDes = robotPosition - GOAL_POINT
    robotVelocityVector = np.array(gps.getSpeedVector()[:2]) * -1
    a = angle_between_vectors(robotVelocityVector, vecToDes)
    print(f'a = {a}')
    speed = np.linalg.norm(vecToDes) *6
    print(a) 
    if(a < 0.0001 and a > -0.0001):
        left_motor.setVelocity(speed)
        right_motor.setVelocity(speed)
    else:
        left_motor.setVelocity(speed-a)
        right_motor.setVelocity(speed+a)