### Thread per request model

- 하나의 쓰레드는 하나의 reqeust를 처리하는 방법이다. 여기서 매 reqeust마다 쓰레드를 생성하고 삭제하는 작업을 반복한다면 이에 따라 request에 응답하는 속도가 지연되게 될 것 이다. 이에 더불어 만약 처리속도보다 요청속도가 더 빠르게 늘어나게 된다면 쓰레드가 계속해서 생성되게 되고 이에 따른 컨텍스트 스위칭이 빈번하게 생기면서 CPU 오버헤드가 증가하게 되고 CPU time낭비와 심해지면 서버가 응답불가가 상태가 될 수 있다. 쓰레드 생성으로 인해 메모리 고갈로 서버가 다운될 가능성이 높아지는 건 덤이다.
- 그래서 등장한 개념이 Thread Pool 이다.

## Thread Pool

Thread Pool은 일정 숫자만큼 Thread를 만들고 Queue를 이용해 request를 관리하게 된다. 해당 reqeust에 Thread를 쓰레드 풀에서 할당하고 사용이 끝난 Thread는 쓰레드 풀에서 다음 요청을 기다리면서 Tread를 재사용할 수 있게 하는 것이다.

 

### Thread pool 사용

Thread pool은 다음과 같이 여러작업을 동시에 처리해야할 때 사용하게 된다.

- Thread per reqeust 모델
- task를 sub task로 나눠서 동시에 처리를 해야할 때
- 순서 상관없이 동시 실행해야하는 작업일 때

### Python Thread pool 주의할 점

### 1. max_workers

Thread pool에 적절한 쓰레드 개수를 지정해야 한다.

- CPU 코어 개수와 Task의 종류에 따라 다르게 된다.
    
    1) CPU bound: Core 개수 만큼 혹은 그 보다 조금더 많은 정도
    
    2) I/O bound: Core 개수보다 많이 만들 수 있지만 경험을 통해 제한해야 한다.
    

### 2. woke_queue

Thread pool에서 실행될 task 개수에 제한이 없을 시 Thread pool의 queue 사이즈의 제한이 있는지 확인해야한다. 파이썬에서는 worker queue를 queue.SimpleQueue를 이용하는데 SimpleQueue는 unbounded FIFO queue로 여기서 unbounded는 제한이 없다는 것을 의미한다. 

- 요청의 개수가 Thread Pool안에 쓰레드보다 많은 경우 Thread pool의 queue에 request가 쌓이게 된다. 만약 이 queue에 쌓이는 쓰레드 개수의 제한이 없게되면 그만큼 메모리 고갈이 생기기 때문에 반드시 제한을 둘 수 있도록 해야한다.(요청을 버리게 되더라도,,)
