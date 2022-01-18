import paho.mqtt.client as mqtt
import json
import threading


class Speaker:

    def __init__(self, path):
        self.__path = path
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("localhost", 1883, 60)
        self.__client.loop_start()
        self.__is_on = False
        self.__is_playing = False
        self.__song = ""
        self.__time_left = 0
        self.send_speaker_report()

    def __on_connect(self, client, userdata, flags, rc):
        self.__client.subscribe([(f'smart/{self.__path}', 0)])

    def __on_message(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8", "ignore")))["data"]
        is_on, is_playing, song = message["is_on"], message["is_playing"], message["song"]
        if song != "":
            self.play(song, message["time_left"])
        if is_on != self.__is_on:
            self.__is_on = is_on

    @staticmethod
    def __set_timeout(func, sec):
        t = threading.Timer(sec, func)
        t.start()
        return t

    def __song_ends(self):
        self.__is_playing = False
        self.__song = ""
        self.send_speaker_report()

    def send_speaker_report(self):
        data = {
            "is_on": self.__is_on, "is_playing": self.__is_playing, "song": self.__song, "time_left": self.__time_left
        }
        self.__client.publish(f'smart', json.dumps({"device": f"{self.__path}", "data": data}))

    def play(self, song: str = None, duration_in_seconds: int = None):
        if song or duration_in_seconds:
            self.__is_playing = True
            self.__song = song
            self.__time_left = duration_in_seconds
        self.send_speaker_report()
        if self.__time_left <= 0:
            self.__time_left = 0
            self.__song_ends()
        else:
            self.__time_left -= 5
            self.__set_timeout(self.play, 5)
