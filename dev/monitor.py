import os.path
import time
import json

readyfile = "ready.txt"

while True:
	if not os.path.isfile(readyfile):
                time.sleep(10)
                f = open(readyfile, "w")
                f2 = open(os.path.join("/shared/", readyfile))
                print("Waiting for the life to start")
                while os.path.isfile(readyfile):
                    continue
                time.sleep(15)
                stopfile = "stop.txt"
                f = open(stopfile, "w")
                f2 = open(os.path.join("/shared/", stopfile))
                print("waiting for the life to stop")
                while os.path.isfile(stopfile):
                    continue
