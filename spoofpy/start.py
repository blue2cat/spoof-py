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
import spoofpy.friendly_organizer

def start_threads():

    with global_state.global_state_lock:
        if global_state.inspector_started[0]:
            spoofpy.common.log('Another instance of Spoofpy is already running. Aborted.')
            return
        global_state.inspector_started[0] = True
        global_state.inspector_started_ts = time.time()

    spoofpy.common.log('Starting Spoofpy ')

    # Initialize the database
    spoofpy.common.log('Initializing the database')
    spoofpy.model.initialize_tables()

    # Initialize the networking variables
    spoofpy.common.log('Initializing the networking variables')
    # spoofpy.networking.enable_ip_forwarding()
    spoofpy.networking.update_network_info()

    # Start various threads
    spoofpy.common.SafeLoopThread(spoofpy.arp_scanner.start_arp_scanner, sleep_time=5)
    spoofpy.common.SafeLoopThread(spoofpy.packet_collector.start_packet_collector, sleep_time=0)
    spoofpy.common.SafeLoopThread(spoofpy.packet_processor.process_packet, sleep_time=0)
    spoofpy.common.SafeLoopThread(spoofpy.arp_spoofer.spoof_internet_traffic, sleep_time=5)
    spoofpy.common.SafeLoopThread(spoofpy.friendly_organizer.add_hostname_info_to_flows, sleep_time=5)
    spoofpy.common.SafeLoopThread(spoofpy.friendly_organizer.add_product_info_to_devices, sleep_time=5)

    spoofpy.common.log('Spoofpy started')





def init():
    """
    Function executed to start Spoofpy in command line mode

    """

    # Start the command line version
    spoofpy.common.log('Starting Inspector in command line mode')

    start_threads()

    spoofpy.common.log('Inspector started')
    try:
        while global_state.is_running:
            time.sleep(1)
    except: # Catch all exceptions
        spoofpy.common.log('Inspector stopped unexpectedly')
        return 0
    

    spoofpy.common.log('Inspector stopped')
    return 0            