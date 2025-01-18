# import asyncio
# import websockets

# async def echo(websocket, path):
#     print("Client connected")
#     # Send a message to the client
#     await websocket.send("Hello, Client!")
#     async for message in websocket:
#         print(f"Received: {message}")
#         # Echo the message back to the client
#         await websocket.send(f"Echo: {message}")

# async def main():   
#     print("Starting server...") 
#     start_server = websockets.serve(echo, "localhost", 3000)
#     await start_server
#     print("Server started")
#     await asyncio.Future()  # run forever

# asyncio.run(main())