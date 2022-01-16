import paho.mqtt.client as mqtt
import json
from datetime import datetime
from src.Sensors.TemperatureSensor import TemperatureSensor


class SmartHomeSystem:

    def __init__(self):
        self.__connected = False
        self.__client = mqtt.Client()
        self.__reports = []
        self.__devices = {}
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        print("***Connecting...***")
        try:
            self.__client.connect("localhost", 1883, 60)
            self.__connected = True
            print("***Connected to smart house***\n")
            self.__client.loop_start()
        except:
            print("***Failed to connect***")

    def __on_connect(self, client, userdata, flags, rc):
        self.__client.subscribe(f'smart')

    def __on_message(self, client, userdata, msg):
        now = datetime.now()
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))
        print(message)

    def connected(self):
        return self.__connected

    def add_device(self, name, room, device_type):
        device_types = {"temp_sensor": TemperatureSensor}
        if name in self.__devices[room].keys():
            return False
        self.__devices[room][f'{name}'] = device_types[device_type]
        TemperatureSensor(f'{room}/{name}')
        return True

    def add_room(self, room):
        self.__devices[room] = {}

    def get_rooms(self):
        rooms = []
        for room in self.__devices.keys():
            rooms.append(room)
        return rooms

    def get_room_devices(self, room):
        devices = []
        if room in self.__devices.keys():
            for device in self.__devices[room]:
                devices.append(device)
        return devices

    def set_temperature(self, temperature, room, name):
        try:
            message = {
                "device": "controller",
                "data": {
                    "temp": temperature
                }
            }
            self.__client.publish(f'smart/{room}/{name}', json.dumps(message))
        except:
            return False
