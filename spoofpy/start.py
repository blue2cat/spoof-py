import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import time
import spoofpy.global_state as global_state
import spoofpy.common
import spoofpy.model
import spoofpy.networking
import spoofpy.arp_scanner
import spoofpy.arp_spoofer
import spoofpy.packet_collector
import spoofpy.packet_processor
#import spoofpy.friendly_organizer
#import spoofpy.data_donation
import os
from . import ui

def start_threads():

    with global_state.global_state_lock:
        if global_state.inspector_started[0]:
            spoofpy.common.log('Another instance of Inspector is already running. Aborted.')
            return
        global_state.inspector_started[0] = True
        global_state.inspector_started_ts = time.time()

    spoofpy.common.log('Starting Inspector')

    # Initialize the database
    spoofpy.common.log('Initializing the database')
    spoofpy.model.initialize_tables()

    # Initialize the networking variables
    spoofpy.common.log('Initializing the networking variables')
    spoofpy.networking.enable_ip_forwarding()
    spoofpy.networking.update_network_info()

    # Start various threads
    spoofpy.common.SafeLoopThread(spoofpy.arp_scanner.start_arp_scanner, sleep_time=5)
    spoofpy.common.SafeLoopThread(spoofpy.packet_collector.start_packet_collector, sleep_time=0)
    spoofpy.common.SafeLoopThread(spoofpy.packet_processor.process_packet, sleep_time=0)
    spoofpy.common.SafeLoopThread(spoofpy.arp_spoofer.spoof_internet_traffic, sleep_time=5)
    #spoofpy.common.SafeLoopThread(spoofpy.friendly_organizer.add_hostname_info_to_flows, sleep_time=5)
    #spoofpy.common.SafeLoopThread(spoofpy.friendly_organizer.add_product_info_to_devices, sleep_time=5)
    #spoofpy.common.SafeLoopThread(spoofpy.data_donation.start, sleep_time=15)

    spoofpy.common.log('Inspector started')



def clean_up():

    spoofpy.networking.disable_ip_forwarding()


def init():
    """
    Execute this function to start Inspector as a standalone application from the command line.

    """
    
    #user welcome
    ui.welcome()

    #ask the user which ip they want to spoof
    #ui 

    targets = ["10.4.110"]


    start_threads()

    print('Started Inspector')
    # Loop until the user quits
    try:
        while True:
            time.sleep(1)
            with global_state.global_state_lock:
                if not global_state.is_running:
                    break

    except KeyboardInterrupt:
        pass

    clean_up()



