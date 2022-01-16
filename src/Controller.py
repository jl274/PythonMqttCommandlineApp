import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime


class SmartHomeSystem:

    def __init__(self):
        self.__connected = False
        self.__client = mqtt.Client()
        self.__reports = []
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


if __name__ == "__main__":
    controller = SmartHomeSystem()
    menu = {0: "Smart home controller menu:", "q": "1.\t press q to quit"}
    while controller.connected():
        for option in menu.values():
            print(option)
        selected = input("#\t")
        if selected == "q":
            print("Goodbye")
            break
        print("Invalid option")
