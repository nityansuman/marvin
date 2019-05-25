"""
This script runs the ATP application using a development server.
"""

from os import environ
from atp import app

if __name__ == "__main__":
    HOST = environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(environ.get("SERVER_PORT", "5555"))
    except ValueError:
        PORT = 1234
    app.run(HOST, PORT, debug=True)
