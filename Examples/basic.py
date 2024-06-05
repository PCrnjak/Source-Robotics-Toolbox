import SourceRoboticsToolbox
import time

Master_position = 14000 # This is represents encoder ticks where your joint should be at 0 rad
Joint_reduction_ratio = 6 # Joint has reduction ratio of 6:1

Joint = SourceRoboticsToolbox.Joint(encoder_resolution = 14,
                                    master_position=Master_position,
                                    gear_ratio = Joint_reduction_ratio,
                                    offset = 0, #If your motor is not at 0 rad at master position change this
                                    dir = 0) # Change joint direction

current_motor_encoder_position = 10000 #This emulates the data you would get from your motor encoder
# Init flag; used to run .determine_sector once
Intial = 0

while True:

    # This will give you Joint position in radians 
    # NOTE that joint position is value after the gear reduction of your actuator
    position_values =  Joint.get_joint_position(current_motor_encoder_position)
    print(position_values)

    # This will perform sector homing and determine the sector motor is in
    if Intial ==0 :
        Intial = 1
        Joint.determine_sector(current_motor_encoder_position)

    time.sleep(0.5)