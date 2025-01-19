import socketio
import pygame
import io
from PIL import Image
from game import P1, play
import threading

# Create a Socket.IO client
sio = socketio.Client()
game_id = None  # Store the game ID for this client

# Handle connection events
@sio.event
def connect():
    print("Connected to server")
    sio.emit("register", "pygame")

@sio.event
def paired(data):
    global game_id
    game_id = data["gameId"]
    print(f"Paired with game ID: {game_id}")

@sio.event
def connect_error(data):
    print("Connection failed:", data)

@sio.event
def disconnect():
    print("Disconnected from server")

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
    if not game_id:
        return  # Don't send frames until paired
    buffer = pygame.surfarray.array3d(pygame.display.get_surface())
    image = Image.fromarray(buffer.transpose(1, 0, 2))
    byte_io = io.BytesIO()
    image.save(byte_io, 'JPEG')
    sio.emit("binary-data", {"gameId": game_id, "data": byte_io.getvalue()})

def run_socket_io():
    # Connect to the Socket.IO server
    sio.connect("http://localhost:3000")
    # Wait for pairing
    sio.emit("pair", "your-game-id")  # Replace with actual game ID
    sio.wait()

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")

running = True

def game_loop():
    global running
    while running:
        play()
        send_game_frame()

# Start the Socket.IO thread
socket_thread = threading.Thread(target=run_socket_io, daemon=True)
socket_thread.start()

# Start the game loop in the main thread
try:
    game_loop()
except KeyboardInterrupt:
    running = False
    sio.disconnect()
    pygame.quit()