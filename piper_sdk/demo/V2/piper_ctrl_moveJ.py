#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo: Move Piper arm between two joint-space target positions.

Notes:
- This demo requires piper_sdk to be installed.
- Make sure the CAN interface is already active before running:
    sudo ip link set can0 type can bitrate 1000000
    sudo ip link set can0 up

Behavior:
- Connects to Piper on can0.
- Enables the arm.
- Enables gripper control.
- Repeatedly switches between:
    1. Zero joint pose with gripper closed.
    2. A non-zero joint pose with gripper opened.
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

    # Conversion factor:
    # radians -> degrees -> 0.001 degrees
    # 1000 * 180 / pi = 57295.7795
    factor = 57295.7795

    # Initial target:
    # [joint1(rad), joint2(rad), joint3(rad),
    #  joint4(rad), joint5(rad), joint6(rad), gripper(m)]
    position = [0, 0, 0, 0, 0, 0, 0]

    count = 0

    while True:
        count = count + 1

        if count == 0:
            print("1-----------")
            position = [0, 0, 0, 0, 0, 0, 0]

        elif count == 300:
            print("2-----------")
            position = [0.2, 0.2, -0.2, 0.3, -0.2, 0.5, 0.08]

        elif count == 600:
            print("1-----------")
            position = [0, 0, 0, 0, 0, 0, 0]
            count = 0

        # Convert joint targets from radians to SDK units: 0.001 degrees
        joint_0 = round(position[0] * factor)
        joint_1 = round(position[1] * factor)
        joint_2 = round(position[2] * factor)
        joint_3 = round(position[3] * factor)
        joint_4 = round(position[4] * factor)
        joint_5 = round(position[5] * factor)

        # Convert gripper target from meters to SDK units: 0.001 mm
        joint_6 = round(position[6] * 1000 * 1000)

        # Set motion mode:
        # 0x01: CAN command control mode
        # 0x01: MOVE J / joint control mode
        # 100 : speed percentage
        # 0x00: position-velocity mode
        piper.MotionCtrl_2(0x01, 0x01, 100, 0x00)

        # Send joint-space command
        piper.JointCtrl(
            joint_0,
            joint_1,
            joint_2,
            joint_3,
            joint_4,
            joint_5,
        )

        # Send gripper command
        piper.GripperCtrl(abs(joint_6), 1000, 0x01, 0)

        # Print arm status and the current commanded target
        print(piper.GetArmStatus())
        print(position)

        time.sleep(0.005)