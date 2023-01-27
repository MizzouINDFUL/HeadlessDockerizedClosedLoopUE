import mmap
import sys
import fileinput

filename = "/project/Source/"+sys.argv[1]+"/"+sys.argv[1]+".Build.cs"
text_to_search = "PublicDependencyModuleNames.AddRange(new string[] {"
replacement_text = 'PublicDependencyModuleNames.AddRange(new string[] { "UnrealEd",'

with open(filename, 'rb', 0) as file, \
     mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
    if s.find(b'"UnrealEd",') != -1:
        print('Made sure that UnrealEd module is included')
    else:
        with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(text_to_search, replacement_text), end='')
