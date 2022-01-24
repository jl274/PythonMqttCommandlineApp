import paho.mqtt.client as mqtt
import json
import threading
import random


class SmokeDetector:

    def __init__(self, path):
        self.__path = path
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()
        self.__smoke_level = 50
        self.send_smoke_report()
        self.__set_interval(self.check_smoke_level, 15)

    def __on_connect(self, client, userdata, flags, rc):
        self.__client.subscribe([(f'smart/{self.__path}', 0)])

    def __on_message(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))["data"]
        if message["action"] == "open_window":
            self.__smoke_level = 50

    def __set_interval(self, func, sec):
        def func_wrapper():
            self.__set_interval(func, sec)
            func()

        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t

    def check_smoke_level(self):
        random_num = random.randint(-10, 10)
        self.__smoke_level += random_num
        if self.__smoke_level in range(85, 101):
            self.send_smoke_report(alarm=True)
        else:
            self.send_smoke_report()

    def send_smoke_report(self, alarm=False):
        self.__client.publish(
            f'smart',
            json.dumps({"device": f"{self.__path}", "data": {"smoke": self.__smoke_level, "alarm": alarm}})
        )

