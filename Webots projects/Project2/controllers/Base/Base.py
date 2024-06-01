from controller import Robot, Motor, DistanceSensor, PositionSensor, Camera, Accelerometer
import math
import numpy as np
from controller import supervisor

# create the Robot instance.
robot = Robot()

time_step = int(64)
# get a handler to the motors and set target position to infinity (speed control).
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(1)
right_motor.setVelocity(1)

ps = []
psNames = [
    #angle values taken from documentation
    ('ps0', 1.27 - (math.pi / 2) ),
    ('ps1', 0.77 - (math.pi / 2) ),
    ('ps2', 0.00 - (math.pi / 2) ),
    ('ps3', 5.21- (math.pi / 2) ),
    ('ps4', 4.21- (math.pi / 2) ),
    ('ps5', 3.14159- (math.pi / 2) ),
    ('ps6', 2.37- (math.pi / 2) ),
    ('ps7', 1.87- (math.pi / 2) )
]

for i in range(8):
    ps.append(robot.getDevice(psNames[i][0]))
    ps[i].enable(time_step)
    ps[i].angle = psNames[i][1]
    ps[i].cname = psNames[i][0]
    
gps = robot.getDevice('gps')
gps.enable(time_step)

imu = robot.getDevice('imu')
imu.enable(time_step)

GOAL_POINT = np.array([-0.540104, 0.523896])

def angle_between_vectors(vector1, vector2):
    dot_product = np.dot(vector1, vector2)

    magnitude_vector1 = np.linalg.norm(vector1)
    magnitude_vector2 = np.linalg.norm(vector2)

    cosine_angle = dot_product / (magnitude_vector1 * magnitude_vector2)

    angle_radians = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    cross = np.cross(vector1, vector2)
    return np.sign(cross)*(angle_radians)

def polar_to_cartesian(sensor, robotAngle):
    r = sensor.getValue()
    theta = sensor.angle
    #normalize
    minValue = sensor.getMinValue()
    maxValue = sensor.getMaxValue()
    r = (r - minValue) / (maxValue - minValue)
    if r == 0: return np.array([0, 0])
    
    # calculate vector relative to the robot
    r = r*3
    x = r * np.cos(theta + robotAngle)
    y = r * np.sin(theta + robotAngle)
    
    # -x and -y because repulsive force
    return np.array([-x, -y])

def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v  # Avoid division by zero
    return v / norm
 
# main loop
while robot.step(time_step) != -1:
    vectorsToAdd = []
    
    #robot orientation
    robotAngle = imu.getRollPitchYaw()[2]
    robotHeadingVector = [np.cos(robotAngle), np.sin(robotAngle)]
    
    #goalVector
    robotPosition = np.array(gps.getValues()[:2])
    vecToDes = GOAL_POINT - robotPosition
    
    #add normalized goal Vector (magnitude = 1)
    vectorsToAdd.append(normalize_vector(vecToDes))
    
    #distance sensor vectors
    for sensor in ps:
        vectorsToAdd.append(polar_to_cartesian(sensor, robotAngle))

    #resultant vector
    finalVector = np.sum(vectorsToAdd, axis=0)
    
    #final vector to control    
    a = angle_between_vectors(robotHeadingVector, finalVector)
    speed = 2
    #distance cut off for goal
    if np.linalg.norm(vecToDes) < 0.01: 
        speed = 0
        a = 0
    
    #set control based on angle
    if(a < 0.01 and a > -0.01):
        left_motor.setVelocity(speed)
        right_motor.setVelocity(speed)
    else:
        left_motor.setVelocity(speed-a*0.95)
        right_motor.setVelocity(speed+a*0.95)    