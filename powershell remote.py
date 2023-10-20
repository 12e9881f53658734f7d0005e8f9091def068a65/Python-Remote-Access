import subprocess


def spawnPowerShell():
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
            if "ENDOFOUTPUT9" in line and "Write-Host" not in line:
                break
            else:
                output.append(line)
        return output

    directory = ""
    while True:
        cmd = input(f"PS{directory}> ")

        if cmd.lower() == "exit": break

        output = readWriteSTD(ps, cmd)
        
        for line in output:
            if "PS C:\\" in line and f"> {cmd}" in line:
                directory = " " + line.split("PS C:\\")[1].split(f"> {cmd}")[0]
            elif line:
                print(line)

    ps.stdin.close()
    ps.terminate()


spawnPowerShell()