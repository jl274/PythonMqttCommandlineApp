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
        self.send_temperature_report()
        self.__set_interval(self.send_temperature_report, 20)

    def __on_connect(self, client, userdata, flags, rc):
        print(f'smart/{self.__path}')
        self.__client.subscribe([(f'smart/{self.__path}', 0)])

    def __on_message(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))["data"]
        if message["temp"] is not False:
            self.set_temperature(int(message["temp"]))
            self.send_temperature_report()

    def __set_interval(self, func, sec):
        def func_wrapper():
            self.__set_interval(func, sec)
            func()

        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t

    def set_temperature(self, temp):
        self.__temp = temp

    def send_temperature_report(self):
        temperature = self.__temp
        self.__client.publish(f'smart',
                              json.dumps({"device": f"{self.__path}", "data": temperature}))

