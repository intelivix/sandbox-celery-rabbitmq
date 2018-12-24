from raven import Client
from loafer.ext.sentry import sentry_handler
from decouple import config


def sum_(x, y):
    return x + y


async def handler_add(data, *args):
    print(data)
    return sum_(data['x'], data['y'])

client = Client(config('SENTRY_TOKEN_URL'))
error_handler = sentry_handler(client, delete_message=False)
