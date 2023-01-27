import mmap
import sys
import fileinput

project = sys.argv[1]
newapi = (project.upper())+"_API"
filename = "/project/Source/"+sys.argv[1]+"/Public/MindfulLib.h"
text_to_search = "PROJECTNAME_API"


with open(filename, 'rb', 0) as file, \
     mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
    if s.find(b'PROJECTNAME_API') != -1:
        with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(text_to_search, newapi), end='')
        

