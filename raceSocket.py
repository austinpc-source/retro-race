import socketio

import pygame
import io
from PIL import Image
from game import P1, play

# Create a Socket.IO client
sio = socketio.Client()

# Handle connection events
@sio.event
def connect():
    print("Connected to server")
    # Register as "pygame"
    sio.emit("register", "pygame")

@sio.event
def connect_error(data):
    print("Connection failed:", data)

@sio.event
def disconnect():
    print("Disconnected from server")

# Handle text messages from the server
@sio.on("input")
def handle_input(data):
    print("Received input:", data)
    if data == "QUIT":
        running = False
    elif data == "LEFT":
        P1.move_left()
    elif data == "RIGHT":
        P1.move_right()

def send_game_frame():
    buffer = pygame.surfarray.array3d(pygame.display.get_surface())
    image = Image.fromarray(buffer.transpose(1, 0, 2))
    byte_io = io.BytesIO()
    image.save(byte_io, 'JPEG')
    sio.emit("game", byte_io.getvalue())

# Connect to the Socket.IO server
sio.connect("http://localhost:3000")

# Keep the connection alive
try:
    while True:
        play()

        send_game_frame()


        
except KeyboardInterrupt:
    sio.disconnect()
