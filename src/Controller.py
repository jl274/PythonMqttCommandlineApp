import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime


class SmartHomeSystem:

    def __init__(self):
        self.__client = mqtt.Client()
        self.__reports = []
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()

    def __on_connect(self, client, userdata, flags, rc):
        self.__client.subscribe(f'smart')

    def __on_message(self, client, userdata, msg):
        now = datetime.now()
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))
        print(message)


if __name__ == "__main__":
    menu = {0: "Smart home controller menu:", "q": "1.\t press q to quit"}
    while True:
        for option in menu.values():
            print(option)
        selected = input("#\t")
        if selected == "q":
            print("Goodbye")
            break
        print("Invalid option")
