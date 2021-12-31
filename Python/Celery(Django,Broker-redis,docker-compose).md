## 🌱 Celery
**분산 메시지 전달을 기반으로 동작하는 비동기 작업을 도와주는 python framework**로서 Worker의 한 종류이다. 
celery는 메일발송등 즉각적인 결과(응답)를 제공하기 어려운 작업 수행시 활용하는데, 즉 요청한 작업의 결과가 바로 주어지지 않더라도 다음 작업을 수행하도록 할 때 사용한다.

<br>

### Broker
요청한 작업의 결과를 확인하고 다음 작업을 수행하는게 아니다보니 해당 작업마다 소요되는 시간, 환경이 다름에 따라 **중복작업, 작업 누락**등의 문제가 생길 수 있다. 이러한 문제해결을 위해 **대기중인 작업을 관리하고 작업이 제대로 Worker(Celery)에게 전달되도록 Broker가 필요**하게 된다.

Message Broker는 어플리케이션 간 메시지를 교환할 수 있도록 Publisher(송신자)에게 전달받은 메시지를 Subscriber(수신자)에게 전달하는 중간역할을 한다. 이 때 **작업 메시지가 적재되는 공간이 Message Queue(대기열)**이며 메시지의 그룹을 Topic이라고 하고 Topic을 이용해 데이터구분을 하게 된다. 즉 Broker가 쉬고있는 Worker에게 작업을 할당하고 Celery는 작업메시지를 Message Queue에 보관, 메시지를 가져가 작업을 수행하는 역할을 한다. 

### Broker의 종류
#### RabbitMQ
- AMQP를 구현한 Message broker, 메일발송 등 즉각적인 결과(응답)를 제공하기 어려운 작업 수행시 활용
- AMQP : Client어플리케이션과 middleware broker와의 메시지를 주고받기 위한 프로토콜
#### Redis	
- 디스크에 상주하는 인메모리 데이터베이스로 메모리를 이용한(in-memory) Cache서버
- key-value를 이용해 celery가 처리할  작업을 redis로 보낸 후 cache에서 해당 key를 제거하는 방식으로 작동

그 외에도 `Kafka`, `ActiveMQ`, `ZeroMQ`, `AmazonSNS`, `Gearman` 등이 있다. 

<br>

## Django와 함께 Celery 설정하기
### [python, django, celery, redis, mysql, docker-compose 기반]


- 장고 서버에서 Message Queue로 Task를 전달하면 이를 Message Broker인 Redis에 Queue에 적재하고 이를 Worker인 Celery가 받아 Task를 비동기로 처리하고 그 결과를 Redis에 저장하도록 할 것이다.

<br>
 
기본적인 장고 세팅과 db연결이 되어있다는 가정하에 celery를 사용시 추가할 부분을 작성하도록 하겠다.

> _그 전에는 장고에서 celery시 장고와 맞는 라이브러리를 설치해줘야 했지만 장고 3.1버전부터는 별도의 라이브러리 설치 없이 Celery사용이 가능하다._

### 파일구조
```
- proj
  - api
     - settings.py
  - app
  - dockercompose.yml
  - Dockerfile
  - manage.py
```
### 1. celery 설치
장고에 맞는 라이브러리를 설치안하는 것 뿐. python celery 패키지는 설치해줘야한다.
```
pip install Celery
pip install django_celery_results
```

### 2. docker-compose.yml 추가
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
worker의 docker image는 기존 api에 사용했던 dockerfile을 기반으로 container로 실행할 것이다. command로 `celery -A api worker --loglevel=info`를 넣어 celery worker 서버를 실행하도록 한다. 여기서 api는 프로젝트 파일의 이름이다.


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
        'LOCATION': 'redis://redis_server:6379/1',  # redis_server: docker container이름
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

`CELERY_RESULT_BACKEND`
- **Task호출 결과로 Task 완료여부를 알 수 있는 AsyncResult인스턴스가 반환되는데 기본적으로 Task실행결과는 저장되지 않으니 result backend 설정을 통해 결과를 저장할 수 있다.**


### 4. celeryconf.py
celery를 사용하기위해서는 celery 라이브러리의 인스턴스를 정의해야한다. 
celeryconf.py는 setting.py가 있는 api파일 아래 만들도록 한다.
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
- 이 설정을 통해 celery가 장고 프로젝트의 위치를 알수 있게 된다. 비슷한 의미로 장고 manage.py에도 동일한 내용이 있는걸 확인할 수 있다.

`app = Celery('api')`
- celery라이브러리의 인스턴스를 정의한다. 여기서 api는 celery 앱의 이름이다.
`app.config_from_object('django.conf:settings', namespace='CELERY')`
- settings에 정의한 namespace가 CELERY인 항목은 celery환경설정 내용을 불러온다.(설정을 settings.py로 분리했을 경우 입력)

`app.autodiscover_tasks()`
- autodiscover를 하게되면 만든 앱들을 `CELERY_IMPORTS`에 추가할 필요 없이 celery를 사용할 수 있다.


### 5. `__init__.py`
```
from __future__ import absolute_import
from .celeryconf import app as celery_app

__all__ = ["celery_app"]
```
celery를 넣은 api폴더의 `__init__.py`를 설정하지않으면 모듈인식을 못하게되므로 설정해주도록 한다. 

<br>

## Celery 사용하기
api container에 들어가서 `celery -A api status` 입력을 통해 연결을 확인한다.
![](https://images.velog.io/images/anjaekk/post/83065c6c-c13e-43bf-be73-a01a29e4ecab/image.png)

아래와 같이 간단한 Task함수를 작성하고 Task를 호출해보도록 하겠다.
```
# app.task.py

import time, random
from celery import shared_task


@shared_task
def print_hello(user):
    time.sleep( random.randint(1,5) )
    return print('hello {}'.format(user))
```

celery task호출은 delay()메서드를 사용한다. 
```
<시행하고자하는 함수>.delay(인자1, 인자2)
```
python shell에서 task를 실행시켜본다. 
```
>>> from app.tasks import *
>>> print_hello.delay('banana')
```
![](https://images.velog.io/images/anjaekk/post/58ec5d79-6ab1-42cb-93c7-34485a605659/image.png)

### worker log 확인
worker container에 들어가 `celery -A api worker -l info`를 입력해준다.

![](https://images.velog.io/images/anjaekk/post/76b0a045-1b46-4ad5-98c7-73404ba3f97b/image.png)


모니터링에 관련된 사항은 [celery문서](https://docs.celeryproject.org/en/latest/userguide/monitoring.html#guide-monitoring)에 잘 나와있다. 


<br>


> 참조   
> 🔗 [Celery 문서 | First Steps with Celery](https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps-with-celery)   
> 🔗 [분산 비동기 작업 처리를 위한 Celery 첫걸음 | 조은우 개발 블로그](https://jonnung.dev/python/2018/12/22/celery-distributed-task-queue/)  
> 🔗 [RabbitMQ 와 Redis 의 차이 | 방랑자 블로그](https://m.blog.naver.com/aim4u/221766568746)  
> 🔗 [Docker로 Django, Celery, MairaDB, Redis 개발환경 설정하기 | khtinsoft 블로그](https://blog.khtinsoft.xyz/posts/django-celery-mariadb-redis-docker/)  
> 🔗 [[Celery] 무작정 시작하기 (2) - Task | 개발하는 도치 블로그](https://heodolf.tistory.com/63) 
