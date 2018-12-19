import boto3
import json
from decouple import config

sqs = boto3.resource('sqs')

MESSAGE_RETENTION_DAYS = config('MESSAGE_RETENTION_DAYS', default=10, cast=int)
MESSAGE_VISIBILITY_TIMEOUT_MINUTES = config('MESSAGE_VISIBILITY_TIMEOUT_MINUTES', default=1, cast=int)  # noqa
QUEUE_NAME = config('QUEUE_NAME', default='queue-example')


if __name__ == '__main__':

    assert MESSAGE_RETENTION_DAYS <= 14
    assert MESSAGE_VISIBILITY_TIMEOUT_MINUTES <= 720

    queue_default_attributes = {
        'DelaySeconds': '5',
        'VisibilityTimeout': str(60 * MESSAGE_VISIBILITY_TIMEOUT_MINUTES),
        'MessageRetentionPeriod': str(60 * 60 * 24 * MESSAGE_RETENTION_DAYS)
    }

    dead_letter_queue = sqs.create_queue(QueueName=f'{QUEUE_NAME}-DEAD-LETTER',
                                         Attributes=queue_default_attributes)

    redrive_policy = {
        'RedrivePolicy': json.dumps({
            'deadLetterTargetArn': dead_letter_queue.attributes['QueueArn'],
            'maxReceiveCount': 2,
        })
    }

    queue_default_attributes.update(redrive_policy)

    queue = sqs.create_queue(QueueName=QUEUE_NAME,
                             Attributes=queue_default_attributes)

    print(queue.url)
    print(queue.attributes.get('DelaySeconds'))

    print(dead_letter_queue.url)
    print(dead_letter_queue.attributes.get('DelaySeconds'))
