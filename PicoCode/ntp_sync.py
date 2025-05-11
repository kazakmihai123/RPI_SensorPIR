# ntp_sync.py
import ntptime
import time

def sync_time():
    connected = False
    while not connected:
        try:
            ntptime.settime()
            print("Ora sincronizata.")
            connected = True
        except:
            print("Eroare la sincronizarea cu NTP.")
        time.sleep(1)
