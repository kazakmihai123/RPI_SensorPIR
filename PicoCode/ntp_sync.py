# ntp_sync.py
import ntptime

def sync_time():
    try:
        ntptime.settime()
        print("Ora sincronizata.")
    except:
        print("Eroare la sincronizarea cu NTP.")
