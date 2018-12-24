import boto3
import json
import random
import time
from decouple import config
from concurrent.futures import ThreadPoolExecutor
import asyncio

QNT_TASKS = config('QNT_TASKS', default=1000, cast=int)
QUEUE_NAME = config('QUEUE_NAME', default='celery-sandbox-sqs')

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)


def add_(x, y):
    return queue.send_message(
        MessageBody=json.dumps({'x': x, 'y': y}),
        MessageAttributes={
            'key': {
                'StringValue': 'just-an-example-string',
                'DataType': 'String'
            },
            'number': {
                'StringValue': '1',
                'DataType': 'Number'
            }
         })


async def call(executor, num, futs):
    print(num)
    futs.append(executor.submit(add_, random.randint(1, 100),
                                random.randint(-100, 1)))


async def run():
    futs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        await asyncio.gather(*[call(executor, n, futs)
                             for n in range(QNT_TASKS)])
        results = [fut.result() for fut in futs]


if __name__ == '__main__':
    t0 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    t1 = time.time()

    print('Job took %.03f sec.' % (t1 - t0))
