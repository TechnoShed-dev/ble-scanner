# ---------------------------------------------------------------------------------------
# ZIGGY MICRO BOOTLOADER - V2.1.0 (Time Gatekeeper)
# ---------------------------------------------------------------------------------------
# DEVICE:  ESP32-C3 (Ziggy Micro)
# PURPOSE: Network Initialization & Strict NTP Time Sync
# AUTHOR:  Karl (TechnoShed)
# DATE:    04-12-2025
# ---------------------------------------------------------------------------------------

import network
import secrets
import time
import ntptime
import machine

# --- CONFIGURATION ---
MIN_VALID_YEAR = 2025
MAX_RETRIES = 5

# --- LED SETUP ---
try:
    led = machine.Pin("LED", machine.Pin.OUT)
except:
    led = machine.Pin(8, machine.Pin.OUT) # C3 SuperMini

def blink_status(times, speed_ms):
    for _ in range(times):
        led.on(); time.sleep_ms(speed_ms)
        led.off(); time.sleep_ms(speed_ms)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f'[Boot] Connecting to {secrets.SSID}...')
        wlan.connect(secrets.SSID, secrets.PASS)
        
        # Wait for connection (15s timeout)
        for _ in range(15):
            if wlan.isconnected():
                print('[Boot] WiFi Connected.')
                blink_status(3, 100) # 3 fast blinks = WiFi OK
                return True
            time.sleep(1)
            
    if wlan.isconnected():
        return True
    
    print('[Boot] WiFi Failed.')
    return False

def force_time_sync():
    print("[Boot] Attempting NTP Sync...")
    
    # Retry loop
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            ntptime.settime() # Request time from pool.ntp.org
            
            # Check if it actually worked
            # (Sometimes it returns successfully but the year is still 2000)
            now = time.localtime()
            year = now[0]
            
            if year >= MIN_VALID_YEAR:
                print(f"[Boot] Time Synced: {now[0]}-{now[1]:02d}-{now[2]:02d} {now[3]:02d}:{now[4]:02d}")
                return True
            else:
                print(f"[Boot] NTP success but year invalid ({year}). Retrying...")
                
        except Exception as e:
            print(f"[Boot] NTP Attempt {attempt}/{MAX_RETRIES} Failed: {e}")
        
        # Wait before retry (flash LED slowly to indicate waiting)
        blink_status(1, 500)
        time.sleep(2)
        
    return False

# ==========================================
# MAIN BOOT LOGIC
# ==========================================

# 1. Connect to WiFi
if do_connect():
    
    # 2. The Time Trap
    if force_time_sync():
        print("[Boot] System Ready. Starting Main...")
        # Success! Exit boot.py, which automatically starts main.py
    else:
        print("[Boot] CRITICAL: Time Sync Failed after retries.")
        print("[Boot] Halting to prevent bad data.")
        print("[Boot] Device will REBOOT in 10 seconds...")
        
        # Panic Flash (Fast infinite blinking)
        for _ in range(50):
            led.on(); time.sleep_ms(50)
            led.off(); time.sleep_ms(50)
            
        machine.reset() # Hard reset is often the best fix for network stuck states
        
else:
    print("[Boot] WiFi Failure. Rebooting in 5s...")
    time.sleep(5)
    machine.reset()