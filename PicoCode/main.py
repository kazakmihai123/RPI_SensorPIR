import network
import time
from config import WIFI_SSID, WIFI_PASSWORD
from logic import handle_logic
from ntp_sync import sync_time
import machine


# Conectare WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

while not wlan.isconnected():
    print("Conectare WiFi...")
    time.sleep(1)

print("Conectat la:", wlan.ifconfig()[0])

sync_time()

# Bucla principală
while True:
    try:
        handle_logic()
    except Exception as e:
        print("Eroare în bucla principală:", e)

    time.sleep_ms(100)
