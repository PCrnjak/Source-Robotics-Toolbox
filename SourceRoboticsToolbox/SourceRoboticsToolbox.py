import time
import math

class Joint:
    def __init__(self, encoder_resolution = 14, master_position=9569, gear_ratio = 1, offset = 0, dir = 0):
        self.gear_ratio = gear_ratio # Gear ratio of the joint
        self.dir = dir #
        self.offset = offset
        self.encoder_resolution = 2 ** encoder_resolution - 1
        self.master_position = master_position
        self.encoder_max_counts = self.encoder_resolution + 1
        self.encoder_midpoint = self.encoder_resolution // 2
        self.range_midpoint = self.encoder_max_counts / 2

        self.initial_pos = 0
        self.sector = "middle"
        self.sector_initial = "middle"
        # Calculate offset_ticks based on direction
        if self.dir == 0:
            self.offset_ticks = self.radians_to_ticks(self.offset)
        else:
            # If direction is reversed, adjust the offset accordingly
            self.offset_ticks = self.radians_to_ticks(2 * math.pi - self.offset)

    def ticks_to_degrees(self, ticks):
        degrees_per_tick = 360.0 / (self.encoder_max_counts * self.gear_ratio)
        degrees = ticks * degrees_per_tick
        return degrees

    def degrees_to_ticks(self, degrees):
        ticks_per_degree = (self.encoder_max_counts * self.gear_ratio) / 360.0
        ticks = round(degrees * ticks_per_degree)
        return ticks

    def radians_to_ticks(self, radians):
        ticks_per_radian = (self.encoder_max_counts* self.gear_ratio) / (2 * math.pi)
        ticks = round(radians * ticks_per_radian)
        return ticks 

    def ticks_to_radians(self, ticks):
        radians_per_tick = (2 * math.pi) / (self.encoder_max_counts * self.gear_ratio)
        radians = ticks * radians_per_tick
        return radians

    # Returns encoder value in terms of single revolution
    def unwrap_position(self, position_ticks):
        # Apply modular arithmetic to ensure position falls within valid range
        unwrapped_encoder_raw = position_ticks % self.encoder_resolution
        return unwrapped_encoder_raw

    def determine_sector(self, initial):

            # Check the initial encoder position we are at. 
            # Depending on that encoder position and master position we determine the sector.
            self.initial_pos = self.unwrap_position(initial)

            if (self.master_position + self.encoder_midpoint - self.encoder_resolution ) > 0:
                self.sector = "left"
                if self.initial_pos >= 0 and self.initial_pos < self.master_position - self.range_midpoint:
                    self.sector_initial = "left_1"
                if self.initial_pos > self.master_position - self.range_midpoint and self.initial_pos <= self.encoder_resolution:
                    self.sector_initial = "left_2"

            elif (self.master_position + self.encoder_midpoint - self.encoder_resolution ) < 0:
                self.sector = "right"
                if self.sector == "right":
                    if self.initial_pos >= 0 and self.initial_pos < self.master_position + self.encoder_midpoint:
                        self.sector_initial = "right_1"
                    if self.initial_pos > self.master_position + self.encoder_midpoint and self.initial_pos <= self.encoder_resolution:
                        self.sector_initial = "right_2"

            elif (self.master_position + self.encoder_midpoint - self.encoder_resolution ) == 0:
                self.sector = "middle"
                self.sector_initial = "middle"

    # Returns Joint position in radians (This is the position AFTER the reduction!)
    def get_joint_position(self, motor_position):

        if self.sector == "right":
            if self.sector_initial == "right_1":
                joint_position = motor_position - self.master_position + self.offset_ticks
            if self.sector_initial == "right_2":
                joint_position = motor_position - self.master_position - self.encoder_max_counts + self.offset_ticks

        elif self.sector == "left":
            if self.sector_initial == "left_1":
                joint_position = motor_position - self.master_position + self.encoder_max_counts + self.offset_ticks
            if self.sector_initial == "left_2":
                joint_position = motor_position - self.master_position + self.offset_ticks

        elif self.sector == "middle":
            joint_position = motor_position - self.master_position + self.offset_ticks
        
        joint_position = self.ticks_to_radians(joint_position)
        # Adjust radians based on direction
        if self.dir == 1:  # Check the direction variable
            joint_position = 2 * math.pi - joint_position  # Reverse the radians value if direction is 1
        return joint_position
    
    # Returns Joint speed in radians/s (This is the speed AFTER the reduction!)
    def get_joint_speed(self, motor_speed):
        # Adjust the motor speed based on direction
        motor_speed *= -1 if self.dir == 1 else 1
        # Calculate the joint speed in radians per second        
        revolutions_per_second = motor_speed / self.encoder_max_counts
        radians_per_second = revolutions_per_second * 2 * math.pi
        joint_speed = radians_per_second /  self.gear_ratio
        
        return joint_speed
    
    # Returns raw encoder speed in tick/s
    def get_encoder_speed(self, joint_speed):
        # Adjust the joint speed based on direction
        joint_speed *= -1 if self.dir == 1 else 1
        # Calculate the encoder speed in ticks per second
        revolutions_per_second = (joint_speed * self.gear_ratio) / (2 * math.pi)
        encoder_speed = revolutions_per_second * self.encoder_max_counts

        return encoder_speed

    # Returns raw encoder ticks 
    def get_encoder_position(self,joint_position):

        if self.dir == 1:  # Check the direction variable
            joint_position = 2 * math.pi - joint_position  # Reverse the radians value if direction is 1
            
        joint_position = self.radians_to_ticks(joint_position)

        if self.sector == "right":
            if self.sector_initial == "right_1":
                motor_position = joint_position + self.master_position - self.offset_ticks
            if self.sector_initial == "right_2":
                motor_position = joint_position + self.master_position + self.encoder_max_counts - self.offset_ticks

        elif self.sector == "left":
            if self.sector_initial == "left_1":
                motor_position = joint_position + self.master_position - self.encoder_max_counts - self.offset_ticks
            if self.sector_initial == "left_2":
                motor_position =  joint_position + self.master_position - self.offset_ticks 

        elif self.sector == "middle":
            motor_position = joint_position + self.master_position - self.offset_ticks
        return motor_position      
            
        
# Example usage:
if __name__ == "__main__":
    joint = Joint(encoder_resolution = 14, master_position=9569, gear_ratio = 1, offset = 0, dir = 0)

    # Continuously get joint position
    while True:
        # Get motor position from Motor6 object
        positon = 100
        joint_position = joint.get_joint_position(positon)
        time.sleep(1)
