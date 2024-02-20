"""
Network schemas

This module contains the schemas for storing network information.
"""

network = {
    "type": "object",
    "properties": {
        "ip": {
            "type": "string",
            "pattern": "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",
            "description": "The IP address of the host"
        },
        "ip_range": {
            "type": "string",
            "pattern": "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",
            "description": "The IP range of the network"
        },
        "gateway_ip": {
            "type": "string",
            "pattern": "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",
            "description": "The IP address of the gateway"
        },
        "mac": {
            "type": "string",
            "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
            "description": "The MAC address of the host"
        }, 
        "netmask": {
            "type": "string",
            "pattern": "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",
            "description": "The netmask of the network"
        }, 
        "interface": {
            "type": "string",
            "description": "The network interface"
        }
    },
    "required": ["ip", "ip_range", "gateway_ip", "mac", "netmask", "interface"]
}
