import RPi.GPIO as gpio
import time
import os


def playFile(filename):
    os.system("mpg123 " + filename + " > /dev/null 2>&1")
    time.sleep(1)
    #client.play(1)
    #client.stop()
    pass


class Relay:
    pins = {}

    def __init__(self, pins):
        self.pins = pins

        for i in self.pins.values():
            gpio.setup(i[1], gpio.OUT)

    def soundnow(self, relayPin, filename):
        #gpio.output(21, False)
        playFile(filename)
        #time.sleep(0.1)
        #gpio.output(21, True) 

    # on key press, play sound and switch on relay light
    def press(self, key):
        #t = Process(target=self.soundnow, args=[self.pins[key][1], "sounds/" + self.pins[key][2] + ".mp3"])
        #t.start()
        self.soundnow(self.pins[key][1], "sounds/" + self.pins[key][2] + ".mp3")
