# Source Robotics Toolbox

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) ![Issues](https://img.shields.io/github/issues/PCrnjak/Source-Robotics-Toolbox) ![release](https://img.shields.io/github/v/release/PCrnjak/Source-Robotics-Toolbox)

# How to use?

This lib was created to simplify the control of your robot with Source robotic line of motor drivers.<br />
It works perfectly with [Spectral-BLDC lib](https://github.com/PCrnjak/Spectral-BLDC-Python).<br />
Some features it offers:

* Sector homing
* Robot joint mastering/calibration
* Converting encoder ticks to joint position and speed 
* Converting joint position and speed to encoder ticks
* Radian 2 degreee, degree 2 radian position and speed manipulation

## What is sector homing?



## Skeleton sketch

``` py 
import SourceRoboticsToolbox
import time

# This is represents encoder ticks where your joint should be at 0 rad
# Usually you know that position from your robots DH table / kinematic diagram
Master_position = 14000 
Joint_reduction_ratio = 6 # Joint has reduction ratio of 6:1

Joint = SourceRoboticsToolbox.Joint(encoder_resolution = 14,
                                    master_position=Master_position,
                                    gear_ratio = Joint_reduction_ratio,
                                    offset = 0, #Change If your motor is not at 0 rad at master position 
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

```


# More about our projects
- [Youtube](https://www.youtube.com/channel/UCp3sDRwVkbm7b2M-2qwf5aQ)
- [Instagram](https://www.instagram.com/source_robotics/)
- [Twitter](https://twitter.com/SourceRobotics)
- [Discord](https://discord.com/invite/prjUvjmGpZ )
- [Forum](https://discourse.source-robotics.com/)
- [Blog](https://source-robotics.com/blogs/blog)


# Liability 
1. The software and hardware are still in development and may contain bugs, errors, or incomplete features.
2. Users are encouraged to use this software and hardware responsibly and at their own risk.

# Support the project

The majority of this project is open source and freely available to everyone. Your assistance, whether through donations or advice, is highly valued. Thank you!

 [![General badge](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/PCrnjak?locale.x=en_US)
[![General badge](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/PCrnjak)

# Project is under MIT Licence
