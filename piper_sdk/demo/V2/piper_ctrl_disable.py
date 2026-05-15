#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo: Disable the Piper robotic arm.

Note:
- This demo requires the Piper SDK to be installed.
- Make sure the CAN interface is already up before running this script:
    sudo ip link set can0 type can bitrate 1000000
    sudo ip link set can0 up
"""

import time
from piper_sdk import *


if __name__ == "__main__":
    # Create Piper interface on CAN port can0
    piper = C_PiperInterface_V2(can_name="can1")

    # Connect to the CAN port
    piper.ConnectPort()

    # Keep trying until the arm is disabled
    while piper.DisablePiper():
        time.sleep(0.01)

    print("Piper arm disabled successfully!")