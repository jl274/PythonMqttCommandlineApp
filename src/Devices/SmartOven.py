import paho.mqtt.client as mqtt
import json
import threading


class SmartOven:

    def __init__(self, path):
        self.__path = path
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()
        self.__temp = 0
        self.__is_on = False
        self.__time = 0
        self.send_oven_report()

    def __on_connect(self, client, userdata, flags, rc):
        self.__client.subscribe([(f'smart/{self.__path}', 0)])

    def __on_message(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))["data"]
        is_on, temp, time = message["is_on"], message["temp"], message["time"]
        if is_on != self.__is_on:
            self.__is_on = is_on
            if not self.__is_on and self.__time > 0 :
                self.__time = 0
                self.__temp = 0
            self.send_oven_report()
        if is_on and temp != self.__temp and time != self.__time:
            self.oven_working(temp=temp, time=time)

    @staticmethod
    def __set_timeout(func, sec):
        t = threading.Timer(sec, func)
        t.start()
        return t

    def oven_working(self, temp=None, time=None):
        if temp and time:
            self.__temp = temp
            self.__time = time
            self.send_oven_report()
            self.__set_timeout(self.oven_working, 10)
        else:
            if self.__time <= 0:
                self.__time = 0
                self.__temp = 0
                self.__is_on = False
                self.send_oven_report()
            else:
                self.__time -= 10
                self.send_oven_report()
                self.__set_timeout(self.oven_working, 10)

    def send_oven_report(self):
        is_on, temp, time = self.__is_on, self.__temp, self.__time
        self.__client.publish(
            f'smart',
            json.dumps({"device": f"{self.__path}", "data": {"is_on": is_on, "temp": temp, "time": time}})
        )

