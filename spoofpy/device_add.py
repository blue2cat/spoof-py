import datetime
import os
import sys
import time
import traceback
import spoofpy.global_state as global_state
import spoofpy.model as model
import threading
import requests

def add_device_to_inspected(ip_addr):
    """
    Checks the device table for the given IP address and sets the is_inspected field to 1 if the device is found.
    """

    # Check if the device is already in the device table
    try:
        device = model.Device.get(model.Device.ip_addr == ip_addr)
    except model.Device.DoesNotExist:
        return

    # Update the device's is_inspected field
    with model.write_lock:
        device.is_inspected = 0
        device.save()