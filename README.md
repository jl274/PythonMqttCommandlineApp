# MQTT-Smarrt-Home

College related project aiming at creating fully adjustable smart home system based on mqtt (paho python client).

## Project structure
* ***Devices*** folder contains implementations for smart home devices.
* ***MenuElements*** folder contains menu interfaces for each available device.
* *Controller.py* contains methods that connect menus with devices and hub.
* *Menu.py* contains some kind of main menu, logistic hub that helps select devices and gives access settings.

## Data sent through MQTT
Data about device state that is sent to hub have JSON format and looks like this:
```json
{
    "device": "device name",
    "data": "all data from device",
    "date": "date of message"
}
```
