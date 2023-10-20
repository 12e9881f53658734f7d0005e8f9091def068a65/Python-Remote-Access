import os

from websocket import WebSocket
from platform import node

op = os.path

def buildDirectory(path, recursive=False):
    if path == None: path = "c:\\"

    try:
        listing = os.listdir(path)
    except FileNotFoundError:
        return "Directory not found!"
    
    dirMap = {}

    for item in listing:
        fullItemPath = op.join(path, item)

        if op.isdir(fullItemPath):
            if recursive:
                dirMap[item] = buildDirectory(fullItemPath, recursive=True)
            else:
                dirMap[item] = {}
        elif op.isfile(fullItemPath):
            dirMap[item] = 1
        else:
            dirMap[item] = 2
    
    return dirMap

"""
dir: {}
file: 1
unknown: 2
"""
# Transfer in binary
# have to append local path to each file

def rebuildDirectory(localTargetDir, directoryList, recursive=False):
    for item in directoryList:
        joinedItemPath = os.path.join(localTargetDir, item)
        if type(directoryList[item]) == "set":
            os.mkdir(item) # have to append local path here

            if recursive:
                rebuildDirectory(joinedItemPath, directoryList, True)
        elif directoryList[item] == 1 or directoryList[item] == 2:
            with open(item, "wb") as file:
                pass


print(buildDirectory("C:\\Users\\knaro\\OneDrive\\Desktop\\testDir", True))