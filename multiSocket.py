import socketio
import pygame
import io
from PIL import Image
from game import P1, play, pause
import asyncio

# Create an asynchronous Socket.IO client
sio = socketio.AsyncClient()

# Handle connection events
@sio.event
async def connect():
    print("Connected to server")
    await sio.emit("register", "pygame")

@sio.event
async def connect_error(data):
    print("Connection failed:", data)

@sio.event
async def disconnect():
    print("Disconnected from server")

# Handle text messages from the server
@sio.on("input")
async def handle_input(data):
    print("Received input:", data)
    if data == "QUIT":
        global running
        running = False
    elif data == "LEFT":
        P1.move_left()
    elif data == "RIGHT":
        P1.move_right()
    elif data == "PAUSE":
        pause = True

async def send_game_frame():
    buffer = pygame.surfarray.array3d(pygame.display.get_surface())
    image = Image.fromarray(buffer.transpose(1, 0, 2))
    byte_io = io.BytesIO()
    image.save(byte_io, 'JPEG')
    await sio.emit("game", byte_io.getvalue())

async def run_socket_io():
    await sio.connect("http://localhost:3000")
    await sio.wait()

async def game_loop():
    global running
    while running:
        play()
        await send_game_frame()

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")

running = True

async def main():
    # Run both the Socket.IO client and the game loop concurrently
    await asyncio.gather(run_socket_io(), game_loop())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    running = False
    pygame.quit()