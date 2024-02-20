"""
Author: Gavin - blue2cat
Description: This module contains the user interface functions for the spoofpy application.
"""
def welcome():
    print(r"""
   _____                   ____      ______  __
  / ___/____  ____  ____  / __/     / __ \ \/ /
  \__ \/ __ \/ __ \/ __ \/ /_______/ /_/ /\  / 
 ___/ / /_/ / /_/ / /_/ / __/_____/ ____/ / /  
/____/ .___/\____/\____/_/       /_/     /_/   
    /_/
    """)

    print("Welcome to SpoofPy! This tool allows you to perform ARP spoofing attacks on a local network.")
    print("This tool is for educational purposes only. Do not use it for malicious purposes.")
    print("By using this tool, you accept the responsibility for any damage caused by its usage.")
    print("The author of this tool is not responsible for any damage caused by its usage.")
    print("Use at your own risk.")
    print("\n")


def gather_targets(ip_range):
    """
    Queries the user for a range or a single IP address to target, then returns the list of targets.
    - Targets must be in the same network as the host (ip_range).
    """

    #query the user for a range or a single IP address
    print("[*] Enter a single IP address (e.g. 192.168.1.46):")
    targets = input("[>] ")
    #if the user entered a range, generate the list of targets
    if "-" in targets:
        start, end = targets.split("-")
        start = int(start.split(".")[-1])
        end = int(end)
        targets = [f"{ip_range}.{i}" for i in range(start, end+1)]

    #if the user entered a single IP address, return it as a list
    else:
        targets = [targets]

    return targets


def print_network_info(network_info):
    """
    Prints the network information in a human-readable format.
    """
    print("\n[*] Network information:")
    print(f"    - IP address: {network_info['ip']}")
    print(f"    - IP range: {network_info['ip_range']}.0/24")
    print(f"    - Gateway IP: {network_info['gateway_ip']}")
    print(f"    - MAC address: {network_info['mac']}")
    print(f"    - Netmask: {network_info['netmask']}")
    print(f"    - Interface: {network_info['interface']}\n")