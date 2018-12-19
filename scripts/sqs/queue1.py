import boto3
from decouple import config

sqsr = boto3.resource('sqs')
sqs = boto3.client('sqs')

QUEUE_NAME = config('QUEUE_NAME', default='queue-example')


if __name__ == '__main__':

    queues = sqs.list_queues(
        QueueNamePrefix=QUEUE_NAME
    )

    for q in queues.get('QueueUrls', []):
        queue = sqsr.Queue(q)
        print(queue.url)
        print(queue.attributes)
        queue.purge()
        queue.delete()
