import os

from websocket import WebSocket
from platform import node

op = os.path

def mapDirectory(path, recursive=False):
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
                dirMap[item] = mapDirectory(fullItemPath, True)
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

def uploadFile(websocket, path, readSize=16000000):
    if not os.path.exists(path): return False
    # send size of file so that server can tell when data stream is done
    with open(path, "rb") as f:
        d = f.read(16000000)
        while d:
            websocket.send(d)
            d = f.read(readSize)
    
    print("File sent!")

# TOGO in client
def rebuildDirectory(localTargetDir, directoryList, recursive=False):
    for item in directoryList:
        joinedItemPath = os.path.join(localTargetDir, item)

        if type(directoryList[item]) is dict:

            os.mkdir(joinedItemPath) # have to append local path here
            if recursive:
                rebuildDirectory(joinedItemPath, directoryList[item], True)
        
        elif directoryList[item] == 1 or directoryList[item] == 2:
            with open(joinedItemPath, "wb") as file:
                pass

path = "C:\\Users\\knaro\\OneDrive\\Desktop\\testDir"

dirMap = {}
dirMap[os.path.basename(path)] = mapDirectory(path, True)

print(dirMap)

rebuildDirectory(os.path.dirname(os.path.abspath(__file__)), dirMap, True)