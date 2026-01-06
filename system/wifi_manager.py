# wifi_manager.py -> WiFi management module.
import network
import time
from system.config import BIG_DISPLAY

def connect_to_wifi(ssid, password, timeout=25):
    if ssid == "fake":
        from env import wifi_ssid, wifi_password
        ssid = wifi_ssid()
        password = wifi_password()

    wlan = network.WLAN(network.STA_IF) # Create a station interface
    wlan.active(True) # Activate the interface

    if wlan.isconnected():
        BIG_DISPLAY.show_info(["Already connected to:", wlan.config('essid')], 2)
        return True

    BIG_DISPLAY.show_info(["Connecting to:", ssid + "..."], 2)
    wlan.connect(ssid, password) # Connect to the specified SSID with password

    while timeout > 0:
        if wlan.isconnected():
            BIG_DISPLAY.show_info(["Connected to:", ssid], 2)
            return True
        time.sleep(1)
        timeout -= 1
    
    BIG_DISPLAY.show_info(["Failed to connect to:", ssid], 2)
    return False

def get_wifi_status():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        return {"connected": False, "message": "WiFi is disabled"}
    
    if not wlan.isconnected():
        return {"connected": False, "message": "Not connected"}
    
    config = wlan.ifconfig()
    return {
        "connected": True,
        "ssid": wlan.config('essid'),
        "ip": config[0],
        "netmask": config[1],
        "gateway": config[2],
        "dns": config[3]
    }

def test_connection():
    import socket
    wlan = network.WLAN(network.STA_IF)
    
    if not wlan.isconnected():
        return False, "Not connected to WiFi"
    
    try:
        addr = socket.getaddrinfo("google.com", 80)[0][-1]
        s = socket.socket()
        s.settimeout(5)
        s.connect(addr)
        s.close()
        return True, "Internet connection OK"
    except Exception as e:
        return False, "No internet: " + str(e)