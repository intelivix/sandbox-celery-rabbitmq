from decouple import config

BROKER_URL = config('RABBITMQ_URL',
                    default='amqp://guest:guest@localhost:5672/')

TASK_SERIALIZER = 'json'
RESULT_SERIALIZER = 'json'
ACCEPT_CONTENT = ['application/json']
CONTENT_ENCODING = 'utf-8'
TIMEZONE = 'America/Recife'
ENABLE_UTC = True

CELERY_IGNORE_RESULT = True

if 'sqs://' in BROKER_URL:
    BROKER_TRANSPORT = 'sqs'
    CELERY_ENABLE_REMOTE_CONTROL = False
    CELERY_SEND_EVENTS = False
    SQS_QUEUE_NAME = config('QUEUE_NAME', default='celery-sandbox-sqs')

    BROKER_TRANSPORT_OPTIONS = {
        'region': 'us-east-1',
        'polling_interval': 20,
        'visibility_timeout': 1800,
        'queue_name_prefix': f'{SQS_QUEUE_NAME}-'
    }


# TASK_APPS = (
#    'tasks',
# )

CELERY_ROUTES = {
    'tasks.add': {'queue': 'default'},
    'tasks.download': {'queue': 'download'},
}
