# logic.py
import machine
import time
import urequests
import gc

from config import *
from time_utils import localtime_offset

# GPIOs
sensor_one = machine.Pin(PIR1_PIN, machine.Pin.IN)
sensor_two = machine.Pin(PIR2_PIN, machine.Pin.IN)
red_led = machine.Pin(RED_LED_PIN, machine.Pin.OUT)
green_led = machine.Pin(GREEN_LED_PIN, machine.Pin.OUT)
yellow_led = machine.Pin(YELLOW_LED_PIN, machine.Pin.OUT)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Variabile interne
state = 0
last_triggered = None
timer_start = 0
last_event_time = 0
active = False
last_button_state = 1
debounce_time = 0

# Trimitere eveniment la serverul Flask
def trimite_eveniment(tip, ora):
    try:
        # Trimite un POST request la serverul Flask
        # Asigură-te că adresa IP este corectă
        urequests.post("http://" + IP_ADDRESS + ":5000/event", json={
            "type": tip,
            "time": ora
        })
        print("Eveniment trimis:", tip, ora)
    except Exception as e:
        print("Eroare la trimitere {}: {}".format(tip, e))
    finally:
        gc.collect()

# Verifică starea senzorilor
def pir1_triggered():
    return sensor_one.value() == 1

def pir2_triggered():
    return sensor_two.value() == 1

# Logica principală
def handle_logic():
    global state, last_triggered, timer_start, last_event_time
    global active, last_button_state, debounce_time

    now = time.ticks_ms()

    # Buton activare/dezactivare
    current_button_state = button.value()
    if current_button_state == 0 and last_button_state == 1:
        if time.ticks_diff(now, debounce_time) > DEBOUNCE_DELAY:
            active = not active
            print("Sistem ACTIVAT" if active else "Sistem OPRIT")
            debounce_time = now
    last_button_state = current_button_state

    # Sistem inactiv sau în cooldown
    if not active or time.ticks_diff(now, last_event_time) < COOLDOWN:
        red_led.value(0)
        green_led.value(0)
        yellow_led.value(0)
        return

    # Stare inițială
    if state == 0:
        if pir1_triggered():
            last_triggered = "PIR1"
            timer_start = now
            state = 1
        elif pir2_triggered():
            last_triggered = "PIR2"
            timer_start = now
            state = 1
        red_led.value(0)
        green_led.value(0)
        yellow_led.value(1)

    # Așteptare al doilea senzor sau timeout
    elif state == 1:
        if time.ticks_diff(now, timer_start) > TIMEOUT:
            state = 0
        elif last_triggered == "PIR1" and pir2_triggered():
            t = localtime_offset(3)
            ora = "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])
            trimite_eveniment("intrare", ora)
            green_led.value(1)
            red_led.value(0)
            yellow_led.value(0)
            last_event_time = now
            state = 0
        elif last_triggered == "PIR2" and pir1_triggered():
            t = localtime_offset(3)
            ora = "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])
            trimite_eveniment("iesire", ora)
            red_led.value(1)
            green_led.value(0)
            yellow_led.value(0)
            last_event_time = now
            state = 0

# Returnează status-ul curent (dacă mai e necesar)
def get_status():
    return {
        "active": active,
        "last_event": last_triggered if last_triggered else "N/A",
        "last_time": "{:02d}:{:02d}:{:02d}".format(*localtime_offset(3)[3:6])
    }
