import datetime
import os
import sys
import time
import traceback
import spoofpy.global_state as global_state
import spoofpy.model as model
import threading
import requests
from time import sleep
import spoofpy.common as common


def add_device_to_inspected(ip_addr):
    """
    Checks the device table for the given IP address and sets the is_inspected field to 1 if the device is found.
    """
    TIME_TO_WAIT = 10


    while(TIME_TO_WAIT > 0):
        try:
            device = model.Device.get(model.Device.ip_addr == ip_addr)
            common.log(f'Adding {ip_addr} to the list of inspected devices')

            # Update the device's is_inspected field
            with model.write_lock:
                device.is_inspected = 1
                device.save()

            break
        except model.Device.DoesNotExist:
            sleep(1)
            TIME_TO_WAIT -= 1
            common.log(f'Waiting for {ip_addr} to appear in the device table')
            if(TIME_TO_WAIT == 0):
                return
        except Exception as e:
            common.log(f'Error: {e}')
            return