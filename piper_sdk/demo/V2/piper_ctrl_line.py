#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo: Move Piper arm between two Cartesian end-effector poses using MOVE L mode.

Notes:
- This demo requires piper_sdk to be installed.
- Make sure the CAN interface is already active before running:
    sudo ip link set can0 type can bitrate 1000000
    sudo ip link set can0 up

Behavior:
- Connects to Piper on can0.
- Enables the arm.
- Commands the end-effector between two Z positions:
    1. Z = 215 mm
    2. Z = 260 mm
- Uses MOVE L / linear motion mode.
- This script does NOT disable the arm when stopped.
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

    print("Piper arm enabled successfully on can0.")

    # Enable gripper control at 0 position
    piper.GripperCtrl(0, 1000, 0x01, 0)

    # SDK expects pose command values in 0.001 units
    # Position: mm -> 0.001 mm
    # Orientation: degree -> 0.001 degree
    factor = 1000

    # Initial target pose:
    # [X(mm), Y(mm), Z(mm), RX(deg), RY(deg), RZ(deg), gripper(mm)]
    position = [
        57.0,
        0.0,
        215.0,
        0,
        85.0,
        0,
        0,
    ]

    count = 0

    while True:
        # Print current end-effector feedback pose
        print(piper.GetArmEndPoseMsgs())

        count = count + 1

        if count == 0:
            print("1-----------")
            position = [
                57.0,
                0.0,
                215.0,
                0,
                85.0,
                0,
                0,
            ]

        elif count == 2:
            print("2-----------")
            position = [
                57.0,
                0.0,
                290.0,
                0,
                85.0,
                0,
                0,
            ]

        elif count == 3:
            print("1-----------")
            position = [
                57.0,
                0.0,
                215.0,
                0,
                85.0,
                0,
                0,
            ]
            count = 0

        X = round(position[0] * factor)
        Y = round(position[1] * factor)
        Z = round(position[2] * factor)
        RX = round(position[3] * factor)
        RY = round(position[4] * factor)
        RZ = round(position[5] * factor)
        joint_6 = round(position[6] * factor)

        print(X, Y, Z, RX, RY, RZ)

        # Set motion mode:
        # 0x01: CAN command control mode
        # 0x02: MOVE L / linear motion mode
        # 100 : speed percentage
        # 0x00: position-velocity mode
        piper.MotionCtrl_2(0x01, 0x02, 100, 0x00)

        # Send Cartesian end-effector pose command
        piper.EndPoseCtrl(X, Y, Z, RX, RY, RZ)

        # Send gripper command
        piper.GripperCtrl(abs(joint_6), 1000, 0x01, 0)

        time.sleep(2)