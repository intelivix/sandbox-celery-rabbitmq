import random
from tasks import add
from datetime import datetime
from datetime import timedelta
from decouple import config


QNT_TASKS = config('QNT_TASKS', default=1000, cast=int)
NOW = datetime.utcnow()

print(NOW.isoformat())

for num, _ in enumerate(range(QNT_TASKS)):
    print(num)
    a = random.randint(1, 100)
    b = random.randint(-100, 1)
    LATER = NOW + timedelta(seconds=10)
    add.apply_async((a, b), eta=LATER)
