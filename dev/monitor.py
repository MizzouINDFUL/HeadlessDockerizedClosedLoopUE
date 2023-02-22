import os.path
import time
import json
import subprocess

readyfile = "ready.txt"

while True:
	if not os.path.isfile(readyfile):
                time.sleep(10)
                f = open(readyfile, "w")
                print(subprocess.run(["touch", "/share/ready.txt"],
                     capture_output=True))
                # f2 = open(os.path.join("/root/shared/", readyfile), "w")
                print("Waiting for the life to start")
                while os.path.isfile(readyfile):
                    continue
                time.sleep(15)
                stopfile = "stop.txt"
                f = open(stopfile, "w")
                print(subprocess.run(["touch", "/share/stop.txt"],
                     capture_output=True))
                # f2 = open(os.path.join("/root/shared/", stopfile), "w")
                print("waiting for the life to stop")
                while os.path.isfile(stopfile):
                    continue
