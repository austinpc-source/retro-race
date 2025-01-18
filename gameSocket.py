# import asyncio
# import websockets
# import pygame
# import io
# from PIL import Image
# from game import P1, play, DISPLAYSURF, clock

# async def handle_client(websocket, path):
#     print("Client connected.")
#     running = True

#     while running:
#         # Handle inputs from the WebSocket
#         try:
#             data = await websocket.recv()  # Receive input as JSON string
#             print("Received:", data)
#             if data == "QUIT":
#                 running = False
#             elif data == "UP":
#                 P1.move_up()
#             elif data == "DOWN":
#                 P1.move_down()
#             elif data == "LEFT":
#                 P1.move_left()
#             elif data == "RIGHT":
#                 P1.move_right()
#         except websockets.ConnectionClosed:
#             print("Client disconnected.")
#             break

#         # Update game logic
#         # play()
#         DISPLAYSURF.fill((0, 0, 0))
#         P1.draw(DISPLAYSURF)
#         pygame.display.flip()
#         clock.tick(30)

#         # Capture and send the frame
#         buffer = pygame.surfarray.array3d(pygame.display.get_surface())
#         image = Image.fromarray(buffer.transpose(1, 0, 2))
#         byte_io = io.BytesIO()
#         image.save(byte_io, 'JPEG')
#         await websocket.send(byte_io.getvalue())  # Send frame as binary data

# async def main():   
#     print("Starting server...") 
#     start_server = websockets.serve(handle_client, "localhost", 6018)
#     await start_server
#     print("Server started")
#     await asyncio.Future()  # run forever

# asyncio.run(main())