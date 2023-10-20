from websockets import serve
from asyncio import get_event_loop

connectedMachines = []
async def main(websocket, path):
    while True:
        res = await websocket.recv()
        if "KEY: OmG" in res:
            try:
                print(res.split("CONNECT: ")[1].split(" KEY:")[0])
                await websocket.send("SUCCESS")
            except:
                pass
        await websocket.send("server.py")

asyncEventLoop = get_event_loop()
startWebSockets = serve(main, "localhost", 8765)
asyncEventLoop.run_until_complete(startWebSockets)
asyncEventLoop.run_forever()







# connect to 

