import os
import subprocess
import sys
script = sys.argv[1]
# Specify path
path = 'start_docker'
# Check whether the specified
# path exists or not
isExist = os.path.exists(path)
while not isExist:
    print("Waiting for the editor to start")
    isExist = os.path.exists(path)
print("Unreal Engine project is ready. Starting the agent at "+script)
