import socket
from kombu import Connection
from decouple import config

RABBITMQ_URL = config('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')

with Connection(RABBITMQ_URL) as c:
    try:
        c.connect()
    except socket.error:
        raise ValueError("Received socket.error, "
                         "rabbitmq server probably isn't running")
    except IOError:
        raise ValueError("Received IOError, probably bad credentials")
    else:
        print("Credentials are valid")
