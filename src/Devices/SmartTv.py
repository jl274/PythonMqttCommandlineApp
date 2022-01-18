import paho.mqtt.client as mqtt
import json
import threading


class SmartTV:

    def __init__(self, path):
        self.__path = path
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()
        self.__is_on = False
        self.__channel = 1
        self.__volume = 10
        self.__is_recording = False
        self.send_tv_report()
        # self.__set_interval(self.send_tv_report, 20)

    def __on_connect(self, client, userdata, flags, rc):
        # print(f'smart/{self.__path}')
        self.__client.subscribe([(f'smart/{self.__path}', 0)])

    def __on_message(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))["data"]
        [is_on, channel, volume, is_recording] = [
            message["is_on"], message["channel"], message["volume"], message["is_recording"]
        ]
        if is_on != self.__is_on:
            self.__is_on = is_on
        if channel != self.__channel:
            self.__channel = channel
        if volume != self.__volume:
            self.__volume = volume
        if is_recording != self.__is_recording:
            self.__is_recording = is_recording
        self.send_tv_report()

    # def __set_interval(self, func, sec):
    #     def func_wrapper():
    #         self.__set_interval(func, sec)
    #         func()
    #
    #     t = threading.Timer(sec, func_wrapper)
    #     t.start()
    #     return t

    def send_tv_report(self):
        data = {
            "is_on": self.__is_on, "channel": self.__channel,
            "volume": self.__volume, "is_recording": self.__is_recording
        }
        self.__client.publish(f'smart', json.dumps({"device": f"{self.__path}", "data": data}))

