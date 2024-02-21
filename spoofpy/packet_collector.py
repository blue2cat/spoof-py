"""
Captures and analyzes packets from the network.

"""
import scapy.all as sc
import spoofpy.global_state as global_state
import spoofpy.common as common
import spoofpy.friendly_organizer as friendly_organizer


def start_packet_collector():

    sc.load_layer('tls')

    # Continuously sniff packets for 30 second intervals
    sc.sniff(
        prn=add_packet_to_queue,
        iface=global_state.host_active_interface,
        stop_filter=lambda _: not global_state.is_running,
        filter=f'(not arp and host not {global_state.host_ip_addr}) or arp', # Avoid capturing packets to/from the host itself, except ARP, which we need for discovery -- this is for performance improvement
        timeout=30
    )


def add_packet_to_queue(pkt):
    """
    Adds a packet to the packet queue.

    """
    with global_state.global_state_lock:
        if not global_state.is_inspecting:
            return

    global_state.packet_queue.put(pkt)