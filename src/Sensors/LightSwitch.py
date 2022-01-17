import paho.mqtt.client as mqtt
import json
import threading


class LightSwitch:

    def __init__(self, path):
        self.__path = path
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()
        self.__on = False
        self.send_on_report()
        self.__set_interval(self.send_on_report, 60)

    def __on_connect(self, client, userdata, flags, rc):
        # print(f'smart/{self.__path}')
        self.__client.subscribe([(f'smart/{self.__path}', 0)])

    def __on_message(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))["data"]
        self.__on = message["switch"]
        self.send_on_report()

    def __set_interval(self, func, sec):
        def func_wrapper():
            self.__set_interval(func, sec)
            func()

        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t

    def send_on_report(self):
        is_on = self.__on
        self.__client.publish(f'smart',
                              json.dumps({"device": f"{self.__path}", "data": is_on}))
