# Redis cache

레디스는 전세계에서 가장 유명한 캐싱 솔루션임

레디스에서 데이터 하나를 가져오는데 평군 작업속도가 1ms으로 굉장히 빠르게 처리함

### 캐시를 사용하는 이유

어플리케이션은 데이터를 가져올 때 캐시를 먼저 확인하게 된다.(Memory에 접근하는 속도가 Disk에 접근하는 속도보다 빠르기 때문에) 캐시에 해당하는 값이 있으면 캐시에서 데이터를 가져오는 작업을 반복한다. 캐시에 해당하는 값이 없으면 원 데이터베이스에서 데이터를 직접가져오고 그 후 캐시에 이를 저장하게된다. 

- 원본 데이터베이스에 접근하는 속도보다 더 빠름
- 같은 데이터를 재사용할 때 효율적
- 값이 자주 변하지 않는 데이터에 접근할 때 효율적임

### 레디스를 캐시로 사용하는 장점

- key-value 형태로 저장하기 때문에 데이터 종류에 구애받지 않고 저장할 수 있음
- In-memory(RAM)에 데이터를 저장하기 때문에 빠르게 사용 가능

### 레디스 캐싱 특징

레디스를 캐시로 사용할 때 어떻게 전략을 짜느냐에 따라 성능에 큰 영향을 끼치게 된다. 해당 데이터 유형과 액세스 패턴을 잘 고려하여 짜야한다. 

[ 읽기 ]

1. Look-Aside(Lazy loading) 패턴
    
    캐시에 데이터가 없을 때에만 입력(Lazy loading)되고 따라서 레디스에 장애가 생기더라도 원 데이터베이스에서 찾는 값을 가져오면 되기 때문에 바로 서비스의 장애로 이어지지 않는다. 
    
    - 캐시에서 값을 확인하고 없으면 DB에서 가져오는 방법
    - 데이터를 읽는 작업이 많을 때 사용
    - 레디스를 캐시로 사용할 때 가장 일반적으로 많이 사용하는 전략이다.
2. cache warming
    
    캐시와 이어진 connection이 많다면 레디스에 장애가 생겼을 때 해당 connection들이 원 데이터베이스로 connectiong되면서 DB 과부화가 생길 수 있다. 즉, 새로 레디스 캐시를 도입하게 되면 많은 cache miss가 발생해 성능의 저하가 올 수 있는데 이럴 때는 cache warming을 통해 미리 캐시에 데이터를 밀어 넣어주는 작업을 해주면 된다.
    

[ 쓰기 ]

1. Write-Around
    - 일단 모든 데이터를 DB에 저장하고 cache miss가 발생한 경우에만 캐시에 데이터를 가져오는 방법
    - 캐시 내의 데이터와 DB의 데이터가 다를 수 있기 때문에 주의해야 함
2. Write-Through
    - DB에 데이터를 저장할 때 cache에도 함께 저장하는 방법
    - 캐시에 항상 최신 정보를 가지고 있게됨
    - 저장할 때 캐시와 DB 모두 저장을 해야하기 때문에 그만큼 저장 프로세스의 시간이 걸리게 됨
    - 캐시에 저장하는 데이터가 재사용 되지 않으면 그 만큼의 리소스 낭비로 이어질 수 있기 때문에 주의해야 함 ⇒ 캐시 Expire time을 설정해 줘야함
3. Write-Back
    - 다량의 데이터를 저장해야 할 때 memory에 모아두었다가 한번에 DB에 저장하는 방법
    - 중간에 장애가 생길시 memory에 저장한 데이터가 지워질 수 있기 때문에 주의해야 함

### Redis Collection

1. String
    - set 커맨드로 저장되는 데이터는 모두 String으로 들어감
2. Bitmaps
    - string의 변형으로 bit단위의 연산이 가능
3. Lists
    - queue로 사용하기 적합
4. Hashes
    - redis value값에 key-value저장
5. Sets
    - 중복되지 않은 문자열의 집합
6. Sorted Sets
    - score로 정렬된 sets
7. HyperLogLogs
    - 다량의 데이터를 다룰 때, 중복되지 않은 값의 개수를 카운트할 때 사용
8. Streams
    - Log 저장용

### 레디스 사용 예

1. Counting(단순 증감 연산)
    - String
    
    INCR / INCRBY / INCRBYFLOAT / HINCRBY / HINCRBYFLOAT / ZINCRBY
    
    ```tsx
    > SET score:a 10
    "OK"
    > INCR score:a    -> INCR 1 증가
    (integer) 11
    > INCRBY score:a 4    -> INCRBY 4 증가
    (integer) 15
    ```
    
    - Bits
    
    데이터 저장공간 절약, 정수로 된 데이터만 카운팅 가능
    
    ```tsx
    > SETBIT visitors:20220817 3 1    -> user ID에 해당하는 bit 1로 올려주기
    (integer) 0
    > SETBIT visitors:20220817 6 1
    (integer) 0
    > BITCOUNT visitors:20220817       -> 1로 설정된 값 counting
    (integer) 2
    ```
    

- HyperLogLogs
    
    모든 string 데이터 값을 유니크하게 구분할 수 있음. Set과 비슷하지만 HyperLogLogs는 저장되는 데이터 개수에 상관없이 모든 값이 12KB로 고정되기 때문에 대량의 데이터를 카운팅할 때 사용하면 좋음.
    
    한번 저장된 값은 다시 불러올 수 없기 때문에 데이터 보호 목적으로 사용할 수도 있음
    
    사용 예) 웹사이트 방문 IP가 몇개인지, 크롤링한 url 개수 등..
    
    ```tsx
    > PFADD ip:20220817 123.123.123.123
    (integer) 1
    > PFADD ip:20220817 123.123.123.124
    (integer) 1
    > PFCOUNT ip:20220817
    (integer) 2
    > PFMERGE ip:all ip:20220817 ip:20220818..    -> 취합해서 조회
    (integer) 2390515
    ```
    

1. Messaging
- Lists
    
    Event Queue로 사용하기 좋음
    
    Blocking 기능을 이용해 불필요한 polling 프로세스를 막을 수 있음
    
    LPUSHX / RPUSHX 는 키가 있을 때에만 그 리스트에 데이터를 추가하게 되는데 이는 key가 존재한다는건 이전에 사용했던 queue라는 거고 사용했던 queue에만 데이터를 넣을 수 있어서 비효율적인 데이터 이동을 막을 수 있다. 
    
    사용 예) 트위터에서 팔로우한 사람들 피드 보여줄 때 레디스의 List, RPUSHX 커맨드를 이용한다. 이렇게 되면 자주 트위터를 이용하던 사용자에게는 새로운 데이터를 캐시해놓을 수 있고 자주 사용안하는 사용자는 캐싱 key가 없어서 자주 사용안하는 사용자를 위해 데이터를 미리 쌓아놓는 비효율을 막을 수 있다. 
    
    ```tsx
    # client A가 myqueue에서 데이터를 가져오려고 하나 현재 리스트 안에 데이터가 없어서 대기하는중
    > BRPOP myqueue 0
    ```
    
    ```tsx
    # client B가 "hey"값을 넣으면
    > LPUSH myqueue "hey"
    (integer) 1
    ```
    
    ```tsx
    # client A에서 바로 이값 확인 가능
    > BRPOP myqueue 0
    
    "myqueue"
    "hey"
    (26.65s)
    ```
    

- Streams
    
    로그를 저장하기 가장 적절한 자료구조로 실제 log가 저장되는 것처럼 append-only방식으로 저장되어 중간에 데이터가 변경될 수 없다. 
    
    id값을 직접 저장할 수도 있지만 “*”로 이용하면 redis가 알아서 id를 저장하고 반환한다. id값은 저장된 시간으로 저장되며 값은 key-value쌍으로 저장되게 된다. 
    { ”163482324147-0”: { ”user-id”: 1234, “click”:2 } }
    
    ID값을 이용해 시간 대역대로 저장된 값을 검색할 수도 있고 실제 서버에서 로그를 읽을 때 tail -f 를 쓰는 것처럼 새로 들어오는 값만 리스닝할 수도 있다. 
    
    또한 kafka처럼 소비자 그룹이라는 개념이 존재해서 원하는 소비자만 특정 데이터가 보이도록 할 수 있다. 레디스 공식문서에서 Stream을 메세징 브로커가 필요할 때 kafka를 대체해서 간단하게 사용할 수 있다고 설명한다.
    
    ```tsx
    > XADD mystream * user-id 1234 click 2     -> *: id값
    "163482324147-0"
    > XADD 
    > XADD mystream * user-id 1234 click 2
    "163482321549-0"
    ```
    

### Redis Persistence(영구 저장)

AOF, RDB둘다 사람이 읽을 순 없으며 직접 생성할 수도 있고 백업 시간을 지정할 수도 있음

AOF(Append-Only-File) 

- 데이터를 변경하는 커맨드가 들어오면 해당 커맨드를 모두 저장한다.
- 레디스 프로토콜 형태로 저장

RDB(snapshot)

- 스냅샷 방식으로 저장 당시의 메모리 그대로를 저장한다.
- 바이너리 파일 형태로 저장

### 레디스 아키텍처 및 HA(High Availabilty)기능

레디스의 아키텍쳐는 Replication, Sentinel, Cluster 세가지로 나뉜다. 

1. Replication(복제 연결)
    - master 노드와 replica노드 이렇게 두 가지만 존재하는 가장 간단한 구성
    - replicaof 커맨드를 이용해 간단한 복제 연결
    - 모든 복제는 비동기식으로 동작
    - HA기능이 없으므로 master 노드에 장애 발생시 수동 복구 해야함(replica 노드에 직접 접속해서 복제를 끊기, 어플리케이션에서 연결설정 변경)
2. Sentinel
    - master 노드와 replica 노드 외에 sentinel노드가 추가적으로 필요(sentinel 프로세스를 추가로 띄어줘야 함)
    - sentinel은 노드의 갯수가 3대 이상의 홀수로 존재해야 함(최소 master 1대, replica 1대, sentinel 1대)
    - sentinel은 일반 노드들(master와 replica)을 모니터링 하는 역할을 함
    - master 노드 장애 발생시 자동으로 페일오버를 발생시켜 기존 replica 노드가 master가 됨
    - 어플리케이션에서 sentinel의 연결정보만 가지고 있기 때문에 페일오버가 발생하더라도 sentinel에서 master 노드정보로 바로 연결시켜 줌
    - 과반수 이상의 sentinel이 동의해야 페일오버 진행(sentinel이 홀수로 존재해야하는 이유)
3. Cluster
    - 클러스터 구성에서는 최소 3대의 마스터가 필요
    - 데이터가 여러 마스터 노드에 자동으로 분할되어 저장되는 “샤딩기능” 제공
    - 모든 노드가 서로를 감시하며, master 노드 장애 발생시 자동으로 페일오버
    - 최소 3대의 마스터 노드가 필요하며 마스터 노드에 대응하는 replica 노드를 두는게 일반적

### 모니터링

모니터링할 때는 rss값을 잘봐야 함

used_memory: 논리적으로 레디스가 사용하는 메모리

user_memory_rss: OS가 레디스에 할당하기 위해 사용한 물리적 메모리

*fragmentation: used_memory와 used_memory_rss의 차이가 큰 경우 fragmentation이 크다고 말함. 주로 삭제되는 키가 많을 때 fragmentation이 증가하게 됨

→ fragmentation이 커졌을 때는 activefrag라는 기능을 잠시 켜두면 도움이 됨(공식문서)
