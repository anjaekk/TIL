# Grpc

공식문서: [https://grpc.io/docs/what-is-grpc/introduction/](https://grpc.io/docs/what-is-grpc/introduction/)

# Grpc

- 언어 제약이 없는 오픈소스
- 고성능 RPC(Remote Procedure Calls, 원격 프로시저 호출)
- http/2 기반
- protocol buffer 기반이라 바이너리 파일로 데이터를 주고 받음
- 쿠버네티스 백엔드가 Grpc로 되어있음
- 페이로드가 작을때는 차이가 나지 않지만 페이로드가 클 경우에 그 격차가 더욱 벌어지게 됨

## 특징

1. 클라이언트와 서버의 통신 구조
    - 클라이언트와 서버 사이에 grpc channel이라고 하여 http/2 엔드포인트에 대한 virtual connection을 나타낸다.
    - 클라이언트가 grpc 채널을 만들면 내부적으로 서버와 http/2 connection을 맺게 된다.
    - rpc는 http/2의 stream으로  처리 됨
    - 메세지는 http/2dml frame 단위로 처리 됨
2. Protocol Buffers
    - 데이터를 바이너리 형태로 인코딩 하는 방식
    - json은 key와 value값을 매번 보내야 하지만 protocol buffer는 매번 어떤 값을 보내고 받을지 정해놓기 때문에 매우 빠르게 데이터 전송과 수신이 가능하다
3. Stub
    - 하지만 서버와 클라이언트 모두 동일한 proto 파일을 가지고 있고 이를 통해 메시지를 주고 받아야 한다는 제약이 있다.
    - proto파일을 빌드하면 각 언어별로 서버와 통신 가능한 Stub 파일을 생성
    - stub파일을 일종의 sdk로서 클라이언트와 서버가 손쉽게 protobuf 메세지를 주고 받을 수 있게 해준다. (직렬, 역직렬화)
4. 메세지 순서 보장
    - grpc는 개별 RPC 호출 내에서 메세지 순서를 보장한다.
5. 대기시간 지정 가능
    - `DEADLINE_EXCEEDED`: 클라이언트는 rpc가 오류로 종료되기 전에 rpc가 완료될 때까지 대기시간을 지정할 수 있음

### Grpc의 서비스 정의 방법

grpc의 서비스 정의 방법은 총 4가지가 있다.

- 단방향 RPC
- 서버 스트리밍 RPC
- 클라이언트 스트리밍 RPC
- 양방향 스트밍 RPC

### 1. 단방향 RPC

일반 함수호출과 마찬가지로 클라이언트가 서버에 단일 요청을 보내고 단일 응답을 받는 단항 RPC

```java
rpc SayHello(HelloRequest) returns (HelloResponse);
```

### 2. 서버 스트리밍 RPC

클라이언트가 서버에 요청을 보내고 스트림을 가져와 일련의 메세지를 다시 읽는 서버 스트리밍 RPC로 클라이언트는 더 이상 메세지가 없을 때까지 반환된 스트림에서 읽는다.

```java
rpc LotsOfReplies(HelloRequest) returns (stream HelloResponse);
```

### 3. 클라이언트 스트리밍 RPC

클라이언트가 일련의 메세지를 작성하고 다시 제공된 스트림을 사용하여 서버로 보내는 클라이언트 스트리밍 RPC로 클라이언트가 메세지 쓰기를 마치면 서버가 메세지를 읽고 응답을 반환할 때까지 기다린다.

```java
rpc LotsOfGreetings(stream HelloRequest) returns (HelloResponse);
```

### 4. 양방향 스트밍 RPC

클라이언트와 서버 양쪽이 read-write 스트림을 사용하여 일련의 메세지를 보내는 양향방 스트리밍이다. 두 스트림은 독립적으로 작동하기 때문에 클라이언트와 서버는 원하는 순서대로 read와 write가 가능하다. 예를 들어 서버는 응답을 쓰기 전에 모든 클라이언트 메세지를 수신하기를 기다릴 수 있고 번갈아 메세지를 읽은 다음 메세지를 쓸 수도 있다.

```java
rpc BidiHello(stream HelloRequest) returns (stream HelloResponse);
```

## Grpc 서버를 만드는 방법

### 1. ProtoBuf 명세

- helloworld.proto
- protobuf에는 아래의 내용이 포함된다.
    - 서비스에 어떤 메소드가 있는지
    - 요청을 어떻게 하는지
    - 응답은 어떻게 오는지
    - 메세지 형식은 어떻게 되는지

### 2. ProtoBuf 컴파일

- helloworld_pb2.py
- helloworld_pb2_grpc.py
- 1에서 생성한 protobuf 파일을 컴파일해서 stub 파일로 생성하는 과정이다.
- grpc_tools 패키지를 이용해 protobuf파일을 컴파일 할 수 있다.
- _pb2.py 파일: 서비스 및 메세지에 대한 ORM과 유사한 코드가 생성(메세지 직렬화에 사용)
- _pb2_grpc.py 파일: 서버와 클라이언트를 구현할 수 있는 헬퍼 클래스 위조로 생성
- _pb2_grpc.py 파일을 이용해 서버를 구현하고 클라이언트도 이를 이용해 서버에 요청을 보내게 된다.

### 3. 서비스 구현

### 4. 서버에 서비스 등록
