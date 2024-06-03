import socketio
import time
import sys

def generate_ogs_socket_handler():
    url = "https://online-go.com"
    params = {"transports": ["websocket"]}

    socket = socketio.Client()
    socket.connect(url, transports=params["transports"])

    @socket.event
    def connect():
        print("connected to OGS socket!")

    return socket

def listen_review_full_state(socket: socketio.Client, review_id):
    event_name = f"review/{review_id}/full_state"
    socket.on(event_name, print)  # Print the received message
    print(f"Listening to event: {event_name}")

def listen_review_move_response(socket: socketio.Client, review_id):
    event_name = f"review/{review_id}/r"
    socket.on(event_name, print)  # Print the received message
    print(f"Listening to event: {event_name}")

def listen_hostinfo(socket: socketio.Client):
    event_name = "hostinfo"
    socket.on(event_name, print)  # Print the received message
    print(f"Listening to event: {event_name}")
  
# emit

def emit_authenticate(socket: socketio.Client, chat_auth, player_id, username, jwt):
    event_name = "authenticate"
    data = {
        "auth": str(chat_auth),
        "player_id": str(player_id),
        "username": str(username),
        "jwt": str(jwt)
    }
    socket.emit(event_name, data)
    print("Emitting 'authenticate' event")

def emit_connect_review(socket: socketio.Client, chat_auth, review_id, player_id):
    event_name = "review/connect"
    data = {
        "auth": chat_auth,
        "review_id": review_id,
        "player_id": player_id
    }
    socket.emit(event_name, data)
    print("Emitting 'review/connect' event")

def emit_hostinfo(socket: socketio.Client):
    event_name = "hostinfo"
    socket.emit(event_name)
    print("Emitting 'hostinfo' event")

# Placeholder functions for unimplemented events
def emit_connect_chat(socket: socketio.Client):
    pass  # Implement logic for 'connect/chat' event

def emit_connect_notification(socket: socketio.Client):
    pass  # Implement logic for 'connect/notification' event

def emit_connect_incident(socket: socketio.Client):
    pass  # Implement logic for 'connect/incident' event

def emit_review_append_move(socket: socketio.Client, updated_move_string, review_id, player_id):
    event_name = "review/append"
    data = {
        "f": 0,
        "t": "",
        "m": updated_move_string,
        "k": {},
        "review_id": review_id,
        "player_id": player_id
    }
    socket.emit(event_name, data)
    print("Emitting 'review/append' event")
    
def emit_ping(socket: socketio.Client):
    event_name = "net/ping"
    data = {
        "client": int(time.time()),
        "drift": 400,
        "latency": 130
    }
    socket.emit(event_name, data)
    print("Emitting 'net/ping' event")
