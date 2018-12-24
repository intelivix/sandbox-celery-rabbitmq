from loafer.ext.aws.routes import SQSRoute
from .handlers import handler_add
from .handlers import error_handler
from decouple import config


routes = (
    SQSRoute(config('QUEUE_NAME', 'loafer-test'),
             {'options': {'WaitTimeSeconds': 3}},
             handler=handler_add,
             error_handler=error_handler),
)
