
from celeryapp import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def add(a, b):
    logger.info('Adding {0} + {1}'.format(a, b))
    return a + b


@app.task
def sub(a, b):
    logger.info('Subtraction {0} + {1}'.format(a, b))
    return a - b


@app.task
def mult(a, b):
    logger.info('Multiplication {0} + {1}'.format(a, b))
    return a * b


@app.task
def div(a, b):
    logger.info('Division {0} + {1}'.format(a, b))
    return a / b


@app.task
def mod(a, b):
    logger.info('Mod {0} + {1}'.format(a, b))
    return a % b
