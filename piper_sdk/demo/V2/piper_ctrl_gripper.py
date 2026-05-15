#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo: Control the Piper gripper.

Note:
- This demo requires piper_sdk to be installed before running.
- Make sure the CAN interface is already active before running:
    sudo ip link set can0 type can bitrate 1000000
    sudo ip link set can0 up
"""

import time
from piper_sdk import *


if __name__ == "__main__":
    # Select the Piper arm connected on CAN interface can0
    piper = C_PiperInterface_V2(can_name="can1")

    # Connect to the CAN port
    piper.ConnectPort()

    # Enable the robotic arm
    while not piper.EnablePiper():
        time.sleep(0.01)

    # Initialize/reset gripper control
    piper.GripperCtrl(0, 1000, 0x02, 0)

    # Enable gripper control
    piper.GripperCtrl(0, 1000, 0x01, 0)

    gripper_range = 0
    count = 0

    while True:
        # Print current gripper feedback message
        print(piper.GetArmGripperMsgs())

        count = count + 1

        if count == 0:
            print("1-----------")
            gripper_range = 0

        elif count == 300:
            print("2-----------")
            gripper_range = 0.07 * 1000 * 1000  # 0.05 m = 50 mm

        elif count == 600:
            print("3-----------")
            gripper_range = 0
            count = 0

        gripper_range = round(gripper_range)

        # Send gripper position command
        piper.GripperCtrl(abs(gripper_range), 1000, 0x01, 0)

        time.sleep(0.005)