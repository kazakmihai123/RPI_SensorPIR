# PIR-Based Entry/Exit Monitoring System

This is a MicroPython-based project for ESP or Raspberry Pi boards that monitors entry and exit events using two PIR sensors. It sends status updates to a remote Flask server hosted on a PC for centralized data logging or display.

## Features

- Detects direction of movement (entry vs. exit) using two PIR sensors
- Debounced push-button to activate or deactivate the system
- Visual feedback using LEDs (red, green, yellow)
- WiFi connectivity
- Sends data to a Flask server for visualization or further processing

## Hardware Requirements

- 2 × PIR motion sensors
- 3 × LEDs (Red, Green, Yellow)
- 1 × Push-button
- Raspberry Pi or ESP with MicroPython support
- WiFi network
- Remote PC running a Flask-based server

## Remote Flask Server

A separate Flask application runs on a PC. The Raspberry Pi sends HTTP requests to this server with the current status (active state, last event, timestamp).

Example payload:
```json
{
  "active": true,
  "last_event": "Entry",
  "last_time": "14:32:17"
}
