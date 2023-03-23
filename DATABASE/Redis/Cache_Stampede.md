*+) 아직은 공부가 더 많이 필요한 부분.*

Redis Conf2020

[https://www.youtube.com/watch?v=mPg20ykAFU4](https://www.youtube.com/watch?v=mPg20ykAFU4)

</br>

## Cache Stampede

#Expire time(TTL)설정 주의

대규모 트래픽 환경에서 cache key에 설정된 Expire time(TTL)값은 문제가 될 수 있다. 
키가 만료되는 시점에 순간 대량의 트래픽이 해당 키를 참조하게 되면 `duplicate read`와 `duplicate write`가 발생하게 된다. 
이렇게 키 만료 시점에 read와 write에 병목현상이 생기는 것을 cache stampede라고 한다. 
<img src = "https://user-images.githubusercontent.com/74139727/213616430-f1769a98-a205-4b4a-adae-0890d14d85ca.png" width="40%" height="40%">


단어 그대로 cache에 대한 접근이 우르르 몰리게 되면서 생기는 현상이다. 

![image](https://user-images.githubusercontent.com/74139727/213616436-cff2b276-911b-48b0-8ed4-c69ef00acb67.png)


위의 그림에서 초록색 → 정상 응답, 빨간색 → redis key miss, 파란색 → 데이터베이스에 질의를 나타낸다. 

key가 만료되는 시점에 `duplicate read`와 `duplicate write`가 발생하는 걸 확인할 수 있다. 

2010년 9월 23일 페이스북이 4시간 동안 다운된 원인이 된 일이기도 한데 꽤 오래전 이야기이긴 하지만 대규모 트래픽 환경에서는 현재도 존재하고 있는 위험이다.

</br>

## 방지 방법

### 여러대의 Cache 서버 두기

여러대의 Cache서버를 두어 읽기를 분산시키는 방법이다. 
여러대의 replica 노드를 두어 데이터를 읽어와 부하를 줄이고 병목을 해결하게 된다. 
이 방법은 자주 액세스 하는 Hot key에 대한 스탬피드를 방지하는데 유용한 방법이다. 
하지만 메모리 부족문제가 생길 수 있으므로 주의해야하고 write 문제에 대한 해결방법이 되지 못한다. 

### Locking

캐시 스탬피드가 발생하는 이유는 redis의 자원을 두고 여러 스레드가 경쟁하기 때문이다. 

비슷한 상황인 DB동시성 문제가 생길 경우 이를 해결하는 방법중 하나는 DB의 row나 해당 테이블을 locking하는 방법이다. 
이를 Redis에도 적용할 수 있을 것이다. 이렇게 lock을 설정할 경우 key read와 write문제는 해결될 수 있을 것이다.

하지만 전제가 대규모 트래픽이었기에, 결과값을 요청하고 기다리는 스레드들에 스핀락을 사용하게되고 여기서는 busy waiting이 발생할 수 있다. 

### Early Recomputation

#키 만료기한 전에 미리 재계산하여 키 만료 시간 갱신

간단하게는 백그라운드 프로세스나 cron을 이용해 key의 만료시간 전에 갱산하는 방법이다. 주로 아래와 같은 상황일 때 갱신하게 된다. 

- 만료시간에 가까워 졌을 때
- 특정 시간텀을 두고 주기적으로
- 캐시 미스가 발생했을 경우

### PER(Probablistic Early Recomputation)

#확률에 기반하여 캐시 만료 이전에 키 만료시간을 갱신

캐시 만료 이전에 발생한 요청에 만료 시간을 갱신하는 알고리즘으로 위에서 설명한 Early Recoomputation의 발전 버전이라고 생각하면 된다. 캐시 값을 갱신할 때를 확률적으로 개산해 갱신하게 된다. 

- 관련 논문: [https://cseweb.ucsd.edu//~avattani/papers/cache_stampede.pdf](https://cseweb.ucsd.edu//~avattani/papers/cache_stampede.pdf)

*+) 아직은 공부가 더 많이 필요한 부분.*

</br>

참고 

- [https://betterprogramming.pub/how-a-cache-stampede-caused-one-of-facebooks-biggest-outages-dbb964ffc8ed](https://betterprogramming.pub/how-a-cache-stampede-caused-one-of-facebooks-biggest-outages-dbb964ffc8ed)
- [https://serantechexplore.wixsite.com/website/post/multithreading-thundering-herd-cache-stampede-and-lock-convoy-problems](https://serantechexplore.wixsite.com/website/post/multithreading-thundering-herd-cache-stampede-and-lock-convoy-problems)
