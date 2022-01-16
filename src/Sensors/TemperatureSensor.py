import paho.mqtt.client as mqtt
import json
import threading


class TemperatureSensor:

    def __init__(self, path):
        self.__path = path
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()
        self.__temp = 21

    def __on_connect(self, client, userdata, flags, rc):
        self.__client.subscribe(f'smart/{self.__path}')

    def __on_message(self, client, userdata, msg):
        msg_int = int(str(msg.payload.decode("utf-8", "ignore")))
        self.set_temperature(msg_int)

    def set_temperature(self, temp):
        self.__temp = temp

    def send_temperature_raport(self):
        temperature = self.__temp
        self.__client.publish(f'smart',
                              json.dumps({"from": f"smart/{self.__path}", "temp": temperature}))

