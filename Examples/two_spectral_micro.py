import Spectral_BLDC as Spectral
import SourceRoboticsToolbox
import time
import numpy as np


Master_position = [14000,2430]
Joint_reduction_ratio = [3, 0.5] 

Communication1 = Spectral.CanCommunication(bustype='slcan', channel='COM41', bitrate=1000000)

Motor = []
Motor.append(Spectral.SpectralCAN(node_id=0, communication=Communication1))
Motor.append(Spectral.SpectralCAN(node_id=1, communication=Communication1))

Joint = []
Joint.append(SourceRoboticsToolbox.Joint(encoder_resolution = 14,
                                        master_position=Master_position[0], 
                                        gear_ratio = Joint_reduction_ratio[0],
                                        offset = -np.pi/2,
                                        dir = 0))
Joint.append(SourceRoboticsToolbox.Joint(encoder_resolution = 14,
                                        master_position=Master_position[1],
                                        gear_ratio = Joint_reduction_ratio[1],
                                        offset = 0,
                                        dir = 0))

timeout_setting = 0.001

initial_setup = [0,0]


# Initialize position values
position_values =  np.array([0.0,0.0])
Motor_values = np.array([0,0])
received_ids = [0,0]

while True:

    Motor[0].Send_Respond_Encoder_data()
    Motor[1].Send_Respond_Encoder_data()

    for i in range(1, 3):  # Loop 3-1=2 to check for received data
        message, UnpackedMessageID = Communication1.receive_can_messages(timeout=timeout_setting)


        # Check if UnpackedMessageID is not None 
        if UnpackedMessageID is not None:
            
            Motor[UnpackedMessageID[0]].UnpackData(message,UnpackedMessageID)
            #print(f"Motor {UnpackedMessageID[0]}, position is: {Motor[UnpackedMessageID[0]].position}")
            Motor_values[UnpackedMessageID[0]] = Motor[UnpackedMessageID[0]].position
            position_values[UnpackedMessageID[0]] =  Joint[UnpackedMessageID[0]].get_joint_position(Motor[UnpackedMessageID[0]].position)
            print(f"Motor encoder ticks are: {Motor_values}, Joint values are: {position_values}")


            if initial_setup[UnpackedMessageID[0]] == 0:
                initial_setup[UnpackedMessageID[0]] = 1
                Joint[UnpackedMessageID[0]].determine_sector(Motor[UnpackedMessageID[0]].position)


    time.sleep(0.5)