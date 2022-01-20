import paho.mqtt.client as mqtt
import json
import threading


class CoffeeMaker:

    def __init__(self, path):
        self.__path = path
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()
        self.__is_on = False
        self.__coffee_beans_level = 0.6
        self.__water_level = 0.6
        self.__status = ""
        self.send_report()

    def __on_connect(self, client, userdata, flags, rc):
        self.__client.subscribe([(f'smart/{self.__path}', 0)])

    def __on_message(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))["data"]
        if self.__is_on != message["is_on"]:
            self.__is_on = message["is_on"]
            self.send_report()
        if message["action"]:
            if message["action"] == "coffee":
                self.make_coffee()

    def make_coffee(self):
        if self.__coffee_beans_level >= 0.05:
            if self.__water_level >= 0.1:
                self.__coffee_beans_level -= 0.05
                self.__water_level -= 0.1
                self.__status = "Making coffee..."
                self.send_report()
                self.__set_timeout(self.coffee_made, 10)
            else:
                self.__status = "Water level is too low!"
                self.send_report()
        else:
            self.__status = "Coffee beans level is too low!"
            self.send_report()

    def coffee_made(self):
        self.__status = ""
        self.send_report()

    @staticmethod
    def __set_timeout(func, sec):
        t = threading.Timer(sec, func)
        t.start()
        return t

    def send_report(self):
        is_on, status, bean_level, water_level = self.__is_on, self.__status,\
                                                 self.__coffee_beans_level, self.__water_level
        self.__client.publish(
            f'smart',
            json.dumps({"device": f"{self.__path}", "data": {
                "is_on": is_on, "status": status,
                "bean": bean_level, "water": water_level
            }})
        )
