import paho.mqtt.client as mqtt
import json
import threading


class SmartBlinds:

    def __init__(self, path):
        self.__path = path
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()
        self.__on_status = "Open"
        self.send_on_report()

    def __on_connect(self, client, userdata, flags, rc):
        self.__client.subscribe([(f'smart/{self.__path}', 0)])

    def __on_message(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))["data"]
        new_on_status = message["on_status"]
        if new_on_status == "Closed" and self.__on_status == "Open":
            self.__on_status = "Closing..."
            self.__set_timeout(self.__close, 10)
        elif new_on_status == "Open" and self.__on_status == "Closed":
            self.__on_status = "Opening..."
            self.__set_timeout(self.__open, 10)

        self.send_on_report()

    def __open(self):
        self.__on_status = "Open"
        self.send_on_report()

    def __close(self):
        self.__on_status = "Closed"
        self.send_on_report()

    @staticmethod
    def __set_timeout(func, sec):
        t = threading.Timer(sec, func)
        t.start()
        return t

    def send_on_report(self):
        is_on = self.__on_status
        self.__client.publish(f'smart',
                              json.dumps({"device": f"{self.__path}", "data": is_on}))
