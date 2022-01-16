import paho.mqtt.client as mqtt
import json
from datetime import datetime


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

    # def add_device(self, path):
    #     self.__devices[path]



