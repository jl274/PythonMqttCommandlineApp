import paho.mqtt.client as mqtt
import json
import threading


class CleaningRobot:

    def __init__(self, path):
        self.__path = path
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()
        self.__cleaning = False
        self.__battery = 100
        self.__timeout = None
        self.send_report()

    def __on_connect(self, client, userdata, flags, rc):
        self.__client.subscribe([(f'smart/{self.__path}', 0)])

    def __on_message(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))["data"]
        if self.__timeout:
            self.__timeout()
        if message["task"] == "start":
            self.cleaning()
        elif message["task"] == "stop":
            self.charging()

    def __set_timeout(self, func, sec):
        t = threading.Timer(sec, func)
        t.start()
        self.__timeout = t.cancel

    def cleaning(self):
        if self.__cleaning is False:
            self.__cleaning = True
        else:
            self.__battery -= 10
        if self.__battery <= 15:
            self.charging()
        else:
            self.send_report()
            self.__set_timeout(self.cleaning, 10)

    def charging(self):
        if self.__cleaning is True:
            self.__cleaning = False
        else:
            self.__battery += 10
        if self.__battery != 100:
            self.__set_timeout(self.charging, 10)
        self.send_report()

    def send_report(self):
        cleaning, battery = self.__cleaning, self.__battery
        self.__client.publish(
            f'smart',
            json.dumps({"device": f"{self.__path}", "data": {"cleaning": cleaning, "battery": battery}})
        )
