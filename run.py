from app import create_app
from flask_socketio import (
    SocketIO,
)  # Flask-SocketIO enables real-time communication between the server and the client.

appln = create_app()
socketio = SocketIO(appln)

if __name__ == "__main__":
    socketio.run(appln, debug=True)
