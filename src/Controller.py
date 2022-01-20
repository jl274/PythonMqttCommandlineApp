import paho.mqtt.client as mqtt
import json
from datetime import datetime
from src.Devices.Heater import Heater
from src.Devices.LightSwitch import LightSwitch
from src.Devices.SmartTv import SmartTV
from src.Devices.Speaker import Speaker
from src.Devices.SmartBlinds import SmartBlinds
from src.Devices.SmartOven import SmartOven


class SmartHomeSystem:

    def __init__(self, role="user"):
        self.role = role
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
        self.__reports = [{
            "device": message["device"],
            "date": now,
            "data": message["data"]
        }] + self.__reports
        # print(message)

    def change_active_role(self, role):
        self.role = role

    def find_last_report(self, device):
        for index in range(len(self.__reports)):
            if self.__reports[index]["device"] == device:
                return self.__reports[index]
        return {f'{device}': "Data not found"}

    def connected(self):
        return self.__connected

    def add_device(self, name, room, device_type):
        device_types = {
            "heater": Heater,
            "light_switch": LightSwitch,
            "smart_tv": SmartTV,
            "speaker": Speaker,
            "smart_blinds": SmartBlinds,
            "smart_oven": SmartOven
        }
        if name in self.__devices[room].keys():
            return False
        self.__devices[room][f'{name}'] = device_type
        device_types[device_type](f'{room}/{name}')
        return True

    def add_room(self, room):
        self.__devices[room] = {}

    def delete_device(self, room, device):
        if room in self.__devices.keys():
            del self.__devices[room][device]
            return True
        return False

    def move_device(self, room, device, new_room):
        if new_room in self.__devices.keys():
            device_type = self.__devices[room][device]
            del self.__devices[room][device]
            self.__devices[new_room][device] = device_type
            return True
        return False

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

    def get_device_type(self, room, name):
        dev_type = self.__devices[room][name]
        return dev_type

    # logs
    def get_logs(self, number: int) -> list:
        logs = []
        count = 0
        for log in self.__reports:
            logs.append(log)
            if count == number:
                break
        return logs

    def get_all_device_logs(self, device_name: str) -> list:
        logs = []
        for log in self.__reports:
            if log["device"] == device_name:
                logs.append(log)
        return logs

    # list devices
    def list_devices(self):
        devices = []
        for room in self.__devices.keys():
            room_devices = {room: []}
            if len(self.__devices[room]) == 0:
                break
            for device in self.__devices[room].keys():
                room_devices[room].append(device)
            devices.append(room_devices)
        return devices

    # temperature sensor
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

    # light switch
    def switch_light(self, is_on: bool, room, name):
        try:
            message = {
                "device": "controller",
                "data": {
                    "switch": is_on
                }
            }
            self.__client.publish(f'smart/{room}/{name}', json.dumps(message))
            return True
        except:
            return False

    # smart blinds
    def switch_blinds(self, on_status, room, name):
        try:
            message = {
                "device": "controller",
                "data": {
                    "on_status": on_status
                }
            }
            self.__client.publish(f'smart/{room}/{name}', json.dumps(message))
            return True
        except:
            return False

    # tv remote
    def use_tv_remote(self, is_on: bool, channel: int, volume: int, is_recording: bool, room, name):
        try:
            message = {
                "device": "controller",
                "data": {
                    "is_on": is_on, "channel": channel, "volume": volume, "is_recording": is_recording
                }
            }
            self.__client.publish(f'smart/{room}/{name}', json.dumps(message))
            return True
        except:
            return False

    # speaker remote
    def use_speaker_remote(self, is_on, song, is_playing, time_left, room, name):
        try:
            message = {
                "device": "controller",
                "data": {
                    "is_on": is_on, "song": song, "is_playing": is_playing, "time_left": time_left
                }
            }
            self.__client.publish(f'smart/{room}/{name}', json.dumps(message))
        except:
            return False

    # smart oven
    def control_smart_oven(self, is_on, temp, time, room, name):
        try:
            message = {
                "device": "controller",
                "data": {
                    "is_on": is_on, "temp": temp, "time": time
                }
            }
            self.__client.publish(f'smart/{room}/{name}', json.dumps(message))
        except:
            return False
