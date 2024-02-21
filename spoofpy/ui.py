from spoofpy.device_add import add_device_to_inspected
from spoofpy import global_state
import time
from spoofpy import common
from spoofpy import model

def welcome():
    print(r"""
==================================================
   _____                   ____      ______  __
  / ___/____  ____  ____  / __/     / __ \ \/ /
  \__ \/ __ \/ __ \/ __ \/ /_______/ /_/ /\  / 
 ___/ / /_/ / /_/ / /_/ / __/_____/ ____/ / /  
/____/ .___/\____/\____/_/       /_/     /_/   
    /_/
==================================================
    """)

    print("Welcome to SpoofPy! This tool allows you to perform ARP spoofing attacks on a local network.")
    print("This tool is for educational purposes only. Do not use it for malicious purposes.")
    print("By using this tool, you accept the responsibility for any damage caused by its usage.")
    print("The author of this tool is not responsible for any damage caused by its usage.")
    print("Use at your own risk.")
    print("\n")

def get_user_input():
    print("[*] Please enter the IP address of the target you would like to spoof.")

    targets = []

    while True:
        target = input("[?] Target IP address (or enter to finish): ")
        if target == "":
            print()
            break

    return targets


def print_menu():
    print("==================================================")
    print("Please select an option:")
    print("[1] Add a device to the list of inspected devices")
    print("[2] View the list of inspected devices")
    print("[3] View traffic")
    print("[4] View all devices")
    print("[10] Exit")
    print("==================================================\n")


def get_user_choice():
    while True:
        choice = input("[?] Please enter your choice: ")
        if choice.isdigit() and int(choice) in range(1, 11):
            print()
            return int(choice)
        else:
            print("[!] Invalid choice.")

def add_device():
    targets = get_user_input()
    for target in targets:
        add_device_to_inspected(target)


def list_inspected_devices():
    devices = model.Device.select().where(model.Device.is_inspected == 1)
    for device in devices:
        print(f"[*] IP: {device.ip_addr}, MAC: {device.mac_addr}\n")


def view_traffic():
    print("Viewing traffic...")


def list_all_devices():
    devices = model.Device.select()
    print("[*] Devices discovered by ARP scan:")
    for device in devices:
        print(f"[*] IP: {device.ip_addr}, MAC: {device.mac_addr}")


def quit():
    print("[!] Quitting the application...")
    global_state.is_running = False
    common.log("[UI] Inspector stopped")
