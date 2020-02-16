import RPi.GPIO as gp
import time
from multiprocessing import Process
from relay import Relay


gp.setmode(gp.BCM)

# Ultrasonic pins
# 0 = C piano key
pins = {
    # echo pin, trigger pin, piano key
    0: [17, 18, "c4"],
    1: [27, 23, "d4"],
    2: [22, 24, "e4"],
    3: [5, 25, "f4"],
    4: [6, 12, "g4"],
    5: [13, 16, "a4"],
    6: [19, 20, "b4"],
    7: [26, 21, "c4"],
}
playStatus = {}

gp.setup(trig,gp.OUT)

for k, v in pins.items():
    playStatus[k] = False
    avgDistance[k] = [0, [], 1]
    gp.setup(v[0], gp.IN)
    gp.setup(v[1], gp.OUT)

r = Relay(pins)


def play(k):
    if (playStatus[k]):
        return
    playStatus[k] = True
    print(k)
    r.press(k)


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')


def sonarSensor(k):
    global trig, avgDistance, playStatus, mutex

    echo = pins[k][0]

    '''
    if (mutex):
        return;
    mutex = True
    '''
    trig = pins[k][1]
    # time.sleep(0.2)
    gp.output(trig, True)
    time.sleep(0.1)
    gp.output(trig, False)

    start = time.time()
    stop = time.time()

    while(gp.input(echo) == 0):
        start = time.time()

    while(gp.input(echo) == 1):
        stop = time.time()

    t = stop-start
    distance = 17150*t

    maxDistance = 100
    # print(k, '-', distance)
    # print(get_change(120, 100))

    if (distance > 5 and distance < maxDistance and get_change(distance, 180) < -70):
        play(k)
    else:
        playStatus[k] = False


def looplisten(k):
    while True:
        sonarSensor(k)


try:
    started = False
    while True:
        if (started):
            continue
        for k, v in pins.items():
            t = Process(target=looplisten, args=[k])
            t.start()
        started = True
except KeyboardInterrupt as e:
    print(e)
    gp.cleanup()
