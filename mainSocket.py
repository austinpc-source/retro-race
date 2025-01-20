import socketio
import threading
import pygame
import io
from PIL import Image
import numpy as np
from game import Game

# Main connection
main_sio = socketio.Client()
game_connections = {}

@main_sio.event
def connect():
    print("Main connection established")
    main_sio.emit("register", "pygame")

@main_sio.on("ready-for-games")
def ready_for_games():
    print("Main connection ready for games")

@main_sio.on("start-game")
def start_game(data):
    game_id = data["gameId"]
    print(f"Starting game with ID: {game_id}")
    if game_id not in game_connections:
        game_connection = GameConnection(game_id)
        game_connections[game_id] = game_connection
        game_connection.start()
        # start_game_connection(game_id)

class GameConnection:
    def __init__(self, game_id):
        self.game_id = game_id
        self.game_sio = socketio.Client()
        # self.running = True
        self.game = Game()

        @self.game_sio.event
        def connect():
            print(f"Connected to game {self.game_id}")
            self.game_sio.emit("join-game", {"gameId": self.game_id})

        @self.game_sio.on("input")
        def handle_input(data):
            print(f"Game {self.game_id} input received: {data}")
            if data == "QUIT":
                # self.running = False
                self.game.stop()
            elif data == "LEFT":
                self.game.P1.move_left()
            elif data == "RIGHT":
                self.game.P1.move_right()

        @self.game_sio.on("partner-disconnected")
        def handle_destroy_thread():
            print(len(game_connections))
            game_connections.pop(game_id, None)
            print(len(game_connections))
            # self.running = False
            self.game.stop()

    def send_game_frame(self):
        try:
            buffer = pygame.surfarray.array3d(pygame.display.get_surface())
            image = Image.fromarray(buffer.transpose(1, 0, 2))
            byte_io = io.BytesIO()
            image.save(byte_io, 'JPEG')
            self.game_sio.emit("game-frame", {"gameId": self.game_id, "data": byte_io.getvalue()})
        except Exception as e:
            print(f"Error in sending frame for game {self.game_id}: {e}")
            # self.running = False
            self.game.stop()

    def game_loop(self):
        try:
            print("Starting the loop")
            self.game.play()
            self.send_game_frame()
        except KeyboardInterrupt:
            # self.running = False
            self.game.stop()
        finally:
            self.game_sio.disconnect()
    
    def start(self):
        try:
            self.game_sio.connect("http://localhost:3000")
            print(f"Connection for game {self.game_id} established.")
            game_thread = threading.Thread(target=self.game_loop, daemon=True)
            game_thread.start()
        except Exception as e:
            print(f"Error in starting game connection for game {self.game_id}: {e}")
            # self.running = False
            self.game.stop()

# def start_game_connection(game_id):
#     """Start a new connection for a specific game."""
#     game_sio = socketio.Client()
#     state = { "running": True }

#     @game_sio.event
#     def connect():
#         print(f"Connected to game {game_id}")
#         game_sio.emit("join-game", {"gameId": game_id})

#     @game_sio.on("input")
#     def handle_input(data):
#         print(f"Game {game_id} input received: {data}")
#         if data == "QUIT":
#             state["running"] = False
#         elif data == "LEFT":
#             P1.move_left()
#         elif data == "RIGHT":
#             P1.move_right()

#     @game_sio.on("partner-disconnected")
#     def handle_destroy_thread():
#         print(len(game_connections))
#         game_connections.pop(game_id, None)
#         print(len(game_connections))
#         state["running"] = False

#     def send_game_frame():
#         try:
#             buffer = pygame.surfarray.array3d(pygame.display.get_surface())
#             image = Image.fromarray(buffer.transpose(1, 0, 2))
#             byte_io = io.BytesIO()
#             image.save(byte_io, 'JPEG')
#             game_sio.emit("game-frame", {"gameId": game_id, "data": byte_io.getvalue()})
#         except Exception as e:
#             print(f"Error in sending frame for game {game_id}: {e}")
#             state["running"] = False
    
#     # Run the game in a separate thread
#     def game_loop():
#         try:
#             while state["running"]:
#                 play()
#                 send_game_frame()
#         except KeyboardInterrupt:
#             state["running"] = False
#         finally:
#             game_sio.disconnect()

#     try:
#         game_sio.connect("http://localhost:3000")
#         print(f"Connection for game {game_id} established.")
#         game_connections[game_id] = game_sio
#         game_thread = threading.Thread(target=game_loop, daemon=True)
#         game_thread.start()
#     except Exception as e:
#         print(f"Error connecting for game {game_id}: {e}")
    

main_sio.connect("http://localhost:3000")
main_sio.wait()