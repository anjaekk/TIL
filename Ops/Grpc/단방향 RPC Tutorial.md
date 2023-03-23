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

<img src="https://user-images.githubusercontent.com/74139727/227123573-f85df829-d0b7-44f0-9662-ddaa647c8512.png" width="300"/>

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
