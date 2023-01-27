# importing os module
import os
import sys
import subprocess
name = sys.argv[1]
# Specify path
path = "/project/Source/"+name
public = "/project/Source/"+name+"/Public"
private = "/project/Source/"+name+"/Private"
# process = subprocess.Popen("echo pwd", shell=True, stdout=subprocess.PIPE)
# Check whether the specified
# path exists or not
isExist = os.path.exists(path)
if not os.path.exists(path):
    process = subprocess.Popen("mkdir"+name, cwd="/project/Source", shell=True, stdout=subprocess.PIPE)
    process = subprocess.Popen("mkdir Public", cwd="/project/Source/"+name, shell=True, stdout=subprocess.PIPE)
    process = subprocess.Popen("mkdir Private"+name, cwd="/project/Source"+name, shell=True, stdout=subprocess.PIPE)
elif not os.path.exists(public):
    process = subprocess.Popen("mkdir Public", cwd="/project/Source/"+name, shell=True, stdout=subprocess.PIPE)
    process = subprocess.Popen("mkdir Private"+name, cwd="/project/Source"+name, shell=True, stdout=subprocess.PIPE)
process = subprocess.Popen("cp MindfulLib.h /project/Source/"+name+"/Public", cwd="/shared", shell=True, stdout=subprocess.PIPE)
process = subprocess.Popen("cp MindfulLib.cpp /project/Source/"+name+"/Private", cwd="/shared", shell=True, stdout=subprocess.PIPE)
