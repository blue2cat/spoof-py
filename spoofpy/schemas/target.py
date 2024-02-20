
target = {
    "type": "object",
    "properties": {
        "ip": {
            "type": "string",
            "pattern": "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",
            "description": "The IP address of the target"
        },
        "mac": {
            "type": "string",
            "pattern": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
            "description": "The MAC address of the target"
        }
    },
    "required": ["ip", "mac"]
}