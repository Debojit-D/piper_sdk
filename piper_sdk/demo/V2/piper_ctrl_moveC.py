#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo: Piper robotic arm MOVE C / circular-arc motion.

Notes:
- This demo requires piper_sdk to be installed.
- Make sure the CAN interface is already active before running:
    sudo ip link set can1 type can bitrate 1000000
    sudo ip link set can1 up
- Make sure the robot workspace is clear before running this script.

Behavior:
- Connects to Piper on can1.
- Enables the arm.
- Enables the gripper.
- Switches to MOVE C / circular motion mode.
- Sends three Cartesian poses:
    1. Start point
    2. Middle point
    3. End point
- This script does NOT disable the arm when stopped.
"""

import time
from piper_sdk import *


if __name__ == "__main__":
    # Select the Piper arm connected on CAN interface can1
    piper = C_PiperInterface_V2(can_name="can1")

    # Connect to the CAN port
    piper.ConnectPort()

    # Enable the robotic arm
    while not piper.EnablePiper():
        time.sleep(0.01)

    print("Piper arm enabled successfully on can1.")

    # Enable gripper control at 0 position
    piper.GripperCtrl(0, 1000, 0x01, 0)

    # Switch to MOVE C / circular motion mode
    # 0x01: CAN command control mode
    # 0x03: MOVE C / circular mode
    # 30  : speed percentage
    # 0x00: position-velocity mode
    piper.MotionCtrl_2(0x01, 0x03, 30, 0x00)

    # MOVE C requires three points:
    # 1. Start point
    # 2. Middle point
    # 3. End point
    #
    # EndPoseCtrl units:
    # X, Y, Z    -> 0.001 mm
    # RX, RY, RZ -> 0.001 degrees

    # Start point
    piper.EndPoseCtrl(
        135481,
        9349,
        161129,
        178756,
        6035,
        -178440,
    )
    piper.MoveCAxisUpdateCtrl(0x01)
    time.sleep(0.001)

    # Middle point
    piper.EndPoseCtrl(
        222158,
        128758,
        142126,
        175152,
        -1259,
        -157235,
    )
    piper.MoveCAxisUpdateCtrl(0x02)
    time.sleep(0.001)

    # End point
    piper.EndPoseCtrl(
        359079,
        3221,
        153470,
        179038,
        1105,
        179035,
    )
    piper.MoveCAxisUpdateCtrl(0x03)
    time.sleep(0.001)

    # Re-send MOVE C mode command
    piper.MotionCtrl_2(0x01, 0x03, 30, 0x00)

    print("MOVE C circular command sent.")