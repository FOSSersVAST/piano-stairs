import RPi.GPIO as gp
import time


gp.setmode(gp.BCM)

trig=5

echoes={
	0: 6, #0
	#1: 13
}
lastPlayed = {
	0: False,
	1: False
}

gp.setup(trig,gp.OUT)

for i in echoes.items():
	gp.setup(i, gp.IN)
	
def play(k):
	if (lastPlayed[k]):
		return
	lastPlayed[k] = True
	print(k)

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')

def sonarSensor(k, echo):
	global trig, lastPlayed
	
	gp.output(trig, True)
	time.sleep(0.1)
	gp.output(trig, False)
	
	start = time.time()
	stop = time.time()
	
	while(gp.input(echo)==0):
		start=time.time()
	
	while(gp.input(echo)==1):
		stop=time.time()
	
	t=stop-start
	distance=(34300*t)/2
	#print(echo, '-', distance)
	#print(get_change(distance, 145))
	
	#print(get_change(120, 100))

	if (distance > 0 and distance < 100 and get_change(distance, 145) < -5):
		play(k)
	else:
		lastPlayed[k] = False

try:
	while True:
		for k, v in echoes.items():
			sonarSensor(k, v)
except KeyboardInterrupt as e:
	print(e)
	gp.cleanup()

