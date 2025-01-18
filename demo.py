import socketio
import time

# Create a Socket.IO client
sio = socketio.Client()

# Handle connection events
@sio.event
def connect():
    print("Connected to server")
    # Register as "pygame"
    sio.emit("register", "pygame")
    # Send binary data example
    binary_data = b"\x00\x01\x02\x03"
    sio.emit("game", binary_data)

@sio.event
def connect_error(data):
    print("Connection failed:", data)

@sio.event
def disconnect():
    print("Disconnected from server")

# Handle text messages from the server
@sio.on("input")
def handle_text_message(data):
    print("Received text message:", data)

# Connect to the Socket.IO server
sio.connect("http://localhost:3000")

# Keep the connection alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sio.disconnect()
