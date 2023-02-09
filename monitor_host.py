import os

while True:
    if os.path.isfile("./shared/ready.txt"):
        print("Starting airsim agent")
        os.remove("./shared/ready.txt")
    if os.path.isfile("./shared/stop.txt"):
        print("Stopping airsim agent")
        os.remove("./shared/stop.txt")
    continue
