#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo: Send one joint-space command to the Piper arm.

Notes:
- This demo requires piper_sdk to be installed.
- Make sure can0 is already up:
    sudo ip link set can0 type can bitrate 1000000
    sudo ip link set can0 up
- This script enables the arm, sends one joint command, sends one gripper command,
  and then exits. It does NOT disable the arm.
"""

import time
import math
from piper_sdk import *


if __name__ == "__main__":
    # Select the Piper arm connected to CAN interface can0
    piper = C_PiperInterface_V2(can_name="can1")

    # Connect to the CAN interface
    piper.ConnectPort()

    # Enable the arm
    while not piper.EnablePiper():
        time.sleep(0.01)

    print("Piper arm enabled on can0.")

    # Conversion factor:
    # radians -> degrees -> 0.001 degrees
    factor = 1000.0 * 180.0 / math.pi

    # Joint target:
    # [joint1(rad), joint2(rad), joint3(rad), joint4(rad), joint5(rad), joint6(rad), gripper(m)]
    position = [0, 0, 0, 0, 0, 0, 0]

    joint_0 = round(position[0] * factor)
    joint_1 = round(position[1] * factor)
    joint_2 = round(position[2] * factor)
    joint_3 = round(position[3] * factor)
    joint_4 = round(position[4] * factor)
    joint_5 = round(position[5] * factor)

    # Gripper position conversion:
    # meters -> millimeters -> 0.001 millimeters
    joint_6 = round(position[6] * 1000 * 1000)

    # Set control mode:
    # 0x01: CAN command control mode
    # 0x01: joint control mode
    # 30  : speed percentage
    # 0x00: normal mode
    piper.ModeCtrl(0x01, 0x01, 30, 0x00)

    # Send joint command
    piper.JointCtrl(joint_0, joint_1, joint_2, joint_3, joint_4, joint_5)

    # Send gripper command
    piper.GripperCtrl(abs(joint_6), 1000, 0x01, 0)

    print("Joint command sent.")
    print("Commanded joints:", joint_0, joint_1, joint_2, joint_3, joint_4, joint_5)
    print("Commanded gripper:", abs(joint_6))