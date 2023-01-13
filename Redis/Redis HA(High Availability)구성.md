# Redis HA(High Availability)구성
redis에서 sentinel이나 cluster없이 master와 replica(slave)만 구축하게 되면 단순히 replica는 master의 단순한 복제본이 되므로 장애발생시 수동으로 replica 노드로 재구동 해줘야 한다. 이러한 번거로움을 없애기 위해 redis는 sentinel이나 cluster를 이용하여 고가용성을 높힐 수 있다. 아래는 redis에서 제공하는 HA방법과 이를 docker, python, django, celery, redis-py를 이용해 redis sentinel을 연결하는 예를 포함하고 있다.

# Replica

replica 노드 생성은 `replicaof` 명령어로 간단하게 구성이 가능하다.

### redis replication 주요 매커니즘

1. 레디스에서 복제본을 생성할 경우 master와 replica를 연결해두면 마스터의 데이터 write, 데이터 expire등 변경사항을 replica에 스트림으로 전달하여 복제본을 유지한다.
2. 이 상황에서 master와 replica의 네트워크가 끊긴 뒤 재연결하게되면 데이터의 일관성을 위해 master데이터를 replica로 부분 재 동기화를 시도하게 된다. 
3. 부분 재 동기화가 불가능한경우에는 replica를 모두 재 동기화 한다.

# Sentinel

 sentinel은 장애감지시 sentinel 끼리 과반수(quorum)로 장애 여부를 판단하고 장애 판단시 fail over를 진행하게 된다. fail over는 죽은 master 서버를 대신해 replica로 선언한 서버가 master가 되는데 이후 죽었던 서버가 복구되게되면 해당 서버가 replica가 된다. 여기서 어플리케이션은 master나 replica에 직접 연결되어있지 않고 sentinel 노드와 연결을 시킨다. 그래서 fail over를 하더라도 sentinel에서 죽은 전 master가 아닌 새로운 master의 ip와 port정보를 줄 수 있게 된다.

### Sentinel 기본 사항

아래는 redis sentinel 배포전 알아야할 기본 사항들이다. 

1. 과반수(quorum)방식을 이용하기 때문에 sentinel은 기본적으로 3대 이상의 홀수 인스턴스가 필요하다.
2. sentinel 인스턴스는 기존 redis서버와 별개의 서버에 구축되어야 한다. 여기서 별개의 서버는 서로 다른 가용 영역(availability zone)을 말한다.
3. master는 replica에 비동기식 복제를 하기 때문에 write에 대한 데이터 손실 가능성이 있다. 이를 보안하기 위해 보안 수준은 낮지만 특정 write 순간으로 손실을 제한하는 방법은 있다. 
4. 사용하는 redis 클라이언트에서 sentinel을 지원해줘야한다.(유명한 클라이언트들은 대부분 지원)
    - python의 redis-py는 sentinel을 지원한다.(https://github.com/redis/redis-py)
5. 개발환경에서 테스트를 거쳐야 안전한 고가용성 설정이다.
6. Docker를 사용하거나 다른 형태의 NAT(Network Address Translation) 혹은 포트 매핑은 주의해서 사용해야한다. 특히나 도커는 포트를 재매핑 하면서 sentinel 프로세스 자동 discovery와 replica의 목록을 마스터에게 가져오는 작업에 문제가 생길 수 있다.(뒤에서 자세히…)

*이 외에도 담당자에게 메일을 보내는 notification 기능도 있다고 한다.

### Sentinel 상태

1. SDOWN
    - 주관적 다운(Subjectively Down)
    - 하나의 sentinel인스턴스가 가지고 있는 상태
2. ODOWN 
    - 객관적 다운(Objectively Down)
    - 쿼럼 파라미터 이상의 sentinel이 SDOWN조건을 가지고 있고 다른 sentinel에게 `SENTINEL is-master-down-by-addr` 커맨드를 받았을 때 발생한다.    
     ![image](https://user-images.githubusercontent.com/74139727/212246027-bd0fa7c7-8625-4847-9a57-376c799dbab9.png)

    

# Cluster

레디스 cluster는 확장이 가능하다는 점에서 sentinel에 다르게 장점을 가진다. 데이터셋을 여러 노드에 자동으로 분산하므로써 확장성과 고성능을 가지게 되고 여기서 일부 노드가 다운되더라도 사용가능하기 때문에 고가용성까지 보장가능하다.

redis cluster는 내부 master와 replica가 full mesh구조로 되어있으며 gossip(가십)프로토콜을 이용하여 서로 통신하게 된다. 이 외에도 cluster사용을 위해서는 최소 3개의 master 노드가 필요하다.

### Cluster 특징

1. TCP 포트
    - cluster 노드에는 두 개의 개방형 TCP연결이 필요하다.
        - 클라이언트에 서비스를 제공하는 redis tcp포트(보통 6379)
        - 노드간 통신 채널인 cluster bus port(보통 16379, cluster-port로 변경 가능)
2. Data Sharding
    - cluster에서는 어플리케이션으로부터 들어오는 모든 데이터는 해시슬롯에 저장된다.
    - cluster는 총 16384개의 슬롯을 가지며 master노드는 슬롯을 나누어 저장하게 된다.
    - 입력되는 모든 키는 슬롯에 매핑된다.
    - 해시슬롯은 마스터 노드 내에서 자유롭게 옮길 수 있기 때문에 새로운 노드를 추가하거나 삭제할 때 작업 중지 없이 해시슬롯을 이동시키기만 하면 되서 쉬운 확장이 가능하다.
3. Failover
    - 모든 노드가 서로를 감시하며 failover여부를 정한다.
4. database 0
    - cluster는 database 0 밖에 지원되지 않기 때문에 기존에 redis 설정에서 각기 다른 db를 사용하고 있었다면 적절한 Prefix를 이용해 분리했던 database를 db 0, 한곳에 넣을 수 있도록 해야한다.

# redis HA와 Docker

애플리케이션과 redisrk docker를 이용할 경우 redis HA 구성이 까다로워 진다. redis sentinel과 cluster모두 NAT 혹은 IP/Port 재 맵핑을 지원하지 않기 떄문에 포트매핑을 하는 docker와는 맞지 않다. 이를 위해서 docker에 network_mode를 host로 넣어서 사용할 수 있으나 이마저도 리눅스 호스트 환경이 아니라면 host 네트워크 모드는 지원되지 않는다.(mac, windows 환경에서 불가) 

# Django, celery, redis sentinel 설정

python의 대표적인 비동기 queue 관리자인 celery는 redis cluster를 아직 지원히지 않는다.(2023년 1월 기준) 그러므로 sentinel로 redis HA를 구성하도록 하겠다. **테스팅을 위해 한 서버에 구성하지만 실제 배포 환경에서는 각기 다른 서버에 구성해서 안정성을 보장해야한다.** 

나는 celery와 redis-py 두 라이브러리에 모두 설정을 해야하는 상황이라 함께 진행했지만 해당되는 내용만 진행해도 된다.

### 환경변수 설정

```xml
CELERY_BROKER_URL=sentinel://redis-sentinel-1:26379/1;sentinel://redis-sentinel-2:26380/1;sentinel://redis-sentinel-3:26381/1
CELERY_VISIBILITY_TIMEOUT=3600
CELERY_RESULT_BACKEND=sentinel://redis-sentinel-1:26379/1;sentinel://redis-sentinel-2:26380/1;sentinel://redis-sentinel-3:26381/1
SENTINEL_URL="redis-sentinel-1", 26379),("redis-sentinel-2", 26380),("redis-sentinel-3", 26381)
MASTER_NAME=redis
```

- celery의 환경변수를 `app.config_from_object`를 통해 진행하는 경우 위와 같이 `,`이 아닌 `;`로 sentinel을 구분해줘야 한다.
- VISIBILITY_TIMEOUT: 작업이 ack 되지 않았을 때 재 실행을 요청하는 시간으로 작업 수행시간보다 길게 설정한다.
- REDIS_URL: redis 클라이언트로 redis-py를 이용할 경우에는 `,`로 구분한다.
- MASTER_NAME: master의 alias(master_host와는 별개 개념, 나 같은 경우 동일한 이름으로 지정했다.)

### docker-compose

```xml
redis:
    container_name: redis
    image: library/redis:6.2.8-alpine
    ports:
      - 6379:6379
    restart: unless-stopped
    environment:
      - REDIS_REPLICATION_MODE=master
      - ALLOW_EMPTY_PASSWORD=yes
    networks:
      - redis-networks
    volumes:
      - redis-data:/data

  redis-replica:
    container_name: redis-replica
    image: library/redis:6.2.8-alpine
    ports:
      - 6479:6379
    restart: unless-stopped
    environment:
      - REDIS_REPLICATION_MODE=slave
      - REDIS_MASTER_HOST=redis
      - ALLOW_EMPTY_PASSWORD=yes
    command: redis-server --slaveof redis 6379  #replica 선언
    networks:
      - redis-networks
    volumes:
      - redis-data:/data
    depends_on:
      - redis

  redis-sentinel-1:
    &redis-sentinel
    container_name: redis-sentinel-1
    image: 'bitnami/redis-sentinel:latest'
    ports:
      - 26379:26379
    restart: unless-stopped
    environment:
      - REDIS_SENTINEL_DOWN_AFTER_MILLISECONDS=3000  # 3초간 마스터로부터 응답 받지 못하면 failover진행
      - REDIS_MASTER_PORT_NUMBER=6379
      - REDIS_MASTER_SET=redis
      - REDIS_SENTINEL_QUORUM=2
      - RESOLVE_HOSTNAMES=yes
    networks:
      - redis-networks
    volumes:
      - redis-data:/data
    depends_on:
      - redis
      - redis-replica

  redis-sentinel-2:
    <<: *redis-sentinel
    container_name: redis-sentinel-2
    ports:
      - 26380:26379

  redis-sentinel-3:
    <<: *redis-sentinel
    container_name: redis-sentinel-3
    ports:
      - 26381:26379

volumes:
  redis-data:
    driver: local

networks:
  redis-networks:
    driver: bridge
```

- redis-sentinel 내용은 container와 port를 제외하고 모두 동일하기 때문에 docker 확장필드(extension fields)를 이용해 중복이 없도록 작성해줬다.
- sentinel 포트 설정시 16379처럼 redis 기본포트 앞에 1을 붙여 하면 sentinel이 연결되지 않는다. (16379는 cluster에서 cluster bus의 기본 포트 이기 때문에)
- docker redis 이미지를 사용하여 sentinel을 위해 사용하는 host_name으로 연결은 6.2 이상 버전부터 지원되니 그 이하 버전이면 업그레이드를 권장한다.(업그레이드 하지 않는다면 따로 script를 이용해서 처리)

### Django settings

기존 샐러리 설정에서 아래 내용을 추가한다. 

```xml
CELERY_BROKER_TRANSPORT_OPTIONS = {
        "visibility_timeout":int(os.environ.get("CELERY_VISIBILITY_TIMEOUT", 3600)), 
        "master_name":os.environ.get("MASTER_NAME", "redis")
    }
CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
        "visibility_timeout":int(os.environ.get("CELERY_VISIBILITY_TIMEOUT", 3600)), 
        "master_name":os.environ.get("MASTER_NAME", "redis")
    }
```

기존 Redis 설정 변경

```xml
from redis import sentinel

def get_list(text):
    return [item.strip() for item in text.split(",")]

if SENTINEL_URL := os.environ.get("SENTINEL_URL"):
        REDIS = sentinel.Sentinel(SENTINEL_URL).master_for(
            os.environ.get("MASTER_NAME", "redis")
        )
    
    DJANGO_REDIS_CONNECTION_FACTORY = "django_redis.pool.SentinelConnectionFactory"
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.SentinelClient",
                "SENTINELS": SENTINEL
            },
        }
    }
```

- SENTINEL_URL: redis-py에서 sentinel url은 리스트 안 튜플 형태로 `[(host_name, port), (host_name, port)]` 와 같이 구성되어야 한다.
- REDIS: sentinel에 기존 docker-compose에서 지정한 master_name을 설정한다.
- DJANGO_REDIS_CONNECTION_FACTORY: global django setting에 sentinel connection factory 연결을 생성한다.
- 혹시나 `django_redis.client.SentinelClient` 에서 `SentinelClient`를 찾을 수 없다는 오류가 생성되면 redis-py의 버전을 확인해보길 바란다. django-redis 패키지에서 sentinel은 5.0.0 이상 부터 지원되니 혹시나 버전이 낮다면 업그레이드를 해야한다.
- 옵션으로 C언어로 작성된 Redis client를 함께 사용하면 성능을 더 높힐 수 있다.
    
    ```xml
    "OPTIONS": {
        "PARSER_CLASS": "redis.connection.HiredisParser",
    }
    ```
    

# 확인

1. docker에서 컨테이너가 모두 정상으로 띄어졌는지 확인한다.
    
    ![image](https://user-images.githubusercontent.com/74139727/212245855-0cf88096-2b73-4161-a8cb-fa3ad237e723.png)

    

1. sentinel로 접근하여 센티널의 상태와 모니터링하는 master정보를 확인한다.(포트정보를 꼭 넣어준다.)
    
    ![image](https://user-images.githubusercontent.com/74139727/212245829-84588b70-55c6-4aed-bec0-bb04c6069cc8.png)

    

1. replica 승격 확인
    - master lost: master redis 컨테이너를 다운시키면 아래와 같은 메세지가 replica log에 바로 뜬다.
    
    ```xml
    Connection with replica 172.26.0.8:6379 lost.
    ```
    
    - SDOWN: sentinel-1에서 sdown(주관적 다운) 확인
    
    ```xml
    +sdown master redis 172.26.0.8 6379
    ```
    
    - ODOWN: 설정한 quorum(2) 이상의 센티널에서 해당 마스터가 다운되었다고 인정하고 failover 진행
    
    ```xml
    +odown master redis 172.26.0.8 6379 #quorum 3/2
    ```
    
    - master 서버가 승격처리 완료 되었음을 알려준다.
    
    ```xml
    +switch-master redis 172.26.0.8 6379 172.26.0.9 6379
    ```
    

참고

sentinel

[https://redis.io/docs/management/sentinel/](https://redis.io/docs/management/sentinel/)

[http://redisgate.jp/redis/sentinel/sentinel.php](http://redisgate.jp/redis/sentinel/sentinel.php)

celery

[https://docs.celeryq.dev/en/stable/history/whatsnew-4.2.html?highlight=redis sentinel#new-redis-sentinel-results-backend](https://docs.celeryq.dev/en/stable/history/whatsnew-4.2.html?highlight=redis%20sentinel#new-redis-sentinel-results-backend)

[https://github.com/jazzband/django-redis](https://github.com/jazzband/django-redis)

블로그

[https://garimoo.github.io/database/2019/09/06/redis_ha.html](https://garimoo.github.io/database/2019/09/06/redis_ha.html)
