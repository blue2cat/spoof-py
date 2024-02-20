"""
Sends out ARP spoofing packets for devices in the Device table.

"""
import time
import scapy.all as sc
import network as network
import traceback

# How many seconds between successive ARP spoofing attempts for each host
INTERNET_SPOOFING_INTERVAL = 2


spoof_stat_dict = {
    'last_internet_spoof_ts': 0
}


def spoof_internet_traffic(target):
    """
    Sends out ARP spoofing packets between inspected devices and the gateway.

    """

    # Do not spoof packets if we're not globally inspecting
    with global_state.global_state_lock:
        if not global_state.is_inspecting:
            return

    # Get the MAC address of the gateway
    gateway_mac = network.get_mac(global_state.gateway_ip)

    # Get the MAC address of the host
    host_mac = global_state.host_mac_addr

    # send a spoofed ARP packet to the gateway
    send_spoofed_arp(target['mac'], target['ip'], gateway_mac, global_state.gateway_ip)

    # send a spoofed ARP packet to the target
    send_spoofed_arp(gateway_mac, global_state.gateway_ip, target['mac'], target['ip'])

    # Update the last time we spoofed the internet
    spoof_stat_dict['last_internet_spoof_ts'] = time.time()



def send_spoofed_arp(victim_mac_addr, victim_ip_addr, dest_mac_addr, dest_ip_addr):
    """
    Sends out bidirectional ARP spoofing packets to the victim so that the host running Inspector appears to have the `dest_ip_addr` IP address.

    """
    host_mac_addr = global_state.host_mac_addr

    if victim_ip_addr == dest_ip_addr:
        return

    # Do not spoof packets if we're not globally inspecting
    with global_state.global_state_lock:
        if not global_state.is_inspecting:
            return

    # Send ARP spoof request to destination, so that the destination host thinks that Inspector's host is the victim.

    dest_arp = sc.ARP()
    dest_arp.op = 1
    dest_arp.psrc = victim_ip_addr
    dest_arp.hwsrc = host_mac_addr
    dest_arp.pdst = dest_ip_addr
    dest_arp.hwdst = dest_mac_addr

    sc.send(dest_arp, iface=global_state.host_active_interface, verbose=0)

    # Send ARP spoof request to victim, so that the victim thinks that Inspector's host is the destination.

    victim_arp = sc.ARP()
    victim_arp.op = 1
    victim_arp.psrc = dest_ip_addr
    victim_arp.hwsrc = host_mac_addr
    victim_arp.pdst = victim_ip_addr
    victim_arp.hwdst = victim_mac_addr

    sc.send(victim_arp, iface=global_state.host_active_interface, verbose=0)



def reset_arp_tables():
    pass