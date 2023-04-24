import json

data = {}
data["collection"] = "MyCollection"
data["fileUID"] = "example"
data["startTime"] = "2022-1-5T13:21:05.431000"
data["stopTime"] = "2022-1-5T13:22:18.725000"
data["nFrames"] = 2
data["frameAnnotations"] = {}

# #dump json data to a file
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)