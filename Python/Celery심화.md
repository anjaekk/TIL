# Celery
메세지 전달을 기반으로 한 비동기 task 큐(Distributed task queue, 종합적인 비동기 처리기)

Client = 백엔드 테스크를 실행하는 클라이언트

Worker = task 수행

Broker = 메세지 전달

+) kombu: celery가 이용하는 message 라이브러리

Celery를 사용하는 이유

1. 다양한 기능 제공
2. 좋은 인터페이스 제공
3. 장고와 integration이 쉬움

### 특징

1. 비대칭적 구조
- Client와 worker 각각 scale 관리 가능
- Client 불필요하고 무거운 작업으로부터 자유로움

1. AMQP(Advanced Message Queueing Protocol)
    - 최소한 한번은 전달되도록 하는 컨셉
    - Producer: 작업(Message) 생성하여 브로커에 전달
    - Consumer: 메세지를 받으면 Acknowledge(인정)한다고 브로커에 전달한다.
    - 브로커는 해당 내용은 Confirm하여 Producer에게 전달한다.
    - 만약 Acknowledge를 완료하지 못하면 브로커는 해당 메세지가 제대로 처리했는지 알 수 없어서 브로커는 메세지를 다시 컨슈머에게 보내게 된다.
    - ⇒ 작업은 Idempotent하게 작성이 되야한다.(한번 적용하던 여러번 적용하던 횟수에 상관없이 같은 결과가 되어야한다.)

사용법

Delay() : 비동기적 수행

Apply_async 사용하면 언제 실행할지도 지정할 수 있음, call_back처럼 다른 Task를 실행할 수도 있음

### 사용시 주의사항

1. Late Ack’ 사용하기
    - 보통 Celery worker는 Ack’를 task실행 직전에 하지만 Late Ack’는 실행이 완료된 후에 Ack’를 하게된다. Worker는 Ack’를 하게되면 task Queue에서 해당 작업을 삭제하는데 Late Ack’ 미사용시 완료전에 제거 될 수 있어서 해당 작업이 실행되지 않을 가능성이 생긴다. 하지만 Late Ack’시 실행이 되지 않으면 큐에 남아 있어서 다시 재실행을 할 수 있게 된다.
    - 중복으로 실행될 수 있기 때문에 주의해야한다. ⇒ Idempotent 적으로 task작성

1. Retry 사용하기
- `@app.task(bind=True)` 데코레이터 하위 함수에서 예외처리를 통해 안정적으로 사용할 수 있다.
- ConnectionError등이 발생할 때 try, except안에서 self.retry를 통해 재시도를 할수 있다.
- 최근버전에는 task정의시 arg로 넘겨서 깔끔하게 사용가능한다.
- Atomicity하게 적용이 되어야하고 명확한 오류의 원인이 있을 때 사용하도록 주의해야 한다.

1. Visibility timeout적용하기
    - 전달 후 일정시간 내료 Ack’되지 않으면 다른 worker에 task를 전달
    - rabbimq를 사용한다면 confirm_publish=True조건을 주면 됨
    - AMQP 프로토콜을 사용하는 Broker는 Ack가 오지 않으면 다시 메세지를 보내지만 AMQP 프로토콜을 사용하지 않는 Broker를 사용하게 되면 Visibility timeout으로 구현하게 된다. 일정시간동안 timeout이 안되면 처리되지 않은 것으로 보고 다시 보내게 되는거다.
    - Redis는 모사 AMQP여서 Visibility timeout내에 ack가 전달되지 않으면 task가 중복실행 되게 되는데 eta, countdown(지연실행 방법들) 시간보다 visibility timeout이 커야 문제가 되지 않는다.
    - AWS SQS의 최대 제한시간은 12시간

### 효율적인 처리

일시적으로 처리 속도 < 쌓이는 속도여도 큰 문제가 되진 않지만 지속되면 브로커에 불필요한 로드가 발생하고 작업이 진행되지 않는다. 

[ Ignore_result ]

Celery는 기본적으로 수행결과(return 값)을 저장해야 작업이 끝나게 되어있다. 

Task후 연계하여 작업이 또 있는 경우에만 result를 저장하여 결과저장이 불필요한 경우에는 Ignore_result=True를 통해 결과 저장 비용을 줄이고 성능을 높일 수 있다. 

[ 평균 수행시간이 비슷한 작업끼리 같은 Queue에 있도록 하기 ]

Task 혹은 모듈 단위로 task queue를 지정할 수 있음

```jsx
CELERY_ROUTES = {
	'feed.tasks.import_feed': {
		'queue': 'feeds'
		}
} 
```

워커에서 특정한 queue로 가도록 처리하기

```jsx
celery -A pykr worker -Q feeds
```

[ Limit ]

1. Time Limit
    - Task가 일정시간 이상 실행되면 종료시키기
    - soft_time_limit = 60
    - hard_time_limit = 60

1. Rate limit
    - Task가 일정 빈도이상 실행되지 못하도록
    - rate_limit = “60/m”
    - Rate limit은 worker 별로 관리됨

[ Concurrency, Worker Pool ]

Celery 실행시 아래의 명령어로 실행

```python
celery -A <Project> worker -P <Worker name> -c <Concurrency>
```

-c: concurrency 옵션

-P: 어떤 워커 풀에서 실행할지(Concurency어떻게 구현하느냐에 대한 옵션)

- prefork
- gevent / eventlet
- solo
1. prefort
    
    Multi processing으로 구현되어있다. -c 값을 N으로 실행하면 1개의 master process에 N개의 child process로 실행되게 된다. master에서 task 분배하고 실제 task는 child에서 처리하게 된다. 
    
    - O fair 옵션
        
        Master 에서 Child로 Task를 전달할 때 기본적으로는 pipe buffer가 허용하는 만큼의 메세지를 전달하게 되는데 O fair 옵션을 주게되면 실행이 가능할 경우에만 message를 전달하게 된다. (Prefetch Limit과 비슷하지만 Prefetch Limit은 broker와 worker 사이에서 로직을 통제하는 거라면 O fair옵션은 master와 Child 사이에서 프로세스를 통제한다. Long task와 short task가 섞여 있을 때 Prefetched task가 실행되지 못하고 있으면 O fair옵션을 주게되면 성능향상을 기대할 수 있다. 
        
2. gevent / eventlet
    
     I/O bound 작업에서 사용하며 green thread기반으로 되어있다. concurreny를 몇백개 혹은 몇 천개로 설정도 가능하다.(Prefetch 는 CPU때문에 그정도로는 설정할 수 없음)
    

[ Prefetch ] 

Prefetch Limit: Ack’ 되지 않은 message의 갯수를 워커가 얼마나 가질 수 있냐

- prefetch는 전체 단위의 작업이 소비되면 다시 해당하는 prefetch limit만큼 가져와서 작업을 수행한다.(task payload 크기가 적고 latency가 중요하다면 합리적인 결정이 된다)
- worker_prefetch_multiplier 설정시 worker_prefetch_multiplier * concurrency가 prefetch limit으로 설정된다. (기본 값 4)
- worker_prefetch_multiplier = 0 으로 설정하게 되면 worker_prefetch_multiplier를 설정하지 않겠다는 뜻이여서 limit을 걸지 않고 메모리와 효율성을 고려하지 않고 작업을 실행하게 된다.
- 만약 concurency = 2인 worker와 concurency = 1인 워커가 있고 message가 queue에 쌓여 있을 때 아래와 같이 설정하게 되면
    - worker_prefetch_multiplier = 1
    - acks_late = False
        
        워커에서 테스크를 받으면 이 테스크를 실행하기 직전에 처음 테스크들은 Ack’를 하게 된다. 그리고 그 뒤에 쌓인 message들은(Ack’된 메세지들 제외) prefetch limit이 적용되게 된다. 그러면 concurency = 2인 워커는 multiplier = 1을 곱해 2만큼 message가 prefetch되고 concurency = 1인 워커는 multiplier = 1을 곱해 1개의 message를 prefetch한다. 이렇게 하게되면 긴 task위에 짧은 task들을 쌓아서 짧은 task들이 실행되지 않는 일을 막을 수 있다. 
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/779c6d93-769c-46b1-8a9e-60cad213217d/Untitled.png)
        
        여기서 만약 acks_late = True 로 하게되면 실행중인 task만 prefetch하게 된다.  prefetch를 하는데도 결국 네트워크를 타게 되기 때문에 prefetch_multiplier를 높여주면 짧은 task를 더 빠르게 실행할 수 있게 된다. 
        
        ⇒ 이 옵션을 제대로 활용하기 위해서는 Long task와 short task를 구분해서 worker를 지정해줘야 한다. 
        
    
    [ 결론 ] 
    
    다양한 worker 옵션들 중 자신의 프로젝트와 맞는 옵션을 사용하려면 아래의 조건에 따라 결정하도록 한다.
    
    - IO / CPU
    - 중요도
    - 수행 시간
    - 실행의 빈도
