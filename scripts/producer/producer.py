import random
from tasks import add
from decouple import config


QNT_TASKS = config('QNT_TASKS', default=1000, cast=int)

for num, _ in enumerate(range(QNT_TASKS)):
    print(num)
    a = random.randint(1, 100)
    b = random.randint(-100, 1)
    add.delay(a, b)
