## ๐ฑ Celery
**๋ถ์ฐ ๋ฉ์์ง ์ ๋ฌ์ ๊ธฐ๋ฐ์ผ๋ก ๋์ํ๋ ๋น๋๊ธฐ ์์์ ๋์์ฃผ๋ python framework**๋ก์ Worker์ ํ ์ข๋ฅ์ด๋ค. 
celery๋ ๋ฉ์ผ๋ฐ์ก๋ฑ ์ฆ๊ฐ์ ์ธ ๊ฒฐ๊ณผ(์๋ต)๋ฅผ ์ ๊ณตํ๊ธฐ ์ด๋ ค์ด ์์ ์ํ์ ํ์ฉํ๋๋ฐ, ์ฆ ์์ฒญํ ์์์ ๊ฒฐ๊ณผ๊ฐ ๋ฐ๋ก ์ฃผ์ด์ง์ง ์๋๋ผ๋ ๋ค์ ์์์ ์ํํ๋๋ก ํ  ๋ ์ฌ์ฉํ๋ค.

<br>

### Broker
์์ฒญํ ์์์ ๊ฒฐ๊ณผ๋ฅผ ํ์ธํ๊ณ  ๋ค์ ์์์ ์ํํ๋๊ฒ ์๋๋ค๋ณด๋ ํด๋น ์์๋ง๋ค ์์๋๋ ์๊ฐ, ํ๊ฒฝ์ด ๋ค๋ฆ์ ๋ฐ๋ผ **์ค๋ณต์์, ์์ ๋๋ฝ**๋ฑ์ ๋ฌธ์ ๊ฐ ์๊ธธ ์ ์๋ค. ์ด๋ฌํ ๋ฌธ์ ํด๊ฒฐ์ ์ํด **๋๊ธฐ์ค์ธ ์์์ ๊ด๋ฆฌํ๊ณ  ์์์ด ์ ๋๋ก Worker(Celery)์๊ฒ ์ ๋ฌ๋๋๋ก Broker๊ฐ ํ์**ํ๊ฒ ๋๋ค.

Message Broker๋ ์ดํ๋ฆฌ์ผ์ด์ ๊ฐ ๋ฉ์์ง๋ฅผ ๊ตํํ  ์ ์๋๋ก Publisher(์ก์ ์)์๊ฒ ์ ๋ฌ๋ฐ์ ๋ฉ์์ง๋ฅผ Subscriber(์์ ์)์๊ฒ ์ ๋ฌํ๋ ์ค๊ฐ์ญํ ์ ํ๋ค. ์ด ๋ **์์ ๋ฉ์์ง๊ฐ ์ ์ฌ๋๋ ๊ณต๊ฐ์ด Message Queue(๋๊ธฐ์ด)**์ด๋ฉฐ ๋ฉ์์ง์ ๊ทธ๋ฃน์ Topic์ด๋ผ๊ณ  ํ๊ณ  Topic์ ์ด์ฉํด ๋ฐ์ดํฐ๊ตฌ๋ถ์ ํ๊ฒ ๋๋ค. ์ฆ Broker๊ฐ ์ฌ๊ณ ์๋ Worker์๊ฒ ์์์ ํ ๋นํ๊ณ  Celery๋ ์์๋ฉ์์ง๋ฅผ Message Queue์ ๋ณด๊ด, ๋ฉ์์ง๋ฅผ ๊ฐ์ ธ๊ฐ ์์์ ์ํํ๋ ์ญํ ์ ํ๋ค. 

### Broker์ ์ข๋ฅ
#### RabbitMQ
- AMQP๋ฅผ ๊ตฌํํ Message broker, ๋ฉ์ผ๋ฐ์ก ๋ฑ ์ฆ๊ฐ์ ์ธ ๊ฒฐ๊ณผ(์๋ต)๋ฅผ ์ ๊ณตํ๊ธฐ ์ด๋ ค์ด ์์ ์ํ์ ํ์ฉ
- AMQP : Client์ดํ๋ฆฌ์ผ์ด์๊ณผ middleware broker์์ ๋ฉ์์ง๋ฅผ ์ฃผ๊ณ ๋ฐ๊ธฐ ์ํ ํ๋กํ ์ฝ
#### Redis	
- ๋์คํฌ์ ์์ฃผํ๋ ์ธ๋ฉ๋ชจ๋ฆฌ ๋ฐ์ดํฐ๋ฒ ์ด์ค๋ก ๋ฉ๋ชจ๋ฆฌ๋ฅผ ์ด์ฉํ(in-memory) Cache์๋ฒ
- key-value๋ฅผ ์ด์ฉํด celery๊ฐ ์ฒ๋ฆฌํ   ์์์ redis๋ก ๋ณด๋ธ ํ cache์์ ํด๋น key๋ฅผ ์ ๊ฑฐํ๋ ๋ฐฉ์์ผ๋ก ์๋

๊ทธ ์ธ์๋ `Kafka`, `ActiveMQ`, `ZeroMQ`, `AmazonSNS`, `Gearman` ๋ฑ์ด ์๋ค. 

<br>

### Celery Architecture
![](https://images.velog.io/images/anjaekk/post/f66c7088-68ae-4afb-81a0-7897dd409106/image.png)

<br>


## Django์ ํจ๊ป Celery ์ค์ ํ๊ธฐ
### [python, django, celery, redis, mysql, docker-compose ๊ธฐ๋ฐ]


- ์ฅ๊ณ  ์๋ฒ์์ Message Queue๋ก Task๋ฅผ ์ ๋ฌํ๋ฉด ์ด๋ฅผ Message Broker์ธ Redis์ Queue์ ์ ์ฌํ๊ณ  ์ด๋ฅผ Worker์ธ Celery๊ฐ ๋ฐ์ Task๋ฅผ ๋น๋๊ธฐ๋ก ์ฒ๋ฆฌํ๊ณ  ๊ทธ ๊ฒฐ๊ณผ๋ฅผ Redis์ ์ ์ฅํ๋๋ก ํ  ๊ฒ์ด๋ค.

<br>
 
๊ธฐ๋ณธ์ ์ธ ์ฅ๊ณ  ์ธํ๊ณผ db์ฐ๊ฒฐ์ด ๋์ด์๋ค๋ ๊ฐ์ ํ์ celery๋ฅผ ์ฌ์ฉ์ ์ถ๊ฐํ  ๋ถ๋ถ์ ์์ฑํ๋๋ก ํ๊ฒ ๋ค.

> _๊ทธ ์ ์๋ ์ฅ๊ณ ์์ celery์ ์ฅ๊ณ ์ ๋ง๋ ๋ผ์ด๋ธ๋ฌ๋ฆฌ๋ฅผ ์ค์นํด์ค์ผ ํ์ง๋ง ์ฅ๊ณ  3.1๋ฒ์ ๋ถํฐ๋ ๋ณ๋์ ๋ผ์ด๋ธ๋ฌ๋ฆฌ ์ค์น ์์ด Celery์ฌ์ฉ์ด ๊ฐ๋ฅํ๋ค._

### ํ์ผ๊ตฌ์กฐ
```
- proj
  - api
     - settings.py
  - app
  - dockercompose.yml
  - Dockerfile
  - manage.py
```
### 1. celery ์ค์น
์ฅ๊ณ ์ ๋ง๋ ๋ผ์ด๋ธ๋ฌ๋ฆฌ๋ฅผ ์ค์น์ํ๋ ๊ฒ ๋ฟ. python celery ํจํค์ง๋ ์ค์นํด์ค์ผํ๋ค.
```
pip install Celery
pip install redis
pip install django_celery_results
```

### 2. docker-compose.yml ์ถ๊ฐ
```
  redis:
    image: redis:5.0-alpine
    container_name: redis_server
    ports: 
      - 6379:6379
    restart: unless-stopped
    volumes: 
      - proj-redis:/data
  
  worker:
    build:
      context: .
      dockerfile: Dockerfile.debug
    restart: unless-stopped
    command: celery -A api worker --loglevel=info
    depends_on:
      - redis
    volumes:
      - ./:/app/ 

volumes:
  proj:
  proj-data:
  proj-redis:
```
worker์ docker image๋ ๊ธฐ์กด api์ ์ฌ์ฉํ๋ dockerfile์ ๊ธฐ๋ฐ์ผ๋ก container๋ก ์คํํ  ๊ฒ์ด๋ค. command๋ก `celery -A api worker --loglevel=info`๋ฅผ ๋ฃ์ด celery worker ์๋ฒ๋ฅผ ์คํํ๋๋ก ํ๋ค. ์ฌ๊ธฐ์ api๋ ํ๋ก์ ํธ ํ์ผ์ ์ด๋ฆ์ด๋ค.


### 3. settings.py
```
INSTALLED_APPS = [
	:
    'django_celery_results',
]


# CELERY SETTINGS
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_BROKER_URL = 'redis://redis_server:6379/1'
CELERY_RESULT_BACKEND = 'redis://redis_server:6379/1'
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis_server:6379/1',  # redis_server: docker container์ด๋ฆ
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

`CELERY_RESULT_BACKEND`
- **Taskํธ์ถ ๊ฒฐ๊ณผ๋ก Task ์๋ฃ์ฌ๋ถ๋ฅผ ์ ์ ์๋ AsyncResult์ธ์คํด์ค๊ฐ ๋ฐํ๋๋๋ฐ ๊ธฐ๋ณธ์ ์ผ๋ก Task์คํ๊ฒฐ๊ณผ๋ ์ ์ฅ๋์ง ์์ผ๋ result backend ์ค์ ์ ํตํด ๊ฒฐ๊ณผ๋ฅผ ์ ์ฅํ  ์ ์๋ค.**


### 4. celeryconf.py
celery๋ฅผ ์ฌ์ฉํ๊ธฐ์ํด์๋ celery ๋ผ์ด๋ธ๋ฌ๋ฆฌ์ ์ธ์คํด์ค๋ฅผ ์ ์ํด์ผํ๋ค. 
celeryconf.py๋ setting.py๊ฐ ์๋ apiํ์ผ ์๋ ๋ง๋ค๋๋ก ํ๋ค.
```
from  __future__  import  absolute_import 
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
app = Celery('api')
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

`os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')`
- ์ด ์ค์ ์ ํตํด celery๊ฐ ์ฅ๊ณ  ํ๋ก์ ํธ์ ์์น๋ฅผ ์์ ์๊ฒ ๋๋ค. ๋น์ทํ ์๋ฏธ๋ก ์ฅ๊ณ  manage.py์๋ ๋์ผํ ๋ด์ฉ์ด ์๋๊ฑธ ํ์ธํ  ์ ์๋ค.

`app = Celery('api')`
- celery๋ผ์ด๋ธ๋ฌ๋ฆฌ์ ์ธ์คํด์ค๋ฅผ ์ ์ํ๋ค. ์ฌ๊ธฐ์ api๋ celery ์ฑ์ ์ด๋ฆ์ด๋ค.
`app.config_from_object('django.conf:settings', namespace='CELERY')`
- settings์ ์ ์ํ namespace๊ฐ CELERY์ธ ํญ๋ชฉ์ celeryํ๊ฒฝ์ค์  ๋ด์ฉ์ ๋ถ๋ฌ์จ๋ค.(์ค์ ์ settings.py๋ก ๋ถ๋ฆฌํ์ ๊ฒฝ์ฐ ์๋ ฅ)

`app.autodiscover_tasks()`
- autodiscover๋ฅผ ํ๊ฒ๋๋ฉด ๋ง๋  ์ฑ๋ค์ `CELERY_IMPORTS`์ ์ถ๊ฐํ  ํ์ ์์ด celery๋ฅผ ์ฌ์ฉํ  ์ ์๋ค.


### 5. `__init__.py`
```
from __future__ import absolute_import
from .celeryconf import app as celery_app

__all__ = ["celery_app"]
```
celery๋ฅผ ๋ฃ์ apiํด๋์ `__init__.py`๋ฅผ ์ค์ ํ์ง์์ผ๋ฉด ๋ชจ๋์ธ์์ ๋ชปํ๊ฒ๋๋ฏ๋ก ์ค์ ํด์ฃผ๋๋ก ํ๋ค. 

<br>

## Celery ์ฌ์ฉํ๊ธฐ
api container์ ๋ค์ด๊ฐ์ `celery -A api status` ์๋ ฅ์ ํตํด ์ฐ๊ฒฐ์ ํ์ธํ๋ค.

![](https://images.velog.io/images/anjaekk/post/83065c6c-c13e-43bf-be73-a01a29e4ecab/image.png)

์๋์ ๊ฐ์ด ๊ฐ๋จํ Taskํจ์๋ฅผ ์์ฑํ๊ณ  Task๋ฅผ ํธ์ถํด๋ณด๋๋ก ํ๊ฒ ๋ค.
```
# app.task.py

import time, random
from celery import shared_task


@shared_task
def print_hello(user):
    time.sleep( random.randint(1,5) )
    return print('hello {}'.format(user))
```

celery taskํธ์ถ์ delay()๋ฉ์๋๋ฅผ ์ฌ์ฉํ๋ค. 
```
<์ํํ๊ณ ์ํ๋ ํจ์>.delay(์ธ์1, ์ธ์2)
```
python shell์์ task๋ฅผ ์คํ์์ผ๋ณธ๋ค. 
```
>>> from app.tasks import *
>>> print_hello.delay('banana')
```

![](https://images.velog.io/images/anjaekk/post/58ec5d79-6ab1-42cb-93c7-34485a605659/image.png)

### worker log ํ์ธ
worker container์ ๋ค์ด๊ฐ `celery -A api worker -l info`๋ฅผ ์๋ ฅํด์ค๋ค.

![](https://images.velog.io/images/anjaekk/post/76b0a045-1b46-4ad5-98c7-73404ba3f97b/image.png)

### task id๋ฅผ ํตํด ๊ฒฐ๊ณผ ํ์ธํ๊ธฐ
task id๋ ์คํ ๋งค์๋์ ๊ฒฐ๊ณผ๋ก ๋์จ๋ค.
```
task_id = print_hello.delay('banana')
```
ํ์ง๋ง ์ฌ๊ธฐ์ ๋์จ task_id๋  AsyncResult์ ๊ฒฐ๊ณผ ํ์์ผ๋ก ํ์์ ํ์ธํด๋ณด๋ฉด ์๋์ ๊ฐ๋ค. 
```
<class 'celery.result.AsyncResult'>
```

๊ทธ๋ฌ๋ฏ๋ก ๊ฒฐ๊ณผ๋ฅผ ํ์ธํ  ๋๋ ํด๋น ์์ด๋๋ฅผ ๋ฌธ์์ด๋ก ๋ณํํ `AsyncResult`๋ฅผ ํตํด ํ์ธํด์ค๋ค. 
```
from celery.result import AsyncResult

def celery_state(task_id):
    task = AsyncResult(id=str(task_id), app=app)
   
    return {'state':task.state}
```

์ด์๋ํ ๊ฒฐ๊ณผ๋ ์๋์ ๊ฐ๋ค.
- *PENDING*
๊ฒฐ๊ณผ ๊ธฐ๋ค๋ฆฌ๋ ์ค


- *STARTED*
์์์ด ์์๋จ
 
- *RETRY*
์์์ด ์คํจํ์ฌ ์ฌ์๋ 

- *FAILURE*
์คํจ(์์ธ๊ฐ ๋ฐ์ํ๊ฑฐ๋ ์ฌ์๋ ํ์ ์ ํ ์ด๊ณผ) 

- *SUCCESS*
์ฑ๊ณต

๊ทธ์ธ ์์ธํ ๋ชจ๋ํฐ๋ง์ ๊ด๋ จ๋ ์ฌํญ์ [celery๋ฌธ์](https://docs.celeryproject.org/en/latest/userguide/monitoring.html#guide-monitoring)์ ์ ๋์์๋ค. 



<br>


> ์ฐธ์กฐ   
> ๐ [Celery ๋ฌธ์ | First Steps with Celery](https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps-with-celery)   
> ๐ [๋ถ์ฐ ๋น๋๊ธฐ ์์ ์ฒ๋ฆฌ๋ฅผ ์ํ Celery ์ฒซ๊ฑธ์ | ์กฐ์์ฐ ๊ฐ๋ฐ ๋ธ๋ก๊ทธ](https://jonnung.dev/python/2018/12/22/celery-distributed-task-queue/)  
> ๐ [RabbitMQ ์ Redis ์ ์ฐจ์ด | ๋ฐฉ๋์ ๋ธ๋ก๊ทธ](https://m.blog.naver.com/aim4u/221766568746)  
> ๐ [Docker๋ก Django, Celery, MairaDB, Redis ๊ฐ๋ฐํ๊ฒฝ ์ค์ ํ๊ธฐ | khtinsoft ๋ธ๋ก๊ทธ](https://blog.khtinsoft.xyz/posts/django-celery-mariadb-redis-docker/)  
> ๐ [[Celery] ๋ฌด์์  ์์ํ๊ธฐ (2) - Task | ๊ฐ๋ฐํ๋ ๋์น ๋ธ๋ก๊ทธ](https://heodolf.tistory.com/63) 
