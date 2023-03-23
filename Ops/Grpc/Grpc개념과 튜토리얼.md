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

## 단방향 RPC Tutorial

### 1. grpc 설치

```java
python -m pip install grpcio
```

### 2. grpc tools 설치 → 서버 및 클라이언트의 stub생성을 위해서 설치가 필요

```java
python -m pip install grpcio-tools
```

### 3. protobuf 파일 작성

grpc_test.proto

```java
// proto syntax 버전을 명시해줘야 한다.
syntax = "proto3";

// 서비스 이름 Greeter
service Greeter {
  // SayHello라는 메소드
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// 호출시 사용하는 형식 정의
message HelloRequest {
  string name = 1;
}

// 응답시 사용하는 형식
message HelloReply {
  string message = 1;
}
```

### 4. protobuf 파일 컴파일을 통해 파일 생성

run_grpc_codegen.py

```java
from grpc_tools import protoc

protoc.main((
    '',
    '-I.',
    '--python_out=.',
    '--grpc_python_out=.',
    'grpc_test.proto',
))
```

위처럼 python 파일을 통해 실행할수도 있고 아래처럼 터미널 명령어로도 실행가능하다.

```java
python -m grpc_tools.protoc -I . --python_out=. --pyi_out=. --grpc_python_out=. ./grpc_test.proto
```

- `-I`: import로 탐색할 proto 파일이 들어있는 디렉토리 지정
- `python_out`, `grpc_python_out`: 컴파일 후 생성될 파일 저장할 디렉토리 지정

그럼, 다음과 같이 자동으로 파일이 생성된다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b7f0fa4d-1e14-4482-90c9-0fe44997e619/Untitled.png)

*이후 proto파일의 수정사항이 생길 경우 지우고 삭제할 필요없이 proto파일 수정 후 위의 명령어만 재입력해주면 자동으로 생성된 파일에 수정 반영된다.* 

### 5. 서버 코드 작성

server.py

```java
import asyncio
import logging

import grpc
import grpc_test_pb2
import grpc_test_pb2_grpc

class Greeter(grpc_test_pb2_grpc.GreeterServicer):
    """pb2_grpc파일의 생성된 서비스 이름+Servicer 클래스를 상속받도록 작성"""

    async def SayHello(self, request, context):
        return grpc_test_pb2.HelloReply(message=f"hello, {request.name}")

async def serve() -> None:
    server = grpc.aio.server()
    grpc_test_pb2_grpc.add_GreeterServicer_to_server(
        Greeter(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())
```

- SayHello 메소드
    - proto 파일에서 지정한 메서드 구현
    - request, context를 인자로 받는다.
    - 반환값으로 proto파일에 지정한 형식을 message로 반환

- serve() 함수
    - `grpc.aio.server()`: 비동기 서버로 실행
    - grpc_test_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
        
        위에서 지정한 Greeter 클래스를 서버에 맵핑해준다.
        
    - add_insecure_port 메소드를 통해  포트를 지정하는데 여기서 insecure 인 이유는 TLS를 사용하여 서버 클라이언트간 통신 암호화를 하지 않는다는 걸 의미한다.(프로덕션에서는 TLS 암호화와 함께 사용해야 함)

### 6. 클라이언트 코드 작성

client.py

```java
import asyncio
import logging

import grpc
import grpc_test_pb2
import grpc_test_pb2_grpc

async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = grpc_test_pb2_grpc.GreeterStub(channel)
        response = await stub.SayHello(grpc_test_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
```

### 7. 실행

```java
python server.py
```

실행 후 다른 터미널에서 client 실행

```java
python client.py
```

아래와 같이 결과가 출력되는걸 확인할 수 있음
